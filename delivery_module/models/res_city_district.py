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
    
    # Teslimat günleri ilişkisi
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri')
    delivery_day_count = fields.Integer('Teslimat Günü Sayısı', compute='_compute_delivery_day_count')

    def _compute_delivery_day_count(self):
        for district in self:
            district.delivery_day_count = len(district.delivery_day_ids)

    def action_view_delivery_days(self):
        return {
            'name': f'{self.name} - Teslimat Günleri',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.day',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.delivery_day_ids.ids)],
            'context': {'default_district_ids': [(4, self.id)]},
        } 