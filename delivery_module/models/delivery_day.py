from odoo import models, fields

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günü'
    _order = 'sequence, id'

    name = fields.Char('Gün Adı', required=True)
    day_of_week = fields.Selection([
        ('0', 'Pazartesi'),
        ('1', 'Salı'),
        ('2', 'Çarşamba'),
        ('3', 'Perşembe'),
        ('4', 'Cuma'),
        ('5', 'Cumartesi'),
        ('6', 'Pazar'),
    ], string='Haftanın Günü', required=True)
    sequence = fields.Integer('Sıra', default=10)
    active = fields.Boolean('Aktif', default=True) 