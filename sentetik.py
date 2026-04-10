# -*- coding: utf-8 -*-
import torch
import json
import os
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# ================= KONFIGÜRASYON =================
class Config:
    INPUT_FILE = "/100k_ingilizce_turkce.jsonl"
    OUTPUT_BASE = "/finetune_code_tr"
    LOG_FILE = "//log_code_tr.txt"
    MODEL_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"
    
    # Precision Ayarları
    PRECISION = "16bit"   #32bit, 16bit, 8bit, 4bit gpu vram için uygun birini seçmelisin. unutma BATCH_SIZE ı seçeneklere göre azalt veya çoğalt.
    
    # Model Üretim Parametreleri
    BATCH_SIZE = 20       #aynı anda kaç örnek işleyeceksin vram boyutuna göre düşünmelisin.
    MAX_NEW_TOKENS = 1024 # üretimde 1024 kullanabilirsin böylece token sayısına göre veri setine ölçek belirlersin.
    DO_SAMPLE = True      #Farklı örnekler üretmek için kesinlikle gerekli. False bırakırsan model tembeleşebilir ve papağan gibi olur.
    TEMPERATURE = 0.7     #Sıcaklığa göre token üretimi artar. 0.7 civarı tutarsan 512 / 768 arasında ciddi üretim yapabilirsin.
    TOP_P = 0.9
    REPETITION_PENALTY = 1.1
    
    MAX_SAMPLES = None    #Üretmek istediğin veri sayısını girebilirsin.
    DEBUG_MODE = False    #üretimi yavaşlatıyor bence debug konusuna üretimden sonra bakabilirsin. üretilen kodlarda hata varmı ? kontrol önemli.
    
    TOKEN_CATEGORIES = {128: "_128.jsonl", 256: "_256.jsonl", 384: "_384.jsonl", 512: "_512.jsonl", 768: "_768.jsonl", 1024: "_1024.jsonl"}

# ================= FONKSİYONLAR =================
def setup_logging():
    with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n# --- Yeni Oturum: {datetime.now()} ---\n")

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def load_dataset(filepath):
    topics, translation_map = [], {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    eng, tr = data.get("ingilizce"), data.get("turkce")
                    if eng and tr:
                        topics.append(eng)
                        translation_map[eng] = tr
                except: continue
    return topics, translation_map

def load_processed_topics(output_base):
    processed = set()
    all_path = output_base + "_all.jsonl"
    if os.path.exists(all_path):
        with open(all_path, "r", encoding="utf-8") as f:
            for line in f:
                try: processed.add(json.loads(line).get("ingilizce"))
                except: continue
    return processed

def extract_json(text: str):
    try:
        start, end = text.find('{'), text.rfind('}') + 1
        if start == -1 or end <= start: return None
        data = json.loads(text[start:end])
        if all(k in data for k in ("ingilizce", "explanation", "python")) and isinstance(data["python"], list):
            return data
    except: return None
    return None

def write_to_category(record: dict, token_count: int, all_f, category_files: dict):
    json_line = json.dumps(record, ensure_ascii=False) + "\n"
    all_f.write(json_line)
    for limit in sorted(Config.TOKEN_CATEGORIES.keys()):
        if token_count <= limit:
            category_files[limit].write(json_line)
            category_files[limit].flush()
            return limit
    max_limit = max(Config.TOKEN_CATEGORIES.keys())
    category_files[max_limit].write(json_line)
    category_files[max_limit].flush()
    return max_limit

# ================= MODEL YÜKLEME =================
print("Model yükleniyor...")
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_ID, trust_remote_code=True, padding_side='left')
tokenizer.pad_token = tokenizer.eos_token

model_kwargs = {"device_map": "balanced", "trust_remote_code": True} #Çift gpu varsa Kesinlikle ,"device_map": "balanced", kullan. tek gpuda auto kullan. yada sola yasla.
if Config.PRECISION == "32bit": model_kwargs["torch_dtype"] = torch.float32
elif Config.PRECISION == "16bit": model_kwargs["torch_dtype"] = torch.float16
elif Config.PRECISION == "8bit": model_kwargs["load_in_8bit"] = True
elif Config.PRECISION == "4bit": model_kwargs["load_in_4bit"] = True

model = AutoModelForCausalLM.from_pretrained(Config.MODEL_ID, **model_kwargs)
model.eval()

# ================= ANA DÖNGÜ =================
def main():
    setup_logging()
    topics, translation_map = load_dataset(Config.INPUT_FILE)
    processed = load_processed_topics(Config.OUTPUT_BASE)
    remaining = [t for t in topics if t not in processed]
    if Config.MAX_SAMPLES: remaining = remaining[:Config.MAX_SAMPLES]
    
    log_message(f"✅ Kalan görev sayısı: {len(remaining)}")

    category_files = {limit: open(Config.OUTPUT_BASE + suffix, "a", encoding="utf-8") for limit, suffix in Config.TOKEN_CATEGORIES.items()}
    all_file = open(Config.OUTPUT_BASE + "_all.jsonl", "a", encoding="utf-8")

    system_instruction = (
        "You are an expert coding assistant. Provide a technical explanation and Python code for the topic. "
        "Return ONLY a valid JSON object. Do not output any markdown text other than the JSON itself.\n\n"
        "Output Format:\n"
        '{"ingilizce": "...", "explanation": "...", "python": ["```python\\n...\\n```"]}'
    )

    successful, failed = 0, 0
    cat_success = {limit: 0 for limit in Config.TOKEN_CATEGORIES}

    try:
        for i in tqdm(range(0, len(remaining), Config.BATCH_SIZE)):
            batch = remaining[i:i+Config.BATCH_SIZE]
            messages = [[{"role": "system", "content": system_instruction}, {"role": "user", "content": t}] for t in batch]
            texts = [tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True) for m in messages]
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, 
                    max_new_tokens=Config.MAX_NEW_TOKENS, 
                    do_sample=Config.DO_SAMPLE, 
                    temperature=Config.TEMPERATURE, 
                    top_p=Config.TOP_P, 
                    repetition_penalty=Config.REPETITION_PENALTY,
                    pad_token_id=tokenizer.pad_token_id, 
                    eos_token_id=tokenizer.eos_token_id
                )
            
            input_len = inputs['input_ids'].shape[1]
            for j, gen_ids in enumerate(outputs):
                output_ids = gen_ids[input_len:]
                num_tokens = len([t for t in output_ids if t not in (tokenizer.pad_token_id, tokenizer.eos_token_id)])
                
                json_obj = extract_json(tokenizer.decode(output_ids, skip_special_tokens=True))
                if json_obj:
                    tr = translation_map.get(batch[j], "")
                    record = {
                        "ingilizce": batch[j],
                        "turkce": f"{tr} için örnek bir uygulama yazarmısın" if tr else "",
                        "explanation": json_obj["explanation"],
                        "python": json_obj["python"]
                    }
                    limit = write_to_category(record, num_tokens, all_file, category_files)
                    cat_success[limit] += 1
                    successful += 1
                else: failed += 1
    finally:
        all_file.close()
        for f in category_files.values(): f.close()
        
        log_message(f"İşlem Bitti. Başarılı: {successful}, Başarısız: {failed}")
        if successful > 0:
            log_message("--- Token Dağılım Yüzdeleri ---")
            for limit, count in cat_success.items():
                log_message(f"<= {limit} token: {count} örnek (%{(count / successful) * 100:.1f})")

if __name__ == "__main__":
    main()
