from odoo import models
import base64
import io


class ProdukReportXlsx(models.AbstractModel):
    _name = 'report.tokobaju.report_produk'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'New Description'

    def generate_xlsx_report(self, workbook, data, products):
        row = 2
        col = 1
        bold = workbook.add_format({'bold': True})
        bold.set_border()
        cs = workbook.add_format()
        cs.set_border()
        sheet = workbook.add_worksheet('Report Produk')
        sheet.merge_range(0, 0, 0, 9, "Report Produk", bold)
        sheet.write(1, 0, "s-img", bold)
        sheet.write(1, 1, "Nama Produk", bold)
        sheet.write(1, 2, "Kategori", bold)
        sheet.write(1, 3, "Harga Jual", bold)
        sheet.write(1, 4, "Stok", bold)
        sheet.write(1, 5, "Warna", bold)
        sheet.write(1, 6, "Size", bold)
        sheet.write(1, 7, "Tersedia", bold)
        sheet.write(1, 8, "Barcode", bold)
        sheet.write(1, 9, "Terjual", bold)

        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 28)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 13)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 6)
        sheet.set_column('H:H', 9)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 10)

        for report in products:
            if report.foto:
                produk_image = io.BytesIO(base64.b64decode(report.foto))
                sheet.insert_image(row, 0, "img.png", {
                                   'image_data': produk_image, 'x_scale': 0.030, 'y_scale': 0.030})
            sheet.write(row, col, report.produk, cs)
            col += 1
            sheet.write(row, col, report.kategori_produk_id.kategori, cs)
            col += 1
            sheet.write(row, col, report.harga, cs)
            col += 1
            sheet.write(row, col, report.stok, cs)
            col += 1
            sheet.write(row, col, report.warna, cs)
            col += 1
            sheet.write(row, col, report.ukuran.upper(), cs)
            col += 1
            sheet.write(row, col, report.tersedia, cs)
            col += 1
            sheet.write(row, col, report.barcode, cs)
            col += 1
            sheet.write(
                row, col, f"{report.terjual} / {report.target_penjualan}", cs)
            col = 1
            row += 1
