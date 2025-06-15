from odoo import models, fields, api

class ResCityDistrict(models.Model):
    _name = 'res.city.district'
    _description = 'İlçe'

    name = fields.Char(string='İlçe Adı', required=True)
    city_id = fields.Many2one('res.city', string='İl', required=True)
    delivery_day_ids = fields.Many2many(
        'delivery.day',
        'res_city_district_delivery_day_rel',
        'district_id',
        'day_id',
        string='Teslimat Günleri'
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company) 