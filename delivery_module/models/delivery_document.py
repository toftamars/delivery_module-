from odoo import models, fields, api, _
from odoo.exceptions import UserError
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
    delivery_address = fields.Char('Teslimat Adresi', compute='_compute_delivery_address', store=True)
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri')
    picking_count = fields.Integer(compute='_compute_picking_count', string='Transfer Sayısı')
    
    # Fotoğraf alanları
    delivery_photo_ids = fields.One2many('delivery.photo', 'delivery_id', string='Teslimat Fotoğrafları')
    delivery_photo_count = fields.Integer(compute='_compute_photo_count', string='Fotoğraf Sayısı')
    has_photos = fields.Boolean(compute='_compute_has_photos', string='Fotoğraf Var mı?')

    def _compute_picking_count(self):
        for delivery in self:
            delivery.picking_count = len(delivery.picking_ids)

    def _compute_photo_count(self):
        """Fotoğraf sayısını hesaplar"""
        for delivery in self:
            delivery.delivery_photo_count = len(delivery.delivery_photo_ids)

    def _compute_has_photos(self):
        """Fotoğraf var mı kontrol eder"""
        for delivery in self:
            delivery.has_photos = len(delivery.delivery_photo_ids) > 0

    def _compute_delivery_address(self):
        """Teslimat adresini güvenli şekilde hesaplar"""
        for delivery in self:
            if delivery.partner_id and delivery.partner_id.street:
                delivery.delivery_address = delivery.partner_id.street
            else:
                delivery.delivery_address = False

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
        # self._send_sms_notification('on_the_way')  # SMS pasif
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Başarılı'),
                'message': _('%s numaralı teslimat yola çıktı.') % self.name,  # SMS mesajı kaldırıldı
                'type': 'success',
            }
        }

    def action_complete(self):
        self.write({'state': 'done'})
        # self._send_sms_notification('done')  # SMS pasif

    def action_finish_delivery(self):
        """Tamamla butonu - Hazır durumundan Tamamlandı durumuna geçer"""
        if self.state != 'ready':
            raise UserError(_('Sadece hazır durumundaki teslimatlar tamamlanabilir.'))
        
        self.write({'state': 'done'})
        # self._send_sms_notification('done')  # SMS pasif
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Başarılı'),
                'message': _('%s numaralı teslimat tamamlandı.') % self.name,  # SMS mesajı kaldırıldı
                'type': 'success',
            }
        }

    def action_cancel(self):
        self.write({'state': 'cancel'})
        # self._send_sms_notification('cancel')  # SMS pasif

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_open_in_maps(self):
        """Haritada Aç butonu - Google Maps'te teslimat adresini açar"""
        self.ensure_one()
        
        if not self.delivery_address:
            raise UserError(_('Teslimat adresi bulunamadı.'))
        
        # Google Maps URL oluştur - adres ile
        maps_url = f"https://www.google.com/maps?q={self.delivery_address}"
        
        # Yeni sekmede aç
        return {
            'type': 'ir.actions.act_url',
            'url': maps_url,
            'target': 'new',
        }

    # def _send_sms_notification(self, state):
    #     """SMS gönderme - şimdilik pasif"""
    #     if not self.partner_id.mobile:
    #         return
    #     
    #     message = self._get_sms_message(state)
    #     if message:
    #         self.env['sms.api']._send_sms(
    #             self.partner_id.mobile,
    #             message
    #         )

    # def _get_sms_message(self, state):
    #     """SMS mesajları - şimdilik pasif"""
    #     messages = {
    #         'ready': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız hazırlandı.',
    #         'done': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız tamamlandı.',
    #         'cancel': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız iptal edildi.',
    #         'on_the_way': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız yola çıktı.'
    #     }
    #     return messages.get(state) 