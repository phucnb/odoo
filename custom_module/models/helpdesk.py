from odoo import models, fields, api

PRODUCT_TYPE = [
    ('DVR', 'DVR'),
   	('Camera', 'Camera'),
   	('Bridge', 'Bridge'),
   	('Access Point', 'Access Point'),
   	('Storage', 'Storage'),
   	('DVR Viewer', 'DVR Viewer'),
   	('Wireless', 'Wireless'),
    ('System Related', 'System Related')
]

DVR_MAIN = [
    ('Zeus 16', 'Zeus 16'),
   	('Zeus 8', 'Zeus 8'),
   	('Zeus 6s', 'Zeus 6s'),
   	('Zeus 5', 'Zeus 5'),
   	('Zeus 3', 'Zeus 3'),
   	('514', '514'),
   	('512', '512'),
    ('500', '500'),
    ('300', '300')
]

CAMERA_MAIN = [
		('HDQ 2.1', 'HDQ 2.1'),
		('HDQ 2.9', 'HDQ 2.9'),
		('HDQ 3.6', 'HDQ 3.6'),
		('HDQ 3.6 SC', 'HDQ 3.6 SC'),
		('HDQ 6.0', 'HDQ 6.0'),
		('HDQ SAC 16', 'HDQ SAC 16'),
		('HDQ Dual SAC 16 | 4.3', 'HDQ Dual SAC 16 | 4.3'),
		('AHD 2.1', 'AHD 2.1'),
		('AHD 2.8c (Shield Cam)', 'AHD 2.8c (Shield Cam)'),
		('AHD SAC 12', 'AHD SAC 12'),
		('AHD Dual SAC 12 | 4.3', 'AHD Dual SAC 12 | 4.3'),
		('FHD 2.1', 'FHD 2.1'),
		('FHD OV360s', 'FHD OV360s'),
		('FHD OV360a', 'FHD OV360a'),
		('FHD 2.1 Shield', 'FHD 2.1 Shield'),
		('FHD SAC 12', 'FHD SAC 12'),
		('FHD Dual SAC 12 | 2.8', 'FHD Dual SAC 12 | 2.8'),
		('FHD SAC 1.6', 'FHD SAC 1.6')
]

BRIDGE_MAIN = [
		('MikroTek 2.4Ghz', 'MikroTek 2.4Ghz'),
		('Ubiquiti 2.4Ghz', 'Ubiquiti 2.4Ghz'),
		('Ubiquiti 5Ghz', 'Ubiquiti 5Ghz')
]

ACCESS_POINT_MAIN = [
		('MikroTek 2.4Ghz', 'MikroTek 2.4Ghz'),
		('Ubiquiti 2.4Ghz Omni', 'Ubiquiti 2.4Ghz Omni'),
		('Ubiquiti 5Ghz Omni', 'Ubiquiti 5Ghz Omni'),
		('Ubiquiti Nanobeam', 'Ubiquiti Nanobeam')
]

STORAGE_MAIN = [
		('Infinity', 'Infinity'),
		('DHD2', 'DHD2'),
		('DHD', 'DHD'),
		('SSD', 'SSD'),
		('HDD', 'HDD'),
		('SD Card', 'SD Card')
]

DVR_VIEWER_MAIN = [
		('v19.522 (Win10)', 'v19.522 (Win10)'),
		('v17.1215 (Win7)', 'v17.1215 (Win7)'),
		('Outdated Version', 'Outdated Version')
]

WIRELESS_MAIN = [
		('Touchdown', 'Touchdown'),
		('v3.7.39', 'v3.7.39'),
		('v3.7.38', 'v3.7.38'),
		('v3.7.34', 'v3.7.34'),
		('Laptop Server', 'Laptop Server'),
		('Rack Server', 'Rack Server'),
		('HP ProLiant Server', 'HP ProLiant Server'),
		('Virtual Server', 'Virtual Server'),
		('s247 Server', 's247 Server'),
		('Windows 10', 'Windows 10'),
		('Windows Server 2019', 'Windows Server 2019'),
		('Windows Server 2016', 'Windows Server 2016'),
		('Windows Server 2012R2', 'Windows Server 2012R2'),
		('Windows 7', 'Windows 7'),
		('Network Domain', 'Network Domain'),
		('Windows Defender', 'Windows Defender'),
		('3rd Party Antivirus', '3rd Party Antivirus')
]

SYSTEM_RELATED_MAIN = [
		('Laptop', 'Laptop'),
		('PC', 'PC'),
		('MAC', 'MAC'),
		('All-In-One', 'All-In-One'),
		('Other', 'Other'),
		('Windows 10', 'Windows 10'),
		('Windows 8.1', 'Windows 8.1'),
		('Windows 8', 'Windows 8'),
		('Windows 7', 'Windows 7'),
		('Windows XP', 'Windows XP'),
		('Dell', 'Dell'),
		('HP', 'HP'),
		('Lenovo', 'Lenovo'),
		('Network Domain', 'Network Domain')
]



class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'

    partner_bus_garage_address = fields.Char(string='Bus Garage Address', compute='_compute_partner_contact', store=True, readonly=False)
    partner_phone = fields.Char(string='Main Company Phone', compute='_compute_partner_contact', store=True, readonly=False)
    partner_main_contact = fields.Char(string='Primary Ticket Contact', compute='_compute_partner_contact', store=True, readonly=False)
    partner_main_contact_phone = fields.Char(string='Primary Contact Phone', compute='_compute_partner_contact', store=True, readonly=False)


    def _compute_partner_contact(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.partner_bus_garage_address = ticket.partner_id.bus_garage_address
                ticket.partner_phone = ticket.partner_id.phone
                ticket.partner_main_contact = ticket.partner_id.main_contact.partner_id
                ticket.partner_main_contact_phone = ticket.partner_id.main_contact_phone
	#ISSUE TYPE
	dvr_check = fields.Boolean("DVR")
	cam_check = fields.Boolean("Camera")
	storage_check = fields.Boolean("Storage")
	ap_check = fields.Boolean("Access Point")
	bridge_check = fields.Boolean("Bridge")
	td_check = fields.Boolean("Touchdown")
	dvrv_check = fields.Boolean("DVR Viewer")
	cust_sys_check = fields.Boolean("Customer Side Issue")
	#PROD TYPE
	dvr_type = fields.Selection(DVR_MAIN, "DVR Model")
	cam_type = fields.Selection(CAMERA_MAIN, "Camera Model")
	storage_type = fields.Selection(STORAGE_MAIN, "Storage Model")
	ap_type = fields.Selection(ACCESS_POINT_MAIN, "Access Point Model")
	bridge_type = fields.Selection(BRIDGE_MAIN, "Bridge Model")
	td_type = fields.Selection(WIRELESS_MAIN, "Touchdown Type")
	dvrv_type = fields.Selection(DVR_VIEWER_MAIN, "DVR Viewer Version")
	cust_sys_type = fields.Selection(SYSTEM_RELATED_MAIN, "Customer System Type")




    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     if self.partner_id:
    #             self.name = partner_id
                
            


    # @api.onchange('product_main')
    # def onchange_product_main(self):
    #     if self.product_main:
    #         if self.product_issue \
    #                 and self.product_issue.id not in self.product_main.child_ids.ids:
    #             self.product_issue = False


            