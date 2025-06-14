from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_driver = fields.Boolean(string='Sürücü mü?')
    district_id = fields.Many2one('res.city.district', string='İlçe')
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri') 