# -*- coding: utf-8 -*-
from odoo import models, fields, api


LIFECYCLE_STAGE = [
    ('subscriber', 'Subscriber'),
    ('lead', 'Lead'),
    ('marketingqualifiedlead', 'Marketing qualified lead'),
    ('salesqualifiedlead', 'Sales qualified lead'),
    ('opportunity', 'Opportunity'),
    ('customer', 'Customer'),
    ('evangelist', 'Evangelist'),
    ('other', 'Other'),
]

LEAD_TYPE = [
    ('School', 'School'),
    ('Bus dealer', 'Bus dealer'),
    ('Bus Contractor', 'Bus Contractor'),
    ('PW - Partner', 'PW - Partner'),
    ('PW - End-User', 'PW - End-User'),
    ('BID', 'BID')
]

ROLES = [
    ('ASSISTANT DIRECTOR', 'Assistant Director'),
    ('DIRECTOR', 'Director'),
    ('Fleet Manager', 'Fleet Manager'),
    ('IT', 'IT'),
    ('MECHANIC', 'Mechanic'),
    ('ROUTE PLANNER', 'Route Planner'),
    ('TRAINING COORDINATOR', 'Training Coordinator'),
    ('OTHER', 'Other')
]

INFLUENCE = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

AREA_CODE = [
    ('607', '607'), ('585', '585'), ('719', '719'),
    ('845', '845'), ('518', '518'), ('516', '516'),
    ('615', '615'), ('315', '315'), ('716', '716')
]


SECURITY_BLOG_EMAIL_SUBSCRIPTION = [('instant', 'Instant'),
                                    ('daily', 'Daily'), ('weekly', 'Weekly'),
                                    ('monthly', 'Monthly')]

IACP = [
    ('Yes', 'YES'), ('2019', '2019'), ('2020', '2020'),
    ('2021', '2021'), ('2022', '2022'), ('2023', '2023'),
    ('2024', '2024'), ('2025', '2025')
]

NO_OF_EMPLOYEES = [
    ('1-5', '1-5'), ('5-25', '5-25'), ('25-50', '25-50'),
    ('50-100', '50-100'), ('100-500', '100-500'), ('500-1000', '500-1000'),
    ('1000+', '1000+')
]

ORIGINAL_SOURCE = [
    ('ORGANIC_SEARCH', 'Organic search'), ('PAID_SEARCH', 'Paid search'), ('EMAIL_MARKETING', 'Email Marketing'),
    ('SOCIAL_MEDIA', 'Social media'), ('REFERRALS', 'Referrals'), ('OTHER_CAMPAIGNS', 'Other campaigns'),
    ('DIRECT_TRAFFIC', 'Direct traffic'), ('OFFLINE', 'Offline sources'), ('PAID_SOCIAL', 'Paid social')
]

PERSONA = [
    ('persona_2', 'Small School Samuel'), ('persona_4', 'Large School Larry'),
    ('persona_6', 'Mid Size Marge'), ('persona_7', 'Contractor Carl'),
    ('persona_8', 'Dealer Dan')
]

PRODUCT_INTERESTED = [
    ('ZeusPT', 'ZeusPT'), ('TouchDown', 'TouchDown'),
    ('247Now-Live GPS', '247Now-Live GPS'), ('SmartStop', 'SmartStop'),
    ('OmniView 360', 'OmniView 360'), ('DVR Viewer', 'DVR Viewer'),
    ('Temperature Sensing Station (TSS)', 'Temperature Sensing Station (TSS)')
]

SOLUTION_INSTALLED = [
    ('Gatekeeper', 'Gatekeeper'), ('Angel Trax', 'Angel Trax'),
    ('Seon', 'Seon'), ('REI', 'REI'),
    ('Safety Vision', 'Safety Vision'),
    ('Pro Vision', 'Pro Vision'), ('Other', 'Other')
]


