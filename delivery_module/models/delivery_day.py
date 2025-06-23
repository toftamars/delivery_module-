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
    
    # İlçe ilişkisi
    district_ids = fields.Many2many('res.city.district', string='Teslimat Yapılan İlçeler')
    district_count = fields.Integer('İlçe Sayısı', compute='_compute_district_count')

    def _compute_district_count(self):
        for day in self:
            day.district_count = len(day.district_ids)

    def action_view_districts(self):
        return {
            'name': f'{self.name} - Teslimat İlçeleri',
            'type': 'ir.actions.act_window',
            'res_model': 'res.city.district',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.district_ids.ids)],
            'context': {'default_delivery_day_ids': [(4, self.id)]},
        } 