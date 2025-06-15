from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_document_ids = fields.One2many('delivery.document', 'picking_id', string='Teslimat Belgeleri')
    delivery_date = fields.Date(string='Teslimat Tarihi')
    driver_id = fields.Many2one('res.partner', string='Sürücü', domain=[('is_driver', '=', True)])
    district_id = fields.Many2one('res.city.district', string='İlçe', related='partner_id.district_id', store=True)
    delivery_day_ids = fields.Many2many(
        'delivery.day',
        'stock_picking_delivery_day_rel',
        'picking_id',
        'day_id',
        string='Teslimat Günleri',
        related='partner_id.delivery_day_ids',
        store=True
    )

    def action_create_delivery(self):
        self.ensure_one()
        if not self.is_delivery_created:
            delivery = self.env['delivery.document'].create({
                'name': self.env['ir.sequence'].next_by_code('delivery.document') or 'Yeni',
                'date': fields.Date.context_today(self),
                'partner_id': self.partner_id.id,
                'district_id': self.partner_id.district_id.id,
                'delivery_day_ids': [(6, 0, self.partner_id.delivery_day_ids.ids)],
                'picking_id': self.id,
                'state': 'draft',
            })
            self.write({
                'delivery_id': delivery.id,
                'is_delivery_created': True
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'delivery.document',
                'views': [[False, 'form']],
                'res_id': delivery.id,
            }
        return True 