import sqlite3

# Gerçek veritabanı bağlantısı
conn = sqlite3.connect('hastane.db')
cursor = conn.cursor()

# Eski tabloyu temizleyip yeniden temiz bir tablo oluşturalım
cursor.execute('DROP TABLE IF EXISTS navigasyon')

cursor.execute('''
CREATE TABLE navigasyon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolum_adi TEXT,
    kat TEXT,
    blok_koridor TEXT,
    tarif TEXT
)
''')

# Gerçek haritadan çıkardığımız odaların tam listesi
gercek_harita_verileri = [
    ('Kan ve Numune Alma', 'Zemin', 'Acil Koridoru', 'Ana girişten girince sağa dönün, acil bekleme alanını geçip Acil Koridoruna ilerleyin. Acil Muayene odasını geçince sağdaki odadır. Gözlem odasının hemen yanındadır.'),
    ('Acil Muayene', 'Zemin', 'Acil Koridoru', 'Ana girişten girince sağa dönün, acil koridorunda ilerleyin. Acil Müdahale odasını geçince sağdaki odadır.'),
    ('Acil Müdahale', 'Zemin', 'Acil Koridoru', 'Ana girişten girince hemen sağa dönün, acil bekleme alanının hemen karşısında, acil koridorunun sağındaki ilk odadır.'),
    ('Gözlem Odası', 'Zemin', 'Acil Koridoru', 'Ana girişten girince sağa dönüp acil koridoru boyunca dümdüz ilerleyin. Koridorun sağ en sonundaki odadır, Kan ve Numune Alma odasının yanındadır.'),
    ('MR Odası', 'Zemin', 'Sol Blok / Hol', 'Ana girişten girdikten sonra tıp merkezi giriş holünden düz devam edip sola dönün. Sol koridordaki büyük alandır, Kontrol Odası ile Teknik Oda arasındadır.'),
    ('Kemik Dansitometri', 'Zemin', 'Sol Blok', 'Ana girişten girip holü takip ederek sol koridorun en sonuna kadar ilerleyin. Koridorun sol en sonundaki odadır, Kontrol Odasının hemen yanındadır.'),
    ('Kontrol Odası', 'Zemin', 'Sol Blok', 'Ana girişten girip sol koridora ilerleyin. MR odasını geçince soldaki odadır, Kemik Dansitometri odasının yanındadır.')
]

cursor.executemany('''
INSERT INTO navigasyon (bolum_adi, kat, blok_koridor, tarif)
VALUES (?, ?, ?, ?)
''', gercek_harita_verileri)

conn.commit()
conn.close()
print("🎯 Veritabanı Özel İnkılap Özkaya Tıp Merkezi haritasına göre Başarıyla Güncellendi!")