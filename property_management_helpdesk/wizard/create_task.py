from odoo import models, _


class CreateTask(models.TransientModel):
    _inherit = 'helpdesk.create.fsm.task'

    def action_generate_and_view_task(self):
        self.ensure_one()
        # new_task = self.action_generate_task()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasks from Tickets'),
            'res_model': 'project.task',
            'view_mode': 'gantt,list,form',

            'context': {
                'fsm_mode': True,
                'create': True,
                'default_partner_id': self.helpdesk_ticket_id.partner_id.id,
                'default_helpdesk_ticket_id': self.helpdesk_ticket_id.id,
                'default_description': self.helpdesk_ticket_id.description,
                'default_partner_phone': self.helpdesk_ticket_id.partner_phone,
                'default_name': self.name,
                # 'default_worksheet_template_id': self.worksheet_template_id.id
            }
        }
