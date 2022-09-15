from odoo import models
import base64
import io


class TransaksiReportXlsx(models.AbstractModel):
    _name = 'report.tokobaju.report_transaksi'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, transaksis):
        row = 2
        col = 0
        bold = workbook.add_format()
        bold.set_bold()
        bold.set_border()
        cs = workbook.add_format()
        cs.set_border()
        cs_int = workbook.add_format()
        cs_int.set_border()
        cs_int.set_align('vcenter')
        cs_nota = workbook.add_format()
        cs_nota.set_border()
        cs_nota.set_bold()
        cs_nota.set_font_color("blue")
        cs_nota.set_align('vcenter')
        cs_nota.set_align('center')
        cs_diskon = workbook.add_format()
        cs_diskon.set_border()
        cs_diskon.set_align('vcenter')
        cs_diskon.set_align('center')
        status_selesai = workbook.add_format()
        status_selesai.set_border()
        status_selesai.set_bg_color("#92d2a1")
        status_selesai.set_align('vcenter')
        status_selesai.set_align('center')
        status_refund = workbook.add_format()
        status_refund.set_border()
        status_refund.set_bg_color("#ffd57f")
        status_refund.set_align('vcenter')
        status_refund.set_align('center')
        status_cancel = workbook.add_format()
        status_cancel.set_border()
        status_cancel.set_bg_color("#ec99a1")
        status_cancel.set_align('vcenter')
        status_cancel.set_align('center')
        status_mk = workbook.add_format()
        status_mk.set_border()
        status_mk.set_bg_color("#8bd0db")
        status_mk.set_align('vcenter')
        status_mk.set_align('center')

        sheet = workbook.add_worksheet('Report Transaksi')
        sheet.merge_range(0, 0, 0, 5, "Report Transaksi", bold)
        sheet.write(1, 0, "Nota", bold)
        sheet.write(1, 1, "Diskon", bold)
        sheet.write(1, 2, "Produk Terjual", bold)
        sheet.write(1, 3, "Total Harga", bold)
        sheet.write(1, 4, "Total Bayar", bold)
        sheet.write(1, 5, "Status", bold)

        sheet.set_column('A:A', 18)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 35)
        sheet.set_column('D:D', 13)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 30)

        for report in transaksis:
            if len(report.transaksi_detail_ids) > 1:
                sheet.merge_range(
                    row, col, row+len(report.transaksi_detail_ids)-1, col, report.nota, cs_nota)
            else:
                sheet.write(row, col, report.nota, cs_nota)

            col += 1
            if len(report.transaksi_detail_ids) > 1:
                sheet.merge_range(
                    row, col, row+len(report.transaksi_detail_ids)-1, col, report.diskon, cs_diskon)
            else:
                sheet.write(row, col, report.diskon, cs_diskon)

            col += 1
            for x in report.transaksi_detail_ids:
                sheet.write(row, col, x.produk_id.produk, cs)
                row += 1
            col += 1
            row -= len(report.transaksi_detail_ids)
            if len(report.transaksi_detail_ids) > 1:
                sheet.merge_range(
                    row, col, row+len(report.transaksi_detail_ids)-1, col, report.total_harga, cs_int)
            else:
                sheet.write(row, col, report.total_harga, cs_int)

            col += 1
            if len(report.transaksi_detail_ids) > 1:
                sheet.merge_range(
                    row, col, row+len(report.transaksi_detail_ids)-1, col, report.total_bayar, cs_int)
            else:
                sheet.write(row, col, report.total_bayar, cs_int)

            col += 1
            if report.state == 'selesai':
                if len(report.transaksi_detail_ids) > 1:
                    sheet.merge_range(
                        row, col, row+len(report.transaksi_detail_ids)-1, col, report.state.upper(), status_selesai)
                else:
                    sheet.write(
                        row, col, report.state.upper(), status_selesai)
            elif report.state == 'menunggu_konfirmasi':
                if len(report.transaksi_detail_ids) > 1:
                    sheet.merge_range(
                        row, col, row+len(report.transaksi_detail_ids)-1, col, report.state.upper(), status_mk)
                else:
                    sheet.write(
                        row, col, report.state.upper(), status_mk)
            elif report.state == 'cancel':
                if len(report.transaksi_detail_ids) > 1:
                    sheet.merge_range(
                        row, col, row+len(report.transaksi_detail_ids)-1, col, report.state.upper(), status_cancel)
                else:
                    sheet.write(
                        row, col, report.state.upper(), status_cancel)
            elif report.state == 'refund':
                if len(report.transaksi_detail_ids) > 1:
                    sheet.merge_range(
                        row, col, row+len(report.transaksi_detail_ids)-1, col, report.state.upper(), status_refund)
                else:
                    sheet.write(
                        row, col, report.state.upper(), status_refund)
            col = 0
            row += len(report.transaksi_detail_ids)
