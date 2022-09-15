from odoo import models
import base64
import io


class PemasukanReportXlsx(models.AbstractModel):
    _name = 'report.tokobaju.report_pemasukan'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'New Description'

    def generate_xlsx_report(self, workbook, data, pemasukans):
        row = 2
        col = 0
        bold = workbook.add_format({'bold': True})
        bold.set_border()
        co_warn = workbook.add_format()
        co_warn.set_bg_color("#ffd57f")
        co_warn.set_align('vcenter')
        co_warn.set_align('center')
        co_warn.set_border()
        co_success = workbook.add_format()
        co_success.set_bg_color("#92d2a1")
        co_success.set_align('vcenter')
        co_success.set_align('center')
        co_success.set_border()
        cs = workbook.add_format()
        cs.set_align('vcenter')
        cs.set_align('center')
        cs.set_border()
        cscode = workbook.add_format()
        cscode.set_align('vcenter')
        cscode.set_align('center')
        cscode.set_font_color('blue')
        cscode.set_bold()
        cscode.set_border()
        sb = workbook.add_format()
        sb.set_border()
        sheet = workbook.add_worksheet('Report Pemasukan')
        sheet.merge_range(0, 0, 0, 4, "Report Pemasukan", bold)
        sheet.write(1, 0, "Nota Pemasukan", bold)
        sheet.write(1, 1, "Supplier", bold)
        sheet.write(1, 2, "Daftar Pemasukan", bold)
        sheet.write(1, 3, "Total Harga", bold)
        sheet.write(1, 4, "Status", bold)

        sheet.set_column('A:A', 23)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 29)
        sheet.set_column('D:D', 18)
        sheet.set_column('E:E', 30)

        for report in pemasukans:
            n = report.daftar_pemasukan_lengkap
            n = n.replace("[", "")
            n = n.replace("]", "")
            n = n.replace("'", "")
            n = n.split(",")
            n = [x.strip() for x in n]

            if len(n) > 1:
                sheet.merge_range(row, col, row+len(n)-1,
                                  col, report.name, cscode)
            else:
                sheet.write(row, col, report.name, cscode)
            col += 1
            if len(n) > 1:
                sheet.merge_range(row, col, row+len(n)-1, col,
                                  report.supplier_id.name, cs)
            else:
                sheet.write(row, col, report.supplier_id.name, cs)
            col += 1
            for _ in n:
                sheet.write(row, col, _, sb)
                row += 1
            col += 1
            row -= len(n)
            if len(n) > 1:
                sheet.merge_range(row, col, row+len(n)-1,
                                  col, report.total_harga, cs)
            else:
                sheet.write(row, col, report.total_harga, cs)
            col += 1
            if len(n) > 1:
                if report.state == 'menunggu_konfirmasi':
                    sheet.merge_range(row, col, row+len(n)-1,
                                      col, report.state.upper(), co_warn)
                else:
                    sheet.merge_range(row, col, row+len(n)-1,
                                      col, report.state.upper(), co_success)
            else:
                if report.state == 'menunggu_konfirmasi':
                    sheet.write(row, col, report.state.upper(), co_warn)
                else:
                    sheet.write(row, col, report.state.upper(), co_success)

            col = 0
            row += len(n)
