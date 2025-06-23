from odoo import models, fields

class ResCityDistrict(models.Model):
    _name = 'res.city.district'
    _description = 'İlçe'
    _order = 'name'

    name = fields.Char('İlçe Adı', required=True)
    city_id = fields.Many2one('res.city', string='İl', required=True)
    state_id = fields.Many2one('res.country.state', string='Eyalet/İl', related='city_id.state_id', readonly=True)
    country_id = fields.Many2one('res.country', string='Ülke', related='city_id.country_id', readonly=True)
    active = fields.Boolean('Aktif', default=True) 