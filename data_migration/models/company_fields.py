from odoo import models, fields, api


TERRITORY = [
    ('Central', 'Central'),
    ('Mid-West', 'Mid-West'),
    ('South East', 'South East'),
    ('North West', 'North West'),
    ('South West', 'South West'),
    ('S247', 'S247'),
    ('PW Eastern US', 'PW Eastern US'),
    ('PW Western US', 'PW Western US')
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

NUMBER_OF_CAMERAS_PER_BUS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
]


TOUCHDOWN = [
    ('No', 'No'),
    ('Local', 'Local'),
    ('Cloud Services', 'Cloud Services'),
    ('true', 'true')
]

FLEET_SIZE = [
    ('1-30', '1-30'), ('31-60', '31-60'), ('61-100', '61-100'),
    ('101-150', '101-150'), ('151-200', '151-200'), ('201+', '201+'),
]

S247_PROSPECT_STATUS = [
    ('Lead', 'Lead'), ('Lead with Interest', 'Lead with Interest'),
    ('Online Presentation', 'Online Presentation'),
    ('On-site Presentation', 'On-site Presentation'),
    ('Quoted', 'Quoted'), ('Demo', 'Demo'),
    ('PO Received', 'PO Received')
]

S247_WIRELESS = [
    ('TD50', 'TD50'), ('TD100', 'TD100'),
    ('TD200', 'TD200'), ('S247 TD100', 'S247 TD100'),
    ('S247 TD200', 'S247 TD200'),
    ('Quoted TD', 'Quoted TD'), ('No TD', 'No TD')
]

SERVICE_PLAN = [
    ('Fleet Inspection Only', 'Fleet Inspection Only'),
    ('Yes', 'Yes'), ('Quoted 2019/2020', 'Quoted 2019/2020'),
    ('No', 'No')
]

OPTIONS = [
    ('Yes', 'Yes'), ('No', 'No'), ('Looking', 'Looking'), ('MiniTRACK', 'MiniTRACK'), ('Speed & Mapping', 'Speed & Mapping')
]

GPS_VENDORS = [
    ('Zonar', 'Zonar'), ('Synovia', 'Synovia'),
    ('Motorola', 'Motorola'), ('Samsara', 'Samsara'),
    ('Geotab', 'Geotab'), ('Versatrans', 'Versatrans'),
    ('Seon', 'Seon'), ('Unknown', 'Unknown'),
    ('Other', 'Other')
]

STUDENT_INFO_SYSTEM = [
    ('Infinite Campus', 'Infinite Campus'),
    ('Power School', 'Power School'), ('Skyward', 'Skyward'),
    ('E-school', 'E-school'), ('School Tool', 'School Tool'),
    ('Unkown', 'Unknown'),
    ('Other', 'Other')
]

STUDENT_TRACK_PRO = [
    ('Bus Boss', 'Bus Boss'), ('Seon', 'Seon'), ('Synovia', 'Synovia'),
    ('Transfinder', 'Transfinder'), ('Versatrans', 'Versatrans'),
    ('Zonar', 'Zonar'), ('Other', 'Other')
]

PARENT_PORTAL_PRO = [
    ('Here Comes the Bus(Synovia)', 'Here Comes the Bus(Synovia)')   ,
    ('MyStop(Versatrans)', 'MyStop(Versatrans)'),
    ('Stopfinder(Transfinder)', 'Stopfinder(Transfinder)'),
    ('SafeStop', 'SafeStop'), ('Treker', 'Treker'),
    ('Other', 'Other')
]

ROUTING_SOLUTION = [
    ('Manual', 'Manual'), ('Spreadsheet', 'Spreadsheet'),
    ('Google type maps', 'Google type maps'), ('Bus Boss', 'Bus Boss'),
    ('Seon Path', 'Seon Path'), ('Compass', 'Compass'),
    ('Transfinder', 'Transfinder'), ('Edulog', 'Edulog'),
    ('Versatrans', 'Versatrans'), ('Trapeze', 'Trapeze'),
    ('Unknown', 'Unknown'), ('Other', 'Other')
]

FLEET_MAIN_SYSTEM = [
    ('Servicefinder', 'Servicefinder'),
    ('Fleetmatics', 'Fleetmatics'),
    ('Dolphin', 'Dolphin'),
    ('RTA', 'RTA'),
    ('Seon', 'Seon'),
    ('Versatrans', 'Versatrans'),
    ('Unkown', 'Unknown'),
    ('Other', 'Other')
]

S247_LIFECYCLE_STAGE = [
    ('Active Client', 'Active Client'),
    ('Past Client', 'Past Client'),
    ('Prospect', 'Prospect')
]

