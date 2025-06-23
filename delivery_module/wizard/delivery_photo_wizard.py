from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)

# Geçici olarak devre dışı bırakıldı - tablo oluşturma sorunu nedeniyle
# class DeliveryPhotoWizard(models.TransientModel):
#     _name = 'delivery.photo.wizard'
#     _description = 'Teslimat Fotoğrafı Ekleme'
#     _transient_max_hours = 24  # 24 saat sonra otomatik temizle

#     delivery_id = fields.Many2one('delivery.document', string='Teslimat Belgesi', required=True)
#     photo_type = fields.Selection([
#         ('before', 'Kurulum Öncesi'),
#         ('during', 'Kurulum Sırasında'),
#         ('after', 'Kurulum Sonrası'),
#         ('problem', 'Sorun/Arıza'),
#         ('completion', 'Tamamlanma'),
#         ('other', 'Diğer')
#     ], string='Fotoğraf Tipi', required=True, default='completion')
    
#     image = fields.Binary('Fotoğraf', required=True)
#     image_filename = fields.Char('Dosya Adı')
#     description = fields.Text('Açıklama')
#     name = fields.Char('Fotoğraf Adı', required=True, default=lambda self: _('Teslimat Fotoğrafı'))

#     @api.model
#     def default_get(self, fields_list):
#         """Varsayılan değerleri ayarla"""
#         res = super().default_get(fields_list)
#         if self.env.context.get('active_id'):
#             delivery = self.env['delivery.document'].browse(self.env.context.get('active_id'))
#             res['delivery_id'] = delivery.id
#             res['name'] = f'{delivery.name} - {delivery.partner_id.name}'
#         return res

#     def action_add_photo(self):
#         """Fotoğrafı ekle"""
#         self.ensure_one()
        
#         # Teslimat durumunu kontrol et
#         if self.delivery_id.state not in ['ready', 'done']:
#             raise UserError(_('Sadece hazır veya tamamlanmış teslimat belgelerine fotoğraf eklenebilir.'))
        
#         # Dosya boyutu kontrolü
#         if self.image:
#             try:
#                 image_data = base64.b64decode(self.image)
#                 if len(image_data) > 5 * 1024 * 1024:  # 5MB
#                     raise UserError(_('Fotoğraf boyutu 5MB\'dan büyük olamaz.'))
#             except Exception as e:
#                 _logger.error(f"Fotoğraf boyutu kontrolü hatası: {e}")
#                 raise UserError(_('Fotoğraf yüklenirken hata oluştu.'))
        
#         # Fotoğrafı oluştur
#         photo_vals = {
#             'name': self.name,
#             'delivery_id': self.delivery_id.id,
#             'photo_type': self.photo_type,
#             'image': self.image,
#             'image_filename': self.image_filename,
#             'description': self.description,
#             'taken_by': self.env.user.id,
#         }
        
#         photo = self.env['delivery.photo'].create(photo_vals)
        
#         # Başarı mesajı
#         return {
#             'type': 'ir.actions.client',
#             'tag': 'display_notification',
#             'params': {
#                 'title': _('Başarılı'),
#                 'message': _('Fotoğraf başarıyla eklendi.'),
#                 'type': 'success',
#                 'sticky': False,
#             }
#         }

#     def action_add_multiple_photos(self):
#         """Çoklu fotoğraf ekleme"""
#         self.ensure_one()
        
#         # Bu metod gelecekte çoklu fotoğraf yükleme için kullanılabilir
#         return self.action_add_photo()

# Geçici placeholder model
class DeliveryPhotoWizard(models.TransientModel):
    _name = 'delivery.photo.wizard'
    _description = 'Teslimat Fotoğrafı Ekleme (Geçici Devre Dışı)'
    _transient_max_hours = 24

    def action_add_photo(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Bilgi'),
                'message': _('Fotoğraf özelliği geçici olarak devre dışı bırakılmıştır. Lütfen modülü yeniden yükleyin.'),
                'type': 'warning',
            }
        } 