# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    type = fields.Selection([('tool', 'Use as a Tool'),
                             ('equipment', 'Equipment')], default='tool',
                            string='Equipment Type')
    # mechanism_type = fields.Selection([('use_product', 'Use Product'),
    #                                    ('use_standard', 'Use Standard')],
    #                                   string="Mechanism Type")
    # product_id = fields.Many2one('product.product', string='Product')
    building_id = fields.Many2one('apartment.config', string="Building")
    unit_id = fields.Many2one('apartment.unit', string="Unit")



