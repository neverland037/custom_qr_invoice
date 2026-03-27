from odoo import models, fields, api
import qrcode
import base64
import io

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_qr_code = fields.Binary(string="Código QR", compute="_compute_qr_code")
    x_serie = fields.Char(string="Serie", compute="_compute_invoice_parts")
    x_correlativo = fields.Char(string="Correlativo", compute="_compute_invoice_parts")
    x_emission_date = fields.Datetime(string="Fecha de Emisión", default=fields.Datetime.now)
    x_sale_channel_id = fields.Many2one('sale.channel', string="Canal de ventas")
    x_picking_ids = fields.Many2many('stock.picking', string="Transferencias", compute="_compute_pickings")
    x_total_qty = fields.Float(string="Total Cantidades", compute="_compute_total_qty")

    @api.depends('invoice_line_ids.quantity')
    def _compute_total_qty(self):
        for reg in self:
            reg.x_total_qty = sum(l.quantity for l in reg.invoice_line_ids)

    def _compute_qr_code(self):
        for reg in self:
            if reg.name and reg.partner_id:
                # Formato exacto Tarea 4 [cite: 80]
                qr_str = f"{reg.name}|{reg.partner_id.name}|{reg.invoice_date}|{reg.x_total_qty} {reg.amount_total}"
                qr = qrcode.QRCode(version=1, box_size=4, border=1)
                qr.add_data(qr_str)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                reg.x_qr_code = base64.b64encode(buffer.getvalue())
            else:
                reg.x_qr_code = False

    @api.depends('name')
    def _compute_invoice_parts(self):
        for reg in self:
            if reg.name and '/' in reg.name:
                parts = reg.name.split('/')
                reg.x_serie = parts[0] + parts[1]
                reg.x_correlativo = parts[2].zfill(8)
            else:
                reg.x_serie = reg.x_correlativo = ''

    def _compute_pickings(self):
        for reg in self:
            sale_order = self.env['sale.order'].search([('name', '=', reg.invoice_origin)], limit=1)
            reg.x_picking_ids = sale_order.picking_ids if sale_order else False