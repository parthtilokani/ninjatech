from odoo import fields, models, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    apartment_unit_id = fields.Many2one('apartment.unit')