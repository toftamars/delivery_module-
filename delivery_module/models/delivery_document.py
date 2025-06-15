from odoo import models, fields, api

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

    def action_start(self):
        self.write({'state': 'in_delivery'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'canceled'})

    def action_draft(self):
        self.write({'state': 'draft'}) 