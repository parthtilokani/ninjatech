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

    helpdesk_role_id = fields.Many2one('helpdesk.category')

    state = fields.Selection(
        [('no_task_done', 'No Task Done'),
         ('partially_done', 'Partially Done'),
         ('done', 'Done')],
        string="State",
        compute="_compute_state",
        store=True
    )

    @api.depends('fsm_task_ids.stage_id')
    def _compute_state(self):
        for ticket in self:
            tasks = ticket.fsm_task_ids
            if not tasks:
                ticket.state = 'no_task_done'
            else:
                done_tasks = tasks.filtered(lambda t: t.stage_id.name == 'Done')
                if len(done_tasks) == len(tasks):
                    ticket.state = 'done'
                elif done_tasks:
                    ticket.state = 'partially_done'
                else:
                    ticket.state = 'no_task_done'

    is_helpdesk_manager = fields.Boolean(compute="_compute_user_groups", store=False)
    is_helpdesk_user = fields.Boolean(compute="_compute_user_groups", store=False)
    is_admin_user = fields.Boolean(compute="_compute_user_groups", store=False)

    @api.depends('user_id')
    def _compute_user_groups(self):
        for record in self:
            user = self.env.user
            record.is_helpdesk_manager = user.has_group('helpdesk.group_helpdesk_manager')
            record.is_helpdesk_user = user.has_group('helpdesk.group_helpdesk_user')
            record.is_admin_user = user.has_group('base.group_system')  # Admin group

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

    class HelpdeskSLA(models.Model):
        _inherit = 'helpdesk.sla'

        custom_priority = fields.Selection(
            selection=[
                ('low', 'Low'),
                ('medium', 'Medium'),
                ('high', 'High'),
                ('urgent', 'Urgent'),
            ],
            string="Custom Priority",
        )