BID_STATUS = [
    ('Currently in bid process - DO NOT CALL', 'Currently in bid process - DO NOT CALL'),
    ('Bid submitted - Awaiting response', 'Bid submitted - Awaiting response'),
    ('RFP retracted by owner', 'RFP retracted by owner'),
    ('Opportunity sent over to UbicaBus', 'Opportunity sent over to UbicaBus'),
    ('Opportunity sent up to Surveillance-247', 'Opportunity sent up to Surveillance-247'),
    ('Requested further information from us', 'Requested further information from us'),
    ('Requested demonstration from us', 'Requested demonstration from us'),
    ('Requested interview from us', 'Requested interview from us'),
    ('Requested interview/demonstration from us', 'Requested interview/demonstration from us'),
    ('Declined to Bid', 'Declined to Bid'),
    ('Bid closed Won', 'Bid closed Won'),
    ('Bid closed Lost', 'Bid closed Lost')
]

BUSINESS_VERTICAL = [
    ('School Bus', 'School Bus'),
    ('PW', 'PW'), ('Taxi', 'Taxi'),
    ('Transit', 'Transit'), ('Other', 'Other')
]

CAMERAS = [
    ('Omniview360°', 'Omniview360°'),
    ('Standard View', 'Standard View'),
    ('N/A', 'N/A')
]

COMPANY_TYPE = [
    ('Association', 'Association'),
    ('Contractor', 'Contractor')
    # ('Dealer', 'Dealer'),
    # ('Distributor', 'Distributor'),
    # ('Partner', 'Partner'),
    # ('School Bus Dealer', 'School Bus Dealer'),
    # ('School District', 'School District'),
    # ('Vendor', 'Vendor')
]

Customer_Rating = [
    ('Competitor', 'Competitor'), ('Contractor', 'Contractor'),
    ('Contractor/Client', 'Contractor/Client'),
    ('Client S247', 'Client S247'), ('Dealer', 'Dealer'),
    ('Indiana Prospect', 'Indiana Prospect'),
    ('Indiana Service Client', 'Indiana Service Client'),
    ('New Client', 'New Client'), ('Trade Show', 'Trade Show'),
    ('CURRENT CLIENT', 'Current Client')
]

DEALER_SUB_TYPE = [
    ('Dealer', 'Dealer'), ('Preferred Dealer', 'Preferred Dealer'),
    ('OEM', 'OEM'), ('School Bus Dealer', 'School Bus Dealer'),
    ('Preferred School Bus Dealer', 'Preferred School Bus Dealer')
]

EXTERNAL_CAMERA = [
    ('Single Lens', 'Single Lens'), ('Dual Lens', 'Dual Lens'),
    ('NONE', 'NONE')
]

ISSR = [
    ('Antavia Cooper', 'Antavia Cooper'),
    ('Brian Sapp', 'Brian Sapp'), ('Damon Whitlock', 'Ross Evart'),
    ('Kristi Keaton', 'Kristi Keaton'), ('Lora Pirie-Stafford', 'Lora Pirie-Stafford'),
    ('NE ISSR unnamed', 'NE ISSR unnamed'), ('Carlos Ithier', 'Carlos Ithier'),
    ('Christina Graham', 'Christina Graham'), ('Syreeta Hill', 'Syreeta Hill'),
    ('Theresa Jensen', 'Theresa Jensen')
]

NADP = [
    ('Master Dealer', 'Master Dealer'),
    ('Dealer', 'Dealer'),
    ('Reseller', 'Reseller'),
    ('Sub-Dealer', 'Sub-Dealer'),
    ('Distributor', 'Distributor'),
    ('Partner', 'Partner'),
    ('End-User', 'End-User'),
    ('Installer', 'Installer'),
    ('Target-Active', 'Target-Active'),
    ('Target-Inactive', 'Target-Inactive')
]

PRODUCTS = [
    ('Zeus Pt', 'Zeus Pt'),
    ('Zeus HD', 'Zeus HD'), ('TRS', 'TRS')
]

RSM = [
    ('Brittany Wilkening', 'Brittany Wilkening'),
    ('Brooke Evers', 'Brooke Evers'),
    ('Eddie O\'Connell', 'Eddie O\'Connell'),
    ('Mary Kohn', 'Mary Kohn'),
    ('Rich Hyland', 'Rich Hyland')
]

