from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SetupDeliveryScheduleWizard(models.TransientModel):
    _name = 'setup.delivery.schedule.wizard'
    _description = 'Teslimat Programı Kurulum Sihirbazı'

    def action_setup_schedule(self):
        """Teslimat programını manuel olarak ayarlar"""
        try:
            from ..data.setup_delivery_schedule import setup_delivery_schedule
            setup_delivery_schedule(self.env)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Başarılı'),
                    'message': _('Teslimat programı başarıyla ayarlandı!'),
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(_(f'Teslimat programı ayarlanırken hata oluştu: {str(e)}')) 