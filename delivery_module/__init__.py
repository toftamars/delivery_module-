from . import models
from . import wizard

def post_init_hook(cr, registry):
    """Modül kurulumundan sonra çalışacak fonksiyon"""
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Varsayılan teslimat planlaması oluştur
    if not env['delivery.planning'].search([]):
        env['delivery.planning'].create({
            'name': 'Varsayılan Planlama',
            'active': True
        }) 