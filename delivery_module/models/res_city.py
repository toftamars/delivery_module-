from odoo import models, fields, api

class ResCity(models.Model):
    _name = 'res.city'
    _description = 'Şehir'

    name = fields.Char('Şehir Adı', required=True)
    district_ids = fields.One2many('res.city.district', 'city_id', string='İlçeler')
    active = fields.Boolean('Aktif', default=True) 