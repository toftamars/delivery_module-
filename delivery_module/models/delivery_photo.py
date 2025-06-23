from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)

class DeliveryPhoto(models.Model):
    _name = 'delivery.photo'
    _description = 'Teslimat Fotoğrafı'
    _order = 'create_date desc'

    name = fields.Char('Fotoğraf Adı', required=True)
    delivery_id = fields.Many2one('delivery.document', string='Teslimat Belgesi', required=True, ondelete='cascade')
    photo_type = fields.Selection([
        ('before', 'Kurulum Öncesi'),
        ('during', 'Kurulum Sırasında'),
        ('after', 'Kurulum Sonrası'),
        ('problem', 'Sorun/Arıza'),
        ('completion', 'Tamamlanma'),
        ('other', 'Diğer')
    ], string='Fotoğraf Tipi', required=True, default='completion')
    
    image = fields.Binary('Fotoğraf', attachment=True, required=True)
    image_filename = fields.Char('Dosya Adı')
    description = fields.Text('Açıklama')
    taken_by = fields.Many2one('res.users', string='Çeken Kişi', default=lambda self: self.env.user)
    taken_date = fields.Datetime('Çekim Tarihi', default=fields.Datetime.now)
    
    # Meta veriler
    file_size = fields.Integer('Dosya Boyutu (KB)', compute='_compute_file_size')
    image_width = fields.Integer('Genişlik (px)')
    image_height = fields.Integer('Yükseklik (px)')
    
    @api.depends('image')
    def _compute_file_size(self):
        """Dosya boyutunu hesaplar"""
        for photo in self:
            if photo.image:
                # Base64'ten byte sayısını hesapla
                try:
                    image_data = base64.b64decode(photo.image)
                    photo.file_size = len(image_data) // 1024  # KB'ye çevir
                except Exception as e:
                    _logger.error(f"Fotoğraf boyutu hesaplanamadı: {e}")
                    photo.file_size = 0
            else:
                photo.file_size = 0

    @api.model
    def create(self, vals):
        """Fotoğraf oluşturulurken ek kontroller"""
        # Teslimat belgesinin durumunu kontrol et
        if vals.get('delivery_id'):
            delivery = self.env['delivery.document'].browse(vals['delivery_id'])
            if delivery.state not in ['ready', 'done']:
                raise UserError(_('Sadece hazır veya tamamlanmış teslimat belgelerine fotoğraf eklenebilir.'))
        
        # Dosya boyutu kontrolü (5MB limit)
        if vals.get('image'):
            try:
                image_data = base64.b64decode(vals['image'])
                if len(image_data) > 5 * 1024 * 1024:  # 5MB
                    raise UserError(_('Fotoğraf boyutu 5MB\'dan büyük olamaz.'))
            except Exception as e:
                _logger.error(f"Fotoğraf boyutu kontrolü hatası: {e}")
        
        return super().create(vals)

    def action_view_delivery(self):
        """Teslimat belgesini görüntüle"""
        return {
            'name': _('Teslimat Belgesi'),
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'view_mode': 'form',
            'res_id': self.delivery_id.id,
            'target': 'current',
        }

    def action_download_photo(self):
        """Fotoğrafı indir"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/image/{self.image_filename}?download=true',
            'target': 'self',
        } 