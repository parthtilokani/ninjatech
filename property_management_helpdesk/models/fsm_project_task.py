from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    building_id = fields.Many2one(related="helpdesk_ticket_id.building_id")
    unit_id = fields.Many2one(related="helpdesk_ticket_id.unit_id")
    # category_id = fields.Many2one(related="helpdesk_ticket_id.category_id")
    custom_priority = fields.Selection(related="helpdesk_ticket_id.custom_priority")
    scheduled_slot_ids = fields.One2many(related="helpdesk_ticket_id.scheduled_slot_ids")

    @api.model
    def _default_category_id(self):
        ticket_id = self._context.get('default_helpdesk_ticket_id')
        if ticket_id:
            ticket = self.env['helpdesk.ticket'].browse(ticket_id)
            if ticket.category_id:
                return ticket.category_id.id
        return False

    category_id = fields.Many2one(
        'helpdesk.category',
        string='Issue Category',
        default=_default_category_id,
        index=True,
        tracking=True
    )
