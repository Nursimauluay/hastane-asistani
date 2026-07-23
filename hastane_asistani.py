import sqlite3
from openai import OpenAI

# 1. Bilgisayarındaki yerel yapay zeka sunucusuna bağlanıyoruz
# Yerel yapay zeka sunucuları genelde standart olarak bu adreste (port 11434 veya 5000) çalışır
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Yerel sunucu adresi
    api_key="ollama"  # Yerel çalıştığı için şifre önemsizdir
)

# 2. Veritabanından harita bilgisi çeken fonksiyon
def veritabaninda_ara(soru):
    conn = sqlite3.connect('hastane.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT bolum_adi, kat, blok_koridor, tarif FROM navigasyon")
    satirlar = cursor.fetchall()
    conn.close()
    
    # Kullanıcının sorusuna göre haritayı tarıyoruz
    for bolum, kat, konum, tarif in satirlar:
        if bolum.lower() in soru.lower() or soru.lower() in bolum.lower():
            return f"Bölüm: {bolum}\nKat: {kat}\nKonum: {konum}\nTarif: {tarif}"
            
    return "Aradığınız bölüm Özel İnkılap Özkaya Tıp Merkezi zemin kat planında bulunamadı."

# 3. Ana Akış
def ana_akis():
    kullanici_sorusu = "Merhaba, MR odası nerede acaba?"
    print(f"👤 Kullanıcı Sorusu: {kullanici_sorusu}\n")
    
    # Veritabanından gerçek harita verisini alıyoruz
    harita_bilgisi = veritabaninda_ara(kullanici_sorusu)
    print(f"🔍 Veritabanından Çekilen Gerçek Harita Bilgisi:\n{harita_bilgisi}\n")
    
    print("🤖 Yapay Zeka Cevap Üretiyor (Lütfen bekleyin)...")
    
    try:
        # Bilgisayarındaki phi3, phi3.5 veya llama modelini tetikliyoruz
        response = client.chat.completions.create(
            model="phi3.5",  # Bilgisayarında yüklü olan model adı (phi3 veya phi3.5)
            messages=[
                {
                    "role": "system",
                    "content": f"Sen Özel İnkılap Özkaya Tıp Merkezi navigasyon asistanısın. Şu harita bilgisine sadık kalarak hastaya kibar bir yol tarifi sun: {harita_bilgisi}"
                },
                {
                    "role": "user",
                    "content": kullanici_sorusu
                }
            ]
        )
        
        print("\n✨ Canlı Asistan Cevabı:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"\n❌ Bir sorun oluştu: {e}")
        print("💡 İpucu: Bilgisayarında arka planda yerel yapay zeka sunucusunun (Ollama vb.) açık olduğundan emin ol.")

if __name__ == "__main__":
    ana_akis()