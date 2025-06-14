from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    # Teslimat belgesi bağlantısı
    delivery_document_ids = fields.One2many('delivery.document', 'picking_id', 
                                          string='Teslimat Belgeleri')
    delivery_document_count = fields.Integer('Teslimat Sayısı', 
                                           compute='_compute_delivery_document_count')
    
    # Teslimat için hazır mı?
    ready_for_delivery = fields.Boolean('Teslimat İçin Hazır', 
                                       compute='_compute_ready_for_delivery')
    
    @api.depends('delivery_document_ids')
    def _compute_delivery_document_count(self):
        for record in self:
            record.delivery_document_count = len(record.delivery_document_ids)
    
    @api.depends('state', 'picking_type_id')
    def _compute_ready_for_delivery(self):
        """Transfer belgesi teslimat için hazır mı kontrol et"""
        for record in self:
            # Sadece çıkış transferleri ve durumu 'Hazır' olanlar
            record.ready_for_delivery = (
                record.state == 'assigned' and 
                record.picking_type_id.code == 'outgoing'
            )
    
    def action_create_delivery(self):
        """Teslimat belgesi oluştur"""
        if not self.ready_for_delivery:
            raise UserError(_('Bu transfer belgesi teslimat için hazır değil!'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Belgesi Oluştur',
            'res_model': 'delivery.create.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.id}
        }
    
    def action_view_deliveries(self):
        """Teslimat belgelerini görüntüle"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Belgeleri',
            'res_model': 'delivery.document',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id}
        } 