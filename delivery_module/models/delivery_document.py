from odoo import models, fields, api

class DeliveryDocument(models.Model):
    _name = 'delivery.document'
    _description = 'Teslimat Belgesi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Belge No', required=True, copy=False, readonly=True, default='Yeni')
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandı'),
        ('in_progress', 'Teslimatta'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    partner_id = fields.Many2one('res.partner', string='Müşteri', required=True, tracking=True)
    district_id = fields.Many2one('res.city.district', string='İlçe', related='partner_id.district_id', store=True)
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri', related='partner_id.delivery_day_ids', store=True)
    
    picking_id = fields.Many2one('stock.picking', string='Transfer Belgesi', required=True, tracking=True)
    driver_id = fields.Many2one('res.partner', string='Sürücü', domain="[('is_driver', '=', True)]", tracking=True)
    
    planned_date = fields.Date(string='Planlanan Tarih', tracking=True)
    delivery_date = fields.Date(string='Teslimat Tarihi', tracking=True)
    
    notes = fields.Text(string='Notlar')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni') == 'Yeni':
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.document') or 'Yeni'
        return super().create(vals_list)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_start_delivery(self):
        self.write({'state': 'in_progress'})
    
    def action_done(self):
        self.write({
            'state': 'done',
            'delivery_date': fields.Date.today()
        })
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_draft(self):
        self.write({'state': 'draft'}) 