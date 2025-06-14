from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_ids = fields.One2many('delivery.document', 'picking_id', string='Teslimatlar')
    delivery_count = fields.Integer(compute='_compute_delivery_count', string='Teslimat Sayısı')
    district_id = fields.Many2one('res.city.district', string='İlçe', related='partner_id.district_id', store=True)
    delivery_day = fields.Selection([
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
        ('sunday', 'Pazar')
    ], string='Teslimat Günü', related='partner_id.delivery_day', store=True)

    @api.depends('delivery_ids')
    def _compute_delivery_count(self):
        for picking in self:
            picking.delivery_count = len(picking.delivery_ids)

    def action_view_deliveries(self):
        self.ensure_one()
        return {
            'name': _('Teslimatlar'),
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id},
        } 