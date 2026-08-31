import csv
import json
import sys
import sqlite3
from pathlib import Path
from typing import Any, Iterable
from .core import Baglanabilir

class DosyaHedefi(Baglanabilir):
    def __init__(self, dosya_yolu: str):
        self.dosya_yolu = dosya_yolu

    def yaz(self, veri_akisi: Iterable[dict[str, Any]]) -> None:
        # Eğer terminal ekranına yazdırılmak istenirse (stdout)
        if self.dosya_yolu == "stdout":
            for kayit in veri_akisi:
                print(json.dumps(kayit))
            return

        hedef_yolu = Path(self.dosya_yolu)
        uzanti = hedef_yolu.suffix.lower()
        
        with open(hedef_yolu, "w", encoding="utf-8") as dosya:
            if uzanti == ".jsonl":
                for kayit in veri_akisi:
                    dosya.write(json.dumps(kayit) + "\n")
            
            elif uzanti == ".csv":
                # Veri akışını (generator) başlat ve ilk kaydı alarak sütun isimlerini belirle
                iterator = iter(veri_akisi)
                try:
                    ilk_kayit = next(iterator)
                except StopIteration:
                    return # Veri yoksa işlem yapma
                
                # CSV başlıklarını yaz ve geri kalan veriyi akıtmaya devam et
                yazici = csv.DictWriter(dosya, fieldnames=ilk_kayit.keys())
                yazici.writeheader()
                yazici.writerow(ilk_kayit)
                for kayit in iterator:
                    yazici.writerow(kayit)
            else:
                raise ValueError(f"Desteklenmeyen hedef formatı: {uzanti}")

class SqliteHedefi(Baglanabilir):
    def __init__(self, db_yolu: str, tablo_adi: str = "veriler"):
        self.db_yolu = db_yolu
        self.tablo_adi = tablo_adi

    def yaz(self, veri_akisi: Iterable[dict[str, Any]]) -> None:
        iterator = iter(veri_akisi)
        try:
            ilk_kayit = next(iterator)
        except StopIteration:
            return

        sutunlar = list(ilk_kayit.keys())
        # Dinamik olarak tablo oluşturmak için sütun isimlerini SQL formatına çeviriyoruz
        sutun_tanimlari = ", ".join([f"{s} TEXT" for s in sutunlar])
        soru_isaretleri = ", ".join(["?"] * len(sutunlar))
        
        with sqlite3.connect(self.db_yolu) as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(f"CREATE TABLE IF NOT EXISTS {self.tablo_adi} ({sutun_tanimlari})")
            
            # İlk kaydı ve jeneratörden akmaya devam eden diğer kayıtları veritabanına yaz
            imlec.execute(f"INSERT INTO {self.tablo_adi} VALUES ({soru_isaretleri})", tuple(ilk_kayit.values()))
            for kayit in iterator:
                imlec.execute(f"INSERT INTO {self.tablo_adi} VALUES ({soru_isaretleri})", tuple(kayit.values()))
            
            baglanti.commit()