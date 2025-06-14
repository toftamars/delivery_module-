from odoo import models, fields, api

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günleri'
    _order = 'sequence, name'

    name = fields.Char(string='Gün', required=True)
    region = fields.Selection([
        ('anadolu', 'Anadolu'),
        ('avrupa', 'Avrupa')
    ], string='Bölge', required=True)
    districts = fields.Text(string='İlçeler', required=True)
    sequence = fields.Integer(string='Sıra', default=10)
    active = fields.Boolean(default=True) 