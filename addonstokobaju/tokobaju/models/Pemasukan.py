from email.policy import default
from odoo import api, fields, models


class Pemasukan(models.Model):
    _name = 'tokobaju.pemasukan'
    _description = 'New Description'

    name = fields.Char(string='Nota Pemasukan')
    supplier_id = fields.Many2one(
        comodel_name='tokobaju.supplier', string='Supplier')
    pemasukan_detail_ids = fields.One2many(
        comodel_name='tokobaju.pemasukan_detail', inverse_name='pemasukan_id', string='Pemasukan Detail')
    total_harga = fields.Integer(
        string='Total Harga', compute="_compute_total_harga")
    state = fields.Selection(string='Status', selection=[(
        'menunggu_konfirmasi', 'Menunggu Konfirmasi'), ('selesai', 'Selesai'), ], default='menunggu_konfirmasi', readonly=True)

    @api.depends('pemasukan_detail_ids')
    def _compute_total_harga(self):
        self.total_harga = sum(self.pemasukan_detail_ids.mapped('subtotal'))

    @api.depends('pemasukan_detail_ids')
    def action_selesai(self):
        self.state = 'selesai'
        for rec in self.pemasukan_detail_ids:
            rec.produk.stok += rec.qty


class PemasukanDetail(models.Model):
    _name = 'tokobaju.pemasukan_detail'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    pemasukan_id = fields.Many2one(
        comodel_name='tokobaju.pemasukan', string='Detail Pemasukan')
    produk = fields.Many2one(comodel_name='tokobaju.produk', string='Produk')
    harga = fields.Integer(string='Harga')
    qty = fields.Integer(string='Qty')
    subtotal = fields.Integer(string='Sub Total', compute="_compute_subtotal")

    @api.depends('qty', 'harga')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.harga * rec.qty
