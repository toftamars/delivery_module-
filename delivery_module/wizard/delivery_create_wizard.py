from odoo import models, fields, api

class DeliveryCreateWizard(models.TransientModel):
    _name = 'delivery.create.wizard'
    _description = 'Teslimat Oluşturma Sihirbazı'

    date = fields.Date(string='Teslimat Tarihi', required=True, default=fields.Date.context_today)
    driver_id = fields.Many2one('res.partner', string='Sürücü', required=True, domain=[('is_driver', '=', True)])
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri', required=True,
        domain=[('is_delivery_created', '=', False), ('state', '=', 'done')])

    def action_create_delivery(self):
        self.ensure_one()
        delivery = self.env['delivery.document'].create({
            'name': self.env['ir.sequence'].next_by_code('delivery.document') or 'Yeni',
            'date': self.date,
            'driver_id': self.driver_id.id,
            'picking_ids': [(6, 0, self.picking_ids.ids)],
            'state': 'draft',
        })
        self.picking_ids.write({
            'delivery_id': delivery.id,
            'is_delivery_created': True
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'views': [[False, 'form']],
            'res_id': delivery.id,
        } 