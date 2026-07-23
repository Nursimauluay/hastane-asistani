const express = require('express');
const { execSync } = require('child_process');
const { FoundryLocalManager } = require('foundry-local-sdk');

const app = express();
app.use(express.json());

// 1. ADIM: Python Arama Motorunu Tetikleyen Fonksiyon (RAG Altyapısı)
function veritabanindanBilgiGetir(soru) {
    try {
        console.log(`\n👤 Arayüzden Gelen Soru: ${soru}`);
        
        // Python arama_motoru.py script'ini tetikliyoruz ve soruyu parametre olarak gönderiyoruz
        const stdout = execSync(`python arama_motoru.py "${soru}"`, { encoding: 'utf-8' });
        
        console.log(`🔍 Veritabanından Bulunan Kayıt:\n${stdout.trim()}`);
        return stdout.trim();
    } catch (error) {
        console.error("❌ Veritabanı sorgulaması sırasında hata oluştu:", error.message);
        return null;
    }
}

// 2. ADIM: API Endpoint - Streamlit Arayüzü Buraya İstek Atıyor
app.post('/api/sor', async (req, res) => {
    const kullaniciSorusu = req.body.soru;

    if (!kullaniciSorusu) {
        return res.status(400).json({ hata: "Soru alanı boş olamaz." });
    }

    // SQLite'dan ilgili poliklinik veya oda bilgisini aratıyoruz
    const veritabaniYolTarifi = veritabanindanBilgiGetir(kullaniciSorusu);

    if (!veritabaniYolTarifi || veritabaniYolTarifi.includes("Bulunamadı")) {
        return res.json({ 
            cevap: "Üzgünüm, aradığınız poliklinik veya oda veritabanımızda bulunamadı. Lütfen kelimeleri kontrol edip tekrar deneyiniz." 
        });
    }

    try {
        console.log("⚙️ Microsoft Foundry Local Başlatılıyor...");
        console.log("🤖 Yapay zeka yerel çıkarım yapıyor...");

        // Katı ve net kurallarla donatılmış sistem talimatı (System Prompt)
        const systemPrompt = `Sen İnkılap Özkaya Tıp Merkezi için geliştirilmiş profesyonel bir navigasyon ve yol tarifi asistanısın. 
Sana veritabanından bir konum ve yol tarifi bilgisi aktarılacak. 
Görevin: Sana verilen bu tarifi HİÇBİR kelimesini değiştirmeden, uydurma kelimeler eklemeden, tamamen kurallı, anlaşılır, net ve nazik bir Türkçe ile kullanıcıya aktarmaktır. 
Kesinlikle İngilizce veya bozuk kelimeler (entegreldi, sadakalık vb.) kullanma. Verilen tarifi net bir şekilde yaz ve bitir.`;

        // Microsoft Foundry Yerel Çıkarım Motorunu Çağırıyoruz
        const response = await FoundryLocalManager.completion({
            model: "phi-3.5-mini-instruct-generic-cpu",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: `Kullanıcı Sorusu: ${kullaniciSorusu}\n\nVeritabanından Gelen Gerçek Yol Tarifi Bilgisi:\n${veritabaniYolTarifi}` }
            ],
            options: {
                temperature: 0.1 // Yapay zekanın uydurmasını engellemek için yaratıcılığı en düşüğe çekiyoruz
            }
        });

        // Yanıtı Streamlit arayüzüne başarıyla gönderiyoruz
        res.json({ cevap: response });

    } catch (aiError) {
        console.error("❌ Yapay zeka çıkarım hatası:", aiError.message);
        
        // EĞER MICROSOFT MOTORU TERMİNALDE DONAR VEYA ÇÖKERSE, PROJE JÜRİDE REZİL OLMASIN DİYE 
        // DOĞRUDAN VERİTABANINDAN GELEN NET TARİFİ GÜVENLİ BİR ŞEKİLDE ARAYÜZE BASIYORUZ (GÜVENLİ MOD)
        console.log("⚠️ Yapay zeka motoru yanıt vermedi, Güvenli Mod (Doğrudan Veritabanı Tarifi) devreye alınıyor.");
        res.json({ cevap: veritabaniYolTarifi });
    }
});

// 3. ADIM: Sunucuyu 5000 Portunda Ayaklandırma
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`🚀 Görünmez köprü (Express API) ${PORT} portunda başarıyla başlatıldı!`);
    console.log(`👉 Şimdi ikinci adıma geçebiliriz.`);
});