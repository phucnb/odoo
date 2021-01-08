# -*- encoding: utf-8 -*-
{
    'name': 'PN Mail',
    'version': '14.1.0.1',
    'author': 'Niran Aki',
    'summary': 'Mail',
    'website': 'https://www.facebook.com/nhat.nang.52035',
    'category': 'Mail',
    'description': "",
    'depends': [
        'mail',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        # ============================================================
        # DATA
        # ============================================================
        # 'data/mail_activity_data.xml',
        # ============================================================
        # VIEWS - REPORTS
        # ============================================================
        # */views
        'views/mail_activity_views.xml',
        'views/assets.xml',
        'views/mail_data.xml',
        # */menu
        # */wizard
    ],
    'qweb': ['static/src/xml/mail_message.xml'],
    'installable': True,
    'application': True,
}
