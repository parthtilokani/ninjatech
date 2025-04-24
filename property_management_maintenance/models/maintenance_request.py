from odoo import api, fields, models


class MaintenanceTools(models.Model):
    _name = 'maintenance.tool'

    equipment_id = fields.Many2one('maintenance.equipment',
                                   domain=lambda self: [

                                   ])
    request_id = fields.Many2one('maintenance.request')


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    @api.depends('building_id')
    def default_unit_id(self):
        return [('apartment_config_id', '=', self.building_id.id)]

    building_id = fields.Many2one('apartment.config', string="Building")
    unit_id = fields.Many2one('apartment.unit', string="Unit")
    tool_ids = fields.One2many('maintenance.tool', 'request_id', string="Tools")
    maintenance_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')],
                                        string='Maintenance Type', default="preventive")

    user_id = fields.Many2one(
        'res.users',
        domain="[('is_maintenance_staff', '=', True)]")

    custom_priority = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        string="Custom Priority",
    )
