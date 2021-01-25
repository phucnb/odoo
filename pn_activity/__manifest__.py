# -*- encoding: utf-8 -*-
{
    'name': 'PN Activity',
    'version': '14.1.0.1',
    'author': 'Niran Aki',
    'summary': 'Activities',
    'website': '',
    'sequence': 185,
    'category': 'Activities',
    'description': "",
    'depends': ['base', 'sale', 'mail', 'contacts'],
    'data': [
        'security/activity_group.xml',
        'security/ir.model.access.csv',
        'security/activity_rules.xml',
        'data/schedule_sync_activity_data.xml',
        'views/activity_views.xml',
        'views/mail_activity_views.xml',
        'views/contact_activity_views.xml'
    ],
    'qweb': [],
    'installable': True,
    'application': False,
}