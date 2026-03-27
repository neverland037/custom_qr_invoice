from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_qr_code = fields.Binary(string="Código QR", compute="_compute_qr_code")
    x_serie = fields.Char(string="Serie", compute="_compute_invoice_parts")
    x_correlativo = fields.Char(string="Correlativo", compute="_compute_invoice_parts")
    x_emission_date = fields.Datetime(string="Fecha de Emisión", default=fields.Datetime.now)
    x_sale_channel_id = fields.Many2one('sale.channel', string="Canal de ventas")
    x_picking_ids = fields.Many2many('stock.picking', string="Transferencias", compute="_compute_pickings")

    def _compute_qr_code(self):
        for reg in self:
            if reg.name:
                # FIX: Método correcto para Odoo 17
                reg.x_qr_code = self.env['ir.actions.report']._render_qrcode(reg.name)
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