class ContactFields(models.Model):
    _inherit = 'res.partner'

    hubspot_id = fields.Char("Hubspot Id")
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    life_cycle_stage = fields.Selection(LIFECYCLE_STAGE, "Lifecycle Stage")
    lead_type = fields.Selection(LEAD_TYPE, "Lead Type")
    role = fields.Selection(ROLES, "Role")
    job_title = fields.Char("Job Title")
    job_title_secondary = fields.Char("Job Title-Secondary")
    job_function = fields.Char("Job Function")
    date_of_birth = fields.Date("Date of Birth")
    linkedin_bio = fields.Char("LinkedIn Bio")
    reports_to = fields.Char("Report To")
    purchasing_influence = fields.Selection(INFLUENCE, "Purchasing Influence")
    years_with_company = fields.Integer("Years with Company")
    planned_retirement_date = fields.Date("Planned Retirement Date")
    no_longer_at_school_district_company = fields.Boolean("No longer at school/district/company?")
    why_not_at_school_district_company_ = fields.Char("Why not at school/district/company?")
    did_they_go_to_a_new_school_district_company_ = fields.Boolean("Did they go to a new school/district/company?")
    what_school_district_company_did_they_go_ = fields.Char("What school/district/company did they go?")
    n247_dvr_total = fields.Char("247 DVR Total")
    security_blog_email_subs = fields.Selection(SECURITY_BLOG_EMAIL_SUBSCRIPTION, "247Security Blog Email Subscription",
                                                help="Please select/add years e.g 2015, 2016 ...")
    aapt_ar_ = fields.Many2many('res.partner_years', 'partner_id_year_id53', 'partner_id', 'year_id', "AAPT(AR)",
                               help="Please select/add years e.g 2015, 2016 ...")
    aasbo_az_ = fields.Many2many('res.partner_years', 'partner_id_year_id52', 'partner_id', 'year_id', "AASBO(AZ)",
                                help="Please select/add years e.g 2015, 2016 ...")
    accounting_contact_full_name = fields.Char("Accounting Contact Full Name")
    accounting_email = fields.Char("Accounting Email")
    address2 = fields.Char("Address2")
    annual_revenue = fields.Char("Annual Revenue")
    area_code = fields.Selection(AREA_CODE, "Area Code")
    as_of_date = fields.Char("As of Date")
    asta_al_ = fields.Many2many('res.partner_years', 'partner_id_year_id51', 'partner_id', 'year_id', "ASTA(AL)",
                               help="Please select/add years e.g 2015, 2016 ...")
    average_zoom_webinar_att_duration = fields.Integer("Average Zoom webinar attendance duration")
    bus_garage = fields.Char("Bus Garage")
    business_unit = fields.Many2many('res.partner_business_unit', 'business_unit_id_name_id', 'business_unit_id', 'name_id', "Business Unit",
                                    help='Please select/add 247Security or Surveillance 247 or both')
    buying_role = fields.Many2many('res.partner_buying_role', 'buying_role_id_name_id', 'buying_role_id', 'name_id', "Buying Role",
                                  help='Please select/add Blocker, Budget Holder, Champion, Decision Maker, '
                                       'End User, Executive Sponsor, Influencer, Legal & Compliance, Other')
    cameras = fields.Char("Cameras")
    campaign_of_last_booking_in_meetings_tool = fields.Char("Campaign of last booking in meetings tool")
    casbo_ca_ = fields.Many2many('res.partner_years', 'partner_id_year_id50', 'partner_id', 'year_id', "CASBO(CA)",
                                help="Please select/add years e.g 2015, 2016 ...")
    casto_ca_ = fields.Many2many('res.partner_years', 'partner_id_year_id49', 'partner_id', 'year_id', "CASTO(CA)",
                                help="Please select/add years e.g 2015, 2016 ...")
    cgcs = fields.Many2many('res.partner_years', 'partner_id_year_id48', 'partner_id', 'year_id', "CGCS",
                           help="Please select/add years e.g 2015, 2016 ...")
    chapter_meeting_1 = fields.Many2many('res.partner_years', 'partner_id_year_id47', 'partner_id', 'year_id', "Chapter Meeting-1",
                                        help="Please select/add years e.g 2015, 2016 ...")
    company_size = fields.Char("Company Size")
    cptc_cn_ = fields.Many2many('res.partner_years', 'partner_id_year_id46', 'partner_id', 'year_id', "CPTC(CN)",
                               help="Please select/add years e.g 2015, 2016 ...")
    crtc_wa_ = fields.Many2many('res.partner_years', 'partner_id_year_id45', 'partner_id', 'year_id', "CRTC(WA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    cspta_co_ = fields.Many2many('res.partner_years', 'partner_id_year_id44', 'partner_id', 'year_id', "CSPTA(CO)",
                                help="Please select/add years e.g 2015, 2016 ...")
    ctaa = fields.Many2many('res.partner_years', 'partner_id_year_id43', 'partner_id', 'year_id', "CTAA",
                           help="Please select/add years e.g 2015, 2016 ...")
    date_of_last_meeting_booked_in_meetings_tool = fields.Date("Date of last meeting booked in meetings tool")
    days_to_close = fields.Char("Days to close")
    degree = fields.Char("Degree")
    demo = fields.Char("Demo")
    division_cf_contact = fields.Char("Division(CF)")
    external_camera = fields.Char("External Camera")
    famtec_customer = fields.Char("FAMTEC Customer")
    famtec_sales_rep = fields.Char("FAMTEC Sales Rep")
    field_of_study = fields.Char("Field of study")
    fpta_ctd = fields.Many2many('res.partner_years', 'partner_id_year_id42', 'partner_id', 'year_id', "FPTA/CTD",
                               help="Please select/add years e.g 2015, 2016 ...")
    gapt_ga_ = fields.Many2many('res.partner_years', 'partner_id_year_id41', 'partner_id', 'year_id', "GAPT(GA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    gcapt_tx_ = fields.Many2many('res.partner_years', 'partner_id_year_id40', 'partner_id', 'year_id', "GCAPT(TX)",
                                help="Please select/add years e.g 2015, 2016 ...")
    iapt_id_ = fields.Many2many('res.partner_years', 'partner_id_year_id39', 'partner_id', 'year_id', "IAPT(ID)",
                               help="Please select/add years e.g 2015, 2016 ...")
    iapt_il_ = fields.Many2many('res.partner_years', 'partner_id_year_id38', 'partner_id', 'year_id', "IAPT(IL)",
                               help="Please select/add years e.g 2015, 2016 ...")
    iacp = fields.Selection(IACP, "IACP")
    ip_city = fields.Char("IP City")
    ip_country = fields.Char("IP Country")
    ip_country_code = fields.Char("IP Country Code")
    ip_state_region = fields.Char("IP State/Region")
    ip_state_region_code = fields.Char("IP State/Region Code")
    ipta_ia_ = fields.Many2many('res.partner_years', 'partner_id_year_id37', 'partner_id', 'year_id', "IPTA(IA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    kspta_ks_ = fields.Many2many('res.partner_years', 'partner_id_year_id36', 'partner_id', 'year_id', "KSPTA(KS)",
                                help="Please select/add years e.g 2015, 2016 ...")
    last_registered_zoom_webinar = fields.Char("Last registered Zoom webinar")
    mapt_mi_ = fields.Many2many('res.partner_years', 'partner_id_year_id35',  'partner_id', 'year_id', "MAPT(MI)",
                               help="Please select/add years e.g 2015, 2016 ...")
    mapt_mo_ = fields.Many2many('res.partner_years', 'partner_id_year_id34', 'partner_id', 'year_id', "MAPT(MO)",
                               help="Please select/add years e.g 2015, 2016 ...")
    mnapt_mn_ = fields.Many2many('res.partner_years', 'partner_id_year_id33', 'partner_id', 'year_id', "MNAPT(MN)",
                                help="Please select/add years e.g 2015, 2016 ...")
    military_status = fields.Char("Military Status")
    msboa_mn_ = fields.Many2many('res.partner_years', 'partner_id_year_id32', 'partner_id', 'year_id', "MSBOA(MN)",
                                help="Please select/add years e.g 2015, 2016 ...")
    # nadp = fields.Char("NADP")
    napt = fields.Many2many('res.partner_years', 'partner_id_year_id31', 'partner_id', 'year_id', "NAPT",
                           help="Please select/add years e.g 2015, 2016 ...")
    napt_na_ = fields.Many2many('res.partner_years', 'partner_id_year_id30', 'partner_id', 'year_id', "NAPT(NA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    ncpta_nc_ = fields.Many2many('res.partner_years', 'partner_id_year_id29', 'partner_id', 'year_id', "NCPTA(NC)",
                                help="Please select/add years e.g 2015, 2016 ...")
    ncst = fields.Many2many('res.partner_years', 'partner_id_year_id28', 'partner_id', 'year_id', "NCST",
                           help="Please select/add years e.g 2015, 2016 ...")
    now_in_workflow = fields.Boolean("Now in Workflow")
    now_in_sequence = fields.Boolean("Now in Sequence")
    nsba_na_ = fields.Many2many('res.partner_years', 'partner_id_year_id27', 'partner_id', 'year_id', "NSBA(NA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    nsta_mid = fields.Many2many('res.partner_years', 'partner_id_year_id26', 'partner_id', 'year_id', "NSTA-mid",
                               help="Please select/add years e.g 2015, 2016 ...")
    nsta_national = fields.Many2many('res.partner_years', 'partner_id_year_id25', 'partner_id', 'year_id', "NSTA-national",
                                    help="Please select/add years e.g 2015, 2016 ...")
    nsta_summer = fields.Many2many('res.partner_years', 'partner_id_year_id24', 'partner_id', 'year_id', "NSTA-summer",
                                  help="Please select/add years e.g 2015, 2016 ...")
    no_of_employees = fields.Selection(NO_OF_EMPLOYEES, 'No of Employees')
    oapt_oh_ = fields.Many2many('res.partner_years', 'partner_id_year_id23', 'partner_id', 'year_id', "OAPT(OH)",
                               help="Please select/add years e.g 2015, 2016 ...")
    oapt_ok_ = fields.Many2many('res.partner_years', 'partner_id_year_id22', 'partner_id', 'year_id', "OAPT(OK)",
                               help="Please select/add years e.g 2015, 2016 ...")
    oasbo_on_ = fields.Many2many('res.partner_years', 'partner_id_year_id21', 'partner_id', 'year_id', "OASBO(ON)",
                                help="Please select/add years e.g 2015, 2016 ...")
    oasbo_osba = fields.Many2many('res.partner_years', 'partner_id_year_id20', 'partner_id', 'year_id', "OASBO(OSBA)",
                                 help="Please select/add years e.g 2015, 2016 ...")
    opta_or_ = fields.Many2many('res.partner_years', 'partner_id_year_id19', 'partner_id', 'year_id', "OPTA(OR)",
                               help="Please select/add years e.g 2015, 2016 ...")
    opted_out_of_email_marketing = fields.Boolean("Opted out of email marketing information")
    opted_out_of_email_security_blog_sub = fields.Boolean("Opted out of email: 247Security Blog Subscription")
    opted_out_of_email_customer_Service = fields.Boolean("Opted out of email: Customer Service Communication")
    opted_out_of_email_one2one = fields.Boolean("Opted out of email: One to one")
    opted_out_of_email_quote_follow_up = fields.Boolean("Opted out of email: quote follow up")
    opted_out_of_email_2247_installment = fields.Boolean("Opted out of email: S247 Installment Work Orders")
    opted_out_of_email_sales_check_in = fields.Boolean("Opted out of email: sales check in")
    original_source = fields.Selection(ORIGINAL_SOURCE, "Original Source")
    original_source_dd_1 = fields.Char("Original Source drill-down 1")
    original_source_dd_2 = fields.Char("Original Source drill-down 2")
    osbma_oh_ = fields.Many2many('res.partner_years', 'partner_id_year_id18', 'partner_id', 'year_id', "OSBMA(OH)",
                                help="Please select/add years e.g 2015, 2016 ...")
    persona = fields.Selection(PERSONA, "Persona")
    population = fields.Char("Population")
    product_i_m_interested_in = fields.Selection(PRODUCT_INTERESTED, "Product I'm interested in")
    surveillance_247_district_name = fields.Char("S247 District Name")
    surveillance_247_district_website_domain = fields.Char("S247 District Website Domain")
    surveillance_247_area_code = fields.Char("S247 Area Code")
    s247_secondary_company = fields.Char("S247 Secondary Company")
    sbx = fields.Many2many('res.partner_years', 'partner_id_year_id17', 'partner_id', 'year_id', "SBX",
                          help="Please select/add years e.g 2015, 2016 ...")
    scapt_sc_ = fields.Many2many('res.partner_years', 'partner_id_year_id16', 'partner_id', 'year_id', "SCAPT(SC)",
                                help="Please select/add years e.g 2015, 2016 ...")
    solution_currently_installed = fields.One2many(SOLUTION_INSTALLED, "Solution Currently Installed")
    sesptc = fields.Many2many('res.partner_years', 'partner_id_year_id15', 'partner_id', 'year_id', "SESPTC",
                             help="Please select/add years e.g 2015, 2016 ...")
    special_instructions = fields.Char("Special Instructions")
    stai_in_ = fields.Many2many('res.partner_years', 'partner_id_year_id14', 'partner_id', 'year_id', "STAI(IN)",
                               help="Please select/add years e.g 2015, 2016 ...")
    stn = fields.Many2many('res.partner_years', 'partner_id_year_id13', 'partner_id', 'year_id', "STN",
                          help="Please select/add years e.g 2015, 2016 ...")
    sts_of_nj = fields.Many2many('res.partner_years', 'partner_id_year_id12', 'partner_id', 'year_id', "STS of NJ",
                                help="Please select/add years e.g 2015, 2016 ...")
    taa_az_ = fields.Many2many('res.partner_years', 'partner_id_year_id11', 'partner_id', 'year_id', "TAA(AZ)",
                              help="Please select/add years e.g 2015, 2016 ...")
    tapt_tn_ = fields.Many2many('res.partner_years', 'partner_id_year_id10', 'partner_id', 'year_id', "TAPT(TN)",
                               help="Please select/add years e.g 2015, 2016 ...")
    tapt_tx_ = fields.Many2many('res.partner_years', 'partner_id_year_id9', 'partner_id', 'year_id', "TAPT(TX)",
                               help="Please select/add years e.g 2015, 2016 ...")
    transfinder = fields.Many2many('res.partner_years', 'partner_id_year_id8', 'partner_id', 'year_id', "Transfinder",
                                  help="Please select/add years e.g 2015, 2016 ...")
    tsd = fields.Many2many('res.partner_years', 'partner_id_year_id7', 'partner_id', 'year_id', "TSD",
                          help="Please select/add years e.g 2015, 2016 ...")
    uapt_ut_ = fields.Many2many('res.partner_years', 'partner_id_year_id6', 'partner_id', 'year_id', "UAPT(UT)",
                               help="Please select/add years e.g 2015, 2016 ...")
    vapt_va_ = fields.Many2many('res.partner_years', 'partner_id_year_id5', 'partner_id', 'year_id', "VAPT(VA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    wapt_wa_ = fields.Many2many('res.partner_years', 'partner_id_year_id4', 'partner_id', 'year_id', "WAPT(WA)",
                               help="Please select/add years e.g 2015, 2016 ...")
    wpta_wy_ = fields.Many2many('res.partner_years', 'partner_id_year_id3', 'partner_id', 'year_id', "WPTA(WY)",
                               help="Please select/add years e.g 2015, 2016 ...")
    wsba_wi_ = fields.Many2many('res.partner_years', 'partner_id_year_id2', 'partner_id', 'year_id', "WSBA(WI)",
                               help="Please select/add years e.g 2015, 2016 ...")
    wvapt_wv_ = fields.Many2many('res.partner_years', 'partner_id_year_id1', 'partner_id', 'year_id', "WVAPT(WV)",
                                help="Please select/add years e.g 2015, 2016 ...")
    what_type_of_support = fields.Many2many('res.partner_what_type_of_support', 'partner_id_what_type_of_support_id', 'partner_id',
                                            'what_type_of_support_id', "What type of support?",
                                            help="Please select/add Software or Hardware or both")
    zoom_webinar_attendance_average_duration = fields.Char("Zoom webinar attendance average duration")
    zoom_webinar_attendance_count = fields.Integer("Zoom webinar attendance count")
    zoom_webinar_joinlink = fields.Char("Zoom webinar joinlink")
    zoom_webinar_registration_count = fields.Char("zoom webinar registration count")
    purchasing_contact_full_name = fields.Char("Purchasing contact fullname")
    purchasing_email = fields.Char("Purchasing email")
    last_rma_email_date = fields.Date("Last rma email date")
    request_a_demo = fields.Date('Resquest a demo')
    state_or_province = fields.Many2one('res.country.state', 'State or Province')
    state_or_region = fields.Many2one('res.country.state', 'State or Region')


class GetValues(models.Model):
    _name = 'get.values'

    name = fields.Char('Values')
