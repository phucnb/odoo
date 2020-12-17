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

SERVER_TYPE = [
    ('LAPTOP', 'Laptop'),
    ('BLADE SERVER', 'Blade Server'),
    ('ML310EG8', 'HP ProLiant ML310e Gen8'),
    ('ML30G9', 'HP ProLiant ML30 Gen9'),
    ('ML30G10', 'HP Proliant ML30 Gen10'),
    ('ML110G10', 'HP Prolant ML110 Gen10'),
    ('WXPLGV2', 's247 TD Control Center'),
]
 
WIRELESS_SPEED = [
    ('24GHZ', '2.4GHz'),
    ('5GHZ', '5GHz'),
    ('MIXED', 'Mixed')
]
 
WAP_TYPE = [
    ('OMNI', 'Omnidirectional'),
    ('DIRECT_NON_NANO', 'Directional Antenna w/ standard AP'),
    ('NANO', 'Nanobeam'),
    ('MIXED', 'Mixed'),
]
 
SERVICE_PLAN_TYPE = [
    ('THREE PHASE', 'Three Phase'),
    ('TWO PHASE', 'Two Phase'),
    ('ONE PHASE', 'One Phase'),
    ('FLEET INSPECTION', 'Fleet Inspection'),
]

OPTIONS2 = [
    ('247Security', '247Security'),
    ('Angletrax', 'Angletrax'),
    ('Gatekeeper', 'Gatekeeper'),
    ('Provision', 'Provision'),
    ('REI', 'REI'),
    ('Safety Vision', 'Safety Vision'),
    ('Seon', 'Seon'),
    ('Other', 'Other')
]

WIRELESS = [
    ('TOUCHDOWN I', 'Touchdown I'),
    ('TOUCHDOWN II', 'Touchdown II'),
    ('Touchdown II (50)', 'Touchdown II (50)'),
    ('Touchdown II (100)', 'Touchdown II (100)'),
    ('Quoted Touchdown II', 'Quoted Touchdown II'),
    ('Mini Smart Server', 'Mini Smart Server'),
    ('NO', 'NO')
]
 
WIRELESS_PLATFORM = [
    ('TOUCHDOWN', 'Touchdown'),
    ('CLOUD', 'Cloud'),
]
 
TOUCHDOWN_TYPE = [
    ('TD50', 'TD50'),
    ('TD100', 'TD100'),
    ('TD200', 'TD200'),
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
     camera_vendor_specify = fields.Char("Specify Vendor")
     shield_cams = fields.Boolean('Shield Cams')
     stop_arm_third_party = fields.Selection(STOP_ARM_THIRD_PARTY, 'Stop Arm Third Party')
     district_type = fields.Selection(DISTRICT_TYPE, 'District Type')
     no_bell_times = fields.Selection(NO_BELL_TIMES, '# Bell Times')

     child_ids = fields.One2many(
        'res.partner', 'parent_id',
        string='Contact',
        domain=[('active', '=', True)]
     )  # force "active_test" domain to bypass _search() override
     
     main_contact = fields.Many2one(
            'res.partner', string='Main Contact'
     )
        
     main_contact_title = fields.Char(
            string='Main Contact Title',
            related='main_contact.function', related_sudo=True, compute_sudo=True,
            readonly=True, store=True, index=True
     )
     
     main_contact_phone = fields.Char(
            string='Main Contact Phone',
            related='main_contact.phone', related_sudo=True, compute_sudo=True,
            readonly=True, store=True, index=True
     )

      # ***CAMERA TAB***
     camera_vendor = fields.Selection(OPTIONS2, "Camera Vendor")
     camera_vendor_other = fields.Boolean("Other")
     camera_vendor_specify = fields.Char("Specify Vendor")
     camera_number = fields.Integer("# of Cameras")
     camera_number_per_bus = fields.Integer("# of Cameras / Bus")
     camera_type_shield = fields.Boolean("Shield Cam")
     camera_type_sac = fields.Boolean("Stop Arm Camera")
     camera_type_sac_3rd_pt = fields.Boolean("SAC - 3rd Party")
     camera_type_sac_3rd_pt_vendor = fields.Selection(OPTIONS2, "3rd Party Vendor")
     camera_type_sac_3rd_pt_specify = fields.Char("Specify Vendor")
     camera_vendor_pref = fields.Selection(OPTIONS2, "Preferred Vendor")
     camera_vendor_pref_specify = fields.Char("Specify Vendor")

    # ***SERVICE TAB***
     service_plan = fields.Boolean("Service Plan")
     service_plan_type = fields.Selection(SERVICE_PLAN_TYPE, "Agreement Type")
     service_vehicle_num = fields.Integer("Number of Vehicles Serviced")
     service_po_received = fields.Date("Service Order Signed")

      # ***WIRELESS TAB***
     wireless_check = fields.Boolean("Wireless")
     wireless_platform = fields.Selection(WIRELESS_PLATFORM, "Platform")
     touchdown_type = fields.Selection(TOUCHDOWN_TYPE, "Touchdown Type")
     mss_check = fields.Boolean("MSS")
     mss_count = fields.Integer("MSS Count")
     server_type = fields.Selection(SERVER_TYPE, "Server Type")
     wireless_speed = fields.Selection(WIRELESS_SPEED, "Wireless Speed")
     wireless_ap_type = fields.Selection(WAP_TYPE, "AP Type")
     wireless_ap_count = fields.Integer("AP Count")
     wireless_vehicle_count = fields.Integer("Vehicle Count")
     tv_access = fields.Boolean("TeamViewer")
     tv_id = fields.Char("TeamViewer ID")
     tv_version = fields.Char("TeamViewer Version") 
     tv_monitor = fields.Boolean("TeamViewer Monitor")
     server_inst_date = fields.Date("Server Install Date")

     is_not_tags = fields.Boolean(
        string='Is not tags', default=False,
        compute='_compute_is_not_tags', compute_sudo=True, related_sudo=True
     )

     # def _compute_is_not_tags(self):
     #    for record in self:
     #        record.is_not_tags = True if record.category_id else False



