from odoo import models, fields


class Customer(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Customer', default=True)
