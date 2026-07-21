# CSV & API Data Extraction (ETL Pipeline)

Bu layihə, həm yerli **CSV** fayllarından (`diamonds.csv`), həm də xarici **API** mənbələrindən məlumatları çəkib (Extract), təmizləyib transformasiya edən (Transform) və hədəf verilənlər bazasına yükləyən (Load) avtomatlaşdırılmış bir ETL data pipeline platformasıdır. Layihə izolyasiya olunmuş Docker mühitində işləyəcək şəkildə konfiqurasiya edilmişdir.

## 📁 Layihə Struktur

```text
CSV-API-EXTRACTION/
├── data/
│   └── diamonds.csv        # İşlənəcək yerli dataset faylı
├── docs/                   # Layihə sənədləri
├── src/
│   ├── __init__.py
│   ├── api_reader.py       # API-dən məlumatların çəkilməsi (Extract)
│   ├── csv_reader.py       # CSV faylından məlumatların oxunması (Extract)
│   ├── transformer.py      # Məlumatların təmizlənməsi və manipulyasiyası (Transform)
│   ├── load.py             # Məlumatların verilənlər bazasına yazılması (Load)
│   └── main.py             # ETL axınını idarə edən və işə salan əsas skript
├── .env                    # Həssas məlumatlar və baza bağlantı şifrələri (Git-ə yüklənmir)
├── .gitignore              # Git tərəfindən izlənilməyəcək faylların siyahısı (venv, .env və s.)
├── docker-compose.yml      # Konteynerləşdirilmiş mühit konfiqurasiyası
├── requirements.txt        # Layihə üçün lazımi Python paketləri
└── README.md               # Layihə barədə ümumi məlumat sənədi 


## 🛠️ Texnologiyalar və Kitabxanalar
Python 3.x

Pandas & NumPy — Məlumatların transformasiyası və analizi üçün

Requests — API çağırışlarının edilməsi üçün

Docker & Docker Compose — Mühitin standartlaşdırılması üçün


## 🚀 Quraşdırma və İşə Salma

# Repozitoriyanı klonlayın
git clone [https://github.com/xumarbaghiyeva-111/ETL-engineering-project.git](https://github.com/xumarbaghiyeva-111/ETL-engineering-project.git)
cd ETL-engineering-project

# Virtual mühiti aktivləşdirin
python -m venv venv

# Windows üçün:
venv\Scripts\activate
# macOS/Linux üçün:
source venv/bin/activate

# Lazımi paketləri yükləyin
pip install -r requirements.txt

# Docker konteynerlərini qaldırın
docker-compose up --build

# Və ya lokal olaraq işə salın
python src/main.py


## ⚙️ ETL Prosesinin İşləmə Prinsipi
Extract: csv_reader.py və api_reader.py skriptləri müvafiq mənbələrdən xam məlumatları götürür.

Transform: transformer.py daxilində məlumat tipləri düzəldilir, lazımsız sütunlar kənarlaşdırılır və verilənlər analizə uyğun formata salınır.

Load: load.py təmizlənmiş yekun məlumatları hədəf bazaya yazır.

Main: Bütün bu proses main.py skripti tərəfindən ardıcıl olaraq idarə olunur.
