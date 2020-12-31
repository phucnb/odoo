# -*- encoding: utf-8 -*-
{
    'name': 'PN Helpdesk',
    'version': '14.1.0.1',
    'author': 'Niran Aki',
    'summary': 'Helpdesk',
    'website': '',
    'category': 'Helpdesk',
    'description': "",
    'depends': [
        'helpdesk',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        'security/ir.model.access.csv',
        # ============================================================
        # DATA
        # ============================================================
        # 'data/approval_role_data.xml',
        'data/helpdesk_ticket_type_data.xml',
        'data/cron_create_data.xml',
        # ============================================================
        # VIEWS - REPORTS
        # ============================================================
        # */views
        'views/helpdesk_ticket_views.xml',
        # */menu
        # */wizard
    ],
    'qweb': [],
    'installable': True,
    'application': False,
}
