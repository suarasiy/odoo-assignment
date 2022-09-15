from email.policy import default
from odoo import api, fields, models


class Produk(models.Model):
    _name = 'tokobaju.produk'
    _description = 'New Description'
    _rec_name = 'produk'

    produk = fields.Char(string='Produk')
    kategori_produk_id = fields.Many2one(
        comodel_name='tokobaju.produk_kategori', string='Kategori')
    foto = fields.Image('foto', max_width=800, max_height=800)
    warna = fields.Char(string='Warna')
    ukuran = fields.Selection(string='Ukuran', selection=[('xs', 'XS'), ('s', 'S'), (
        'm', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL'), ('xxxl', 'XXXL'), ('xxxxl', 'XXXXL')], required=True)

    stok = fields.Integer(string='Stok')
    barcode = fields.Char(string='Barcode')
    harga = fields.Integer(string='Harga', required=True, default=0)
    tersedia = fields.Boolean(string='Tersedia', default=True)
    target_penjualan = fields.Integer(string='Target Penjualan', default=0)

    terjual = fields.Integer(
        string='Terjual', compute="_compute_terjual", readonly=True)
    transaksi_ids = fields.One2many(
        comodel_name='tokobaju.transaksi_detail', inverse_name='produk_id', string='Transaksi')

    @api.depends('transaksi_ids')
    def _compute_terjual(self):
        for rec in self:
            rec.terjual = sum(self.env['tokobaju.transaksi_detail'].search(
                [('produk_id', '=', rec.id)]).mapped('qty'))


class ProdukKategori(models.Model):
    _name = 'tokobaju.produk_kategori'
    _description = 'New Description'
    _rec_name = 'kategori'

    kategori = fields.Char(string='Kategori')
    keterangan = fields.Char(string='Keterangan')
    foto = fields.Image('foto', max_width=500, max_height=500)
