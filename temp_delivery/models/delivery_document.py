from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char('Teslimat No', required=True, copy=False, default=lambda self: _('Yeni'))
    
    # Durum bilgileri
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('ready', 'Hazır'),
        ('on_route', 'Yolda'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal')
    ], string='Durum', default='draft', tracking=True)
    
    # Transfer belgesi bağlantısı
    picking_id = fields.Many2one('stock.picking', string='Transfer Belgesi', required=True, readonly=True)
    
    # Tarih ve araç bilgileri
    delivery_date = fields.Date('Teslimat Tarihi', required=True, 
                               states={'draft': [('readonly', False)]}, readonly=True)
    vehicle_type = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası'),
        ('small_1', 'Küçük Araç 1'),
        ('small_2', 'Küçük Araç 2'),
        ('extra', 'Ek Araç')
    ], string='Araç Tipi', required=True, 
       states={'draft': [('readonly', False)]}, readonly=True)
    
    # Müşteri bilgileri
    partner_id = fields.Many2one('res.partner', string='Müşteri', 
                                related='picking_id.partner_id', readonly=True)
    partner_phone = fields.Char(string='Telefon', related='partner_id.phone', readonly=True)
    
    # Adres bilgileri
    delivery_address = fields.Text('Teslimat Adresi', related='picking_id.partner_id.street', readonly=True)
    district = fields.Char('İlçe', compute='_compute_district', store=True)
    
    # Rota bilgileri
    route_info = fields.Text('Rota Bilgisi')
    map_url = fields.Char('Harita URL')
    
    # SMS durumu
    sms_sent_on_route = fields.Boolean('Yolda SMS Gönderildi', default=False, readonly=True)
    sms_sent_delivered = fields.Boolean('Teslim SMS Gönderildi', default=False, readonly=True)
    
    # Notlar
    notes = fields.Text('Notlar')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('Yeni')) == _('Yeni'):
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.document') or _('Yeni')
        return super(DeliveryDocument, self).create(vals)
    
    @api.depends('partner_id')
    def _compute_district(self):
        for record in self:
            if record.partner_id and record.partner_id.city:
                record.district = record.partner_id.city
            else:
                record.district = False
    
    @api.constrains('delivery_date', 'district')
    def _check_delivery_date_district(self):
        """İlçe ve gün uyumluluğunu kontrol et"""
        for record in self:
            if record.delivery_date and record.district:
                if not self._is_valid_delivery_day(record.district, record.delivery_date):
                    # Yönetici kontrolü
                    if not self._is_manager():
                        raise ValidationError(_('Seçilen ilçe (%s) için %s günü teslimat yapılamaz!') % 
                                            (record.district, record.delivery_date.strftime('%A')))
    
    @api.constrains('delivery_date', 'vehicle_type')
    def _check_daily_delivery_limit(self):
        """Günlük teslimat limitini kontrol et"""
        for record in self:
            if record.delivery_date and record.vehicle_type:
                if not self._is_manager():
                    count = self.search_count([
                        ('delivery_date', '=', record.delivery_date),
                        ('vehicle_type', '=', record.vehicle_type),
                        ('state', 'in', ['ready', 'on_route', 'delivered']),
                        ('id', '!=', record.id)
                    ])
                    if count >= 7:
                        raise ValidationError(_('Seçilen araç tipi için günlük maksimum 7 teslimat sınırına ulaşıldı!'))
    
    @api.constrains('delivery_date')
    def _check_sunday_delivery(self):
        """Pazar günü teslimat kontrolü"""
        for record in self:
            if record.delivery_date and record.delivery_date.weekday() == 6:  # Pazar = 6
                raise ValidationError(_('Pazar günleri teslimat yapılamaz!'))
    
    def _is_valid_delivery_day(self, district, date):
        """İlçe ve gün uyumluluğunu kontrol et"""
        weekday = date.weekday()  # 0=Pazartesi, 6=Pazar
        
        # Anadolu Yakası İlçeleri
        anadolu_districts = {
            0: ['Maltepe', 'Kartal', 'Pendik', 'Tuzla'],  # Pazartesi
            1: ['Üsküdar', 'Kadıköy', 'Ataşehir', 'Ümraniye'],  # Salı
            2: ['Üsküdar', 'Kadıköy', 'Ataşehir', 'Ümraniye'],  # Çarşamba
            3: ['Üsküdar', 'Kadıköy', 'Ataşehir', 'Ümraniye'],  # Perşembe
            4: ['Maltepe', 'Kartal', 'Pendik', 'Sultanbeyli'],  # Cuma
            5: ['Sancaktepe', 'Çekmeköy', 'Beykoz', 'Şile'],  # Cumartesi
        }
        
        # Avrupa Yakası İlçeleri
        avrupa_districts = {
            0: ['Beyoğlu', 'Şişli', 'Beşiktaş', 'Kağıthane'],  # Pazartesi
            1: ['Sarıyer', 'Bakırköy', 'Bahçelievler', 'Güngören', 'Esenler', 'Bağcılar'],  # Salı
            2: ['Beyoğlu', 'Şişli', 'Beşiktaş', 'Kağıthane'],  # Çarşamba
            3: ['Eyüpsultan', 'Gaziosmanpaşa', 'Küçükçekmece', 'Avcılar', 'Başakşehir', 'Sultangazi', 'Arnavutköy'],  # Perşembe
            4: ['Fatih', 'Zeytinburnu', 'Bayrampaşa'],  # Cuma
            5: ['Esenyurt', 'Beylikdüzü', 'Silivri', 'Çatalca'],  # Cumartesi
        }
        
        # Pazar günü (6) kontrol
        if weekday == 6:
            return False
        
        # İlçe kontrolü
        all_districts = anadolu_districts.get(weekday, []) + avrupa_districts.get(weekday, [])
        return district in all_districts
    
    def _is_manager(self):
        """Kullanıcının yönetici yetkisi var mı kontrol et"""
        return self.env.user.has_group('delivery_module.group_delivery_manager')
    
    def action_confirm(self):
        """Onayla - Hazır durumuna geçir"""
        for record in self:
            if not record.delivery_date:
                raise UserError(_('Teslimat tarihi seçilmelidir!'))
            if not record.vehicle_type:
                raise UserError(_('Araç tipi seçilmelidir!'))
            record.state = 'ready'
    
    def action_on_route(self):
        """Yolda - SMS gönder"""
        for record in self:
            record.state = 'on_route'
            record._send_sms_on_route()
    
    def action_delivered(self):
        """Teslim Edildi - SMS gönder"""
        for record in self:
            record.state = 'delivered'
            record._send_sms_delivered()
    
    def action_cancel(self):
        """İptal Et"""
        for record in self:
            record.state = 'cancelled'
    
    def _send_sms_on_route(self):
        """Yolda SMS gönder"""
        if self.partner_phone and not self.sms_sent_on_route:
            message = f"Merhaba {self.partner_id.name}, {self.name} numaralı teslimatınız yola çıktı. Teşekkürler."
            self._send_sms(message)
            self.sms_sent_on_route = True
    
    def _send_sms_delivered(self):
        """Teslim Edildi SMS gönder"""
        if self.partner_phone and not self.sms_sent_delivered:
            message = f"Merhaba {self.partner_id.name}, {self.name} numaralı teslimatınız tamamlandı. Teşekkürler."
            self._send_sms(message)
            self.sms_sent_delivered = True
    
    def _send_sms(self, message):
        """SMS gönder"""
        try:
            sms_api = self.env['sms.api']
            sms_api.send_sms(self.partner_phone, message)
        except Exception as e:
            # SMS gönderim hatası log'a yazılır
            self.env['ir.logging'].create({
                'name': 'SMS Gönderim Hatası',
                'type': 'server',
                'message': str(e),
                'level': 'ERROR'
            })
    
    def action_view_picking(self):
        """Transfer belgesini görüntüle"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Belgesi',
            'res_model': 'stock.picking',
            'res_id': self.picking_id.id,
            'view_mode': 'form',
            'target': 'current',
        } 