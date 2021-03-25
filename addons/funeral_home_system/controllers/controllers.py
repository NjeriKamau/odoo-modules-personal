# -*- coding: utf-8 -*-
# from odoo import http


# class FuneralHomeSystem(http.Controller):
#     @http.route('/funeral_home_system/funeral_home_system/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/funeral_home_system/funeral_home_system/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('funeral_home_system.listing', {
#             'root': '/funeral_home_system/funeral_home_system',
#             'objects': http.request.env['funeral_home_system.funeral_home_system'].search([]),
#         })

#     @http.route('/funeral_home_system/funeral_home_system/objects/<model("funeral_home_system.funeral_home_system"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('funeral_home_system.object', {
#             'object': obj
#         })
