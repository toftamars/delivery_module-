from odoo import models, fields, api

class DeliveryPlanning(models.Model):
    _name = 'delivery.planning'
    _description = 'Teslimat Planlaması'
    _order = 'date desc, id desc'

    name = fields.Char(string='Planlama Numarası', required=True, copy=False, readonly=True, default='Yeni')
    date = fields.Date(string='Planlama Tarihi', required=True, default=fields.Date.context_today)
    driver_id = fields.Many2one('res.partner', string='Sürücü', required=True, domain=[('is_driver', '=', True)])
    vehicle_id = fields.Many2one('fleet.vehicle', string='Araç', required=True)
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandı'),
        ('in_progress', 'Teslimatta'),
        ('done', 'Tamamlandı'),
        ('cancel', 'İptal')
    ], string='Durum', default='draft', required=True)
    delivery_ids = fields.One2many('delivery.document', 'planning_id', string='Teslimat Belgeleri')
    note = fields.Text(string='Notlar')
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni') == 'Yeni':
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.planning') or 'Yeni'
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'}) 