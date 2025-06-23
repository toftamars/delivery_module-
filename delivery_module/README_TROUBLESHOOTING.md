# Teslimat Modülü - Sorun Giderme Kılavuzu

## 🚨 "relation delivery_photo_wizard does not exist" Hatası

### **Sorun**: 
```
psycopg2.errors.UndefinedTable: relation "delivery_photo_wizard" does not exist
```

### **Çözüm Adımları**:

#### **1. Modülü Tamamen Kaldır**
1. Odoo'ya giriş yapın
2. Apps > delivery_module > Uninstall
3. "Uninstall" butonuna tıklayın
4. Onaylayın

#### **2. Veritabanını Temizle**
```sql
-- PostgreSQL'e bağlan
sudo -u postgres psql -d your_database_name

-- Modül kayıtlarını temizle
DELETE FROM ir_module_module WHERE name = 'delivery_module';

-- Modül tablolarını temizle (eğer varsa)
DROP TABLE IF EXISTS delivery_photo_wizard CASCADE;
DROP TABLE IF EXISTS delivery_photo CASCADE;
DROP TABLE IF EXISTS delivery_document CASCADE;
DROP TABLE IF EXISTS delivery_vehicle CASCADE;
DROP TABLE IF EXISTS delivery_day CASCADE;

-- Çık
\q
```

#### **3. Odoo'yu Yeniden Başlat**
```bash
sudo systemctl restart odoo
# veya
sudo service odoo restart
```

#### **4. Modülü Yeniden Yükle**
1. Odoo'ya tekrar giriş yapın
2. Apps > Update Apps List
3. delivery_module'ü bulun
4. "Install" butonuna tıklayın

#### **5. Veritabanını Güncelle**
1. Settings > Technical > Database Structure > Update
2. "Update" butonuna tıklayın

### **Alternatif Çözüm - Manuel Tablo Oluşturma**

Eğer yukarıdaki adımlar işe yaramazsa:

```sql
-- PostgreSQL'e bağlan
sudo -u postgres psql -d your_database_name

-- Wizard tablosunu manuel oluştur
CREATE TABLE IF NOT EXISTS delivery_photo_wizard (
    id SERIAL PRIMARY KEY,
    create_uid INTEGER,
    create_date TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP,
    delivery_id INTEGER,
    photo_type VARCHAR(50),
    image TEXT,
    image_filename VARCHAR(255),
    description TEXT,
    name VARCHAR(255)
);

-- Çık
\q
```

### **Önleyici Tedbirler**

#### **1. Modül Güncelleme Öncesi**
- Veritabanı yedeği alın
- Modülü test ortamında deneyin
- Güvenlik ayarlarını kontrol edin

#### **2. Modül Güncelleme Sırasında**
- Odoo'yu kapatmayın
- Tarayıcıyı yenilemeyin
- İşlemi yarıda kesmeyin

#### **3. Modül Güncelleme Sonrası**
- Log dosyalarını kontrol edin
- Modülü test edin
- Güvenlik ayarlarını doğrulayın

### **Log Kontrolü**

```bash
# Odoo log dosyasını kontrol et
sudo tail -f /var/log/odoo/odoo.log

# Hata mesajlarını filtrele
sudo grep -i error /var/log/odoo/odoo.log

# Modül yükleme loglarını kontrol et
sudo grep -i delivery_module /var/log/odoo/odoo.log
```

### **Yaygın Hatalar ve Çözümleri**

#### **1. Güvenlik Hatası**
```
'Group' Alanında dış id 'delivery_module.group_delivery_user' için eşleşen kayıt bulunamadı
```
**Çözüm**: Güvenlik gruplarını yeniden oluştur

#### **2. Transient Model Hatası**
```
relation "delivery_photo_wizard" does not exist
```
**Çözüm**: Modülü tamamen kaldır ve yeniden yükle

#### **3. Assets Hatası**
```
JavaScript dosyaları yüklenmiyor
```
**Çözüm**: Browser cache'ini temizle, Odoo'yu yeniden başlat

### **İletişim**

Sorun devam ederse:
1. Log dosyalarını paylaşın
2. Hata mesajlarını kopyalayın
3. Modül versiyonunu belirtin
4. Odoo versiyonunu belirtin 