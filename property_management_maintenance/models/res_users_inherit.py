from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_maintenance_staff = fields.Boolean(string="Maintenance Staff")
    is_technician = fields.Boolean(string="Technician")
    helpdesk_role_id = fields.Many2one('helpdesk.roles', string="Helpdesk Role")


