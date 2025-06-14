from . import models
from . import wizard

# Kurulum sonrası otomatik veri oluşturma
def post_init_hook(cr, registry):
    """Modül kurulduktan sonra çalışacak fonksiyon"""
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Varsayılan teslimat planlama kaydı oluştur
    if not env['delivery.planning'].search([]):
        env['delivery.planning'].create({
            'name': 'Varsayılan Teslimat Planı'
        }) 