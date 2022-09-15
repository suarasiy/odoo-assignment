from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'tokobaju.supplier'
    _description = 'New Description'

    name = fields.Char(string='Supplier')
    alamat = fields.Text('Alamat')
    no_telp = fields.Char(string='No. Telepon')
    deskripsi = fields.Text('Deskripsi')
