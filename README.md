🚀 Qwen2.5-Coder: Token Bazlı Akıllı Veri Seti Üreticisi

💡 Neden Kategorize Ediyorum?


Veri seti oluştururken, ürettiğim içeriklerin 128 ile 1024+ token arasında çok geniş bir yelpazeye yayıldığını fark ettim. 
Eğitim sırasında, kısa bir fonksiyonu (örneğin 128 token) 1024 token uzunluğunda bir bağlam penceresiyle eğitmenin, 
GPU kaynaklarını gereksiz yere tükettiğini ve modelin öğrenme verimini düşürdüğünü gözlemledim.

Veri setimi inceledikçe, üretilen veriyi token aralıklarına göre kategorize etmenin; 
modelin "cortex" yapısını (öğrenme derinliğini) kademeli olarak büyütmek için en mantıklı yol olduğuna kanaat getirdim.

Stratejim:

    Başlangıç Eğitimi (128/256 Token): Temel mantık ve kısa kod parçacıkları.

    Gelişim Aşaması (384/512 Token): Orta seviye modüller ve algoritmik yapılar.

    Final (768/1024+ Token): Karmaşık projeler ve detaylı sınıf mimarileri.

Bu kademeli geçişin, modelin çok daha kararlı ve düşük maliyetli eğitileceğine inanıyorum. 
Henüz kesin bir akademik ispatım yok, ancak bu yöntemle deneme-yanılma süreçlerini daha verimli hale getirebilirim.


Stratejim:

    Başlangıç Eğitimi (128/256 Token): Temel mantık ve kısa kod parçacıkları.

    Gelişim Aşaması (384/512 Token): Orta seviye modüller ve algoritmik yapılar.

    Final (768/1024+ Token): Karmaşık projeler ve detaylı sınıf mimarileri.
    

Bu kademeli geçişin, modelin çok daha kararlı ve düşük maliyetli eğitileceğine inanıyorum. 
Henüz kesin bir ispatım yok, ancak bu yöntemle deneme-yanılma süreçlerini daha verimli hale getirebilirim.


⚡ Scriptin Özellikleri


    Akıllı Gruplandırma: Veriyi token limitlerine göre _128, _256, _512, _1024 dosyalarına otomatik böler.

    Kaldığı Yerden Devam: output_base dosyasını kontrol eder; yarıda kalan işlemleri tqdm ile takip ederek süreci kaldığı yerden devam ettirir.

    JSON Güvenliği: extract_json fonksiyonu ile modelin çıktısındaki gürültüyü (markdown, konuşma metni) temizler, sadece temiz JSON verisini kaydeder.

    Donanım Optimizasyonu: 4bit, 8bit, 16bit seçenekleri ile VRAM kullanımını yönetmenizi sağlar.
    

📥 Veri Seti Hazırlığı

INPUT_FILE yolundaki dosyanız JSONL formatında olmalıdır. 
Her satır bir görev içerir:

code JSON

{"ingilizce": "How to implement QuickSort?", "turkce": "QuickSort nasıl yazılır?"}
{"ingilizce": "Write a Python class for a library", "turkce": "Kütüphane için sınıf yaz"}

📊 Token Dağılımı ve Kategoriler

Dosya Ön Eki	Token Limiti	Eğitim Aşaması

_128.jsonl	128	Başlangıç (Temel)

_256.jsonl	256	Başlangıç (Temel)

_512.jsonl	512	Gelişim (Orta)

_1024.jsonl	1024	Sonuç (İleri)


⚙️ Hızlı Kurulum


    Bağımlılıkları Yükleyin:
    
    code Bash
    

pip install -r requirements.txt


Ayarları Yapın:

Config sınıfından PRECISION ve BATCH_SIZE değerlerini donanımınıza göre düzenleyin.


Çalıştırın:

code Bash


    python sentetik.py
    

🛠 Çıktı Formatı


Script, her bir görevi şu formatta kayıt altına alır:

code JSON


{

  "ingilizce": "...",
  
  "turkce": "... için örnek bir uygulama yazarmısın",
  
  "explanation": "Teknik açıklama...",
  
  "python": ["```python\n# kodlar...\n```"]
  
}



