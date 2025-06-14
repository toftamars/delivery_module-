from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryCreateWizard(models.TransientModel):
    _name = 'delivery.create.wizard'
    _description = 'Teslimat Oluşturma Sihirbazı'

    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri', required=True)
    delivery_date = fields.Date('Teslimat Tarihi', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Araç')
    driver_id = fields.Many2one('res.partner', string='Sürücü', 
                               domain="[('is_driver', '=', True)]")
    planning_id = fields.Many2one('delivery.planning', string='Teslimat Planlaması')

    def action_create_deliveries(self):
        if not self.picking_ids:
            raise UserError(_('Lütfen en az bir transfer belgesi seçin!'))

        DeliveryDocument = self.env['delivery.document']
        created_deliveries = DeliveryDocument

        for picking in self.picking_ids:
            if picking.delivery_ids:
                continue

            delivery = DeliveryDocument.create({
                'picking_id': picking.id,
                'delivery_date': self.delivery_date,
                'vehicle_id': self.vehicle_id.id,
                'driver_id': self.driver_id.id,
                'planning_id': self.planning_id.id,
            })
            created_deliveries += delivery

        if not created_deliveries:
            raise UserError(_('Seçilen transfer belgeleri için teslimat oluşturulamadı!'))

        return {
            'name': _('Oluşturulan Teslimatlar'),
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', created_deliveries.ids)],
        } 