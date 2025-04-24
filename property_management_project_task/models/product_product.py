# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    custom_po_line_id = fields.Many2one('purchase.order.line', copy=False)

    def action_purchase_order_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {
                'task_id': self._context.get('active_id'),
                'po_order': self.custom_po_line_id.order_id.id
            }

        }


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.order.wizard'

    def default_purchase_id(self):

        task_id = self._context.get('task_id')
        task_rec = self.env['project.task'].browse(task_id)

        if task_rec:
            return task_rec.purchase_order_ids and task_rec.purchase_order_ids[-1].id
        else:
            return

    def default_partner_id(self):

        task_id = self._context.get('task_id')
        task_rec = self.env['project.task'].browse(task_id)
        print("task ................", task_id, task_rec.purchase_order_ids)
        if task_rec:
            return task_rec.purchase_order_ids and task_rec.purchase_order_ids[-1].partner_id.id
        else:
            return

    def default_product_qty(self):
        product_id = self._context.get('active_id')
        task_id = self._context.get('task_id')
        task_rec = self.env['project.task'].browse(task_id)
        purchase_line_rec = task_rec.purchase_order_ids and task_rec.purchase_order_ids[-1].order_line.filtered(
            lambda ol: ol.product_id.id == product_id)

        if purchase_line_rec:
            return purchase_line_rec.product_qty

        return 0

    def default_po_id(self):
        task_id = self._context.get('task_id')
        po_ids = self.env['project.task'].browse(task_id).purchase_order_ids.ids
        print("default_po_ids..............", po_ids)
        return po_ids

    purchase_order_ids = fields.Many2many('purchase.order', default=default_po_id)
    purchase_order_id = fields.Many2one('purchase.order', default=default_purchase_id
                                        )
    partner_id = fields.Many2one('res.partner', string="Vendor", default=default_partner_id, required='1')
    product_qty = fields.Float('Qty', default=default_product_qty)
    purchase_field_visible = fields.Boolean(compute="_check_purchase_orders")

    @api.depends('purchase_order_id')
    def _check_purchase_orders(self):
        task_id = self._context.get('task_id')
        task_rec = self.env['project.task'].browse(task_id)
        if len(task_rec.purchase_order_ids) > 0:
            self.purchase_field_visible = True
        else:
            self.purchase_field_visible = False

    @api.onchange('purchase_order_id')
    def on_purchase_order_id_change(self):
        product_id = self._context.get('active_id')
        if self.purchase_order_id:
            self.partner_id = self.purchase_order_id.partner_id.id
            order_line = self.purchase_order_id.order_line.filtered(lambda ol: ol.product_id.id == product_id)
            if order_line:
                self.product_qty = order_line.product_qty
            else:
                self.product_qty = 0

    def create_view_po(self):
        product_rec = self._context.get('active_id')
        task_rec = self._context.get('task_id')
        product_rec = self.env['product.product'].browse(product_rec)

        if not self.purchase_order_id:
            po_rec = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': [(0, 0, {'product_id': product_rec.id, 'product_qty': self.product_qty})]
            })
            po_rec.button_confirm()
            self.env['project.task'].browse(task_rec).purchase_order_ids = [(4, po_rec.id)]

            # product_rec.write({
            #     'custom_po_line_id': po_rec.order_line[0].id
            # })
        else:

            po_line_rec = product_rec.custom_po_line_id
            po_rec = self.purchase_order_id or po_line_rec.order_id
            if po_line_rec:
                po_line_rec.write({
                    'product_qty': self.product_qty
                })
            else:
                po_line_rec = po_rec.order_line.create({
                    'product_id': product_rec.id, 'product_qty': self.product_qty,
                    'order_id': po_rec.id
                })
                # product_rec.write({
                #     'custom_po_line_id': po_line_rec.id
                # })
