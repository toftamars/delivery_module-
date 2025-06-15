{
    'name': 'Teslimat Modülü',
    'version': '1.0',
    'category': 'Inventory/Delivery',
    'summary': 'Teslimat yönetimi için modül',
    'description': """
        Teslimat yönetimi için modül.
        Özellikler:
        - Transfer belgelerinden otomatik teslimat oluşturma
        - SMS bildirim entegrasyonu
        - Rota ve harita desteği
        - İlçe bazlı gün kısıtlamaları
    """,
    'author': 'Tofta',
    'website': 'https://github.com/toftamars/delivery_module',
    'depends': [
        'base',
        'mail',
        'web',
        'contacts',
        'stock',
        'sms',
        'base_setup',
        'resource'
    ],
    'data': [
        'security/delivery_security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/delivery_data.xml',
        'data/ir_sequence_data.xml',
        'views/delivery_views.xml',
        'views/delivery_day_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
        'wizard/delivery_create_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 