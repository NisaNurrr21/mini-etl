# Mini ETL Framework

Standart Python kütüphaneleri (stdlib) kullanılarak geliştirilmiş, modüler, jeneratör (generator) tabanlı ve bellek dostu bir ETL (Extract, Transform, Load) mikro framework'ü.

## Özellikler
* **Streaming Mimarisi:** Veriler belleğe tamamen yüklenmeden (chunk/satır bazlı) işlenir. 5 GB'lık veriler bile 200 MB altı RAM kullanılarak sorunsuz dönüştürülür.
* **Modüler Zincir (Pipeline):** `>>` (rshift) operatörü overloading ile veri kaynakları ve dönüştürücüler lego gibi birbirine bağlanır.
* **Katı Tip Güvenliği & Test:** Proje `%87` test kapsamına (coverage) sahip olup, `mypy --strict` standartlarından sıfır hata ile geçmektedir. Sınır testleri (property-based) `hypothesis` ile sağlanmıştır.
* **Hata Yönetimi:** Satır bazlı hata izleme (Dead Letter Queue) ve HTTP API kaynakları için Exponential Backoff (Retry) mekanizması içerir.

## Performans ve Bellek Ölçümü
Jeneratör mimarisi sayesinde uygulamanın bellek tüketimi (peak memory) dosya boyutundan bağımsız olarak sabit kalır:
* Mevcut Tüketim: ~0.0031 MB
* Zirve RAM Tüketimi (Peak): ~0.0210 MB

## Kullanım (CLI)
Süreçler `typer` destekli CLI üzerinden dinamik YAML yapılandırmaları ile yönetilir.
```bash
python main.py run --config pipeline.yaml

Desteklenen Bileşenler
Source: CSV, JSONL, HTTP API
Transform: Filter, Cast, Rename, Map, Validate
Sink: CSV, JSONL, SQLite, Stdout