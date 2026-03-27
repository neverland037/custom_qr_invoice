from odoo import models, fields

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Canal de Ventas'
    name = fields.Char(string="Nombre", required=True)