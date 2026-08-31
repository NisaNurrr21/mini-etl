import logging
from typing import Any, Iterable, Generator
from .core import Pipeline

# Yapılandırılmış loglama ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

def boru_hattini_calistir(pipeline: Pipeline) -> dict[str, int]:
    logging.info("ETL Pipeline başlatıldı.")
    adimlar = pipeline.adımlar
    
    ozet = {"okunan": 0, "yazilan": 0, "reddedilen": 0}
    
    # 1. Kaynak ve Okuma Sayacı
    kaynak = adimlar[0]
    def okuma_sayici(akis: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in akis:
            ozet["okunan"] += 1
            yield kayit
            
    veri_akisi = okuma_sayici(kaynak.oku())
    
    # 2. Dönüşümler
    for adim in adimlar[1:-1]:
        veri_akisi = adim.isle(veri_akisi)
        
    # 3. Hedef ve Yazma Sayacı
    def yazma_sayici(akis: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in akis:
            ozet["yazilan"] += 1
            yield kayit
            
    hedef = adimlar[-1]
    hedef.yaz(yazma_sayici(veri_akisi))
    
    # 4. Özet Raporu
    ozet["reddedilen"] = ozet["okunan"] - ozet["yazilan"]
    logging.info(f"Çalıştırma Özeti -> Okunan: {ozet['okunan']} | Yazılan: {ozet['yazilan']} | Reddedilen: {ozet['reddedilen']}")
    
    return ozet