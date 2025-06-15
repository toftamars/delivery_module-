from odoo import models, fields, api
from odoo.exceptions import UserError

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _order = 'date desc, id desc'

    name = fields.Char(string='Belge Numarası', required=True, copy=False, readonly=True, default='Yeni')
    date = fields.Date(string='Teslimat Tarihi', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string='Müşteri', required=True)
    district_id = fields.Many2one('res.city.district', string='İlçe', related='partner_id.district_id', store=True)
    delivery_day_ids = fields.Many2many(
        'delivery.day',
        'delivery_document_delivery_day_rel',
        'document_id',
        'day_id',
        string='Teslimat Günleri',
        related='partner_id.delivery_day_ids',
        store=True
    )
    picking_id = fields.Many2one('stock.picking', string='Transfer Belgesi', required=True)
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri')
    driver_id = fields.Many2one('res.partner', string='Sürücü', required=True, domain=[('is_driver', '=', True)])
    planning_id = fields.Many2one('delivery.planning', string='Teslimat Planlaması')
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('approved', 'Onaylandı'),
        ('in_delivery', 'Teslimatta'),
        ('completed', 'Tamamlandı'),
        ('canceled', 'İptal')
    ], string='Durum', default='draft', required=True)
    note = fields.Text(string='Notlar')
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni') == 'Yeni':
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.document') or 'Yeni'
        return super().create(vals_list)

    def action_approve(self):
        self.write({'state': 'approved'})
        self._send_sms_notification('approved')

    def action_start(self):
        self.write({'state': 'in_delivery'})
        self._send_sms_notification('in_delivery')

    def action_complete(self):
        self.write({'state': 'completed'})
        self._send_sms_notification('completed')

    def action_cancel(self):
        self.write({'state': 'canceled'})
        self._send_sms_notification('canceled')

    def action_draft(self):
        self.write({'state': 'draft'})

    def _send_sms_notification(self, state):
        if not self.partner_id.mobile:
            return

        message = self._get_sms_message(state)
        if message:
            try:
                self.env['sms.sms'].create({
                    'body': message,
                    'partner_id': self.partner_id.id,
                    'mobile': self.partner_id.mobile,
                }).send()
            except Exception as e:
                raise UserError(f'SMS gönderilemedi: {str(e)}')

    def _get_sms_message(self, state):
        messages = {
            'approved': f'Sayın {self.partner_id.name}, {self.date} tarihli {self.name} numaralı teslimatınız onaylanmıştır.',
            'in_delivery': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız yola çıkmıştır. Sürücü: {self.driver_id.name}',
            'completed': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız tamamlanmıştır.',
            'canceled': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız iptal edilmiştir.'
        }
        return messages.get(state) 