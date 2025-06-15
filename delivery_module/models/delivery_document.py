from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Teslimat Numarası', required=True, copy=False, readonly=True, default='New')
    date = fields.Date('Teslimat Tarihi', required=True, default=fields.Date.context_today)
    driver_id = fields.Many2one('res.partner', string='Sürücü', domain=[('is_driver', '=', True)])
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('approved', 'Onaylandı'),
        ('in_delivery', 'Teslimatta'),
        ('done', 'Tamamlandı'),
        ('cancel', 'İptal Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    # Yeni alanlar
    partner_id = fields.Many2one('res.partner', string='Müşteri', required=True)
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri')
    delivery_count = fields.Integer(compute='_compute_delivery_count', string='Transfer Sayısı')

    def _compute_delivery_count(self):
        for delivery in self:
            delivery.delivery_count = len(delivery.picking_ids)

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

    def action_approve(self):
        self.write({'state': 'approved'})
        self._send_sms_notification('approved')

    def action_start(self):
        self.write({'state': 'in_delivery'})
        self._send_sms_notification('in_delivery')

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
            'approved': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız onaylandı.',
            'in_delivery': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız yola çıktı.',
            'done': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız tamamlandı.',
            'cancel': f'Sayın {self.partner_id.name}, {self.name} numaralı teslimatınız iptal edildi.'
        }
        return messages.get(state) 