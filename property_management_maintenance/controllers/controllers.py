# -*- coding: utf-8 -*-
# from odoo import http


# class PropertyManagementMaintenance(http.Controller):
#     @http.route('/property_management_maintenance/property_management_maintenance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property_management_maintenance/property_management_maintenance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('property_management_maintenance.listing', {
#             'root': '/property_management_maintenance/property_management_maintenance',
#             'objects': http.request.env['property_management_maintenance.property_management_maintenance'].search([]),
#         })

#     @http.route('/property_management_maintenance/property_management_maintenance/objects/<model("property_management_maintenance.property_management_maintenance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property_management_maintenance.object', {
#             'object': obj
#         })

