from odoo import models, fields, api

class ResCity(models.Model):
    _name = 'res.city'
    _description = 'İl'

    name = fields.Char(string='İl Adı', required=True)
    code = fields.Char(string='İl Kodu')
    district_ids = fields.One2many('res.city.district', 'city_id', string='İlçeler')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company) 