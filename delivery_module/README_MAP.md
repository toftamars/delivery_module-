# Teslimat Modülü - Harita ve Rota Özelliği

## Eklenen Özellikler

### 1. Harita Koordinatları
- **Başlangıç Koordinatları**: Depo konumu (varsayılan: İstanbul merkez)
- **Hedef Koordinatları**: Müşteri adresi koordinatları
- **Otomatik Hesaplama**: Müşteri koordinatları otomatik olarak hesaplanır

### 2. Rota Hesaplama
- **Gerçek Rota**: OSRM API ile gerçek yol rotası
- **Mesafe Hesaplama**: Gerçek yol mesafesi (km)
- **Süre Tahmini**: Gerçek trafik süresi (dakika)
- **Fallback**: API hatası durumunda Haversine formülü

### 3. Harita Görünümü
- **OpenStreetMap**: Ücretsiz harita servisi
- **Leaflet.js**: Modern harita kütüphanesi
- **İnteraktif**: Zoom, pan ve marker tıklama
- **Gerçek Rota**: Mavi çizgi ile gerçek yol rotası
- **Tahmini Rota**: Kırmızı kesikli çizgi ile kuş uçuşu

### 4. Gelişmiş Özellikler
- **Rota Talimatları**: Adım adım navigasyon talimatları
- **Kontrol Butonları**: Yenile, talimatlar, tam ekran
- **Tam Ekran Modu**: Haritayı tam ekran görüntüleme
- **Gerçek Zamanlı**: Koordinat değişikliklerinde otomatik güncelleme

## Kurulum

### 1. Modül Güncelleme
```bash
# Odoo'da modülü güncelle
# Apps > Update Apps List > delivery_module > Upgrade
```

### 2. Veritabanı Güncelleme
```bash
# Odoo'da veritabanını güncelle
# Settings > Technical > Database Structure > Update
```

### 3. Gerekli Paketler
```bash
# requests kütüphanesi (OSRM API için)
pip install requests
```

## Kullanım

### 1. Teslimat Belgesi
1. **Teslimat Belgesi Oluştur**: Yeni teslimat belgesi oluştur
2. **Müşteri Seç**: Koordinatları olan müşteri seç
3. **Harita Sekmesi**: "Harita ve Rota" sekmesine git
4. **Rota Görüntüle**: Haritada gerçek rota ve bilgileri gör
5. **Rotayı Yenile**: "Rotayı Yenile" butonu ile güncel bilgileri al

### 2. Müşteri Koordinatları
1. **Müşteri Düzenle**: Müşteri kaydını aç
2. **Harita Sekmesi**: "Harita" sekmesine git
3. **Koordinat Gir**: Enlem ve boylam değerlerini gir
4. **Kaydet**: Değişiklikleri kaydet

### 3. Harita Kontrolleri
- **Yenile Butonu**: Rotayı yeniden hesapla
- **Talimatlar Butonu**: Navigasyon talimatlarını göster/gizle
- **Tam Ekran Butonu**: Haritayı tam ekran yap

## Özellikler

### Harita Widget'ı
- **Responsive**: Tüm ekran boyutlarında uyumlu
- **Performanslı**: Lazy loading ile hızlı yükleme
- **Özelleştirilebilir**: CSS ile stil değişiklikleri
- **Kontrol Butonları**: Sağ üst köşede kontrol paneli

### Rota Bilgileri
- **Gerçek Mesafe**: OSRM API ile hesaplanan yol mesafesi
- **Gerçek Süre**: Trafik durumuna göre tahmini süre
- **Rota Tipi**: Gerçek rota (mavi) veya tahmini rota (kırmızı)
- **Güncel**: Koordinat değişikliklerinde otomatik güncelleme

### Rota Talimatları
- **Adım Adım**: Detaylı navigasyon talimatları
- **Mesafe Bilgisi**: Her adımın mesafesi
- **Süre Bilgisi**: Her adımın süresi
- **Gizle/Göster**: Talimatları gizleme özelliği

