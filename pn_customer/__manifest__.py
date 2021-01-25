# -*- encoding: utf-8 -*-
{
    'name': 'PN Customer',
    'version': '14.1.0.1',
    'author': 'Niran Aki',
    'summary': 'Manager message, email, activity on company',
    'website': '',
    'sequence': 185,
    'category': 'Contact',
    'description': "",
    'depends': ['pn_activity', 'contacts'],
    'data': [
        'views/contact_activity_views.xml',
        'views/mail_message_views.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
}