from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeliveryCreateWizard(models.TransientModel):
    _name = 'delivery.create.wizard'
    _description = 'Teslimat Oluşturma Sihirbazı'

    date = fields.Date('Teslimat Tarihi', required=True, default=fields.Date.context_today)
    driver_id = fields.Many2one('res.partner', string='Sürücü', domain=[('is_driver', '=', True)])
    picking_ids = fields.Many2many('stock.picking', string='Transfer Belgeleri')

    def action_create_delivery(self):
        if not self.picking_ids:
            raise UserError(_('Lütfen en az bir transfer belgesi seçin.'))

        delivery = self.env['delivery.document'].create({
            'date': self.date,
            'driver_id': self.driver_id.id,
            'partner_id': self.picking_ids[0].partner_id.id,
            'picking_ids': [(6, 0, self.picking_ids.ids)],
        })

        return {
            'name': _('Teslimat Belgesi'),
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.document',
            'view_mode': 'form',
            'res_id': delivery.id,
        } 