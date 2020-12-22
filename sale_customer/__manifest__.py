# -*- encoding: utf-8 -*-
{
    'name': 'Sales Customer',
    'version': '12.1.0.1',
    'author': 'Niran Aki',
    'summary': 'Sales Customer',
    'website': 'https://www.facebook.com/nhat.nang.52035',
    'category': 'SAles',
    'description': "",
    'depends': [
        'sale',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================

        # ============================================================
        # DATA
        # ============================================================

        # ============================================================
        # VIEWS - REPORTS
        # ============================================================
        # */views
        'views/sale_order_views.xml',
        'views/res_partner_views.xml'
        # */menu
        # */wizard
    ],
    'qweb': [],
    'installable': True,
    'application': True,
}
