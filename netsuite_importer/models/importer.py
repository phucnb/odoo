# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
import hashlib
import hmac
import json
import requests
import os
import base64
import time
import random
import urllib.parse


class NetSuiteImport(models.Model):
    _name = 'netsuite.import'

    field_name = fields.Char('NetSuite')
    last_imported_customers_offset = fields.Integer("Last Imported Offset")
    last_imported_contacts_offset = fields.Integer("Last Imported Offset")

    def _generateTimestamp(self):
        return str(int(time.time()))

    def _generateNonce(self, length=11):
        """Generate pseudorandom number
        """
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def _generateSignature(self, method, url, consumerKey, Nonce, currentTime, token, consumerSecret,
                           tokenSecret, offset):
        signature_method = 'HMAC-SHA256'
        version = '1.0'
        base_url = url
        encoded_url = urllib.parse.quote_plus(base_url)
        collected_string = '&'.join(['oauth_consumer_key=' + consumerKey, 'oauth_nonce=' + Nonce,
                                     'oauth_signature_method=' + signature_method, 'oauth_timestamp=' + currentTime,
                                     'oauth_token=' + token, 'oauth_version=' + version, 'offset='+ str(offset)])
        encoded_string = urllib.parse.quote_plus(collected_string)
        base = '&'.join([method, encoded_url, encoded_string])
        key = '&'.join([consumerSecret, tokenSecret])
        digest = hmac.new(key=str.encode(key), msg=str.encode(base), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()
        return urllib.parse.quote_plus(signature)

    def _generateSingleSignature(self, method, url, consumerKey, Nonce, currentTime, token, consumerSecret, tokenSecret):
        signature_method = 'HMAC-SHA256'
        version = '1.0'
        base_url = url
        encoded_url = urllib.parse.quote_plus(base_url)
        collected_string = '&'.join(['oauth_consumer_key=' + consumerKey, 'oauth_nonce=' + Nonce,
                                     'oauth_signature_method=' + signature_method, 'oauth_timestamp=' + currentTime,
                                     'oauth_token=' + token, 'oauth_version=' + version])
        encoded_string = urllib.parse.quote_plus(collected_string)
        base = '&'.join([method, encoded_url, encoded_string])
        key = '&'.join([consumerSecret, tokenSecret])
        digest = hmac.new(key=str.encode(key), msg=str.encode(base), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()
        return urllib.parse.quote_plus(signature)

    def import_customer(self):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            nsAccountID = icpsudo.get_param('netsuite_importer.nsAccountID')
            consumerKey = icpsudo.get_param('netsuite_importer.consumerKey')
            consumerSecret = icpsudo.get_param('netsuite_importer.consumerSecret')
            token = icpsudo.get_param('netsuite_importer.token')
            tokenSecret = icpsudo.get_param('netsuite_importer.tokenSecret')
            base_url = "https://1056867.suitetalk.api.netsuite.com/services/rest/record/v1/customer"
            has_more = True
            offset = self.last_imported_customers_offset if self.last_imported_customers_offset else 0
            while has_more:
                Nonce = self._generateNonce(length=11)
                currentTime = self._generateTimestamp()
                signature = self._generateSignature('GET', base_url, consumerKey, Nonce, currentTime, token, consumerSecret,
                                                    tokenSecret, offset)

                payload = ""
                oauth = "OAuth realm=\"" + nsAccountID + "\"," \
                        "oauth_consumer_key=\"" + consumerKey + "\"," \
                        "oauth_token=\"" + token + "\"," \
                        "oauth_signature_method=\"HMAC-SHA256\"," \
                        "oauth_timestamp=\"" + currentTime + "\"," \
                        "oauth_nonce=\"" + Nonce + "\"," \
                        "oauth_version=\"1.0\"," \
                        "oauth_signature=\"" + signature + "\""
                headers = {
                    'Content-Type': "application/json",
                    'Authorization': oauth,
                    'cache-control': "no-cache",
                }
                response = requests.request("GET", base_url+'?offset='+str(offset), data=payload, headers=headers)
                response_dict = json.loads(response.text)
                self.create_customers(response_dict['items'], base_url)
                self.last_imported_customers_offset = str(offset)
                offset += 1000
                has_more = response_dict['hasMore']
        except Exception as e:
            raise ValidationError(_(str(e)))

    def create_customers(self, customers, url):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            nsAccountID = icpsudo.get_param('netsuite_importer.nsAccountID')
            consumerKey = icpsudo.get_param('netsuite_importer.consumerKey')
            consumerSecret = icpsudo.get_param('netsuite_importer.consumerSecret')
            token = icpsudo.get_param('netsuite_importer.token')
            tokenSecret = icpsudo.get_param('netsuite_importer.tokenSecret')
            for customer in customers:
                odoo_customer = self.env['res.partner'].search([('netsuite_id', '=', customer['id'])])
                if not odoo_customer:
                    Nonce = self._generateNonce(length=11)
                    currentTime = self._generateTimestamp()
                    customer_url = url + "/" + customer['id']
                    signature = self._generateSingleSignature('GET', customer_url, consumerKey, Nonce, currentTime, token,
                                                        consumerSecret, tokenSecret)
                    oauth = "OAuth realm=\"" + nsAccountID + "\"," \
                            "oauth_consumer_key=\"" + consumerKey + "\"," \
                            "oauth_token=\"" + token + "\"," \
                            "oauth_signature_method=\"HMAC-SHA256\"," \
                            "oauth_timestamp=\"" + currentTime + "\"," \
                            "oauth_nonce=\"" + Nonce + "\"," \
                            "oauth_version=\"1.0\"," \
                            "oauth_signature=\"" + signature + "\""
                    headers = {
                        'Content-Type': "application/json",
                        'Authorization': oauth,
                        'cache-control': "no-cache",
                    }
                    customer_response = requests.request("GET", customer_url, headers=headers)
                    customer = json.loads(customer_response.text)
                    country_id = self.env['res.country'].search([('code', '=', customer['shipCountry'])]).id if \
                        'shipCountry' in customer else None
                    state_id = self.env['res.country.state'].search([('code', '=', customer['shipState']),
                                                                     ('country_id', '=', country_id)]).id if \
                        'shipState' in customer else None
                    self.env['res.partner'].create({
                        'netsuite_id': customer['id'],
                        'name': customer['companyName'] if 'companyName' in customer else customer['entityTitle'],
                        'is_company': False if customer['isPerson'] else True,
                        'phone': customer['phone'] if 'phone' in customer else None,
                        'zip': customer['shipZip'] if 'shipZip' in customer else None,
                        'street': customer['shipAddressee'] if 'shipAddressee' in customer else None,
                        'street2': customer['shipAddr1'] if 'shipAddr1' in customer else None,
                        'state_id': state_id,
                        'country_id': country_id,
                        'custentityare_they_buying_new_busses': customer['custentityare_they_buying_new_busses'],
                        'custentity34': customer['custentity34'],
                        'custentity43': customer['custentity43'],
                        'custentity46': customer['custentity46'],
                        'customer_rank': 1,
                    })
                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(_(str(e)))

    def import_contacts(self):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            nsAccountID = icpsudo.get_param('netsuite_importer.nsAccountID')
            consumerKey = icpsudo.get_param('netsuite_importer.consumerKey')
            consumerSecret = icpsudo.get_param('netsuite_importer.consumerSecret')
            token = icpsudo.get_param('netsuite_importer.token')
            tokenSecret = icpsudo.get_param('netsuite_importer.tokenSecret')
            base_url = "https://1056867.suitetalk.api.netsuite.com/services/rest/record/v1/contact"
            has_more = True
            offset = self.last_imported_contacts_offset if self.last_imported_contacts_offset else 0
            while has_more:
                Nonce = self._generateNonce(length=11)
                currentTime = self._generateTimestamp()
                signature = self._generateSignature('GET', base_url, consumerKey, Nonce, currentTime, token, consumerSecret,
                                                    tokenSecret, offset)

                payload = ""
                oauth = "OAuth realm=\"" + nsAccountID + "\"," \
                        "oauth_consumer_key=\"" + consumerKey + "\"," \
                        "oauth_token=\"" + token + "\"," \
                        "oauth_signature_method=\"HMAC-SHA256\"," \
                        "oauth_timestamp=\"" + currentTime + "\"," \
                        "oauth_nonce=\"" + Nonce + "\"," \
                        "oauth_version=\"1.0\"," \
                        "oauth_signature=\"" + signature + "\""
                headers = {
                    'Content-Type': "application/json",
                    'Authorization': oauth,
                    'cache-control': "no-cache",
                }
                response = requests.request("GET", base_url+'?offset='+str(offset), data=payload, headers=headers)
                response_dict = json.loads(response.text)
                self.create_contacts(response_dict['items'], base_url)
                self.last_imported_contacts_offset = str(offset)
                offset += 1000
                has_more = response_dict['hasMore']
        except Exception as e:
            raise ValidationError(_(str(e)))

    def create_contacts(self, contacts, url):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            nsAccountID = icpsudo.get_param('netsuite_importer.nsAccountID')
            consumerKey = icpsudo.get_param('netsuite_importer.consumerKey')
            consumerSecret = icpsudo.get_param('netsuite_importer.consumerSecret')
            token = icpsudo.get_param('netsuite_importer.token')
            tokenSecret = icpsudo.get_param('netsuite_importer.tokenSecret')
            for new_contact in contacts:
                odoo_contact = self.env['res.partner'].search([('netsuite_id', '=', new_contact['id'])])
                if not odoo_contact:
                    Nonce = self._generateNonce(length=11)
                    currentTime = self._generateTimestamp()
                    contact_url = url + "/" + new_contact['id']
                    signature = self._generateSingleSignature('GET', contact_url, consumerKey, Nonce, currentTime, token,
                                                        consumerSecret, tokenSecret)
                    oauth = "OAuth realm=\"" + nsAccountID + "\"," \
                            "oauth_consumer_key=\"" + consumerKey + "\"," \
                            "oauth_token=\"" + token + "\"," \
                            "oauth_signature_method=\"HMAC-SHA256\"," \
                            "oauth_timestamp=\"" + currentTime + "\"," \
                            "oauth_nonce=\"" + Nonce + "\"," \
                            "oauth_version=\"1.0\"," \
                            "oauth_signature=\"" + signature + "\""
                    headers = {
                        'Content-Type': "application/json",
                        'Authorization': oauth,
                        'cache-control': "no-cache",
                    }
                    contact_response = requests.request("GET", contact_url, headers=headers)
                    contact = json.loads(contact_response.text)
                    company_id = contact['company']['id']
                    parent_id = self.env['res.partner'].search([('netsuite_id', '=', company_id)])
                    contact_name = contact['firstName'] + " " + contact['lastName']
                    self.env['res.partner'].create({
                        'netsuite_id': contact['id'],
                        'name': contact_name,
                        'is_company': False,
                        'email': contact['email'] if 'email' in contact else None,
                        'phone': contact['phone'] if 'phone' in contact else None,
                        'parent_id': parent_id.id if parent_id else None,
                        'function': contact['title'] if 'title' in contact else None
                    })
                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(_(str(e)))