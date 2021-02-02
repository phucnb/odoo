# -*- coding: utf-8 -*-
from odoo import http

# class NetsuiteImporter(http.Controller):
#     @http.route('/netsuite_importer/netsuite_importer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/netsuite_importer/netsuite_importer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('netsuite_importer.listing', {
#             'root': '/netsuite_importer/netsuite_importer',
#             'objects': http.request.env['netsuite_importer.netsuite_importer'].search([]),
#         })

#     @http.route('/netsuite_importer/netsuite_importer/objects/<model("netsuite_importer.netsuite_importer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('netsuite_importer.object', {
#             'object': obj
#         })