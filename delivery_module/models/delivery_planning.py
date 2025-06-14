from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryPlanning(models.Model):
    _name = 'delivery.planning'
    _description = 'Teslimat Planlaması'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Planlama Adı', required=True, tracking=True)
    date = fields.Date('Planlama Tarihi', required=True, tracking=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Araç', required=True, tracking=True)
    driver_id = fields.Many2one('res.partner', string='Sürücü', 
                               domain="[('is_driver', '=', True)]", required=True, tracking=True)
    
    delivery_ids = fields.One2many('delivery.document', 'planning_id', string='Teslimatlar')
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandı'),
        ('in_progress', 'Devam Ediyor'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    notes = fields.Text('Notlar')
    route_map = fields.Char('Rota Haritası')
    active = fields.Boolean('Aktif', default=True)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'}) 