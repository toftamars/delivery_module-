from odoo import models, fields, api

class DeliveryPlanning(models.Model):
    _name = 'delivery.planning'
    _description = 'Teslimat Planlama'

    name = fields.Char('Plan Adı', required=True, default='Teslimat Planı')
    
    # Teslimat günleri bilgisi
    delivery_days_info = fields.Html('Teslimat Günleri', 
                                   default="""
                                   <h3>ANADOLU YAKASI</h3>
                                   <p><strong>Pazartesi:</strong> Maltepe, Kartal, Pendik, Tuzla</p>
                                   <p><strong>Salı:</strong> Üsküdar, Kadıköy, Ataşehir, Ümraniye</p>
                                   <p><strong>Çarşamba:</strong> Üsküdar, Kadıköy, Ataşehir, Ümraniye</p>
                                   <p><strong>Perşembe:</strong> Üsküdar, Kadıköy, Ataşehir, Ümraniye</p>
                                   <p><strong>Cuma:</strong> Maltepe, Kartal, Pendik, Sultanbeyli</p>
                                   <p><strong>Cumartesi:</strong> Sancaktepe, Çekmeköy, Beykoz, Şile</p>
                                   
                                   <h3>AVRUPA YAKASI</h3>
                                   <p><strong>Pazartesi:</strong> Beyoğlu, Şişli, Beşiktaş, Kağıthane</p>
                                   <p><strong>Salı:</strong> Sarıyer, Bakırköy, Bahçelievler, Güngören, Esenler, Bağcılar</p>
                                   <p><strong>Çarşamba:</strong> Beyoğlu, Şişli, Beşiktaş, Kağıthane</p>
                                   <p><strong>Perşembe:</strong> Eyüpsultan, Gaziosmanpaşa, Küçükçekmece, Avcılar, Başakşehir, Sultangazi, Arnavutköy</p>
                                   <p><strong>Cuma:</strong> Fatih, Zeytinburnu, Bayrampaşa</p>
                                   <p><strong>Cumartesi:</strong> Esenyurt, Beylikdüzü, Silivri, Çatalca</p>
                                   """, readonly=True)
    
    # Günlük teslimat limiti bilgisi
    daily_limit_info = fields.Text('Günlük Limit Bilgisi', 
                                  default='Her araç için günlük maksimum 7 teslimat onaylanabilir.',
                                  readonly=True) 