SALE_REP = [
    ('Brett Adoff', 'Brett Adoff'),
    ('Carlos Ithier', 'Carlos Ithier'),
    ('Christina Graham', 'Christina Graham'),
    ('Larry Silba', 'Larry Silba'),
    ('Syreeta Hill', 'Syreeta Hill'),
    ('Theresa Jensen', 'Theresa Jensen')
]

VENDOR = [
    ('Blue Bird', 'Blue Bird'),
    ('Collins', 'Collins'),
    ('IC', 'IC'),
    ('Thomas', 'Thomas'),
    ('Unknown', 'Unknown'),
    ('Transit', 'Transit'),
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

CUSTOMER_PROFILE = [('tier_1', 'Tier 1'), ('tier_2', 'Tier 2'), ('tier_3', 'Tier 3')]

HUBSPOT_TEAM = [
    ('216026', 'Surveillance-247'),
    ('1062727', 'S247S'),
    ('216255', 'PW'),
    ('398602', 'NADP'),
    ('216184', '247Security'),
]


class CustomCompany(models.Model):
    _inherit = 'res.partner'

    dealer_sold_through = fields.Many2many('res.partner_dealer_sold_through', 'partner_id_dealer_sold_through_id',
                                           'partner_id', 'dealer_sold_through_id', 'Dealer Sold Through',
                                           help='Please add from where dealer sold through?')
    camera_system = fields.Many2many('res.partner_camera_system', 'partner_id_camera_system_id', 'partner_id',
                                     'camera_system_id', 'Camera System',
                                     help='Please add/select 247Security, Angletrax, Gatekeeper, '
                                          'Provision, REI, Safety Vision, Seon, Other')
    camera_system_other_ = fields.Char('Camera System Other')
    of_cameras_per_bus = fields.Selection(NUMBER_OF_CAMERAS_PER_BUS, 'Number of camera per bus')
    e360_cameras = fields.Selection(OPTIONS, 'E360 cameras')
    how_many_lots_ = fields.Many2many('res.partner_how_many_lots_', 'partner_id_how_many_lots__id', 'partner_id',
                                      'how_many_lots__id', 'How many lots',
                                      help='Please add/select number of lots e.g. lot1, lot2, lot3...')
    lot_1_address = fields.Text("Lot1 Address")
    lot_2_address = fields.Text("Lot2 Address")
    bus_garage = fields.Char("Bus Garage")
    erie_1_boces = fields.Boolean("ERIE 1 BOCES")
    # fleet_size = fields.Selection(FLEET_SIZE, "Fleet Size")
    fleet_size = fields.Integer("Fleet Size")
    of_buses = fields.Integer("# of buses")
    contracted_services = fields.Boolean("Contract Services")
    contracted_with = fields.Char("Contract With")
    contract_expires = fields.Date("Contract Expires")
    gps = fields.Selection(OPTIONS, "GPS")
    gps_vendor = fields.Selection(GPS_VENDORS, 'GPS Vendor')
    gps_vendor_other_ = fields.Char("GPS Vendor(Other)")
    fleet_maintenance_system = fields.Selection(FLEET_MAIN_SYSTEM, 'Fleet Maintenance System')
    fleet_maintenance_system_other_ = fields.Char('Fleet Maintenance System(Other)')
    n247_bus_saleman = fields.Char('247 Bus Saleman')
    n247s_lifecycle_stage = fields.Selection(S247_LIFECYCLE_STAGE, "247S Lifecycle Stage")
    annual_revenue = fields.Float('Annual Revenue')
    bid_awarded_year = fields.Char('Bid Awarded & Year')
    bid_potential = fields.Char('Bid Potential')
    bid_reference = fields.Boolean('Bid Reference')
    bid_status = fields.Selection(BID_STATUS, 'Bid Status')
    business_vertical = fields.Selection(BUSINESS_VERTICAL, 'Business Vertical')
    business_vertical_other_ = fields.Char("Business Vertical(Other)")
    cameras = fields.Selection(CAMERAS, 'Cameras')
    company_type = fields.Selection(selection_add=COMPANY_TYPE)
    competitor = fields.Many2many('res.partner_competitor', 'partner_id_competitor_id', 'partner_id', 'competitor_id',
                                  help='Please add/select the name of competitor e.g. Seon, AT, Pro-Vision etc')
    contractor = fields.Char("Contractor")
    dealer_sub_type = fields.Selection(DEALER_SUB_TYPE, 'Dealer Sub-Type')
    external_camera = fields.Selection(EXTERNAL_CAMERA, 'External Camera')
    issr = fields.Selection(ISSR, 'ISSR')
    minitrack = fields.Boolean('MiniTRACK')
    netsuite_customer = fields.Char("NetSuite Customer")
    netsuite_refresh = fields.Char("NetSuite Refresh")
    netsuite_status = fields.Char("NetSuite Status")
    netsuite = fields.Char("NetSuite")
    number_of_sales_personnel = fields.Integer("Number of sales personnel")
    of_students_total = fields.Integer("# of total students")
    of_students_transported = fields.Integer("# of students transported")
    number_of_special_needs_students_transported = fields.Integer("Number of special needs students transported")
    opportunity_number = fields.Char("Opportunity Number")
    parent_portal = fields.Selection(PARENT_PORTAL_PRO, 'Parent Portal Provider')
    parent_portal_other_ = fields.Char("Parent Portal Provider(Other)")
    parent_portal_system = fields.Selection(OPTIONS, 'Parent Portal System')
    preferred_camera_vendor = fields.Selection(OPTIONS2, 'Preferred Camera Vendor')
    preferred_camera_vendor_cloned_ = fields.Char('Preferred Camera Vendor Other')
    previous_camera_system = fields.Many2many('res.partner_previous_camera_system',
                                              'partner_id_previous_camera_system_id', 'partner_id',
                                              'previous_camera_system_id', 'Previous Camera System',
                                              help='Please add/select the name of previous camera system '
                                                   'e.g. AngelTrax, Seon, Gatekeeper etc')
    products = fields.Selection(PRODUCTS, 'Products')
    purchase_date = fields.Char('Purchase Date')
    purchased_list_july = fields.Boolean('Purchased List-July')
    remove = fields.Char('Remove')
    rfp_date_posted = fields.Char('RFP & date due')
    routing = fields.Selection(OPTIONS, 'Routing')
    routing_solution = fields.Selection(ROUTING_SOLUTION, 'Routing Solution')
    routing_solution_other_ = fields.Char('Routing Solution(Other)')
    rsm = fields.Selection(RSM, 'RSM')
    fleet_size_s247 = fields.Char("S247 Bus Fleet Size")
    surveillance_247_company_domain = fields.Char("S247 Company Domain")
    s247_contact_email = fields.Char("S247 Contact Email")
    s247_county = fields.Char("S247 County")
    surveillance_247_district = fields.Char("S247 District")
    s247_first_name = fields.Char("S247 First Name")
    s247_last_name = fields.Char("S247 Last Name")
    s247_pre_post_salutation = fields.Char("S247 Pre/Post Salutation")
    s247_lead_contact = fields.Char("S247 Lead Contact")
    prospect_status_s247 = fields.Selection(S247_PROSPECT_STATUS, "S247 Prospect Status")
    s247_title = fields.Char("S247 Title")
    wireless_s247 = fields.Selection(S247_WIRELESS, "S247 Wireless")
    sales_rep = fields.Selection(SALE_REP, 'Sale Rep')
    school_year_budget_begins = fields.Date('School Year Budget Begins')
    school_year_start = fields.Date('School Year Start')
    service_agreement = fields.Selection(SERVICE_PLAN, 'Service Plan')
    sic_code = fields.Integer("Sic Code")
    status = fields.Char("Status")
    stop_arm_camera_s_ = fields.Selection(OPTIONS, 'Stop arm cameras')
    student_count = fields.Char("Student Count")
    student_information_system = fields.Selection(STUDENT_INFO_SYSTEM, "Student Information System")
    student_information_system_other_ = fields.Char("Student Information System(Other)")
    student_tracking = fields.Selection(OPTIONS, 'Student Tracking')
    student_tracking_system = fields.Selection(STUDENT_TRACK_PRO, 'Student Tracking Provider')
    student_tracking_system_other_ = fields.Char("Student Tracking Provides(Other)")
    # service_surveillance_owner = fields.Many2one('res.users', "Surveillance-247 Owner")
    system = fields.Many2many('res.partner_system', 'partner_id_system_id', 'partner_id', 'system_id',
                              'System', help='Please add/select the name of system')
    territory = fields.Selection(TERRITORY, "Territory")
    touchdown = fields.Selection(TOUCHDOWN, "Touchdown")
    touchdown_cloud_services_amount = fields.Char("Touchdown Cloud Services Amount")
    touchdown_cloud_services_renewal_date = fields.Date("Touchdown Cloud Services Renewal Date")
    touchdown_install_date = fields.Date("Touchdown Install Date")
    unique_identifier = fields.Char("Unique Identifier")
    vendor = fields.Selection(VENDOR, "Vendor")
    td_fleet_monitor = fields.Boolean('TD Fleet Monitor')
    web_technologies = fields.Many2many('res.partner_web_technologies', 'partner_id_web_technologies_id',
                                        'partner_id', 'web_technologies_id', 'Web Technologies')
    territory_coverage = fields.Many2many('res.partner_territory_coverage', 'partner_id_territory_coverage_id',
                                          'partner_id', 'territory_coverage_id', 'Territory Coverage')

    about_us = fields.Char("About Us")
    closedate = fields.Date("Close Date")
    # customer_rating = fields.Selection(Customer_Rating, 'Customer Rating')
    description = fields.Text("Description")
    facebook_company_page = fields.Char("Facebook Company Page")
    facebookfans = fields.Integer("Facebook Fans")
    first_conversion_event_name = fields.Char("First Conversion")
    first_conversion_date = fields.Date("First Conversion Date")
    hs_analytics_first_touch_converting_campaign = fields.Char("First Touch Converting Campaign")
    hs_ideal_customer_profile = fields.Selection(CUSTOMER_PROFILE, "Ideal Customer Profile Tier")
    is_public = fields.Boolean("Is Public")
    nadp = fields.Selection(NADP, 'NADP')
    hs_num_contacts_with_buying_roles = fields.Integer("Number of contacts with a buying role")
    hs_num_decision_makers = fields.Char("Number of decision makers")
    numberofemployees = fields.Integer("Number of Employees")
    num_conversion_events = fields.Integer("Number of Form Submissions")
    hs_num_open_deals = fields.Integer("Number of open deals")
    hs_analytics_num_page_views = fields.Integer("Number of page views")
    hs_analytics_num_visits = fields.Integer("Number of Sessions")
    num_contacted_notes = fields.Integer("Number of times contacted")
    recent_conversion_event_name = fields.Char("Recent Conversion")
    recent_conversion_date = fields.Date("Recent Conversion Date")
    engagements_last_meeting_booked_source = fields.Char("Source of last booking in meetings tool")
    total_revenue = fields.Float("Total Revenue")
    # wireless = fields.Selection(WIRELESS, "Wireless")
    founded_year = fields.Char("Year Founded")

    first_contact_createdate = fields.Date("First Contact Create Date")
    first_deal_created_date = fields.Date("First Deal Created Date")
    notes_last_updated = fields.Date("Last Activity Date")
    hs_last_booked_meeting_date = fields.Date("Last Booked Meeting Date")
    notes_last_contacted = fields.Date("Last Contacted")
    hs_last_logged_call_date = fields.Date("Last Logged Call Date")
    hs_lastmodifieddate = fields.Date("Last Modified Date")
    hs_last_open_task_date = fields.Date("Last Open Task Date")
    hs_last_sales_activity_timestamp = fields.Datetime("Last Sales Activity Date")
    hs_analytics_last_touch_converting_campaign = fields.Char("Last Touch Converting Campaign")
    engagements_last_meeting_booked_medium = fields.Char("Medium of last booking in meetings tool")
    hs_num_child_companies = fields.Integer("Number of child companies")
    hubspot_owner_assigneddate = fields.Date("Owner Assigned Date")
    recent_deal_amount = fields.Float("Recent Deal Amount")
    recent_deal_close_date = fields.Date("Recent Deal Close Date")
    hs_analytics_first_timestamp = fields.Datetime("Time First Seen")
    hs_analytics_last_timestamp = fields.Datetime("Time Last Seen")
    hs_analytics_first_visit_timestamp = fields.Datetime("Time of First Session")
    hs_analytics_last_visit_timestamp = fields.Datetime("Time of Last Session")
    total_money_raised = fields.Char("Total Money Raised")
    hs_total_deal_value = fields.Date("Total open deal value")
    number_of_buses = fields.Integer("Number of Buses")
    hubspot_team_id = fields.Selection(HUBSPOT_TEAM, 'Hubspot Team')
    number_of_total_students = fields.Integer('Number of Total Students')
    website = fields.Char('Website URL')

    @api.model
    def _compute_opportunity_count(self):
        for partner in self:
            if partner.is_company:
                partner.opportunity_count = self.env['crm.lead'].search_count([('hs_deal_companies', '=', partner.id)])
            else:
                partner.opportunity_count = self.env['crm.lead'].search_count([('hs_deal_contacts', '=', partner.id)])

    def action_view_opportunity(self):
        '''
        This function returns an action that displays the opportunities from partner.
        '''
        action = self.env.ref('crm.crm_lead_opportunities').read()[0]
        if self.is_company:
            action['domain'] = [('hs_deal_companies', '=', self.id)]
        else:
            action['domain'] = [('hs_deal_contacts', '=', self.id)]
        return action
