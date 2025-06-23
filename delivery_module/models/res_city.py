from odoo import models, fields

class ResCity(models.Model):
    _name = 'res.city'
    _description = 'İl'
    _order = 'name'

    name = fields.Char('İl Adı', required=True)
    state_id = fields.Many2one('res.country.state', string='Eyalet/İl')
    country_id = fields.Many2one('res.country', string='Ülke', related='state_id.country_id', readonly=True)
    active = fields.Boolean('Aktif', default=True) 