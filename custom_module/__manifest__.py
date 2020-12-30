# -*- coding: utf-8 -*-
{
    'name': "custom_module",

    'summary': """
        Custom module to edit layouts""",

    'description': """
        A custom module created by Jimmy and Mark to modify the layout or other basic customizations
    """,

    'author': "Jimmy",
    'website': "http://www.tme-inc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','data_migration', 'sale_management', 'crm','helpdesk','sale_team'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/helpdesk.xml',
        'views/templates.xml',
        'data/selection_data_default.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}