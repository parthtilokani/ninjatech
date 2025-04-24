from odoo import fields, models


class HelpdeskStage(models.Model):
    _inherit = "helpdesk.stage"

    is_pte = fields.Boolean('Permission to Enter?')
    transfer_to_supervisor = fields.Boolean("Transfer to Supervisor?")
    is_missing_info = fields.Boolean("Missing Record?")