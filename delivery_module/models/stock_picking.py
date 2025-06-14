from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_id = fields.Many2one('delivery.document', string='Teslimat Belgesi', readonly=True)
    is_delivery_created = fields.Boolean(string='Teslimat Oluşturuldu', default=False, copy=False)
    delivery_date = fields.Date(string='Teslimat Tarihi', related='delivery_id.date', store=True)
    delivery_state = fields.Selection([
        ('draft', 'Taslak'),
        ('approved', 'Onaylandı'),
        ('in_delivery', 'Teslimatta'),
        ('completed', 'Tamamlandı'),
        ('canceled', 'İptal')
    ], string='Teslimat Durumu', related='delivery_id.state', store=True)
    driver_id = fields.Many2one('res.partner', string='Sürücü', related='delivery_id.driver_id', store=True)
    district_id = fields.Many2one('res.city.district', string='İlçe', related='partner_id.district_id', store=True)
    delivery_day_ids = fields.Many2many('delivery.day', string='Teslimat Günleri', related='partner_id.delivery_day_ids', store=True)

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