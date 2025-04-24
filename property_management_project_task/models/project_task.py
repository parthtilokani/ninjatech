from odoo import models, fields, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    purchase_order_ids = fields.Many2many('purchase.order', copy=False)

    def action_fsm_view_material(self):
        res = super().action_fsm_view_material()
        res['context'].update({
            'po_order': self.purchase_order_ids.ids
        })
        return res

    def action_view_po(self):
        po_ids = self.purchase_order_ids.ids
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "name": _("Purchase Order"),
            "views": [[False, "list"], [False, "kanban"], [False, "form"]],
            "context": {"create": False, "show_purchase": True},
            "domain": [["id", "in", po_ids]],
        }
        if len(po_ids) == 1:
            action_window["views"] = [[False, "form"]]
            action_window["res_id"] = po_ids[0]

        return action_window
