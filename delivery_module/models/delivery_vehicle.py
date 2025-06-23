from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryVehicle(models.Model):
    _name = 'delivery.vehicle'
    _description = 'Teslimat Aracı'
    _order = 'name'

    name = fields.Char('Araç Adı', required=True)
    vehicle_type = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası'),
        ('kucuk_arac_1', 'Küçük Araç 1'),
        ('kucuk_arac_2', 'Küçük Araç 2'),
        ('ek_arac', 'Ek Araç'),
    ], string='Araç Tipi', required=True)
    
    daily_limit = fields.Integer('Günlük Teslimat Limiti', default=7, required=True)
    active = fields.Boolean('Aktif', default=True)
    
    # Bugünkü teslimat sayısını hesapla
    today_delivery_count = fields.Integer('Bugünkü Teslimat Sayısı', compute='_compute_today_delivery_count')
    remaining_capacity = fields.Integer('Kalan Kapasite', compute='_compute_remaining_capacity')

    @api.depends('daily_limit')
    def _compute_today_delivery_count(self):
        for vehicle in self:
            today = fields.Date.today()
            count = self.env['delivery.document'].search_count([
                ('vehicle_id', '=', vehicle.id),
                ('date', '=', today),
                ('state', 'in', ['draft', 'ready'])
            ])
            vehicle.today_delivery_count = count

    @api.depends('daily_limit', 'today_delivery_count')
    def _compute_remaining_capacity(self):
        for vehicle in self:
            vehicle.remaining_capacity = vehicle.daily_limit - vehicle.today_delivery_count

    def action_view_today_deliveries(self):
        today = fields.Date.today()
        return {
            'name': f'{self.name} - Bugünkü Teslimatlar',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'view_mode': 'tree,form',
            'domain': [
                ('vehicle_id', '=', self.id),
                ('date', '=', today),
                ('state', 'in', ['draft', 'ready'])
            ],
            'context': {'default_vehicle_id': self.id, 'default_date': today},
        } 