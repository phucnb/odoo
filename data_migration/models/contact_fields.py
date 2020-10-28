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
    ('615', '615')
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
    security_blog_email_subs = fields.Selection(SECURITY_BLOG_EMAIL_SUBSCRIPTION, "247Security Blog Email Subscription", help="Please select/add years e.g 2015, 2016 ...")
    aapt_ar_ = fields.Many2many('get.values', 'aaptr_ar_values', 'aaptr_ar', 'value', "AAPT(AR)", help="Please select/add years e.g 2015, 2016 ...")
    aasbo_az_ = fields.Many2many('get.values', 'aasbo_az_values', 'aasbo_az', 'value', "AASBO(AZ)", help="Please select/add years e.g 2015, 2016 ...")
    accounting_contact_full_name = fields.Char("Accounting Contact Full Name")
    accounting_email = fields.Char("Accounting Email")
    address2 = fields.Char("Address2")
    annual_revenue = fields.Char("Annual Revenue")
    area_code = fields.Selection(AREA_CODE, "Area Code")
    as_of_date = fields.Char("As of Date")
    asta_al_ = fields.Many2many('get.values', 'asta_al_values', 'asta_al', 'value', "ASTA(AL)", help="Please select/add years e.g 2015, 2016 ...")
    average_zoom_webinar_att_duration = fields.Integer("Average Zoom webinar attendance duration")
    bus_garage = fields.Char("Bus Garage")
    business_unit = fields.Many2many('get.values', 'business_unit_values', 'business_unit', 'value', "Business Unit", help='Please select/add 247Security or Surveillance 247 or both')
    buying_role = fields.Many2many('get.values', 'buying_role_values', 'buying_role', 'value', "Buying Role", help='Please select/add Blocker, Budget Holder, Champion, Decision Maker, End User, Executive Sponsor, Influencer, Legal & Compliance, Other')
    cameras = fields.Char("Cameras")
    campaign_of_last_booking_in_meetings_tool = fields.Char("Campaign of last booking in meetings tool")
    casbo_ca_ = fields.Many2many('get.values', 'casbo_ca_values', 'casbo_ca', 'value', "CASBO(CA)", help="Please select/add years e.g 2015, 2016 ...")
    casto_ca_ = fields.Many2many('get.values', 'casto_ca_values', 'casto_ca', 'value', "CASTO(CA)", help="Please select/add years e.g 2015, 2016 ...")
    cgcs = fields.Many2many('get.values', 'cgcs_values', 'cgcs', 'value', "CGCS", help="Please select/add years e.g 2015, 2016 ...")
    chapter_meeting_1 = fields.Many2many('get.values', 'chapter_meeting_1_values', 'chapter_meeting_1', 'value', "Chapter Meeting-1", help="Please select/add years e.g 2015, 2016 ...")
    company_size = fields.Char("Company Size")
    cptc_cn_ = fields.Many2many('get.values', 'cptc_cn_values', 'cptc_cn', 'value', "CPTC(CN)", help="Please select/add years e.g 2015, 2016 ...")
    crtc_wa_ = fields.Many2many('get.values', 'crtc_wa_values', 'crtc_wa', 'value', "CRTC(WA)", help="Please select/add years e.g 2015, 2016 ...")
    cspta_co_ = fields.Many2many('get.values', 'cspta_co_values', 'cspta_co', 'value', "CSPTA(CO)", help="Please select/add years e.g 2015, 2016 ...")
    ctaa = fields.Many2many('get.values', 'ctaa_values', 'ctaa', 'value', "CTAA", help="Please select/add years e.g 2015, 2016 ...")
    date_of_last_meeting_booked_in_meetings_tool = fields.Date("Date of last meeting booked in meetings tool")
    days_to_close = fields.Char("Days to close")
    degree = fields.Char("Degree")
    demo = fields.Char("Demo")
    division_cf_contact = fields.Char("Division(CF)")
    external_camera = fields.Char("External Camera")
    famtec_customer = fields.Char("FAMTEC Customer")
    famtec_sales_rep = fields.Char("FAMTEC Sales Rep")
    field_of_study = fields.Char("Field of study")
    fpta_ctd = fields.Many2many('get.values', 'fpta_ctd_values', 'fpta_ctd', 'value', "FPTA/CTD", help="Please select/add years e.g 2015, 2016 ...")
    gapt_ga_ =fields.Many2many('get.values', 'gapt_ga_values', 'gapt_ga', 'value', "GAPT(GA)", help="Please select/add years e.g 2015, 2016 ...")
    gcapt_tx_ = fields.Many2many('get.values', 'gcapt_tx_values', 'gcapt_tx', 'value', "GCAPT(TX)", help="Please select/add years e.g 2015, 2016 ...")
    iapt_id_ = fields.Many2many('get.values', 'iapt_id_values', 'iapt_id', 'value', "IAPT(ID)", help="Please select/add years e.g 2015, 2016 ...")
    iapt_il_ = fields.Many2many('get.values', 'iapt_il_values', 'iapt_il', 'value', "IAPT(IL)", help="Please select/add years e.g 2015, 2016 ...")
    iacp = fields.Selection(IACP, "IACP")
    ip_city = fields.Char("IP City")
    ip_country = fields.Char("IP Country")
    ip_country_code = fields.Char("IP Country Code")
    ip_state_region = fields.Char("IP State/Region")
    ip_state_region_code = fields.Char("IP State/Region Code")
    ipta_ia_ = fields.Many2many('get.values', 'ipta_ia_values', 'ipta_ia', 'value', "IPTA(IA)", help="Please select/add years e.g 2015, 2016 ...") # SELECT MULTIPLE
    kspta_ks_ = fields.Many2many('get.values', 'kspta_ks_values', 'kspta_ks', 'value', "KSPTA(KS)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    last_registered_zoom_webinar = fields.Char("Last registered Zoom webinar")
    mapt_mi_ = fields.Many2many('get.values', 'mapt_mi_values', 'mapt_mi', 'value', "MAPT(MI)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    mapt_mo_ = fields.Many2many('get.values', 'mapt_mo_values', 'mapt_mo', 'value', "MAPT(MO)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    mnapt_mn_ = fields.Many2many('get.values', 'mnapt_mn_values', 'mnapt_mn', 'value', "MNAPT(MN)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    military_status = fields.Char("Military Status")
    msboa_mn_ = fields.Many2many('get.values', 'msboa_mn_values', 'msboa_mn', 'value', "MSBOA(MN)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    nadp = fields.Char("NADP")
    napt = fields.Many2many('get.values', 'napt_values', 'napt', 'value', "NAPT", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    napt_na_ = fields.Many2many('get.values', 'napt_na_values', 'napt_na', 'value', "NAPT(NA)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    ncpta_nc_ = fields.Many2many('get.values', 'ncpta_nc_values', 'ncpta_nc', 'value', "NCPTA(NC)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    ncst = fields.Many2many('get.values', 'ncst_values', 'ncst', 'value', "NCST", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    now_in_workflow = fields.Boolean("Now in Workflow")
    now_in_sequence = fields.Boolean("Now in Sequence")
    nsba_na_ = fields.Many2many('get.values', 'nsba_na_values', 'nsba_na', 'value', "NSBA(NA)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    nsta_mid = fields.Many2many('get.values', 'nsta_mid_values', 'nsta_mid', 'value', "NSTA-mid", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    nsta_national = fields.Many2many('get.values', 'nsta_national_values', 'nsta_national', 'value', "NSTA-national", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    nsta_summer = fields.Many2many('get.values', 'nsta_summer_values', 'nsta_summer', 'value', "NSTA-summer", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    no_of_employees = fields.Selection(NO_OF_EMPLOYEES, 'No of Employees')
    oapt_oh_ = fields.Many2many('get.values', 'oapt_oh_values', 'oapt_oh', 'value', "OAPT(OH)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    oapt_ok_ = fields.Many2many('get.values', 'oapt_ok_values', 'oapt_ok', 'value', "OAPT(OK)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    oasbo_on_ = fields.Many2many('get.values', 'oasbo_on_values', 'oasbo_on', 'value', "OASBO(ON)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    oasbo_osba = fields.Many2many('get.values', 'oasbo_osba_values', 'oasbo_osba', 'value', "OASBO(OSBA)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    opta_or_ = fields.Many2many('get.values', 'opta_or_values', 'opta_or', 'value', "OPTA(OR)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
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
    osbma_oh_ = fields.Many2many('get.values', 'osbma_oh_values', 'osbma_oh', 'value', "OSBMA(OH)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    persona = fields.Selection(PERSONA, "Persona")
    population = fields.Char("Population")
    product_i_m_interested_in = fields.Selection(PRODUCT_INTERESTED, "Product I'm interested in")
    surveillance_247_district_name = fields.Char("S247 District Name")
    surveillance_247_district_website_domain = fields.Char("S247 District Website Domain")
    surveillance_247_area_code = fields.Char("S247 Area Code")
    s247_secondary_company = fields.Char("S247 Secondary Company")
    sbx = fields.Many2many('get.values', 'sbx_values', 'sbx', 'value', "SBX", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    scapt_sc_ = fields.Many2many('get.values', 'scapt_sc_values', 'scapt_sc', 'value', "SCAPT(SC)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    solution_currently_installed = fields.Many2many('get.values', 'solution_currently_installed_values', 'solution_currently_installed', 'value', "Solution Currently Installed", help="Please select/add GateKeeper, Angel Trax, Seon, Safety Vision, Pro Vision, Other")  # SELECT MULTIPLE
    sesptc = fields.Many2many('get.values', 'sesptc_values', 'sesptc', 'value', "SESPTC", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    special_instructions = fields.Char("Special Instructions")
    stai_in_ = fields.Many2many('get.values', 'stai_in_values', 'stai_in', 'value', "STAI(IN)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    stn = fields.Many2many('get.values', 'stn_values', 'stn', 'value', "STN", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    sts_nj = fields.Many2many('get.values', 'sts_nj_values', 'sts_nj', 'value', "STN(NJ)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    taa_az_ = fields.Many2many('get.values', 'taa_az_values', 'taa_az', 'value', "TAA(AZ)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    tapt_tn_ = fields.Many2many('get.values', 'tapt_tn_values', 'tapt_tn', 'value', "TAPT(TN)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    tapt_tx_ = fields.Many2many('get.values', 'tapt_tx_values', 'tapt_tx', 'value', "TAPT(TX)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    transfinder = fields.Many2many('get.values', 'transfinder_values', 'transfinder', 'value', "Transfinder", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    tsd = fields.Many2many('get.values', 'tsd_values', 'tsd', 'value', "TSD", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    uapt_ut_ = fields.Many2many('get.values', 'uapt_ut_values', 'uapt_ut', 'value', "UAPT(UT)", help="Please select/add years e.g 2015, 2016 ...") # SELECT MULTIPLE
    vapt_va_ = fields.Many2many('get.values', 'vapt_va_values', 'vapt_va', 'value', "VAPT(VA)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    wapt_wa_ = fields.Many2many('get.values', 'wapt_wa_values', 'wapt_wa', 'value', "WAPT(WA)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    wpta_wy_ = fields.Many2many('get.values', 'wpta_wy_values', 'wpta_wy', 'value', "WPTA(WY)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    wsba_wi_ = fields.Many2many('get.values', 'wsba_wi_values', 'wsba_wi', 'value', "WSBA(WI)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    wvapt_wv_ = fields.Many2many('get.values', 'wvapt_wv_values', 'wvapt_wv', 'value', "WVAPT(WV)", help="Please select/add years e.g 2015, 2016 ...")  # SELECT MULTIPLE
    what_type_of_support = fields.Many2many('get.values', 'what_type_of_support_values', 'what_type_of_support', 'value', "What type of support?", help="Please select/add Software or Hardware or both")  # SELECT MULTIPLE
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
