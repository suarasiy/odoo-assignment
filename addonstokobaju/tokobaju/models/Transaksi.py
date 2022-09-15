from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Transaksi(models.Model):
    _name = 'tokobaju.transaksi'
    _description = 'New Description'
    _rec_name = 'nota'

    nota = fields.Char(string='Nota', compute="_compute_nota")
    diskon = fields.Integer(string='Diskon')
    transaksi_detail_ids = fields.One2many(
        comodel_name='tokobaju.transaksi_detail', inverse_name='transaksi_id', string='Transaksi Detail')
    total_harga = fields.Integer(
        string='Total Harga', compute="_compute_total_harga")
    total_bayar = fields.Integer(string='Total Bayar')
    state = fields.Selection(string='Status', selection=[('menunggu_konfirmasi', 'Menunggu Konfirmasi'), (
        'selesai', 'Selesai'), ('cancel', 'Cancel'), ('refund', 'Produk Refund')], default="menunggu_konfirmasi", readonly=True)

    def _compute_nota(self):
        for rec in self:
            rec.nota = f"TSK-{rec.id}"

    @api.depends('transaksi_detail_ids', 'diskon')
    def _compute_total_harga(self):
        for rec in self:
            if rec.diskon > 0:
                total_harga = sum(rec.transaksi_detail_ids.mapped('subtotal'))
                rec.total_harga = total_harga - \
                    (total_harga / 100 * rec.diskon)
            else:
                rec.total_harga = sum(
                    rec.transaksi_detail_ids.mapped('subtotal'))

    @api.constrains('total_bayar')
    def constrains_total_bayar(self):
        for rec in self:
            if rec.total_bayar < rec.total_harga:
                raise ValidationError("Jumlah bayar kurang dari total harga.")

    def action_selesai(self):
        for rec in self:
            rec.state = 'selesai'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_refund(self):
        for rec in self:
            rec.state = 'refund'

    def write(self, values):
        if values['state'] == 'selesai':
            for rec in self.transaksi_detail_ids:
                rec.produk_id.stok -= rec.qty
        elif values['state'] == 'refund':
            for rec in self.transaksi_detail_ids:
                rec.produk_id.stok += rec.qty
        return super(Transaksi, self).write(values)

    def unlink(self):
        if self.filtered(lambda x: x.state == 'selesai' or x.state == 'refund' or x.state == 'menunggu_konfirmasi'):
            raise ValidationError('Tidak dapat menghapus record.')
        return super().unlink()


class TransaksiDetail(models.Model):
    _name = 'tokobaju.transaksi_detail'
    _description = 'New Description'

    transaksi_id = fields.Many2one(
        comodel_name='tokobaju.transaksi', string='Transaksi', ondelete="cascade")
    produk_id = fields.Many2one(
        comodel_name='tokobaju.produk', string='Produk')
    harga_produk = fields.Integer(string='Harga Produk')
    diskon_produk = fields.Integer(string='Diskon Produk')
    qty = fields.Integer(string='Qty')
    subtotal = fields.Integer(string='Sub Total', compute="_compute_subtotal")

    @api.depends('harga_produk', 'diskon_produk', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            if rec.diskon_produk > 0:
                subtotal = rec.harga_produk * rec.qty
                rec.subtotal = subtotal - (subtotal / 100 * rec.diskon_produk)
            else:
                rec.subtotal = rec.harga_produk * rec.qty

    @api.onchange('produk_id')
    def _compute_harga_produk(self):
        if self.produk_id.harga:
            self.harga_produk = self.produk_id.harga

    @api.constrains('qty')
    def constrains_qty(self):
        for rec in self:
            if rec.qty > rec.produk_id.stok:
                raise ValidationError(
                    f"Jumlah quantity {rec.produk_id.produk} melebihi dari stok.")
