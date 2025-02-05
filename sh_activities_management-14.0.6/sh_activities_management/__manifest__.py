# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': "Activities Management",
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Discuss',
    "license": "OPL-1",
    'version': '14.0.6',
    "summary": """ Activity Management Odoo, Activity Scheduler Odoo, Manage Project Activity, Manage Employee Activity Module, Manage Supervisor Activity, Filter Completed Activity,filter planned Activity Odoo """,
    "description": """Do you want to show the activities list beautifully? Do you want to show the well-organized structure of activities? Do you want to show completed, uncompleted activities easily to your employees? Do you want to show an activity dashboard to the employee? Do you want to manage activities nicely with odoo? Do you want to show the scheduled activity to the manager, supervisor & employee? This module helps the manager can see everyone's activity, the supervisor can see the assigned user and own activity, the user can see only own activity. Everyone can filter activity by the previous year, previous month, previous week, today, yesterday, tomorrow, weekly, monthly, yearly & custom date. You can see activities like all activities, planned activities, completed activities or overdue activities. Manager, Supervisor & Employee have their own dashboard, that provides a beautiful design on the dashboard. Hurray!""",
    'depends': [
        'sh_activity_base',
    ],
    'data': [
        'security/activity_security.xml',
        'security/ir.model.access.csv',
        'data/data_sales_activity_notification.xml',
        'data/sales_activity_email_template.xml',
        'views/activity_config_setting.xml',
        'wizard/feedback.xml',
        'views/activity_views.xml',
        'views/activity_dashboard.xml',
    ],
    'qweb': [
        'static/src/xml/activity_dashboard.xml'
    ],
    'images': ['static/description/background.png', ],
    "price": 100,
    "currency": "EUR"
}
