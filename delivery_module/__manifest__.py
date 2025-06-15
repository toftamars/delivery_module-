{
    'name': 'Teslimat Modülü',
    'version': '1.0',
    'category': 'Inventory/Delivery',
    'summary': 'Teslimat yönetimi için özel modül',
    'description': """
        Bu modül teslimat yönetimi için özel olarak geliştirilmiştir.
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
        'base_setup',
        'stock',
        'sale',
        'mail',
        'web',
        'contacts',
        'sms',
        'resource',
    ],
    'data': [
        'security/delivery_security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/ir_sequence_data.xml',
        'data/delivery_data.xml',
        'views/menu_views.xml',
        'views/delivery_views.xml',
        'views/delivery_planning_views.xml',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'wizard/delivery_create_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 