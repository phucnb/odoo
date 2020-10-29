# -*- coding: utf-8 -*-
import logging
import re
from odoo.exceptions import ValidationError
from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from datetime import datetime
import time
import datetime
import os.path
from odoo.osv import osv
import requests
import json
import urllib
import threading
from functools import reduce

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/]{3,}=*)([\'"])', re.I)


class HubspotImportIntegration(models.Model):
    _name = 'hubspot.import.integration'

    field_name = fields.Char('Hubspot')
    start = fields.Datetime('Start from')
    end = fields.Datetime('Till')

    import_company = fields.Boolean('Import companies',strore=True)
    import_contact = fields.Boolean('Import contacts',strore=True)
    import_deal = fields.Boolean('Import deals',strore=True)
    import_ticket = fields.Boolean('Import tickets',strore=True)
    custom_date_range = fields.Boolean(string='Custom Date Range Sync')

    def read_file(self, file_name):
        lines = []
        if file_name == 'contacts':
            lines = ['aapt_ar_','associated_company','business_unit','contact_import_list_name','county','demo',
                    'did_they_go_to_a_new_school_district_company_','iacp','lead_type','middle_name','nadp','napt',
                    'no_longer_at_school_district_company','planned_retirement_date','population',
                    'product_i_m_interested_in','purchased_list_july','purchasing_influence','remove','reports_to',
                    'request_a_demo','role','s247_secondary_company','service_surveillance_owner','state_or_province',
                    'state_or_region','surveillance_247_area_code','surveillance_247_district_name',
                    'surveillance_247_district_website_domain','territory','what_school_district_company_did_they_go_',
                    'what_type_of_support','why_not_at_school_district_company_','years_with_company',
                    'zoom_webinar_attendance_average_duration','zoom_webinar_attendance_count','zoom_webinar_joinlink',
                    'zoom_webinar_registration_count','aasbo_az_','address2','asta_al_','casbo_ca_','nickname',
                    'casto_ca_','full_name','accounting_contact_full_name','cgcs','accounting_email','cptc_cn_',
                    'crtc_wa_','purchasing_contact_full_name','cspta_co_','purchasing_email','ctaa',
                    'division_cf_contact','fpta_ctd','gapt_ga_','last_rma_email_date',
                    'customer_rating','gcapt_tx_','famtec_customer','iapt_il_','famtec_sales_rep','iapt_id_',
                    'bus_garage','ipta_ia_','kspta_ks_','mapt_mi_','mapt_mo_','mnapt_mn_','n247_dvr_total','as_of_date',
                    'msboa_mn_','cameras','napt_na_','external_camera','ncpta_nc_','ncst','special_instructions',
                    'area_code','nsba_na_','job_title_secondary','nsta_mid','nsta_summer','unique_identifier',
                    'nsta_national','solution_currently_installed','oapt_oh_','oapt_ok_','oasbo_on_','oasbo_osba',
                    'opta_or_','osbma_oh_','sbx','scapt_sc_','sesptc','stai_in_','stn','taa_az_','tapt_tn_','tapt_tx_',
                    'transfinder','tsd','uapt_ut_','vapt_va_','wapt_wa_','wpta_wy_','wsba_wi_','wvapt_wv_',
                    'chapter_meeting_1','sts_of_nj']
        elif file_name == 'companies':
            lines = [
                'bid_potential','bid_status','business_vertical','business_vertical_other_','camera_system',
                'camera_system_other_','cameras','competitor','contract_expires','contracted_services',
                'customer_rating','dealer_sold_through','e360_cameras','external_camera','fleet_maintenance_system',
                'fleet_maintenance_system_other_','fleet_size_s247','gps','gps_vendor','gps_vendor_other_','how_many_lots_',
                'issr','n247_bus_saleman','n247s_lifecycle_stage','nadp','netsuite_refresh','company_type',
                'number_of_sales_personnel','number_of_special_needs_students_transported',
                'of_buses','of_cameras_per_bus','of_students_total','of_students_transported',
                'parent_portal','parent_portal_other_','parent_portal_system','preferred_camera_vendor','preferred_camera_vendor_cloned_',
                'previous_camera_system','products','prospect_status_s247','purchase_date','purchased_list_july','remove','rfp_date_posted',
                'routing','routing_solution','routing_solution_other_','rsm','s247_contact_email',
                's247_county','s247_first_name','s247_last_name','s247_lead_contact','s247_pre_post_salutation','s247_title',
                'sales_rep','school_year_budget_begins','school_year_start','service_agreement','service_surveillance_owner',
                'sic_code','stop_arm_camera_s_','student_count','student_information_system','student_information_system_other_',
                'student_tracking','student_tracking_system','student_tracking_system_other_','surveillance_247_company_domain',
                'surveillance_247_district','system','td_fleet_monitor','territory','touchdown',
                'touchdown_cloud_services_amount','touchdown_cloud_services_renewal_date','touchdown_install_date','wireless','wireless_s247',
                'internal_id','new_id','lot_1_address','status','fleet_size','lot_2_address','netsuite_customer','netsuite_status',
                'bid_awarded_year','bus_garage','n247_dvr_total','special_instructions','area_code','vendor',
                'dealer_sub_type','unique_identifier','opportunity_number','contractor','minitrack','erie_1_boces','bid_reference',
            ]
        elif file_name == 'deals':
            lines = [
                'deal_entered_current_deal_stage', 'dealers_quoting_this_deal', 'end_user', 'isr',
                'lost_reason_notes', 'n247s_lifecycle_stage', 'opportunity_link', 'product_s_considered',
                'sales_order', 'state', 'opportunity_number'
            ]

        property_url = ''
        for line in lines:
            property_url = property_url + '&properties=' + line
        return property_url

    def add_properties(self, odoo_obj, hubspot_obj, name):
        m2m_list = []
        date_fields = ['contract_expires', 'school_year_budget_begins', 'school_year_start',
                       'touchdown_cloud_services_renewal_date', 'touchdown_install_date', 'date_of_birth',
                       'planned_retirement_date', 'last_rma_email_date', 'request_a_demo']
        if name == 'contacts':
            m2m_list = [
                'asta_al_', 'aasbo_az_', 'aapt_ar_',
                'wvapt_wv_', 'wsba_wi_', 'wpta_wy_', 'wapt_wa_', 'vapt_va_', 'uapt_ut_',
                'tsd', 'transfinder', 'tapt_tx_', 'tapt_tn_', 'taa_az_', 'sts_nj', 'stn',
                'stai_in_', 'sesptc', 'scapt_sc_', 'sbx', 'osbma_oh_', 'opta_or_', 'oasbo_osba',
                'oasbo_on_', 'oapt_ok_', 'oapt_oh_', 'nsta_summer', 'nsta_national', 'nsta_mid',
                'nsba_na_', 'ncst', 'ncpta_nc_', 'napt_na_', 'napt', 'msboa_mn_', 'mnapt_mn_',
                'mapt_mo_', 'mapt_mi_', 'kspta_ks_', 'ipta_ia_', 'iapt_il_', 'iapt_id_', 'gcapt_tx_',
                'gapt_ga_', 'fpta_ctd', 'ctaa', 'cspta_co_', 'crtc_wa_', 'cptc_cn_', 'chapter_meeting_1',
                'cgcs', 'casto_ca_', 'casbo_ca_', 'business_unit', 'buying_role', 'what_type_of_support'
            ]
        elif name == 'companies':
            m2m_list = ['system', 'dealer_sold_through', 'camera_system', 'how_many_lots_', 'competitor',
                        'previous_camera_system']
        elif name == 'deals':
            m2m_list = ['dealers_quoting_this_deal', 'product_s_considered']

        else:
            print("hello")

        lines = []
        if name == 'contacts':
            lines = ['aapt_ar_', 'associated_company', 'business_unit', 'contact_import_list_name', 'county', 'demo',
                     'did_they_go_to_a_new_school_district_company_', 'iacp', 'lead_type', 'middle_name', 'nadp',
                     'napt',
                     'no_longer_at_school_district_company', 'planned_retirement_date', 'population',
                     'product_i_m_interested_in', 'purchased_list_july', 'purchasing_influence', 'remove', 'reports_to',
                     'request_a_demo', 'role', 's247_secondary_company', 'service_surveillance_owner',
                     'state_or_province',
                     'state_or_region', 'surveillance_247_area_code', 'surveillance_247_district_name',
                     'surveillance_247_district_website_domain', 'territory',
                     'what_school_district_company_did_they_go_',
                     'what_type_of_support', 'why_not_at_school_district_company_', 'years_with_company',
                     'zoom_webinar_attendance_average_duration', 'zoom_webinar_attendance_count',
                     'zoom_webinar_joinlink',
                     'zoom_webinar_registration_count', 'aasbo_az_', 'address2', 'asta_al_', 'casbo_ca_', 'nickname',
                     'casto_ca_', 'accounting_contact_full_name', 'cgcs', 'accounting_email', 'cptc_cn_',
                     'crtc_wa_', 'purchasing_contact_full_name', 'cspta_co_', 'purchasing_email', 'ctaa',
                     'division_cf_contact', 'fpta_ctd', 'gapt_ga_', 'last_rma_email_date',
                     'customer_rating', 'gcapt_tx_', 'famtec_customer', 'iapt_il_', 'famtec_sales_rep', 'iapt_id_',
                     'bus_garage', 'ipta_ia_', 'kspta_ks_', 'mapt_mi_', 'mapt_mo_', 'mnapt_mn_', 'n247_dvr_total',
                     'as_of_date',
                     'msboa_mn_', 'cameras', 'napt_na_', 'external_camera', 'ncpta_nc_', 'ncst', 'special_instructions',
                     'area_code', 'nsba_na_', 'job_title_secondary', 'nsta_mid', 'nsta_summer', 'unique_identifier',
                     'nsta_national', 'solution_currently_installed', 'oapt_oh_', 'oapt_ok_', 'oasbo_on_', 'oasbo_osba',
                     'opta_or_', 'osbma_oh_', 'sbx', 'scapt_sc_', 'sesptc', 'stai_in_', 'stn', 'taa_az_', 'tapt_tn_',
                     'tapt_tx_',
                     'transfinder', 'tsd', 'uapt_ut_', 'vapt_va_', 'wapt_wa_', 'wpta_wy_', 'wsba_wi_', 'wvapt_wv_',
                     'chapter_meeting_1', 'sts_of_nj']
        elif name == 'companies':
            lines = [
                'bid_potential', 'bid_status', 'business_vertical', 'business_vertical_other_', 'camera_system',
                'camera_system_other_', 'cameras', 'competitor', 'contract_expires',
                'contracted_services',
                'customer_rating', 'dealer_sold_through', 'e360_cameras', 'external_camera', 'fleet_maintenance_system',
                'fleet_maintenance_system_other_', 'fleet_size_s247', 'gps', 'gps_vendor', 'gps_vendor_other_',
                'how_many_lots_',
                'issr', 'n247_bus_saleman', 'n247s_lifecycle_stage', 'nadp', 'netsuite_refresh', 'company_type',
                'number_of_sales_personnel', 'number_of_special_needs_students_transported',
                'of_buses', 'of_cameras_per_bus', 'of_students_total',
                'of_students_transported',
                'parent_portal', 'parent_portal_other_', 'parent_portal_system', 'preferred_camera_vendor',
                'preferred_camera_vendor_cloned_',
                'previous_camera_system', 'products', 'prospect_status_s247', 'purchase_date', 'purchased_list_july',
                'remove', 'rfp_date_posted',
                'routing', 'routing_solution', 'routing_solution_other_', 'rsm', 's247_contact_email',
                's247_county', 's247_first_name', 's247_last_name', 's247_lead_contact', 's247_pre_post_salutation',
                's247_title',
                'sales_rep', 'school_year_budget_begins', 'school_year_start', 'service_agreement',
                'service_surveillance_owner',
                'sic_code', 'stop_arm_camera_s_', 'student_count', 'student_information_system',
                'student_information_system_other_',
                'student_tracking', 'student_tracking_system', 'student_tracking_system_other_',
                'surveillance_247_company_domain',
                'surveillance_247_district', 'system', 'td_fleet_monitor', 'territory',
                'touchdown',
                'touchdown_cloud_services_amount', 'touchdown_cloud_services_renewal_date', 'touchdown_install_date',
                'wireless', 'wireless_s247',
                'internal_id', 'new_id', 'lot_1_address', 'status', 'fleet_size', 'lot_2_address', 'netsuite_customer',
                'netsuite_status',
                'bid_awarded_year', 'bus_garage', 'n247_dvr_total', 'special_instructions', 'area_code',
                'vendor',
                'dealer_sub_type', 'unique_identifier', 'opportunity_number', 'contractor', 'minitrack', 'erie_1_boces',
                'bid_reference',
            ]
        elif name == 'deals':
            lines = [
                'deal_entered_current_deal_stage', 'dealers_quoting_this_deal', 'end_user', 'isr',
                'lost_reason_notes', 'n247s_lifecycle_stage', 'opportunity_link', 'product_s_considered',
                'sales_order', 'state', 'opportunity_number'
            ]
        else:
            print("Hellossss")
        for line in lines:
            if hubspot_obj.get(line):
                if line in m2m_list:
                    odoo_obj.update({
                        line: [[6, 0, self.add_m2m_values(hubspot_obj[line]['value'])]]
                    })
                else:
                    if line in date_fields:
                        date_convert = hubspot_obj[line]['value']
                        date_value = datetime.datetime.fromtimestamp(int(date_convert[:-3]))
                        odoo_obj.update({
                            line: date_value
                        })
                    else:
                        if hubspot_obj[line]['value'] != 'false':
                            state_fields = ['state_or_province', 'state_or_region']
                            if line in state_fields:
                                odoo_state = self.env['res.country.state'].search([('name', '=', hubspot_obj[line]['value'])])
                                odoo_obj.update({
                                    line: odoo_state.id if odoo_state else None
                                })
                            else:
                                odoo_obj.update({
                                    line: hubspot_obj[line]['value'] if hubspot_obj[line]['value'] else None
                                })

    def add_m2m_values(self, values):
        value_ids = []
        for value in values.split(';'):
            odoo_value = self.env['get.values'].search([('name', '=', value)])
            if not odoo_value:
                odoo_value = self.env['get.values'].create({
                    'name': value,
                })
            self.env.cr.commit()
            value_ids.append(odoo_value.id)
        return value_ids

    def import_contacts(self):
        icpsudo = self.env['ir.config_parameter'].sudo()
        hubspot_keys = icpsudo.get_param('odoo_hubspot.hubspot_key')
        hubspot_ids = []
        if not hubspot_keys:
            raise ValidationError('Please! Enter Hubspot key...')
        else:
            try:
                get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
                parameter_dict = {'hapikey': hubspot_keys, 'count': 250}
                headers = {
                    'Accept': 'application/json',
                    'connection': 'keep-Alive'
                }
                has_more = True
                properties = self.read_file('contacts')
                while has_more:
                    parameters = urllib.parse.urlencode(parameter_dict)
                    get_url = get_all_contacts_url + parameters + properties
                    r = requests.get(url=get_url, headers=headers)
                    response_dict = json.loads(r.text)
                    hubspot_ids.extend(self.create_contacts(response_dict['contacts'], hubspot_keys))
                    has_more = response_dict['has-more']
                    parameter_dict['vidOffset'] = response_dict['vid-offset']
                # return hubspot_ids
            except Exception as e:
                _logger.error(e)
                raise ValidationError(_(str(e)))

    def create_contacts(self, contacts, hubspot_keys):
        try:
            hubspot_ids = []
            get_single_contact_url = "https://api.hubapi.com/contacts/v1/contact/vid/"
            get_single_company_url = "https://api.hubapi.com/companies/v2/companies/"
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            for contact in contacts:
                odoo_company = None
                odoo_country = None
                contact_url = get_single_contact_url + str(contact['vid']) + '/profile?hapikey=' + hubspot_keys
                r = requests.get(url=contact_url, headers=headers)
                profile = json.loads(r.text)['properties']
                contact_date = profile['createdate']['value']
                created_date = datetime.datetime.fromtimestamp(int(contact_date[:-3]))
                start_date = self.start
                end_date = self.end

                if start_date <= created_date <= end_date:
                    if 'associatedcompanyid' in profile and not profile['associatedcompanyid']['value'] == '':
                        odoo_company = self.env['res.partner'].search([('hubspot_id', '=', str(profile['associatedcompanyid']['value']))])
                        if not odoo_company:
                            get_url = get_single_company_url + str(profile['associatedcompanyid']['value']) + '?hapikey=' + hubspot_keys
                            company_response = requests.get(url=get_url, headers=headers)
                            company_profile = json.loads(company_response.content.decode('utf-8'))['properties']
                            if 'country' in company_profile.keys():
                                odoo_country = self.env['res.country'].search([('name', '=', company_profile['country']['value'])]).id
                            company_values = {
                                'name': company_profile['name']['value'] if 'name' in company_profile.keys() else '',
                                'website': company_profile['website']['value'] if 'website' in company_profile.keys() else '',
                                'street': company_profile['address']['value'] if 'address' in company_profile.keys() else '',
                                'city': company_profile['city']['value'] if 'city' in company_profile.keys() else '',
                                'phone': company_profile['phone']['value'] if 'phone' in company_profile.keys() else '',
                                'zip': company_profile['zip']['value'] if 'zip' in company_profile.keys() else '',
                                'country_id': odoo_country if odoo_country else None,
                                'hubspot_id': str(profile['associatedcompanyid']['value']),
                                'is_company': True,
                            }
                            self.add_properties(company_values, company_profile, 'companies')
                            odoo_company = self.env['res.partner'].create(company_values)
                    first_name = profile['firstname']['value'] if 'firstname' in profile else ''
                    last_name = profile['lastname']['value'] if 'lastname' in profile else ''
                    name = first_name + ' ' + last_name
                    odoo_partner = self.env['res.partner'].search([('hubspot_id', '=', str(contact['vid']))])
                    if not odoo_partner:
                        contact_values = {
                            'name': name,
                            'email': profile['email']['value'] if 'email' in profile.keys() else '',
                            'website': profile['website']['value'] if 'website' in profile.keys() else '',
                            'city': profile['city']['value'] if 'city' in profile.keys() else '',
                            'zip': profile['zip']['value'] if 'zip' in profile.keys() else '',
                            'parent_id': odoo_company.id if odoo_company else None,
                            'hubspot_id': str(contact['vid']),
                            'phone': profile['phone']['value'] if 'phone' in profile.keys() else '',
                        }
                        self.add_properties(contact_values, profile, 'contacts')
                        new_contact = self.env['res.partner'].create(contact_values)
                        self.get_contact_engagements(new_contact, hubspot_keys)
                    else:
                        self.get_contact_engagements(odoo_partner, hubspot_keys)
                    self.env.cr.commit()
                    hubspot_ids.append(contact['vid'])
            return hubspot_ids
        except Exception as e:
            pass

    def import_companies(self):
        icpsudo = self.env['ir.config_parameter'].sudo()
        hubspot_keys = icpsudo.get_param('odoo_hubspot.hubspot_key')
        hubspot_ids = []
        if not hubspot_keys:
            raise ValidationError('Please! Enter Hubspot key...')
        else:
            try:
                get_all_companies_url = "https://api.hubapi.com/companies/v2/companies/paged?"
                parameter_dict = {'hapikey': hubspot_keys, 'limit': 250}
                headers = {
                    'Accept': 'application/json',
                    'connection': 'keep-Alive'
                }
                properties = self.read_file('companies')
                has_more = True
                while has_more:
                    parameters = urllib.parse.urlencode(parameter_dict)
                    get_url = get_all_companies_url + parameters + properties
                    r = requests.get(url=get_url, headers=headers)
                    response_dict = json.loads(r.text)
                    hubspot_ids.extend(self.create_companies(response_dict['companies'], hubspot_keys))
                    has_more = response_dict['has-more']
                    parameter_dict['offset'] = response_dict['offset']
                # return hubspot_ids
            except Exception as e:
                _logger.error(e)
                raise ValidationError(_(str(e)))

    def create_companies(self, companies, hubspot_keys):
        try:
            hubspot_ids = []
            get_single_company_url = "https://api.hubapi.com/companies/v2/companies/"
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            for company in companies:
                odoo_country = None
                get_url = get_single_company_url + str(company['companyId']) + '?hapikey=' + hubspot_keys
                company_response = requests.get(url=get_url, headers=headers)
                company_profile = json.loads(company_response.content.decode('utf-8'))['properties']
                contact_date = company_profile['createdate']['value']
                created_date = datetime.datetime.fromtimestamp(int(contact_date[:-3]))

                start_date = self.start
                end_date = self.end

                if start_date <= created_date <= end_date:
                    odoo_company = self.env['res.partner'].search([('hubspot_id', '=', str(company['companyId']))])
                    if 'country' in company_profile.keys():
                        odoo_country = self.env['res.country'].search([('name', '=', company_profile['country']['value'])]).id
                    if not odoo_company:
                        company_values = {
                            'name': company_profile['name']['value'] if 'name' in company_profile.keys() else '',
                            'website': company_profile['website']['value'] if 'website' in company_profile.keys() else '',
                            'street': company_profile['address']['value'] if 'address' in company_profile.keys() else '',
                            'city': company_profile['city']['value'] if 'city' in company_profile.keys() else '',
                            'phone': company_profile['phone']['value'] if 'phone' in company_profile.keys() else '',
                            'zip': company_profile['zip']['value'] if 'zip' in company_profile.keys() else '',
                            'country_id': odoo_country if odoo_country else None,
                            'hubspot_id': str(company['companyId']),
                            'is_company': True,
                        }
                        self.add_properties(company_values, company_profile, 'companies')
                        self.env['res.partner'].create(company_values)
                    # else:
                    #     odoo_company.write({
                    #         'name': company_profile['name']['value'] if 'name' in company_profile.keys() else '',
                    #         'website': company_profile['website']['value'] if 'website' in company_profile.keys() else '',
                    #         'street': company_profile['address']['value'] if 'address' in company_profile.keys() else '',
                    #         'city': company_profile['city']['value'] if 'city' in company_profile.keys() else '',
                    #         'phone': company_profile['phone']['value'] if 'phone' in company_profile.keys() else '',
                    #         'zip': company_profile['zip']['value'] if 'zip' in company_profile.keys() else '',
                    #         'country_id': odoo_country if odoo_country else None,
                    #         'hubspot_id': str(company['companyId']),
                    #         'is_company': True,
                    #     })
                    self.env.cr.commit()
                    hubspot_ids.append(company['companyId'])
            return hubspot_ids
        except Exception as e:
            pass

    def import_deals(self, Auto):
        icpsudo = self.env['ir.config_parameter'].sudo()
        hubspot_keys = icpsudo.get_param('odoo_hubspot.hubspot_key')
        hubspot_ids = []
        if not hubspot_keys:
            raise ValidationError('Please! Enter Hubspot key...')
        else:
            try:
                get_all_deals_url = "https://api.hubapi.com/deals/v1/deal/paged?"
                deal_properties = "&includeAssociations=true&properties=dealstage&properties=dealname" \
                                  "&properties=hs_createdate&properties=hubspot_owner_id&properties=dealtype" \
                                  "&properties=closedate&properties=amount&properties=hs_lastmodifieddate"
                parameter_dict = {'hapikey': hubspot_keys, 'limit': 250}
                headers = {
                    'Accept': 'application/json',
                    'connection': 'keep-Alive'
                }
                has_more = True
                while has_more:
                    parameters = urllib.parse.urlencode(parameter_dict)
                    get_url = get_all_deals_url + parameters + deal_properties
                    r = requests.get(url=get_url, headers=headers)
                    response_dict = json.loads(r.text)
                    hubspot_ids.extend(self.create_deals(response_dict['deals'], hubspot_keys, Auto))
                    has_more = response_dict['hasMore']
                    parameter_dict['offset'] = response_dict['offset']
                # return hubspot_ids
            except Exception as e:
                _logger.error(e)
                raise ValidationError(_(str(e)))

    def create_deals(self, deals, hubspot_keys, Auto):
        try:
            hubspot_ids = []
            close_date = None
            deal_stage = None
            i = 0
            for deal in deals:
                deal_date = deal['properties']['hs_createdate']['value']
                created_date = datetime.datetime.fromtimestamp(int(deal_date[:-3]))
                if Auto:
                    if self.start and self.end:
                        end_date = self.end
                        start_date = self.start
                    else:
                        end_date = datetime.datetime.now()
                        start_date = end_date - datetime.timedelta(days=1)
                else:
                    start_date = self.start
                    end_date = self.end

                if start_date <= created_date <= end_date:
                    contacts = []
                    companies = []
                    if len(deal['associations']['associatedVids']) > 0:
                        contacts = self.get_contacts(deal['associations']['associatedVids'], hubspot_keys)
                    if len(deal['associations']['associatedCompanyIds']) > 0:
                        companies = self.get_companies(deal['associations']['associatedCompanyIds'], hubspot_keys)
                    odoo_deal = self.env['crm.lead'].search([('hubspot_id', '=', str(deal['dealId']))])
                    if 'dealstage' in deal['properties'].keys():
                        deal_stage = self.env['crm.stage'].search([('name', '=', deal['properties']['dealstage']['value'])])
                        if not deal_stage:
                            deal_stage = self.env['crm.stage'].create({
                                'name': deal['properties']['dealstage']['value'],
                                'display_name': deal['properties']['dealstage']['value'],
                            })
                    if 'closedate' in deal['properties'].keys():
                        if deal['properties']['closedate']['value'] != "":
                            close_date = datetime.datetime.fromtimestamp(int(deal['properties']['closedate']['value'][:-3]))
                    if not odoo_deal:
                        deal_values = {
                            'hubspot_id': str(deal['dealId']),
                            'name': deal['properties']['dealname']['value'],
                            'planned_revenue': deal['properties']['amount']['value'] if 'amount' in deal['properties'].keys() else None,
                            'stage_id': deal_stage.id if deal_stage else self.env['crm.stage'].search([('name', '=', 'New')]).id,
                            'date_deadline': close_date if close_date else None,
                            'hs_deal_contacts': [[6, 0, contacts]] if contacts else None,
                            'hs_deal_companies': companies[0] if companies else None,
                        }

                        self.add_properties(deal_values, deal, 'companies')
                        self.env['res.partner'].create(deal_values)
                    else:
                        odoo_deal.write({
                            'hubspot_id': str(deal['dealId']),
                            'name': deal['properties']['dealname']['value'],
                            'planned_revenue': deal['properties']['amount']['value'] if 'amount' in deal['properties'].keys() else None,
                            'stage_id': deal_stage.id if deal_stage else self.env['crm.stage'].search([('name', '=', 'New')]).id,
                            'date_deadline': close_date,
                            'hs_deal_contacts': [[6, 0, contacts]] if contacts else None,
                            'hs_deal_companies': companies[0] if companies else None,
                        })
                    self.env.cr.commit()

                    hubspot_ids.append(deal['dealId'])
            return hubspot_ids
        except Exception as e:
            raise ValidationError(_(str(e)))

    def get_contacts(self, contactsIds, hubspot_keys):
        contact_list = []
        get_single_contact_url = "https://api.hubapi.com/contacts/v1/contact/vid/"
        headers = {
            'Accept': 'application/json',
            'connection': 'keep-Alive'
        }
        for contactId in contactsIds:
            contact_url = get_single_contact_url + str(contactId) + '/profile?hapikey=' + hubspot_keys
            r = requests.get(url=contact_url, headers=headers)
            profile = json.loads(r.text)['properties']
            first_name = profile['firstname']['value'] if 'firstname' in profile else ''
            last_name = profile['lastname']['value'] if 'lastname' in profile else ''
            name = first_name + ' ' + last_name
            odoo_partner = self.env['res.partner'].search([('hubspot_id', '=', str(contactId))])
            if not odoo_partner:
                odoo_partner = self.env['res.partner'].create({
                    'name': name,
                    'email': profile['email']['value'] if 'email' in profile.keys() else '',
                    'website': profile['website']['value'] if 'website' in profile.keys() else '',
                    'city': profile['city']['value'] if 'city' in profile.keys() else '',
                    'zip': profile['zip']['value'] if 'zip' in profile.keys() else '',
                    'hubspot_id': str(contactId),
                    'phone': profile['phone']['value'] if 'phone' in profile.keys() else '',
                })
            else:
                odoo_partner.write({
                    'name': name,
                    'email': profile['email']['value'] if 'email' in profile.keys() else '',
                    'website': profile['website']['value'] if 'website' in profile.keys() else '',
                    'city': profile['city']['value'] if 'city' in profile.keys() else '',
                    'zip': profile['zip']['value'] if 'zip' in profile.keys() else '',
                    'hubspot_id': str(contactId),
                    'phone': profile['phone']['value'] if 'phone' in profile.keys() else '',
                })
            contact_list.append(odoo_partner.id)
        return contact_list

    def get_companies(self, companiesIds, hubspot_keys):
        company_list = []
        get_single_company_url = "https://api.hubapi.com/companies/v2/companies/"
        headers = {
            'Accept': 'application/json',
            'connection': 'keep-Alive'
        }
        for companyId in companiesIds:
            odoo_country = None
            get_url = get_single_company_url + str(companyId) + '?hapikey=' + hubspot_keys
            company_response = requests.get(url=get_url, headers=headers)
            company_profile = json.loads(company_response.content.decode('utf-8'))['properties']
            odoo_company = self.env['res.partner'].search([('hubspot_id', '=', str(companyId))])
            if 'country' in company_profile.keys():
                odoo_country = self.env['res.country'].search([('name', '=', company_profile['country']['value'])]).id
            if not odoo_company:
                odoo_company = self.env['res.partner'].create({
                    'name': company_profile['name']['value'] if 'name' in company_profile.keys() else '',
                    'website': company_profile['website']['value'] if 'website' in company_profile.keys() else '',
                    'street': company_profile['address']['value'] if 'address' in company_profile.keys() else '',
                    'city': company_profile['city']['value'] if 'city' in company_profile.keys() else '',
                    'phone': company_profile['phone']['value'] if 'phone' in company_profile.keys() else '',
                    'zip': company_profile['zip']['value'] if 'zip' in company_profile.keys() else '',
                    'country_id': odoo_country if odoo_country else None,
                    'hubspot_id': str(companyId),
                    'is_company': True,
                })
            else:
                odoo_company.write({
                    'name': company_profile['name']['value'] if 'name' in company_profile.keys() else '',
                    'website': company_profile['website']['value'] if 'website' in company_profile.keys() else '',
                    'street': company_profile['address']['value'] if 'address' in company_profile.keys() else '',
                    'city': company_profile['city']['value'] if 'city' in company_profile.keys() else '',
                    'phone': company_profile['phone']['value'] if 'phone' in company_profile.keys() else '',
                    'zip': company_profile['zip']['value'] if 'zip' in company_profile.keys() else '',
                    'country_id': odoo_country if odoo_country else None,
                    'hubspot_id': str(companyId),
                    'is_company': True,
                })
            company_list.append(odoo_company.id)
        return company_list

    def import_tickets(self):
        icpsudo = self.env['ir.config_parameter'].sudo()
        hubspot_keys = icpsudo.get_param('odoo_hubspot.hubspot_key')
        hubspot_ids = []
        if not hubspot_keys:
            raise ValidationError('Please! Enter Hubspot key...')
        else:
            try:
                get_all_tickets_url = "https://api.hubapi.com/crm-objects/v1/objects/tickets/paged?"
                data = "&properties=subject&properties=content&properties=hs_pipeline" \
                       "&properties=hs_pipeline_stage&properties=hs_ticket_priority" \
                       "&properties=hs_ticket_category&properties=hubspot_owner_id" \
                       "&properties=source_type&properties=hs_createdate&properties=createdate" \
                       "&properties=hs_lastmodifieddate"
                parameter_dict = {'hapikey': hubspot_keys, 'limit': 250}
                headers = {
                    'Accept': 'application/json',
                    'connection': 'keep-Alive'
                }
                has_more = True
                while has_more:
                    parameters = urllib.parse.urlencode(parameter_dict)
                    get_url = get_all_tickets_url + parameters + data
                    r = requests.get(url=get_url, headers=headers)
                    response_dict = json.loads(r.text)
                    hubspot_ids.extend(self.create_tickets(response_dict['objects'], hubspot_keys))
                    has_more = response_dict['hasMore']
                    parameter_dict['offset'] = response_dict['offset']
                return hubspot_ids
            except Exception as e:
                _logger.error(e)
                raise ValidationError(_(str(e)))

    def create_tickets(self, tickets, hubspot_keys):
        try:
            hubspot_ids = []
            get_association_url = 'https://api.hubapi.com/crm-associations/v1/associations/'
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            for ticket in tickets:
                contacts = []
                companies = []
                tag_ids = []
                priority = None
                get_ticket_contact_url = get_association_url + str(ticket['objectId']) + '/HUBSPOT_DEFINED/16?hapikey=' + hubspot_keys
                contact_response = requests.get(url=get_ticket_contact_url, headers=headers)
                contact_info = json.loads(contact_response.content.decode('utf-8'))['results']
                contacts = self.get_contacts(contact_info, hubspot_keys)
                get_ticket_company_url = get_association_url + str(
                    ticket['objectId']) + '/HUBSPOT_DEFINED/26?hapikey=' + hubspot_keys
                company_response = requests.get(url=get_ticket_company_url, headers=headers)
                company_info = json.loads(company_response.content.decode('utf-8'))['results']
                companies = self.get_companies(company_info, hubspot_keys)
                if 'source_type' in ticket['properties']:
                    odoo_type = self.env['helpdesk.ticket.type'].search([('name', '=', ticket['properties']['source_type']['value'])])
                    if not odoo_type:
                        odoo_type = self.env['helpdesk.ticket.type'].create({
                            'name': ticket['properties']['source_type']['value'],
                        })
                if 'hs_pipeline_stage' in ticket['properties']:
                    odoo_stage = self.env['helpdesk.stage'].search([('hubspot_id', '=', ticket['properties']['hs_pipeline_stage']['value'])])
                if 'hs_ticket_category' in ticket['properties']:
                    tags = ticket['properties']['hs_ticket_category']['value'].split(';')
                    for tag in tags:
                        odoo_tag = self.env['helpdesk.tag'].search([('name', '=', tag)])
                        if not odoo_tag:
                            odoo_tag = self.env['helpdesk.tag'].create({
                                'name': tag,
                            })
                        tag_ids.append(odoo_tag.id)
                if 'hs_ticket_priority' in ticket['properties']:
                    if ticket['properties']['hs_ticket_priority']['value'] == 'LOW':
                        priority = '1'
                    elif ticket['properties']['hs_ticket_priority']['value'] == 'MEDIUM':
                        priority = '2'
                    elif ticket['properties']['hs_ticket_priority']['value'] == 'HIGH':
                        priority = '3'
                    else:
                        priority = '0'

                odoo_ticket = self.env['helpdesk.ticket'].search([('hubspot_id', '=', str(ticket['objectId']))])
                if not odoo_ticket:
                    self.env['helpdesk.ticket'].create({
                        'hubspot_id': str(ticket['objectId']),
                        'name': ticket['properties']['subject']['value'] if 'subject' in ticket['properties'] else " ",
                        'priority': priority,
                        'stage_id': odoo_stage.id,
                        'ticket_type_id': odoo_type.id,
                        'tag_ids': [[6, 0, tag_ids]],
                        'hs_ticket_contacts': [[6, 0, contacts]] if contacts else None,
                        'hs_ticket_company':  companies[0] if companies else None,
                    })
                else:
                    odoo_ticket.write({
                        'hubspot_id': str(ticket['objectId']),
                        'name': ticket['properties']['subject']['value'] if 'subject' in ticket['properties'] else " ",
                        'priority': priority,
                        'stage_id': odoo_stage.id,
                        'ticket_type_id': odoo_type.id,
                        'tag_ids': [[6, 0, tag_ids]],
                        'hs_ticket_contacts': [[6, 0, contacts]] if contacts else None,
                        'hs_ticket_company': companies[0] if companies else None,
                    })
                self.env.cr.commit()
                hubspot_ids.append(ticket['objectId'])
            return hubspot_ids
        except Exception as e:
            raise ValidationError(_(str(e)))

    def get_contact_engagements(self, odoo_contact, hubspot_keys):
        try:

            url = 'https://api.hubapi.com/engagements/v1/engagements/associated/CONTACT/{0}/paged?hapikey={1}'.format(
                odoo_contact.hubspot_id, hubspot_keys)
            # url = 'https://api.hubapi.com/engagements/v1/engagements/paged?hapikey={}'.format(API_KEY)
            response = requests.get(url)
            res_data = json.loads(response.content.decode("utf-8"))
            engagements = res_data['results']
            for engagement in engagements:
                engagement_data = engagement['engagement']
                odoo_message = self.env['mail.message'].search([('engagement_id', '=', engagement_data['id'])])
                odoo_activity = self.env['mail.activity'].search([('engagement_id', '=', engagement_data['id'])])
                if odoo_message or odoo_activity:
                    continue
                association_data = engagement['associations']
                meta_data = engagement['metadata']
                if engagement_data['type'] == 'EMAIL' and len(meta_data['from']) > 0:
                    try:
                        author = self.env['res.partner'].search([('email', '=', meta_data['from'])])
                        author_id = None
                        if author:
                            author_id = author.id
                        else:
                            author_id = self.env.user.id
                        odoo_comment = self.env['mail.message'].create({
                            'engagement_id': engagement_data['id'],
                            'message_type': 'email',
                            'body': meta_data['text'].encode().decode('unicode-escape'),
                            'create_date': datetime.datetime.fromtimestamp(int(str(engagement_data['createdAt'])[:-3])),
                            'display_name': author.name if author.name else None,
                            'email_from': meta_data['from'],  # comment.author.email if comment.author.email else None,
                            'author_id': author_id,
                            'model': 'res.partner',
                            'res_id': odoo_contact.id
                        })
                    except:
                        pass
                elif engagement_data['type'] == 'NOTE':
                    try:
                        print(odoo_contact.name)
                        author = self.env.user
                        author_id = self.env.user.id
                        odoo_comment = self.env['mail.message'].create({
                            'engagement_id': engagement_data['id'],
                            'message_type': 'notification',
                            'body': engagement_data['bodyPreview'],
                            'create_date': datetime.datetime.fromtimestamp(int(str(engagement_data['createdAt'])[:-3])),
                            'display_name': author.name if author.name else None,
                            'author_id': author_id,
                            'model': 'res.partner',
                            'res_id': odoo_contact.id
                        })
                        # print(odoo_comment.name)
                    except:
                        pass
                elif engagement_data['type'] == 'TASK':
                    try:
                        if meta_data['status'] != 'COMPLETED':
                            print(odoo_contact.name)
                            activity_type = self.env['mail.activity.type'].search([('name', '=', 'Todo')])
                            partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')])
                            self.env['mail.activity'].create({
                                'engagement_id': engagement_data['id'],
                                'res_id': odoo_contact.id,
                                'activity_type_id': activity_type.id,
                                'summary': meta_data['subject'],
                                'hubspot_status': meta_data['status'],
                                'note': meta_data['body'] if meta_data.get('body') else None,
                                'forObjectType': meta_data['forObjectType'],
                                'res_model_id': partner_model.id,
                                'date_deadline': datetime.datetime.fromtimestamp(
                                    int(str(meta_data['completionDate'])[:-3])) if meta_data.get(
                                    'completionDate') else datetime.datetime.now()
                            })
                            self.env.cr.commit()
                        else:
                            print('message created for task', odoo_contact.name)
                            author = odoo_contact
                            author_id = None
                            if author:
                                author_id = author.id
                            else:
                                author_id = self.env.user.id
                            odoo_comment = self.env['mail.message'].create({
                                'engagement_id': engagement_data['id'],
                                'message_type': 'comment',
                                # 'from': odoo_contact.email,
                                'body': meta_data['body'] if meta_data.get('body') else meta_data['subject'],
                                'create_date': datetime.datetime.fromtimestamp(
                                    int(str(engagement_data['createdAt'])[:-3])),
                                'display_name': author.name if author.name else None,
                                'author_id': author_id,
                                'model': 'res.partner',
                                'res_id': odoo_contact.id
                            })
                    except:
                        pass
                elif engagement_data['type'] == 'CALL':
                    try:
                        if meta_data['status'] != 'COMPLETED':
                            print(odoo_contact.name)
                            activity_type = self.env['mail.activity.type'].search([('name', '=', 'Call')])
                            partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')])
                            self.env['mail.activity'].create({
                                'engagement_id': engagement_data['id'],
                                'res_id': odoo_contact.id,
                                'activity_type_id': activity_type.id,
                                'summary': meta_data['subject'] if meta_data.get('subject') else meta_data[
                                    'body'] if meta_data.get('body') else None,
                                'hubspot_status': meta_data['status'],
                                'note': meta_data['body'] if meta_data.get('body') else None,
                                'toNumber': meta_data['toNumber'] if meta_data.get('toNumber') else None,
                                'fromNumber': meta_data['fromNumber'] if meta_data.get('fromNumber') else None,
                                'durationMilliseconds': str(meta_data['durationMilliseconds']) if meta_data.get(
                                    'durationMilliseconds') else None,
                                'recordingUrl': meta_data['recordingUrl'] if meta_data.get('recordingUrl') else None,
                                'disposition': meta_data['disposition'] if meta_data.get('disposition') else None,
                                'res_model_id': partner_model.id,
                                'date_deadline': datetime.datetime.fromtimestamp(
                                    int(str(meta_data['completionDate'])[:-3])) if meta_data.get(
                                    'completionDate') else datetime.datetime.now()
                            })
                            self.env.cr.commit()
                        else:
                            print('message created for call', odoo_contact.name)
                            author = odoo_contact
                            author_id = None
                            if author:
                                author_id = author.id
                            else:
                                author_id = self.env.user.id
                            odoo_comment = self.env['mail.message'].create({
                                'message_type': 'comment',
                                'engagement_id': engagement_data['id'],
                                'body': meta_data['body'] if meta_data.get('body') else meta_data['subject'],
                                'create_date': datetime.datetime.fromtimestamp(
                                    int(str(engagement_data['createdAt'])[:-3])),
                                'display_name': author.name if author.name else None,
                                'author_id': author_id,
                                'model': 'res.partner',
                                'res_id': odoo_contact.id
                            })
                    except:
                        pass

                elif engagement_data['type'] == 'MEETING':
                    try:
                        end_time = datetime.datetime.fromtimestamp(int(str(meta_data['endTime'])[:-3]))
                        if end_time > datetime.datetime.now():
                            print(odoo_contact.name)
                            activity_type = self.env['mail.activity.type'].search([('name', '=', 'Meeting')])
                            partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')])
                            self.env['mail.activity'].create({
                                'engagement_id': engagement_data['id'],
                                'res_id': odoo_contact.id,
                                'activity_type_id': activity_type.id,
                                'summary': meta_data['title'] if meta_data.get('title') else meta_data[
                                    'body'] if meta_data.get('body') else None,
                                'note': meta_data['body'] if meta_data.get('body') else None,
                                'startTime': datetime.datetime.fromtimestamp(
                                    int(str(meta_data['startTime'])[:-3])) if meta_data.get(
                                    'startTime') else datetime.datetime.now(),
                                'endTime': datetime.datetime.fromtimestamp(
                                    int(str(meta_data['endTime'])[:-3])) if meta_data.get(
                                    'endTime') else datetime.datetime.now(),
                                'res_model_id': partner_model.id,
                                'date_deadline': datetime.datetime.fromtimestamp(
                                    int(str(meta_data['endTime'])[:-3])) if meta_data.get(
                                    'endTime') else datetime.datetime.now()
                            })
                            self.env.cr.commit()
                        else:
                            print('message created for call', odoo_contact.name)
                            author = odoo_contact
                            author_id = None
                            if author:
                                author_id = author.id
                            else:
                                author_id = self.env.user.id
                            odoo_comment = self.env['mail.message'].create({
                                'engagement_id': engagement_data['id'],
                                'message_type': 'comment',
                                'body': meta_data['body'] if meta_data.get('body') else meta_data['title'],
                                'create_date': datetime.datetime.fromtimestamp(
                                    int(str(engagement_data['createdAt'])[:-3])),
                                'display_name': author.name if author.name else None,
                                'author_id': author_id,
                                'model': 'res.partner',
                                'res_id': odoo_contact.id
                            })
                    except:
                        pass
        except:
            pass
