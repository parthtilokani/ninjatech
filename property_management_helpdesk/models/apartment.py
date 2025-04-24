# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Apartment(models.Model):
    _name = 'apartment.config'
    _description = 'Apartment Config'

    name = fields.Char()
    street = fields.Char()
    supervisor_id = fields.Many2one('res.users',
                                    domain=lambda self: [
                                        ('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_user').id)
                                    ], required=True)
    city = fields.Char()
    state_id = fields.Many2one('res.country.state')
    country_id = fields.Many2one('res.country')
    zip_code = fields.Char()
    apartment_units_ids = fields.One2many('apartment.unit', 'apartment_config_id')

    @api.constrains('user_ids')
    def _check_unique_users(self):
        for record in self:
            user_list = record.user_ids.ids
            if len(user_list) != len(set(user_list)):
                raise ValidationError(_("Each user must be unique in the apartment configuration!"))


class ApartmentUnits(models.Model):
    _name = "apartment.unit"
    _description = "Apartment Units"

    name = fields.Char()
    tenants_ids = fields.One2many('res.partner', 'apartment_unit_id')
    apartment_config_id = fields.Many2one('apartment.config')

    def view_tenants(self):
        return {
            'name': 'Tenants',
            'domain': [['id', 'in', self.tenants_ids.ids]],
            'res_model': 'partner',
            'type': 'ir.actions.act_window',
            'context': {},
            'views': ["list"],
            'view_mode': 'list',
        }
