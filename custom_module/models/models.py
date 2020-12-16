from odoo import models, fields, api

NP_SCORE = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10')
]

CRR = [
    ('demo', 'demo')
]

BUS_MFG = [
    ('demo', 'demo')
]

BUS_TYPE = [
    ('demo', 'demo')
]

SERVICE_PLAN_TYPE = [
    ('1 visit', '1 visit'),
    ('2 visit', '2 visit'),
    ('3 visit', '3 visit')
]

CAMERA_VENDOR = [
    ('Angletrax', 'Angletrax'),
    ('Seon', 'Seon'),
    ('Gatekeeper', 'Gatekeeper'),
    ('REI', 'REI'),
    ('Safety Vision', 'Safety Vision'),
    ('Provision', 'Provision'),
    ('Zentinel', 'Zentinel'),    
    ('Other', 'Other')
]

STOP_ARM_THIRD_PARTY = [
    ('No', 'No'),
    ('Busgaurd', 'Busgaurd'),
    ('ATs', 'ATs')
]

DISTRICT_TYPE = [
    ('Rural', 'Rural'),
    ('Urban', 'Urban')
]

NO_BELL_TIMES = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
]

class ResPartnerField(models.Model):

     _inherit = 'res.partner'

     x_field = fields.Char('X Field')
     hs_analytics_num_event_completions = fields.Integer('Number of event completions')
     num_notes = fields.Integer("Number of Sales Activities")
     hs_email_bounce = fields.Integer("Marketing emails bounced")
     hs_email_click = fields.Integer("Marketing emails clicked")
     hs_email_delivered = fields.Integer("Marketing emails delivered")
     hs_email_open = fields.Integer("Marketing emails opened")
     hs_email_last_send_date = fields.Date('Last marketing email send date')
     hs_email_last_open_date = fields.Date('Last marketing email open date')
     hs_email_last_click_date = fields.Date('Last marketing email click date')
     hs_email_last_email_name = fields.Text("Last marketing email name")
     hs_marketable_until_renewal = fields.Boolean('Marketing Until Next Update')
     hs_email_optout = fields.Boolean('Unsubscribed from all email')     
     _247_customer = fields.Boolean('247 Customer')
     np_score = fields.Selection(NP_SCORE, "NP Score")
     crr = fields.Selection(CRR, 'CRR')
     bus_mfg = fields.Selection(BUS_MFG, 'Bus MFG')
     bus_type = fields.Selection(BUS_TYPE, 'Bus Type')
     service_plan_type = fields.Selection(SERVICE_PLAN_TYPE, 'Service Plan Type')
     fleet_inspection = fields.Boolean('Fleet Inspection')   
     no_vehicles_serviced = fields.Integer('# Vehicles Serviced')
     camera_vendor = fields.Selection(CAMERA_VENDOR, 'Camera Vendor')
     shield_cams = fields.Boolean('Shield Cams')
     stop_arm_third_party = fields.Selection(STOP_ARM_THIRD_PARTY, 'Stop Arm Third Party')
     district_type = fields.Selection(DISTRICT_TYPE, 'District Type')
     no_bell_times = fields.Selection(NO_BELL_TIMES, '# Bell Times')

