from odoo import models, fields, api

class ResCityDistrict(models.Model):
    _name = 'res.city.district'
    _description = 'İlçe'

    name = fields.Char('İlçe Adı', required=True)
    city_id = fields.Many2one('res.city', string='Şehir', required=True, ondelete='cascade')
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri')
    active = fields.Boolean('Aktif', default=True)

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günü'

    name = fields.Char('Gün Adı', required=True)
    code = fields.Selection([
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
        ('sunday', 'Pazar')
    ], string='Gün Kodu', required=True)
    active = fields.Boolean('Aktif', default=True) 