from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('Belge No', required=True, copy=False, 
                      readonly=True, default=lambda self: _('Yeni'))
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandı'),
        ('in_progress', 'Teslimatta'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    picking_id = fields.Many2one('stock.picking', string='Transfer Belgesi', 
                                required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Müşteri', 
                                related='picking_id.partner_id', store=True)
    delivery_date = fields.Date('Teslimat Tarihi', required=True, tracking=True)
    delivery_time = fields.Float('Teslimat Saati', tracking=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Araç', tracking=True)
    driver_id = fields.Many2one('res.partner', string='Sürücü', 
                               domain="[('is_driver', '=', True)]", tracking=True)
    planning_id = fields.Many2one('delivery.planning', string='Teslimat Planlaması')
    
    notes = fields.Text('Notlar')
    route_map = fields.Char('Rota Haritası')
    sms_sent = fields.Boolean('SMS Gönderildi', default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Yeni')) == _('Yeni'):
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.document') or _('Yeni')
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start_delivery(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_send_sms(self):
        if not self.partner_id.mobile:
            raise UserError(_('Müşterinin telefon numarası bulunamadı!'))
        
        # SMS gönderme işlemi burada yapılacak
        self.sms_sent = True 