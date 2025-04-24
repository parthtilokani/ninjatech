
from odoo import fields, models, _



class HelpdeskCreateFSMTask(models.TransientModel):

    _inherit = 'helpdesk.create.fsm.task'

    # category_id = fields.Many2one('helpdesk.category', string="Issue Category")
    category_id = fields.Many2one(related="helpdesk_ticket_id.category_id")

    def action_generate_and_view_task(self):
        self.ensure_one()
        new_task = self.action_generate_task()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Work Order from Tickets'),
            'res_model': 'project.task',
            'res_id': new_task.id,
            'view_mode': 'form',
            'view_id': self.env.ref('project.view_task_form2').id,
            'context': {
                'fsm_mode': True,
                'create': False,
            }
        }
