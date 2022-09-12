# -*- coding: utf-8 -*-
# from odoo import http


# class Tokobaju(http.Controller):
#     @http.route('/tokobaju/tokobaju', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tokobaju/tokobaju/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tokobaju.listing', {
#             'root': '/tokobaju/tokobaju',
#             'objects': http.request.env['tokobaju.tokobaju'].search([]),
#         })

#     @http.route('/tokobaju/tokobaju/objects/<model("tokobaju.tokobaju"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tokobaju.object', {
#             'object': obj
#         })
