from odoo import models, fields, api

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günleri'

    name = fields.Char(string='Gün', required=True)
    districts = fields.Text(string='İlçeler', required=True)
    region = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası')
    ], string='Bölge', required=True)
    sequence = fields.Integer(string='Sıra', default=10)
    active = fields.Boolean(default=True)

    _order = 'sequence, name' 