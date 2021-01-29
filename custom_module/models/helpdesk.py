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

DVR_TYPE = [
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

CAM_TYPE = [
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

BRIDGE_TYPE = [
		('MikroTek 2.4Ghz', 'MikroTek 2.4Ghz'),
		('Ubiquiti 2.4Ghz', 'Ubiquiti 2.4Ghz'),
		('Ubiquiti 5Ghz', 'Ubiquiti 5Ghz')
]

AP_TYPE = [
		('MikroTek 2.4Ghz', 'MikroTek 2.4Ghz'),
		('Ubiquiti 2.4Ghz Omni', 'Ubiquiti 2.4Ghz Omni'),
		('Ubiquiti 5Ghz Omni', 'Ubiquiti 5Ghz Omni'),
		('Ubiquiti Nanobeam', 'Ubiquiti Nanobeam')
]

STORAGE_TYPE = [
		('Infinity', 'Infinity'),
		('DHD2', 'DHD2'),
		('DHD', 'DHD'),
		('SSD', 'SSD'),
		('HDD', 'HDD'),
		('SD Card', 'SD Card')
]

DVRV_VERSION = [
		('v19.522 (Win10)', 'v19.522 (Win10)'),
		('v17.1215 (Win7)', 'v17.1215 (Win7)'),
		('Outdated Version', 'Outdated Version')
]

TD_SRVR_TYPE = [
		('Laptop Server', 'Laptop Server'),
		('Rack Server', 'Rack Server'),
		('HP ProLiant Server', 'HP ProLiant Server'),
		('Virtual Server', 'Virtual Server'),
		('s247 Server', 's247 Server'),
		('TD Cloud', 'TD Cloud')
]

TD_VERSION = [
	('v3.7.34', 'v3.7.34'),
	('v3.7.38', 'v3.7.38'),
	('v3.7.39', 'v3.7.39'),
	('OTHER', 'Other Version: See Notes')
]

TD_OS = [
	('Windows 10', 'Windows 10'),
	('Windows Server 2019', 'Windows Server 2019'),
	('Windows Server 2016', 'Windows Server 2016'),
	('Windows Server 2012R2', 'Windows Server 2012R2'),
	('Windows 7', 'Windows 7')
]

CUST_SYS_TYPE = [
		('Laptop', 'Laptop'),
		('PC', 'PC'),
		('MAC', 'MAC'),
		('All-In-One', 'All-In-One'),
		('Other', 'Other'),
]

CUST_SYS_OS = [
	('Windows 10', 'Windows 10'),
	('Windows 8.1', 'Windows 8.1'),
	('Windows 8', 'Windows 8'),
	('Windows 7', 'Windows 7'),
	('Windows XP', 'Windows XP')
]

CUST_SYS_MODEL = [
	('Dell', 'Dell'),
	('HP', 'HP'),
	('Lenovo', 'Lenovo'),
	('Other', 'Other')
]

TICKET_RESOLUTION = [
    ('RESOLVED', 'Resolved'),
    ('NORESOLVE', 'Cannot Resolve'),
    ('SERVER INSPECTION', 'Wireless Inspection Complete')
]

TICKET_RESOLUTION_RESOLVED = [
    ('INSTRUCT', 'Instructions / Training'),
    ('DVRVLink', 'DVR Viewer Link Sent'),
    ('RMA', 'Equipment RMA Performed'),
    ('SITE VISIT', 'Site Visit Scheduled'),
    ('WIRELESS', 'Touchdown Software / Server Repaired'),
    ('ZOOM', 'Zoom Cable Sent to Customer')
]

TICKET_RESOLUTION_SERVER_INSPECTION = [
    ('COMPLETE', 'No Action Required'),
    ('COMPELTE RMA', 'RMA Sent'),
    ('COMPLETE SOFTWARE REP', 'TD Software Repaired'),
    ('COMPLETE SERVER REP', 'TD Server to be Repaired'),
    ('COMPLETE SITE VISIT', 'Site Visit Scheduled')
]

TICKET_RESOLUTION_CANNOT_RESOLVE = [
    ('CANNOT CONTACT', 'Could not Contact Customer')
]

class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'
    #RESOLUTIONS
    resolution_main = fields.Selection(TICKET_RESOLUTION, "Resolution")
    resolution_resolved = fields.Selection(TICKET_RESOLUTION_RESOLVED, "Resolution Cont")
    resolution_server_inspection = fields.Selection(TICKET_RESOLUTION_SERVER_INSPECTION, "Resolution Cont")
    resolution_cannot_resolve = fields.Selection(TICKET_RESOLUTION_CANNOT_RESOLVE, "Resolution Cont")
    resolution_notes = fields.Text("Resolution Notes")
    issue_notes = fields.Text("Issue Description")
    #DVRs
    dvr_check = fields.Boolean("DVR")
    dvr_type_1 = fields.Selection(DVR_TYPE, "DVR Type")
    dvr_qty_1 = fields.Integer("Quantity")
    add_dvr_1 = fields.Boolean("Add Additional DVR Type")
    dvr_type_2 = fields.Selection(DVR_TYPE, "DVR Type")
    dvr_qty_2 = fields.Integer("Quantity")
    add_dvr_2 = fields.Boolean("Add Additional DVR Type")
    dvr_type_3 = fields.Selection(DVR_TYPE, "DVR Type")
    dvr_qty_3 = fields.Integer("Quantity")
    dvr_sn = fields.Text("Serial Numbers")
    dvr_edcMdc = fields.Text("EDC / MDC")
    dvr_firmware = fields.Text("Firmware")
    dvr_mcu = fields.Text("MCU")
    dvr_notes = fields.Text("Additional Notes")
    #CAMERAS
    cam_check = fields.Boolean("Camera")
    cam_type_1 = fields.Selection(CAM_TYPE, "Camera Type")
    cam_qty_1 = fields.Integer("Quantity")
    add_cam_1 = fields.Boolean("Add Additional Camera Type")
    cam_type_2 = fields.Selection(CAM_TYPE, "Camera Type")
    cam_qty_2 = fields.Integer("Quantity")
    add_cam_2 = fields.Boolean("Add Additional Camera Type")
    cam_type_3 = fields.Selection(CAM_TYPE, "Camera Type")
    cam_qty_3 = fields.Integer("Quantity")
    cam_notes = fields.Text("Camera Notes")
    #STORAGE
    storage_check = fields.Boolean("Storage")
    storage_type_1 = fields.Selection(STORAGE_TYPE, "Storage Type")
    storage_qty_1 = fields.Integer("Quantity")
    add_storage_1 = fields.Boolean("Add Additional Storage Type")
    storage_type_2 = fields.Selection(STORAGE_TYPE, "Storage Type")
    storage_qty_2 = fields.Integer("Quantity")
    add_storage_2 = fields.Boolean("Add Additional Storage Type")
    storage_type_3 = fields.Selection(STORAGE_TYPE, "Storage Type")
    storage_qty_3 = fields.Integer("Quantity")
    storage_notes = fields.Text("Storage Notes")
    #APs
    ap_check = fields.Boolean("Access Point")
    ap_type_1 = fields.Selection(AP_TYPE, "Access Point Type")
    ap_qty_1 = fields.Integer("Quantity")
    add_ap_1 = fields.Boolean("Add Additional AP Type")
    ap_type_2 = fields.Selection(AP_TYPE, "Access Point Type")
    ap_qty_2 = fields.Integer("Quantity")
    add_ap_2 = fields.Boolean("Add Additional AP Type")
    ap_type_3 = fields.Selection(AP_TYPE, "Access Point Type")
    ap_qty_3 = fields.Integer("Quantity")
    ap_notes = fields.Text("Access Point Notes")
    #BRIDGEs
    bridge_check = fields.Boolean("Bridge")
    bridge_type_1 = fields.Selection(BRIDGE_TYPE, "Bridge Type")
    bridge_qty_1 = fields.Integer("Quantity")
    add_bridge_1 = fields.Boolean("Add Additional Bridge Type")
    bridge_type_2 = fields.Selection(BRIDGE_TYPE, "Bridge Type")
    bridge_qty_2 = fields.Integer("Quantity")
    add_bridge_2 = fields.Boolean("Add Additional Bridge Type")
    bridge_type_3 = fields.Selection(BRIDGE_TYPE, "Bridge Type")
    bridge_qty_3 = fields.Integer("Quantity")
    bridge_notes = fields.Text("Bridge Notes")
    #TD
    td_check = fields.Boolean("Touchdown")
    td_type = fields.Selection(TD_SRVR_TYPE, "Touchdown Type")
    td_os = fields.Selection(TD_OS, "Operating System")
    td_version = fields.Selection(TD_VERSION, "Version")
    td_notes = fields.Text("Touchdown Notes")
    #DVRViewer
    dvrv_check = fields.Boolean("DVR Viewer")
    dvrv_type = fields.Selection(DVRV_VERSION, "DVR Viewer Version")
    dvrv_notes = fields.Text("DVRViewer Notes")
    #CUSTOMER SYSTEM
    cust_sys_check = fields.Boolean("Customer Related")
    cust_sys_type = fields.Selection(CUST_SYS_TYPE, "Customer Related Type")
    cust_sys_model = fields.Selection(CUST_SYS_MODEL, "Computer Model")
    cust_sys_os = fields.Selection(CUST_SYS_OS, "Operating System")
    cust_sys_notes = fields.Text("Customer Related System Notes")

    #ticket owner

    ticket_owner = fields.Many2one(
        'res.users', string='Ticket Owner'
    )
