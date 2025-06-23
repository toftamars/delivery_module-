{
    'name': 'Teslimat Modülü',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Teslimat yönetimi için modül',
    'description': """
        Teslimat yönetimi için modül.
        Özellikler:
        - Transfer belgelerinden otomatik teslimat oluşturma
        - SMS bildirim entegrasyonu
        - Rota ve harita desteği
        - İlçe bazlı gün kısıtlamaları
        - Araç bazlı teslimat yönetimi
        - Günlük teslimat limitleri
        - Geçici teslimat günü kapatma
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
        'data/delivery_data.xml',
        'data/ir_sequence_data.xml',
        'views/action_views.xml',
        'views/delivery_views.xml',
        'views/delivery_vehicle_views.xml',
        'views/delivery_day_views.xml',
        'views/delivery_photo_views.xml',
        'views/res_partner_views.xml',
        'views/res_city_views.xml',
        'views/res_city_district_views.xml',
        'wizard/delivery_create_wizard_views.xml',
        'wizard/delivery_photo_wizard_views.xml',
        'wizard/delivery_limit_warning_wizard_views.xml',
        'wizard/delivery_day_closure_wizard_views.xml',
        'wizard/delivery_vehicle_closure_wizard_views.xml',
        'wizard/setup_delivery_schedule_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'delivery_module/static/src/js/delivery_map.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
} 