## Teknik Detaylar

### JavaScript Dosyaları
- `delivery_map.js`: Ana harita widget'ı
- `delivery_map.xml`: QWeb template

### Model Alanları
```python
# Teslimat Belgesi
start_latitude = fields.Float('Başlangıç Enlem')
start_longitude = fields.Float('Başlangıç Boylam')
end_latitude = fields.Float('Hedef Enlem')
end_longitude = fields.Float('Hedef Boylam')
route_distance = fields.Float('Rota Mesafesi (km)')
route_duration = fields.Float('Tahmini Süre (dk)')
show_map = fields.Boolean('Haritayı Göster')

# Müşteri
partner_latitude = fields.Float('Enlem')
partner_longitude = fields.Float('Boylam')
```

### Hesaplama Metodları
- `_compute_end_coordinates()`: Müşteri koordinatlarını al
- `_compute_route_distance()`: Haversine formülü ile mesafe
- `_compute_route_duration()`: Hız bazlı süre hesaplama
- `_get_osrm_route_data()`: OSRM API'den gerçek rota
- `refresh_route()`: Rota yenileme butonu

### API Entegrasyonu
- **OSRM API**: Açık kaynak rota servisi
- **Endpoint**: http://router.project-osrm.org/route/v1/driving/
- **Parametreler**: overview=full, geometries=geojson, steps=true
- **Fallback**: API hatası durumunda Haversine formülü

## Gelecek Geliştirmeler

### 1. Gelişmiş Rota API
- **Google Maps**: Ticari rota servisi
- **Çoklu Durak**: Birden fazla teslimat noktası
- **Trafik Durumu**: Gerçek zamanlı trafik bilgisi

### 2. Gelişmiş Özellikler
- **Yakıt Hesaplama**: Mesafe bazlı yakıt maliyeti
- **Optimizasyon**: En kısa rota algoritması
- **Rota Geçmişi**: Önceki rotaları kaydetme

### 3. Mobil Uygulama
- **GPS Takibi**: Gerçek zamanlı konum
- **Offline Harita**: İnternet olmadan kullanım
- **Push Bildirim**: Teslimat durumu bildirimleri

## Test Senaryoları

### 1. Temel Test
1. Yeni teslimat belgesi oluştur
2. Koordinatları olan müşteri seç
3. Harita sekmesini aç
4. Gerçek rota ve bilgileri kontrol et

### 2. API Testi
1. İnternet bağlantısını kes
2. Harita sekmesini aç
3. Fallback rotayı kontrol et
4. İnternet bağlantısını geri aç
5. "Rotayı Yenile" butonuna tıkla

### 3. Koordinat Testi
1. Müşteri koordinatlarını değiştir
2. Teslimat belgesini yenile
3. Yeni rotayı kontrol et
4. Rota talimatlarını kontrol et

### 4. Performans Testi
1. Çoklu teslimat belgesi aç
2. Harita yükleme süresini ölç
3. Bellek kullanımını kontrol et
4. Tam ekran modunu test et

## Sorun Giderme

### Harita Yüklenmiyor
- İnternet bağlantısını kontrol et
- Browser console'da hata var mı bak
- Leaflet.js yüklendi mi kontrol et
- CORS hatası var mı kontrol et

### OSRM API Hatası
- İnternet bağlantısını kontrol et
- API endpoint erişilebilir mi
- Koordinat formatı doğru mu
- Rate limit aşıldı mı

### Koordinat Hatalı
- Koordinat formatını kontrol et (ondalık)
- Müşteri koordinatları doğru mu
- Varsayılan değerler kullanılıyor mu
- Koordinat sınırları içinde mi

### Performans Sorunu
- Çok fazla marker var mı
- Harita boyutu çok büyük mü
- Browser cache'ini temizle
- API çağrıları çok sık mı

### Rota Talimatları Görünmüyor
- OSRM API çalışıyor mu
- steps parametresi true mu
- Browser console'da hata var mı
- Talimatlar butonu çalışıyor mu 