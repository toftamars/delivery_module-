from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryCreateWizard(models.TransientModel):
    _name = 'delivery.create.wizard'
    _description = 'Teslimat Belgesi Oluşturma Sihirbazı'
    
    picking_id = fields.Many2one('stock.picking', string='Transfer Belgesi', required=True)
    delivery_date = fields.Date('Teslimat Tarihi', required=True)
    vehicle_type = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası'),
        ('small_1', 'Küçük Araç 1'),
        ('small_2', 'Küçük Araç 2'),
        ('extra', 'Ek Araç')
    ], string='Araç Tipi', required=True)
    notes = fields.Text('Notlar')
    
    def action_create_delivery(self):
        """Teslimat belgesi oluştur"""
        delivery_vals = {
            'picking_id': self.picking_id.id,
            'delivery_date': self.delivery_date,
            'vehicle_type': self.vehicle_type,
            'notes': self.notes,
        }
        
        delivery = self.env['delivery.document'].create(delivery_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Belgesi',
            'res_model': 'delivery.document',
            'res_id': delivery.id,
            'view_mode': 'form',
            'target': 'current'
        } 