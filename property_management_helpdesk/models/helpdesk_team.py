from odoo import fields, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    member_ids = fields.Many2many('res.users', string='Team Members', domain=lambda self: [
        ('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_manager').id)],
                                  default=lambda self: self.env.user, required=True)
