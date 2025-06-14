{
    'name': 'Teslimat Modülü',
    'version': '16.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Transfer belgelerinden otomatik teslimat oluşturma ve yönetim',
    'description': """
        Teslimat Modülü:
        - Transfer belgelerinden otomatik teslimat oluşturma
        - Araç bazlı teslimat planlama
        - SMS bilgilendirme entegrasyonu
        - Rota ve harita desteği
        - İlçe bazlı gün kısıtlamaları
    """,
    'author': 'Alper Tofta',
    'depends': [
        'base',
        'stock',
        'sms',
        'base_address_extended',
        'base_address_city',
        'mail',
        'web',
    ],
    'data': [
        'security/delivery_security.xml',
        'security/ir.model.access.csv',
        'data/delivery_data.xml',
        'views/res_partner_views.xml',
        'views/delivery_views.xml',
        'views/delivery_planning_views.xml',
        'views/stock_picking_views.xml',
        'views/menu_views.xml',
        'wizard/delivery_create_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
} 