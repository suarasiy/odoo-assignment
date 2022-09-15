from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Pemasukan(models.Model):
    _name = 'tokobaju.pemasukan'
    _description = 'New Description'

    name = fields.Char(string='Nota Pemasukan',
                       compute="_compute_nota_pemasukan")
    supplier_id = fields.Many2one(
        comodel_name='tokobaju.supplier', string='Supplier')
    pemasukan_detail_ids = fields.One2many(
        comodel_name='tokobaju.pemasukan_detail', inverse_name='pemasukan_id', string='Pemasukan Detail')
    daftar_pemasukan = fields.Char(
        string='Daftar Pemasukan', compute="_compute_daftar_pemasukan")
    daftar_pemasukan_lengkap = fields.Char(
        string='Daftar Pemasukan Lengkap', compute="_compute_daftar_pemasukan_lengkap")

    total_harga = fields.Integer(
        string='Total Harga', compute="_compute_total_harga")
    state = fields.Selection(string='Status', selection=[(
        'menunggu_konfirmasi', 'Menunggu Konfirmasi'), ('selesai', 'Selesai'), ], default='menunggu_konfirmasi', readonly=True)

    def _compute_nota_pemasukan(self):
        for rec in self:
            rec.name = f"PMS-{rec.id}"

    @api.depends('pemasukan_detail_ids')
    def _compute_total_harga(self):
        for rec in self:
            rec.total_harga = sum(rec.pemasukan_detail_ids.mapped('subtotal'))

    @api.depends('pemasukan_detail_ids')
    def action_selesai(self):
        self.state = 'selesai'
        for rec in self.pemasukan_detail_ids:
            rec.produk.stok += rec.qty

    def _compute_daftar_pemasukan(self):
        for rec in self:
            result = rec.pemasukan_detail_ids.search(
                [('pemasukan_id', '=', rec.id)]).mapped('produk.produk')
            if len(result) > 3:
                cresult = result[:3]
                _ = ", ".join(cresult)
                rec.daftar_pemasukan = f"{_}...(+{len(result)-3})"
            else:
                rec.daftar_pemasukan = ", ".join(result)

    def _compute_daftar_pemasukan_lengkap(self):
        for rec in self:
            rec.daftar_pemasukan_lengkap = rec.pemasukan_detail_ids.search(
                [('pemasukan_id', '=', rec.id)]).mapped('produk.produk')

    def unlink(self):
        if self.filtered(lambda x: x.state == 'selesai'):
            raise ValidationError('Tidak dapat menghapus record.')
        return super(Pemasukan, self).unlink()


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
