{
    'name': "property_management_helpdesk",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk', 'website_helpdesk', 'web', 'bus',
                'mail', 'helpdesk_fsm','industry_fsm_sale',
                'project_enterprise', 'hr_timesheet', 'sale_timesheet'],

    'assets': {
        'web.assets_frontend': [
            ('before', 'web/static/src/core/datetime/*', 'property_management_helpdesk/static/src/js/core/*'),
            'property_management_helpdesk/static/src/js/l10/*',
            'property_management_helpdesk/static/src/js/public/*',
            'property_management_helpdesk/static/src/css/style.css',
            'property_management_helpdesk/static/src/js/services/mail_message_service.js',
            # 'property_management_helpdesk/static/src/js/notification/*',
        ],
        'web.assets_backend': [
            'property_management_helpdesk/static/src/css/tom_select.css',
            'property_management_helpdesk/static/src/js/lib/*',
            'property_management_helpdesk/static/src/js/fields/*',
            'property_management_helpdesk/static/src/js/services/mail_message_service.js',

        ]
    },

    # always loaded
    'data': [
        'data/data.xml',
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/helpdesk_user_group.xml',
        'views/apartment_config_view.xml',
        'views/helpdesk_ticket_view.xml',
        'views/helpdesk_sla_policies_view.xml',
        'views/helpdesk_roles_view.xml',
        'views/helpdesk_template.xml',
        'views/helpdesk_category.xml',
        'views/fsm_project_task_view.xml',
        'views/website_templates.xml',

    ],

}
# -*- coding: utf-8 -*-

