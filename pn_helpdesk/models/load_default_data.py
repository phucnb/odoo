from odoo import api, fields, models

DVR_PRODUCTS = ['Zeus 16', 'Zeus 8', 'Zeus 6s', 'Zeus 5', 'Zeus 3', '514', '512', '500', '300']
DVR_ISSUES = [
    'No Power / Ignition', 'Blinking Ignition', 'No Record Mode',
    'Video Loss Light', 'No EMR Lights', 'Popping Fuses', 'Transfer Issue',
    'Firmware Outdated', 'Wireless Upload'
]
DVR_RESOLUTION = [
    'RMA DVR', 'RMA EMR', 'Fuse Change', 'RMA Power Cable',
    'Update Firmware', 'Modify DVR Settings', 'Host Deploy DVR', 'Schedule Service Visit'
]
CAMERA_PRODUCTS = [
    'HDQ 2.1', 'HDQ 2.9', 'HDQ 3.6', 'HDQ 3.6 SC',
    'HDQ 6.0', 'HDQ SAC 16', 'HDQ Dual SAC 16 | 4.3', 'AHD 2.1',
    'AHD 2.8c (Shield Cam)', 'AHD SAC 12', 'AHD Dual SAC 12 | 4.3', 'FHD 2.1',
    'FHD OV360s', 'FHD OV360a', 'FHD 2.1 Shield', 'FHD SAC 12', 'FHD Dual SAC 12 | 2.8'
]
CAMERA_ISSUES = [
    'No Video', 'Distorted Video', 'Poor Audio', 'Frame Skipping',
    'Intermittent Outtage', 'IR Issue'
]
CAMERA_RESOLUTION = ['Change DVR Port', 'RMA Camera', 'RMA Cable']
BRIDGE_PRODUCT = ['MikroTek 2.4Ghz', 'Ubiquiti 2.4Ghz', 'Ubiquiti 5Ghz']
ACCESS_PRODUCT = ['MikroTek 2.4Ghz', 'Ubiquiti 2.4Ghz Omni', 'Ubiquiti 5Ghz Omni', 'Ubiquiti Nanobeam']
STORAGE_PRODUCT = ['Infinity', 'DHD2', 'DHD', 'SSD', 'HDD', 'SD Card']
DVR_VIEWER_PRODUCT = ['v19.522 (Win10)', 'v17.1215 (Win7)', 'Outdated Version']
WIRELESS_PRODUCT = [
    'Touchdown', 'v3.7.39', 'v3.7.38', 'v3.7.34',
    'Laptop Server', 'Rack Server', 'HP ProLiant Server', 'Virtual Server',
    's247 Server', 'Windows 10', 'Windows Server 2019', 'Windows Server 2016',
    'Windows Server 2012R2', 'Windows 7', 'Network Domain', 'Windows Defender',
    '3rd Party Antivirus'
]
SYSTEM_PRODUCT = [
    'Laptop', 'PC', 'MAC', 'All-In-One',
    'Other', 'Windows 10', 'Windows 8.1', 'Windows 8',
    'Windows 7', 'Windows XP', 'Dell', 'HP',
    'Lenovo', 'Network Domain'
]
BRIDGE_ISSUES = [
    'No Video', 'Distorted Video', 'Poor Audio', 'Frame Skipping',
    'Intermittent Outtage', 'IR Issue'
]
BRIDGE_RESOLUTION = ['Change DVR Port', 'RMA Camera', 'RMA Cable']
ACCESS_ISSUES = [
    'SSID Config', 'Bent / Broken Antenna', 'Disconnected Cable', 'No Power',
    'Switch / Injector Issue', 'Cat Cable Issue'
]
ACCESS_RESOLUTION = ['RMA AP', 'RMA Switch', 'Service Visit Scheduled']
STORAGE_ISSUES = ['Missing Video', 'Transfer Issue', 'Playback Issue', 'Encrypted']
STORAGE_RESOLUTION = ['RMA Storage', 'Format Storage']
DVR_VIEWER_ISSUE = ['Video Playback', 'Create Clips', 'General Use'],
DVR_VIEWER_RESOLUTION = ['Reinstall DVRViewer', 'Update DVRViewer', 'Provide Instruction']
WIRELESS_ISSUE = ['Check-In', 'Video Request', 'Video Review', 'E-Mail']
WIRELESS_RESOLUTION = ['Update TD Software', 'Restart TD Applications', 'Configure Settings', 'Add AV Exclusions']
SYSTEM_ISSUE = ["Can't Create Video", "Can't Cut Clips", 'DVR Viewer Issue']
SYSTEM_RESOLUTION = ['Training Scheduled']


