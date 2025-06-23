# -*- coding: utf-8 -*-

def setup_delivery_schedule(env):
    """
    Teslimat programını otomatik olarak ayarlar
    """
    
    # Teslimat günlerini al
    monday = env.ref('delivery_module.delivery_day_monday')
    tuesday = env.ref('delivery_module.delivery_day_tuesday')
    wednesday = env.ref('delivery_module.delivery_day_wednesday')
    thursday = env.ref('delivery_module.delivery_day_thursday')
    friday = env.ref('delivery_module.delivery_day_friday')
    saturday = env.ref('delivery_module.delivery_day_saturday')
    
    # İlçeleri al
    # Anadolu Yakası
    maltepe = env.ref('delivery_module.district_maltepe')
    kartal = env.ref('delivery_module.district_kartal')
    pendik = env.ref('delivery_module.district_pendik')
    tuzla = env.ref('delivery_module.district_tuzla')
    uskudar = env.ref('delivery_module.district_uskudar')
    kadikoy = env.ref('delivery_module.district_kadikoy')
    atasehir = env.ref('delivery_module.district_atasehir')
    umraniye = env.ref('delivery_module.district_umraniye')
    sancaktepe = env.ref('delivery_module.district_sancaktepe')
    cekmekoy = env.ref('delivery_module.district_cekmekoy')
    beykoz = env.ref('delivery_module.district_beykoz')
    sile = env.ref('delivery_module.district_sile')
    sultanbeyli = env.ref('delivery_module.district_sultanbeyli')
    
    # Avrupa Yakası
    beyoglu = env.ref('delivery_module.district_beyoglu')
    sisli = env.ref('delivery_module.district_sisli')
    besiktas = env.ref('delivery_module.district_besiktas')
    kagithane = env.ref('delivery_module.district_kagithane')
    sariyer = env.ref('delivery_module.district_sariyer')
    bakirkoy = env.ref('delivery_module.district_bakirkoy')
    bahcelievler = env.ref('delivery_module.district_bahcelievler')
    gungoren = env.ref('delivery_module.district_gungoren')
    esenler = env.ref('delivery_module.district_esenler')
    bagcilar = env.ref('delivery_module.district_bagcilar')
    eyupsultan = env.ref('delivery_module.district_eyupsultan')
    gaziosmanpasa = env.ref('delivery_module.district_gaziosmanpasa')
    kucukcekmece = env.ref('delivery_module.district_kucukcekmece')
    avcilar = env.ref('delivery_module.district_avcilar')
    basaksehir = env.ref('delivery_module.district_basaksehir')
    sultangazi = env.ref('delivery_module.district_sultangazi')
    arnavutkoy = env.ref('delivery_module.district_arnavutkoy')
    fatih = env.ref('delivery_module.district_fatih')
    zeytinburnu = env.ref('delivery_module.district_zeytinburnu')
    bayrampasa = env.ref('delivery_module.district_bayrampasa')
    esenyurt = env.ref('delivery_module.district_esenyurt')
    beylikduzu = env.ref('delivery_module.district_beylikduzu')
    silivri = env.ref('delivery_module.district_silivri')
    catalca = env.ref('delivery_module.district_catalca')
    
    # Önce tüm teslimat günlerini temizle
    monday.district_ids = [(5, 0, 0)]
    tuesday.district_ids = [(5, 0, 0)]
    wednesday.district_ids = [(5, 0, 0)]
    thursday.district_ids = [(5, 0, 0)]
    friday.district_ids = [(5, 0, 0)]
    saturday.district_ids = [(5, 0, 0)]
    
    # Pazartesi - Anadolu Yakası + Avrupa Yakası
    monday.district_ids = [(4, maltepe.id), (4, kartal.id), (4, pendik.id), (4, tuzla.id),
                          (4, beyoglu.id), (4, sisli.id), (4, besiktas.id), (4, kagithane.id)]
    
    # Salı - Anadolu Yakası + Avrupa Yakası
    tuesday.district_ids = [(4, uskudar.id), (4, kadikoy.id), (4, atasehir.id), (4, umraniye.id),
                           (4, sariyer.id), (4, bakirkoy.id), (4, bahcelievler.id), (4, gungoren.id), (4, esenler.id), (4, bagcilar.id)]
    
    # Çarşamba - Anadolu Yakası + Avrupa Yakası
    wednesday.district_ids = [(4, uskudar.id), (4, kadikoy.id), (4, atasehir.id), (4, umraniye.id),
                             (4, beyoglu.id), (4, sisli.id), (4, besiktas.id), (4, kagithane.id)]
    
    # Perşembe - Anadolu Yakası + Avrupa Yakası
    thursday.district_ids = [(4, uskudar.id), (4, kadikoy.id), (4, atasehir.id), (4, umraniye.id),
                            (4, eyupsultan.id), (4, gaziosmanpasa.id), (4, kucukcekmece.id), (4, avcilar.id), (4, basaksehir.id), (4, sultangazi.id), (4, arnavutkoy.id)]
    
    # Cuma - Anadolu Yakası + Avrupa Yakası
    friday.district_ids = [(4, maltepe.id), (4, kartal.id), (4, pendik.id),
                          (4, fatih.id), (4, zeytinburnu.id), (4, bayrampasa.id)]
    
    # Cumartesi - Anadolu Yakası + Avrupa Yakası
    saturday.district_ids = [(4, sancaktepe.id), (4, cekmekoy.id), (4, beykoz.id), (4, sile.id), (4, sultanbeyli.id),
                            (4, esenyurt.id), (4, beylikduzu.id), (4, silivri.id), (4, catalca.id)]
    
    print("Teslimat programı başarıyla ayarlandı!")
    print("\nANADOLU YAKASI:")
    print("Pazartesi: Maltepe, Kartal, Pendik, Tuzla")
    print("Salı: Üsküdar, Kadıköy, Ataşehir, Ümraniye")
    print("Çarşamba: Üsküdar, Kadıköy, Ataşehir, Ümraniye")
    print("Perşembe: Üsküdar, Kadıköy, Ataşehir, Ümraniye")
    print("Cuma: Maltepe, Kartal, Pendik")
    print("Cumartesi: Sancaktepe, Çekmeköy, Beykoz, Şile, Sultanbeyli")
    
    print("\nAVRUPA YAKASI:")
    print("Pazartesi: Beyoğlu, Şişli, Beşiktaş, Kağıthane")
    print("Salı: Sarıyer, Bakırköy, Bahçelievler, Güngören, Esenler, Bağcılar")
    print("Çarşamba: Beyoğlu, Şişli, Beşiktaş, Kağıthane")
    print("Perşembe: Eyüpsultan, Gaziosmanpaşa, Küçükçekmece, Avcılar, Başakşehir, Sultangazi, Arnavutköy")
    print("Cuma: Fatih, Zeytinburnu, Bayrampaşa")
    print("Cumartesi: Esenyurt, Beylikdüzü, Silivri, Çatalca") 