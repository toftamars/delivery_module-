from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_driver = fields.Boolean('Sürücü mü?')
    district_id = fields.Many2one('res.city.district', string='İlçe')
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri')
    delivery_day = fields.Selection([
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
        ('sunday', 'Pazar')
    ], string='Teslimat Günü') 