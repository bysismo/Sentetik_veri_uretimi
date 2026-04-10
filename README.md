🚀 Qwen2.5-Coder Otomatik Veri Seti Üreticisi

Bu proje, Qwen2.5-Coder-7B-Instruct modelini kullanarak verilen İngilizce konu başlıklarını, Türkçe karşılıklarıyla eşleştirip; bu konular hakkında teknik açıklamalar ve örnek Python kodları içeren sentetik bir veri seti oluşturmanızı sağlar.

Özellikle büyük ölçekli dil modellerini eğitmek veya ince ayar (fine-tuning) yapmak için ihtiyaç duyulan "Instruction-Response" formatında veri üretmek amacıyla geliştirilmiştir.
✨ Temel Özellikler

    Otomatik JSON Çıktısı: Modelden gelen ham veriyi temizleyip belirli bir JSON şemasına sokar.

    Token Bazlı Gruplandırma: Üretilen kodları token uzunluklarına göre (128, 256, 512, 1024 vb.) otomatik kategorize eder.

    Hata Payı Yönetimi: Geçersiz JSON çıktılarını ayıklar.

    Kaldığı Yerden Devam Etme: output_base dosyasını kontrol ederek daha önce işlenmiş konuları atlar, böylece yarıda kalan işlemleri güvenle devam ettirmenize olanak tanır.

    Esnek Donanım Desteği: 4bit, 8bit, 16bit ve 32bit hassasiyet seçenekleriyle farklı VRAM kapasitelerine sahip GPU'larda çalışabilir.

🛠 Kurulum ve Gereksinimler

Gerekli kütüphaneleri yükleyin:
code Bash

pip install torch transformers tqdm

⚙️ Yapılandırma

Config sınıfı içerisinden kendi sisteminize göre şu ayarları yapabilirsiniz:

    INPUT_FILE: Veri setinizin bulunduğu .jsonl dosyası.

    OUTPUT_BASE: Çıktı dosyalarınızın kaydedileceği dizin ve ön ek.

    PRECISION: GPU VRAM durumunuza göre 4bit, 8bit veya 16bit seçimi yapın.

    BATCH_SIZE: GPU belleğine göre aynı anda kaç örnek işleneceğini belirler.

🚀 Kullanım

    Veri setinizi 100k_ingilizce_turkce.jsonl formatında hazırlayın (içerisinde ingilizce ve turkce anahtarları olmalıdır).

    Kod içerisindeki dosya yollarını (özellikle /kaggle/ yollarını) kendi yerel dizin yapınıza göre güncelleyin.

    Çalıştırın:
    code Bash

    python main.py

📊 Çıktı Yapısı

Program, veriyi token uzunluklarına göre klasörleyerek _128.jsonl, _256.jsonl vb. dosyalar oluşturur. Her satır şu formattadır:
code JSON

{
  "ingilizce": "Topic Name",
  "turkce": "Topic Name için örnek bir uygulama yazarmısın",
  "explanation": "Teknik açıklama burada yer alır...",
  "python": ["```python\nprint('Kod buraya gelir')\n```"]
}

⚠️ Dikkat Edilmesi Gerekenler

    VRAM Kullanımı: 4bit veya 8bit kullanmak büyük modelleri tüketici sınıfı kartlarda (örn. RTX 3060/4060) çalıştırmanıza olanak tanır.

    Sistem Talimatı: system_instruction değişkeni, modelin çıktı formatını belirler. Eğer model JSON formatını bozarsa bu talimatı daha katı hale getirebilirsiniz.

📝 Lisans

Bu proje [MIT Lisansı] altında sunulmuştur.
