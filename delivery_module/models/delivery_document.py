from odoo import models, fields, api, _
from odoo.exceptions import UserError
import math
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Teslimat Numarası', required=True, copy=False, readonly=True, default='New')
    date = fields.Date('Teslimat Tarihi', required=True, default=fields.Date.context_today)
    vehicle_id = fields.Many2one('delivery.vehicle', string='Araç', required=True, ondelete='cascade')
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('ready', 'Hazır'),
        ('done', 'Teslim Edildi'),
        ('cancel', 'İptal')
    ], string='Durum', default='draft', tracking=True)
    
    # Yeni alanlar
    partner_id = fields.Many2one('res.partner', string='Müşteri', required=True)
    district_id = fields.Many2one('res.city.district', string='İlçe', required=True)
    delivery_address = fields.Char('Teslimat Adresi', related='partner_id.street', readonly=True)
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri')
    picking_count = fields.Integer(compute='_compute_picking_count', string='Transfer Sayısı')
    
    # Harita ve rota alanları
    start_latitude = fields.Float('Başlangıç Enlem', default=41.0082)  # İstanbul merkez
    start_longitude = fields.Float('Başlangıç Boylam', default=28.9784)
    end_latitude = fields.Float('Hedef Enlem', compute='_compute_end_coordinates', store=True)
    end_longitude = fields.Float('Hedef Boylam', compute='_compute_end_coordinates', store=True)
    route_distance = fields.Float('Rota Mesafesi (km)', compute='_compute_route_distance', store=True)
    route_duration = fields.Float('Tahmini Süre (dk)', compute='_compute_route_duration', store=True)
    show_map = fields.Boolean('Haritayı Göster', default=True)
    
    # Fotoğraf alanları
    delivery_photo_ids = fields.One2many('delivery.photo', 'delivery_id', string='Teslimat Fotoğrafları')
    delivery_photo_count = fields.Integer(compute='_compute_photo_count', string='Fotoğraf Sayısı')
    has_photos = fields.Boolean(compute='_compute_has_photos', string='Fotoğraf Var mı?')

    def _compute_picking_count(self):
        for delivery in self:
            delivery.picking_count = len(delivery.picking_ids)

    def _compute_end_coordinates(self):
        """Müşteri adresinden koordinatları hesaplar"""
        for delivery in self:
            if delivery.partner_id and delivery.partner_id.partner_latitude and delivery.partner_id.partner_longitude:
                delivery.end_latitude = delivery.partner_id.partner_latitude
                delivery.end_longitude = delivery.partner_id.partner_longitude
            else:
                # Varsayılan İstanbul koordinatları
                delivery.end_latitude = 41.0082
                delivery.end_longitude = 28.9784

    def _compute_route_distance(self):
        """Rota mesafesini hesaplar (Haversine formülü)"""
        for delivery in self:
            if delivery.start_latitude and delivery.start_longitude and delivery.end_latitude and delivery.end_longitude:
                # Haversine formülü ile mesafe hesaplama
                R = 6371  # Dünya yarıçapı (km)
                lat1, lon1 = math.radians(delivery.start_latitude), math.radians(delivery.start_longitude)
                lat2, lon2 = math.radians(delivery.end_latitude), math.radians(delivery.end_longitude)
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                
                delivery.route_distance = round(R * c, 2)
            else:
                delivery.route_distance = 0.0

    def _compute_route_duration(self):
        """Tahmini süreyi hesaplar (ortalama 30 km/saat)"""
        for delivery in self:
            if delivery.route_distance > 0:
                # Ortalama 30 km/saat hızla
                delivery.route_duration = round((delivery.route_distance / 30) * 60, 1)
            else:
                delivery.route_duration = 0.0

    def _compute_photo_count(self):
        """Fotoğraf sayısını hesaplar"""
        for delivery in self:
            delivery.delivery_photo_count = len(delivery.delivery_photo_ids)

    def _compute_has_photos(self):
        """Fotoğraf var mı kontrol eder"""
        for delivery in self:
            delivery.has_photos = len(delivery.delivery_photo_ids) > 0

    def refresh_route(self):
        """Rota yenileme butonu için metod"""
        route_data = self._get_osrm_route_data()
        if route_data:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Rota Güncellendi',
                    'message': f'Mesafe: {route_data["distance"]:.2f} km, Süre: {route_data["duration"]:.1f} dakika',
                    'type': 'success',
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Rota Hatası',
                    'message': 'Rota bilgileri alınamadı. Lütfen koordinatları kontrol edin.',
                    'type': 'warning',
                }
            }

    def _get_osrm_route_data(self):
        """OSRM API'den gerçek rota alır"""
        for delivery in self:
            if not (delivery.start_latitude and delivery.start_longitude and 
                   delivery.end_latitude and delivery.end_longitude):
                continue
                
            try:
                # OSRM API endpoint
                url = "http://router.project-osrm.org/route/v1/driving/{},{};{},{}".format(
                    delivery.start_longitude, delivery.start_latitude,
                    delivery.end_longitude, delivery.end_latitude
                )
                
                params = {
                    'overview': 'full',  # Tam rota geometrisi
                    'geometries': 'geojson',  # GeoJSON format
                    'steps': 'true'  # Adım adım talimatlar
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('code') == 'Ok' and data.get('routes'):
                    route = data['routes'][0]
                    
                    # Gerçek mesafe ve süre
                    real_distance = route.get('distance', 0) / 1000  # km'ye çevir
                    real_duration = route.get('duration', 0) / 60  # dakikaya çevir
                    
                    # Alanları güncelle
                    delivery.route_distance = round(real_distance, 2)
                    delivery.route_duration = round(real_duration, 1)
                    
                    # Rota koordinatlarını döndür
                    return {
                        'coordinates': route.get('geometry', {}).get('coordinates', []),
                        'distance': real_distance,
                        'duration': real_duration,
                        'steps': route.get('legs', [{}])[0].get('steps', [])
                    }
                    
            except Exception as e:
                _logger.error(f"OSRM API hatası: {e}")
                # Hata durumunda varsayılan hesaplama kullan
                continue
                
        return None

    def action_view_pickings(self):
        return {
            'name': _('Transfer Belgeleri'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.picking_ids.ids)],
            'context': {'default_partner_id': self.partner_id.id},
        }

    def action_view_photos(self):
        """Fotoğrafları görüntüle"""
        return {
            'name': _('Teslimat Fotoğrafları'),
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.photo',
            'view_mode': 'tree,form',
            'domain': [('delivery_id', '=', self.id)],
            'context': {'default_delivery_id': self.id},
        }

    def action_view_picking_count(self):
        """Transfer sayısına tıklandığında transferleri göster"""
        return self.action_view_pickings()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.document') or 'New'
        return super().create(vals_list)

    @api.onchange('vehicle_id', 'date')
    def _onchange_vehicle_date(self):
        if self.vehicle_id and self.date:
            # Aracın o günkü teslimat sayısını kontrol et
            today_count = self.env['delivery.document'].search_count([
                ('vehicle_id', '=', self.vehicle_id.id),
                ('date', '=', self.date),
                ('state', 'in', ['draft', 'ready']),
                ('id', '!=', self.id)
            ])
            
            if today_count >= self.vehicle_id.daily_limit:
                # Teslimat yöneticisi için sadece uyarı ver, engelleme
                if not self.env.user.has_group('delivery_module.group_delivery_manager'):
                    return {
                        'warning': {
                            'title': 'Uyarı',
                            'message': f'{self.vehicle_id.name} aracının günlük limiti ({self.vehicle_id.daily_limit}) dolmuş. İlave teslimat için yetkilendirme gerekli.'
                        }
                    }
                else:
                    return {
                        'warning': {
                            'title': 'Uyarı - Teslimat Yöneticisi',
                            'message': f'{self.vehicle_id.name} aracının günlük limiti ({self.vehicle_id.daily_limit}) dolmuş, ancak teslimat yöneticisi olarak ilave teslimat oluşturabilirsiniz.'
                        }
                    }

    def action_approve(self):
        self.write({'state': 'ready'})
        self._send_sms_notification('ready')

    def action_on_the_way(self):
        """Yolda butonu - Taslaktan Hazır durumuna geçer"""
        if self.state != 'draft':
            raise UserError(_('Sadece taslak durumundaki teslimatlar yola çıkabilir.'))
        
        self.write({'state': 'ready'})
        self._send_sms_notification('on_the_way')
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Başarılı'),
                'message': _('%s numaralı teslimat yola çıktı ve müşteriye SMS gönderildi.') % self.name,
                'type': 'success',
            }
        }

    def action_complete(self):
        self.write({'state': 'done'})
        self._send_sms_notification('done')

    def action_finish_delivery(self):
        """Tamamla butonu - Hazır durumundan Tamamlandı durumuna geçer"""
        if self.state != 'ready':
            raise UserError(_('Sadece hazır durumundaki teslimatlar tamamlanabilir.'))
        
        self.write({'state': 'done'})
        self._send_sms_notification('done')
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Başarılı'),
                'message': _('%s numaralı teslimat tamamlandı ve müşteriye SMS gönderildi.') % self.name,
                'type': 'success',
            }
        }

    def action_cancel(self):
        self.write({'state': 'cancel'})
        self._send_sms_notification('cancel')

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_open_in_maps(self):
        """Haritada Aç butonu - Google Maps'te teslimat adresini açar"""
        self.ensure_one()
        
        if not self.end_latitude or not self.end_longitude:
            raise UserError(_('Teslimat adresi için koordinat bilgisi bulunamadı.'))
        
        # Google Maps URL oluştur
        maps_url = f"https://www.google.com/maps?q={self.end_latitude},{self.end_longitude}"
        
        # Yeni sekmede aç
        return {
            'type': 'ir.actions.act_url',
            'url': maps_url,
            'target': 'new',
        }

    def _send_sms_notification(self, state):
        if not self.partner_id.mobile:
            return
        
        message = self._get_sms_message(state)
        if message:
            self.env['sms.api']._send_sms(
                self.partner_id.mobile,
                message
            )

    def _get_sms_message(self, state):
        messages = {
            'ready': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız hazırlandı.',
            'done': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız tamamlandı.',
            'cancel': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız iptal edildi.',
            'on_the_way': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız yola çıktı.'
        }
        return messages.get(state) 