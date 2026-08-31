import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.mini_etl.source import DosyaKaynagi
from src.mini_etl.transform import Filter, Cast, Rename
from src.mini_etl.sink import DosyaHedefi
from src.mini_etl.engine import boru_hattini_calistir

def test_tam_boru_hatti_entegrasyonu():
    kaynak = DosyaKaynagi("test_veri.jsonl")
    filtre = Filter(lambda x: int(x.get("yas", 0)) > 18)
    tip_degisim = Cast({"yas": int})
    isim_degisim = Rename({"ad": "isim"})
    hedef = DosyaHedefi("test_entegrasyon_sonuc.csv")
    
    # Tüm lego parçalarını birleştir ve motoru çalıştır
    pipeline = kaynak >> filtre >> tip_degisim >> isim_degisim >> hedef
    boru_hattini_calistir(pipeline)
    
    # İşlemin başarılı olup çıktının oluştuğunu doğrula
    assert os.path.exists("test_entegrasyon_sonuc.csv")