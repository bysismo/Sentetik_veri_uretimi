🚀 Qwen2.5-Coder Otomatik Veri Seti Üreticisi

Kod yazan herkes veri seti oluşturur, kategorize eder. 
Bu script, Qwen2.5-Coder modelini kullanarak İngilizce konu başlıklarını; 
açıklama ve kod içeren JSON formatında bir veri setine dönüştürür.

⚡ Neden Bu Script?

    Token Bazlı Kategori Sistemi: Veriyi token uzunluğuna göre _128, _256, _512, _768, _1024 dosyalarına otomatik böler.

    Akıllı Kaldığı Yerden Devam: output_base dosyasını kontrol eder, tamamlanmış görevleri atlayarak GPU'nuzu boşuna yormaz.

    JSON Filtreleme: Modelin saçmaladığı veya formatı bozduğu yanıtları otomatik reddeder; sadece kusursuz JSON verilerini kaydeder.

    Tam Kontrol: Batch size, temperature, precision (4bit/8bit/16bit) ayarlarıyla donanımınıza göre optimize edilebilir.

📥 Veri Seti Hazırlığı

Scriptin çalışması için INPUT_FILE yolunda belirttiğiniz dosyanın JSONL (JSON Lines) formatında olması gerekir. 
Her satırda bir görev bulunmalı ve şu anahtarları içermelidir:
code JSON

{"ingilizce": "How to use list comprehension in Python", "turkce": "Python'da liste üreteçleri nasıl kullanılır"}
{"ingilizce": "Implement binary search algorithm", "turkce": "İkili arama algoritması gerçekle"}

    ingilizce: Modelin üzerinde çalışacağı ana konu başlığı.

    turkce: Çıktı verisinde kullanılacak açıklayıcı soru kökü.

🛠 Çıktı Formatı

Script başarıyla işlediği her satırı şu formatta kaydeder:
code JSON

{
  "ingilizce": "Implement binary search",
  "turkce": "İkili arama algoritması gerçekle için örnek bir uygulama yazarmısın",
  "explanation": "Binary search, sıralı bir dizide aranan elemanın indeksini...",
  "python": ["```python\ndef binary_search(arr, target):\n    # kod buraya gelir...\n```"]
}


📊 Token Kategorizasyonu

Scriptin en güçlü yanı, veriyi işlerken token sayısına göre sınıflandırmasıdır. Çıktı klasörünüzde şu dosyalar oluşur:
Kategori	Token Limiti	Kullanım Amacı
_128.jsonl	0-128	Kısa fonksiyonlar ve hızlı örnekler
_256.jsonl	129-256	Orta seviye algoritmalar
_512.jsonl	257-512	Standart modül yapıları
_1024.jsonl	513-1024	Kompleks projeler ve detaylı sınıflar
⚙️ Hızlı Kurulum

1. Gereksinimleri Yükleyin:
code Bash

pip install -r requirements.txt

2. Ayarları Yapın:
   
Config sınıfı içinde:

    PRECISION: GPU VRAM'inize göre (4bit, 8bit, 16bit) seçin.

    BATCH_SIZE: Bellek kapasitenize göre 10-50 arası değerler deneyin.

    INPUT_FILE: Veri setinizi gösterin.

4. Çalıştırın:
code Bash

python main.py

🛠 Teknik Detaylar

    Model: Varsayılan olarak Qwen/Qwen2.5-Coder-7B-Instruct kullanır.

    JSON Extraction: extract_json fonksiyonu, modelin markdown veya ekstra metinlerini temizleyip saf JSON çıktısını yakalar.

    İstatistik: İşlem bittiğinde her kategorideki başarı oranını % olarak loglar (örn: %12.5 = 128 token).

⚠️ Önemli İpucu

Config içindeki TOKEN_CATEGORIES sözlüğünü projenizin ihtiyacına göre özelleştirebilirsiniz. 
Eğer modelinizin daha uzun kodlar yazmasını istiyorsanız MAX_NEW_TOKENS değerini yükseltip yeni bir kategori tanımlamanız yeterlidir.

