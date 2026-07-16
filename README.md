# Data Engineering Pipeline - Tapşırıq 1: Məlumat Çıxarışı (Extraction)

Bu layihə, Data Engineering kursunun/tapşırığının 1-ci hissəsidir. Layihənin məqsədi fərqli formatlarda olan iki məlumat mənbəyindən (**Yerli CSV faylı** və **Canlı API**) ardıcıl (sequential) və təhlükəsiz şəkildə məlumatın çıxarılmasını (Extract) təmin etməkdir.

---

## 🏗️ Layihə Arxitekturası və İşləmə Məntiqi

Sistem tamamilə modulyar şəkildə qurulmuşdur və aşağıdakı ardıcıllıqla işləyir:

```text
[ diamonds.csv (Yerli Fayl) ] ──(1. Uğurlu Oxunma)──► [ Python Orchestrator ]
                                                            │
                                                     (2. Növbəti Addım)
                                                            │
                                                            ▼
[ jsonplaceholder API (Canlı) ] ◄──(3. HTTP GET)─── [ api_reader Modulu ]   


CSV-API-EXTRACTION/
│
├── data/
│   └── diamonds.csv          # Oxunacaq yerli verilənlər bazası
│
├── src/
│   ├── csv_reader.py         # CSV oxumaq üçün modul
│   ├── api_reader.py         # API-dan məlumat çəkmək üçün modul
│   └── main.py               # Prosesi ardıcıl idarə edən əsas skript
│
├── venv/                     # Python Virtual Environment (Lokal)
├── .gitignore                # Git tərəfindən izlənilməyəcək faylların siyahısı
├── requirements.txt          # Lazımi Python kitabxanaları
└── README.md                 # Layihə sənədləşməsi (Bu fayl)

# Layihəni öz lokal mühitinizdə işə salmaq üçün aşağıdakı addımları izləyin:

git clone https://github.com/xumarbaghiyeva-111/task-1-csv-api-extraction.git
cd task-1-csv-api-extraction

# Virtual mühit yaratmaq üçün
python -m venv venv

# Aktivləşdirmək üçün (Windows)
.\venv\Scripts\activate

# Aktivləşdirmək üçün (macOS/Linux)
source venv/bin/activate



pip install -r requirements.txt



python src/main.py
