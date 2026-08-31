import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from hypothesis import given, strategies as st
from src.mini_etl.transform import Cast, Rename

# 1. Cast (Tip Dönüşümü) Sınır Testi
@given(st.integers())
def test_cast_integer_property(rastgele_sayi):
    donusturucu = Cast({"deger": int})
    veri = [{"deger": str(rastgele_sayi)}]
    sonuc = list(donusturucu.isle(veri))
    assert sonuc[0]["deger"] == rastgele_sayi

# 2. Rename (Yeniden Adlandırma) Sınır Testi
@given(st.text(min_size=1), st.text(min_size=1), st.integers())
def test_rename_property(eski_isim, yeni_isim, rastgele_deger):
    # Rastgele isim çakışmalarını önle
    if eski_isim == yeni_isim: return 
    
    adlandirici = Rename({eski_isim: yeni_isim})
    veri = [{eski_isim: rastgele_deger}]
    sonuc = list(adlandirici.isle(veri))
    assert yeni_isim in sonuc[0]
    assert sonuc[0][yeni_isim] == rastgele_deger

# 3. Hata Yönetimi Sınır Testi
@given(st.text(alphabet=st.characters(exclude_categories=["Nd"]))) # Rakam içermeyen metinler
def test_cast_error_handling(hatali_metin):
    donusturucu = Cast({"deger": int})
    veri = [{"deger": hatali_metin}]
    sonuc = list(donusturucu.isle(veri))
    # Hatalı veri dönüştürülemeyeceği için liste boş dönmeli (Dead Letter'a düşer)
    assert len(sonuc) == 0