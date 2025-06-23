from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Teslimat Numarası', required=True, copy=False, readonly=True, default='New')
    date = fields.Date('Teslimat Tarihi', required=True, default=fields.Date.context_today)
    vehicle_id = fields.Many2one('delivery.vehicle', string='Araç', required=True)
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

    def _compute_picking_count(self):
        for delivery in self:
            delivery.picking_count = len(delivery.picking_ids)

    def action_view_pickings(self):
        return {
            'name': 'Transferler',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.picking_ids.ids)],
        }

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
                return {
                    'warning': {
                        'title': 'Uyarı',
                        'message': f'{self.vehicle_id.name} aracının günlük limiti ({self.vehicle_id.daily_limit}) dolmuş. İlave teslimat için yetkilendirme gerekli.'
                    }
                }

    def action_approve(self):
        self.write({'state': 'ready'})
        self._send_sms_notification('ready')

    def action_complete(self):
        self.write({'state': 'done'})
        self._send_sms_notification('done')

    def action_cancel(self):
        self.write({'state': 'cancel'})
        self._send_sms_notification('cancel')

    def action_draft(self):
        self.write({'state': 'draft'})

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
            'cancel': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız iptal edildi.'
        }
        return messages.get(state) 