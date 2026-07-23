import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

def veritabaninda_ara(soru):
    conn = sqlite3.connect('hastane.db')
    cursor = conn.cursor()
    
    soru_kucuk = soru.lower()
    
    cursor.execute("SELECT bolum_adi, kat, blok_koridor, tarif FROM navigasyon")
    tum_odalar = cursor.fetchall()
    
    for bolum_adi, kat, blok_koridor, tarif in tum_odalar:
        bolum_kucuk = bolum_adi.lower()
        parcalar = bolum_kucuk.split()
        eslesti = False
        
        for parca in parcalar:
            if len(parca) > 2 and parca in soru_kucuk:
                eslesti = True
                break
        
        if bolum_kucuk in soru_kucuk or eslesti:
            if "mr" in soru_kucuk and "mr" not in bolum_kucuk:
                continue
                
            conn.close()
            return (f"Merhaba! Sorduğunuz {bolum_adi} için size yardımcı olmaktan memnuniyet duyarım. "
                    f"Bu alan {kat} katında, {blok_koridor} bölgesinde yer almaktadır. "
                    f"Ulaşmak için: {tarif} Başka bir poliklinik veya oda hakkında bilgi istemiştiniz?")

    conn.close()
    return "Üzgünüm, aradığınız poliklinik veya odayı şu an sistemde bulamadım. Lütfen kelimeyi kontrol edip tekrar deneyin."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(veritabaninda_ara(sys.argv[1]))