

from odoo import fields, models


class HelpdeskCategory(models.Model):

    _name = "helpdesk.category"

    name = fields.Char()
    # role_id = fields.Many2one('helpdesk.roles', string="Helpdesk Role")
    role_id = fields.Many2many( 'helpdesk.roles', string='Roles')





