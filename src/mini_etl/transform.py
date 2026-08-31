from typing import Any, Iterable, Generator, Callable
from .core import Baglanabilir
from .errors import DeadLetterQueue

dlq = DeadLetterQueue() # Hata yakalayıcıyı başlatıyoruz

class Filter(Baglanabilir):
    def __init__(self, kural: Callable[[dict[str, Any]], bool]):
        self.kural = kural
        
    def isle(self, veri_akisi: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in veri_akisi:
            try:
                # Kurala uyan satırları bir sonraki adıma geçirir
                if self.kural(kayit):
                    yield kayit
            except Exception as e:
                dlq.kaydet(kayit, f"Filter hatası: {str(e)}")

class Rename(Baglanabilir):
    def __init__(self, harita: dict[str, str]):
        self.harita = harita
        
    def isle(self, veri_akisi: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in veri_akisi:
            yeni_kayit = {}
            for anahtar, deger in kayit.items():
                # Haritada yeni isim varsa onu kullan, yoksa eski ismi bırak
                yeni_isim = self.harita.get(anahtar, anahtar)
                yeni_kayit[yeni_isim] = deger
            yield yeni_kayit

class Cast(Baglanabilir):
    def __init__(self, tipler: dict[str, type]):
        self.tipler = tipler
        
    def isle(self, veri_akisi: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in veri_akisi:
            yeni_kayit = kayit.copy()
            hata_var = False
            for alan, tip in self.tipler.items():
                if alan in yeni_kayit:
                    try:
                        yeni_kayit[alan] = tip(yeni_kayit[alan])
                    except ValueError as e:
                        dlq.kaydet(kayit, f"Tip dönüşüm hatası ({alan}): {str(e)}")
                        hata_var = True
                        break
            
            if not hata_var:
                yield yeni_kayit

class Map(Baglanabilir):
    def __init__(self, islem: Callable[[dict[str, Any]], dict[str, Any]]):
        self.islem = islem
        
    def isle(self, veri_akisi: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in veri_akisi:
            try:
                yield self.islem(kayit.copy())
            except Exception as e:
                dlq.kaydet(kayit, f"Map hatası: {str(e)}")

class Validate(Baglanabilir):
    def __init__(self, kural: Callable[[dict[str, Any]], bool]):
        self.kural = kural
        
    def isle(self, veri_akisi: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for kayit in veri_akisi:
            try:
                if self.kural(kayit):
                    yield kayit
                else:
                    dlq.kaydet(kayit, "Doğrulama (Validate) kuralına uymadı.")
            except Exception as e:
                dlq.kaydet(kayit, f"Validate kural hatası: {str(e)}")