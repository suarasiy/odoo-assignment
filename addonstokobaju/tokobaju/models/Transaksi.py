from odoo import api, fields, models


class Transaksi(models.Model):
    _name = 'tokobaju.transaksi'
    _description = 'New Description'
    _rec_name = 'nota'

    nota = fields.Char(string='Nota')
    diskon = fields.Integer(string='Diskon')
    transaksi_detail_ids = fields.One2many(
        comodel_name='tokobaju.transaksi_detail', inverse_name='transaksi_id', string='Transaksi Detail')
    total_harga = fields.Integer(string='Total Harga')
    total_bayar = fields.Integer(string='Total Bayar')


class TransaksiDetail(models.Model):
    _name = 'tokobaju.transaksi_detail'
    _description = 'New Description'

    transaksi_id = fields.Many2one(
        comodel_name='tokobaju.transaksi', string='Transaksi')
    produk_id = fields.Many2one(
        comodel_name='tokobaju.produk', string='Produk')
    harga_produk = fields.Integer(string='Harga Produk')
    diskon_produk = fields.Integer(string='Diskon Produk')
    qty = fields.Integer(string='Qty')
    subtotal = fields.Integer(string='Sub Total', compute="_compute_subtotal")

    @api.depends('harga_produk', 'diskon_produk', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.harga_produk * rec.qty
