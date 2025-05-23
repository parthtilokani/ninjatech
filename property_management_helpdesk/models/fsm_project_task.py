from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    building_id = fields.Many2one(related="helpdesk_ticket_id.building_id")
    unit_id = fields.Many2one(related="helpdesk_ticket_id.unit_id")
    # category_id = fields.Many2one(related="helpdesk_ticket_id.category_id")
    custom_priority = fields.Selection(related="helpdesk_ticket_id.custom_priority")
    scheduled_slot_ids = fields.One2many(related="helpdesk_ticket_id.scheduled_slot_ids")
    sequence_number = fields.Char(string='Sequence', readonly=True, copy=False)
    is_editable_user = fields.Boolean(
        string="Is Editable User",
        compute='_compute_is_editable_user',
        store=False  # This should remain False as it's a transient property.
    )

    def _compute_is_editable_user(self):
        group = self.env.ref('industry_fsm.group_fsm_user')
        is_in_group = self.env.user in group.users
        print('is_in_group',is_in_group)
        for task in self:
            task.is_editable_user = is_in_group
            print('task.is_editable_user',task.is_editable_user)

    @api.model
    def _default_category_id(self):
        ticket_id = self._context.get('default_helpdesk_ticket_id')
        if ticket_id:
            ticket = self.env['helpdesk.ticket'].browse(ticket_id)
            if ticket.category_id:
                return ticket.category_id.id
        return False

    category_id = fields.Many2one(
        'helpdesk.category',
        string='Issue Category',
        default=_default_category_id,
        index=True,
        tracking=True
    )

    allowed_role_ids = fields.Many2many(
        'helpdesk.roles',
        compute='_compute_allowed_roles',
        store=False
    )

    @api.depends('category_id')
    def _compute_allowed_roles(self):
        for task in self:
            task.allowed_role_ids = task.category_id.role_id.ids if task.category_id else []

    allowed_user_ids = fields.Many2many(
        'res.users',
        compute='_compute_allowed_users',
        store=False
    )

    @api.depends('helpdesk_role_id')
    def _compute_allowed_users(self):
        for task in self:
            if task.helpdesk_role_id:
                task.allowed_user_ids = self.env['res.users'].search([
                    ('helpdesk_role_id', '=', task.helpdesk_role_id.id)
                ]).ids
            else:
                task.allowed_user_ids = []

    helpdesk_role_id = fields.Many2one(
        'helpdesk.roles',
        string='Helpdesk Role',
        domain="[('id', 'in', allowed_role_ids)]"
    )

    @api.model
    def create(self, vals):
        if 'helpdesk_role_id' in vals and vals['helpdesk_role_id']:
            role = self.env['helpdesk.roles'].browse(vals['helpdesk_role_id'])
            if role and role.code:
                sequence = self.env['ir.sequence'].next_by_code('project.task.sequence') or '000'
                vals['sequence_number'] = f"{role.code}{sequence}"
        return super(ProjectTask, self).create(vals)

    def _compute_display_name(self):
        res = super()._compute_display_name()
        if self._context.get('is_view'):
            for rec in self:
                stage_name = rec.stage_id.name if rec.stage_id else ''
                rec.display_name = f"{rec.display_name}-{stage_name}"
        return res


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    is_project_manager = fields.Boolean(compute="_compute_user_groups", store=False, groups="base.group_user")
    is_project_user = fields.Boolean(compute="_compute_user_groups", store=False, groups="base.group_user")
    is_admin_user = fields.Boolean(compute="_compute_user_groups", store=False, groups="base.group_user")

    @api.model
    def _get_employee_domain(self):
        # Get the current user and their employee
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

        # Get the task assigned user and their employee
        assigned_employee = self.env['hr.employee']
        if self.task_id and self.task_id.user_id:
            assigned_employee = self.env['hr.employee'].search([('user_id', '=', self.task_id.user_id.id)], limit=1)

        # Combine the employee IDs
        employee_ids = (current_employee | assigned_employee).ids
        return [('id', 'in', employee_ids)]

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        domain=_get_employee_domain
    )

    @api.depends('user_id')
    def _compute_user_groups(self):
        for record in self:
            user = self.env.user
            record.is_project_manager = user.has_group('project.group_project_manager')
            record.is_project_user = user.has_group('project.group_project_user')
            record.is_admin_user = user.has_group('base.group_system')  # Admin group
