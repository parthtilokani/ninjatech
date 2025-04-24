# -*- coding: utf-8 -*-
{
    'name': "property_management_project_task",

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
    'depends': ['base', 'industry_fsm_sale', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_product_view.xml',
        'views/purchase_order_wizard_view.xml',
        'views/project_task_view.xml'
    ],

}

