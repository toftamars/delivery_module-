{
    'name': 'Teslimat Modülü',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Teslimat yönetimi için özel modül',
    'description': """
        Bu modül, teslimat süreçlerini yönetmek için özel olarak tasarlanmıştır.
        Özellikler:
        - Transfer belgelerinden otomatik teslimat oluşturma
        - Araç bazlı teslimat planlaması
        - SMS bildirim entegrasyonu
        - Rota ve harita desteği
        - İlçe bazlı gün kısıtlamaları
    """,
    'author': 'Zuhal Müzik',
    'website': 'https://www.zuhalmuzik.com',
    'depends': [
        'base',
        'stock',
        'sale',
        'sms',
    ],
    'data': [
        'security/delivery_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/delivery_data.xml',
        'views/delivery_views.xml',
        'views/delivery_planning_views.xml',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
        'wizard/delivery_create_wizard_views.xml',
        'security/ir_rule.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 