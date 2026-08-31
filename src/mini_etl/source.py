import csv
import json
import time
import urllib.request
from urllib.error import URLError
from pathlib import Path
from typing import Generator, Any
from .core import Baglanabilir

class DosyaKaynagi(Baglanabilir):
    def __init__(self, dosya_yolu: str):
        self.dosya_yolu = Path(dosya_yolu)
        if not self.dosya_yolu.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {dosya_yolu}")

    def oku(self) -> Generator[dict[str, Any], None, None]:
        uzanti = self.dosya_yolu.suffix.lower()
        
        with open(self.dosya_yolu, "r", encoding="utf-8") as dosya:
            if uzanti == ".jsonl":
                for satir_no, satir in enumerate(dosya, start=1):
                    satir = satir.strip()
                    if not satir:
                        continue 
                    try:
                        yield json.loads(satir)
                    except json.JSONDecodeError as e:
                        print(f"Uyarı: {satir_no}. satır atlandı (Bozuk JSON).")
            
            elif uzanti == ".csv":
                okuyucu = csv.DictReader(dosya)
                for csv_satiri in okuyucu:
                    yield dict(csv_satiri)
            
            else:
                raise ValueError(f"Desteklenmeyen format: {uzanti}. CSV veya JSONL gerekli.")

class HttpApiKaynagi(Baglanabilir):
    def __init__(self, url: str, maks_deneme: int = 3):
        self.url = url
        self.maks_deneme = maks_deneme

    def oku(self) -> Generator[dict[str, Any], None, None]:
        deneme = 0
        bekleme = 1 

        while deneme < self.maks_deneme:
            try:
                istek = urllib.request.Request(self.url)
                with urllib.request.urlopen(istek) as yanit:
                    veri = json.loads(yanit.read().decode('utf-8'))
                    if isinstance(veri, list):
                        for kayit in veri:
                            yield kayit
                    else:
                        yield veri
                return 
            
            except URLError as e:
                deneme += 1
                print(f"API Bağlantı Hatası: {e}. {bekleme} saniye sonra tekrar deneniyor... (Deneme {deneme}/{self.maks_deneme})")
                time.sleep(bekleme)
                bekleme *= 2 

        raise ConnectionError(f"API'ye {self.maks_deneme} deneme sonrası ulaşılamadı: {self.url}")