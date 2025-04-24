

from odoo import fields, models


class HelpdeskRoles(models.Model):
    _name = 'helpdesk.roles'
    _description = 'Helpdesk Roles'

    name = fields.Char(string='Role Name', required=True)
    description = fields.Text(string='Description')
    code = fields.Char(string='Code', required=True, help="A unique code for each role")





