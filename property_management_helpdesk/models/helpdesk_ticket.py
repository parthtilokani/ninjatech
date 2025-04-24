from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.addons.mail.tools.discuss import Store


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = ['helpdesk.ticket', "mail.thread", "bus.listener.mixin"]

    building_id = fields.Many2one('apartment.config',
                                  related='partner_id.apartment_unit_id.apartment_config_id',
                                  string="Building")
    unit_id = fields.Many2one('apartment.unit',
                              related='partner_id.apartment_unit_id', string="Unit")
    scheduled_slot_ids = fields.One2many('time.slots', 'helpdesk_id')
    customer_is_pte = fields.Boolean("Permission To Enter?")
    category_id = fields.Many2one('helpdesk.category')
    is_reviewed = fields.Boolean('Reviewed?')
    custom_priority = fields.Selection([('urgent', 'Urgent'), ('high', 'High'),
                                        ('normal', 'Normal'), ('low', 'Low')], "Priority", default='low', required=True)

    @api.onchange('stage_id')
    def assign_supervisor(self):
        for rec in self:
            if rec.stage_id.transfer_to_supervisor:
                rec.is_reviewed = True
                rec.user_id = rec.building_id.supervisor_id.id

    # @api.constrains('customer_is_pte', 'scheduled_slot_ids')
    # def check_for_missing_record(self):
    #     for rec in self:
    #         if not rec.customer_is_pte or len(rec.scheduled_slot_ids.ids) < 1:
    #             missing_stage_rec = rec.stage_id.search([('is_missing_info', '=', True)], limit=1)
    #
    #             if (missing_stage_rec and not rec.stage_id == missing_stage_rec.id and
    #                     not rec.is_reviewed):
    #                 rec.stage_id = missing_stage_rec.id

    def action_generate_fsm_task(self):
        res = super().action_generate_fsm_task()
        res.update({'name': _('Create a Work Order')})
        return res

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        # link message to channel
        rdata = super()._notify_thread(message, msg_vals=msg_vals, **kwargs)
        partner_rec = self.partner_id | self.env.user.partner_id
        payload = {"data": Store(message).get_result(), "id": self.id}
        if temporary_id := self.env.context.get("temporary_id"):
            payload["temporary_id"] = temporary_id
        if kwargs.get("silent"):
            payload["silent"] = True

        self._bus_send_store(self, {"is_pinned": True}, subchannel="members")
        # adding partner will update message in respective chatter
        partner_rec._bus_send("helpdesk.ticket/new_message", payload)

        return rdata

    helpdesk_role_id = fields.Many2one(related="category_id.role_id")

    # @api.depends('category_id')
    # def _compute_helpdesk_role_id(self):
    #     for ticket in self:
    #         ticket.helpdesk_role_id = ticket.category_id.role_id if ticket.category_id else False


class TimeSlots(models.Model):
    _name = 'time.slots'

    from_time = fields.Float('From')
    from_formatted_time = fields.Char("From Time", compute="_compute_formatted_time", store=True)
    to_time = fields.Float('To')
    to_formatted_time = fields.Char("To Time", compute="_compute_formatted_time", store=True)
    date = fields.Date('Date')
    helpdesk_id = fields.Many2one('helpdesk.ticket')

    @api.depends("from_time", "to_time")
    def _compute_formatted_time(self):
        for record in self:
            if record.from_time:
                hours = int(record.from_time)
                minutes = int((record.from_time - hours) * 60)
                suffix = "AM" if hours < 12 else "PM"
                hours = hours if hours <= 12 else hours - 12
                record.from_formatted_time = f"{hours}:{minutes:02d} {suffix}"
            else:
                record.from_formatted_time = ""
            if record.to_time:
                hours = int(record.to_time)
                minutes = int((record.to_time - hours) * 60)
                suffix = "AM" if hours < 12 else "PM"
                hours = hours if hours <= 12 else hours - 12
                record.to_formatted_time = f"{hours}:{minutes:02d} {suffix}"
            else:
                record.to_formatted_time = ""
