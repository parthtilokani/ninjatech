# -*- coding: utf-8 -*-
# from odoo import http


# class PropertyManagementProjectTask(http.Controller):
#     @http.route('/property_management_project_task/property_management_project_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property_management_project_task/property_management_project_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('property_management_project_task.listing', {
#             'root': '/property_management_project_task/property_management_project_task',
#             'objects': http.request.env['property_management_project_task.property_management_project_task'].search([]),
#         })

#     @http.route('/property_management_project_task/property_management_project_task/objects/<model("property_management_project_task.property_management_project_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property_management_project_task.object', {
#             'object': obj
#         })