class HelpdeskLoadData(models.Model):
    _inherit = 'helpdesk.ticket.product'

    @api.model
    def act_cron_create_data(self):
        dvr_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_dvr').id
        camera_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_camera').id
        bridge_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_bridge').id
        access_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_access_point').id
        storage_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_storage').id
        dvr_view_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_dvr_viewer').id
        wrieless_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_wrieless').id
        system_type_id = self.env.ref('pn_helpdesk.helpdesk_ticket_type_system_rel').id
        # Create product
        try:
            # DVR
            self._create_helpdesk_ticket_product(DVR_PRODUCTS, dvr_type_id)
            self._create_helpdesk_ticket_issue(DVR_ISSUES, dvr_type_id)
            self._create_helpdesk_ticket_resolution(DVR_RESOLUTION, dvr_type_id)
            # CAM
            self._create_helpdesk_ticket_product(CAMERA_PRODUCTS, camera_type_id)
            self._create_helpdesk_ticket_issue(CAMERA_ISSUES, camera_type_id)
            self._create_helpdesk_ticket_resolution(CAMERA_RESOLUTION, camera_type_id)
            # BRI
            self._create_helpdesk_ticket_product(BRIDGE_PRODUCT, bridge_type_id)
            self._create_helpdesk_ticket_issue(DVR_ISSUES, bridge_type_id)
            self._create_helpdesk_ticket_resolution(BRIDGE_RESOLUTION, bridge_type_id)
            # DVR
            self._create_helpdesk_ticket_product(ACCESS_PRODUCT, access_type_id)
            self._create_helpdesk_ticket_issue(ACCESS_ISSUES, access_type_id)
            self._create_helpdesk_ticket_resolution(ACCESS_RESOLUTION, access_type_id)
            # DVR
            self._create_helpdesk_ticket_product(STORAGE_PRODUCT, storage_type_id)
            self._create_helpdesk_ticket_issue(STORAGE_ISSUES, storage_type_id)
            self._create_helpdesk_ticket_resolution(STORAGE_RESOLUTION, storage_type_id)
            # DVR
            self._create_helpdesk_ticket_product(DVR_VIEWER_PRODUCT, dvr_view_type_id)
            self._create_helpdesk_ticket_issue(DVR_VIEWER_ISSUE, dvr_view_type_id)
            self._create_helpdesk_ticket_resolution(DVR_VIEWER_RESOLUTION, dvr_view_type_id)
            # DVR
            self._create_helpdesk_ticket_product(WIRELESS_PRODUCT, wrieless_type_id)
            self._create_helpdesk_ticket_issue(WIRELESS_ISSUE, wrieless_type_id)
            self._create_helpdesk_ticket_resolution(WIRELESS_RESOLUTION, wrieless_type_id)
            # DVR
            self._create_helpdesk_ticket_product(SYSTEM_PRODUCT, system_type_id)
            self._create_helpdesk_ticket_issue(SYSTEM_ISSUE, system_type_id)
            self._create_helpdesk_ticket_resolution(SYSTEM_RESOLUTION, system_type_id)
            # DVR
            return True
        except Exception as e:
            print(str(e))
            pass

    def _create_helpdesk_ticket_product(self, products, type_id):
        product_modules = self.env['helpdesk.ticket.product'].sudo()
        for product in products:
            product_modules.create({
                'name': product,
                'ticket_type_id': type_id,
            })

    def _create_helpdesk_ticket_issue(self, issues, type_id):
        issue_modules = self.env['helpdesk.ticket.issue'].sudo()
        for issue in issues:
            issue_modules.create({
                'name': issue,
                'ticket_type_id': type_id,
            })

    def _create_helpdesk_ticket_resolution(self, resolutions, type_id):
        resolution_modules = self.env['helpdesk.ticket.resolution'].sudo()
        for resolution in resolutions:
            resolution_modules.create({
                'name': resolution,
                'ticket_type_id': type_id,
            })
