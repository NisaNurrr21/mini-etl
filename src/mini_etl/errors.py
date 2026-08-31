import json
from pathlib import Path
from typing import Any

class DeadLetterQueue:
    def __init__(self, dosya_yolu: str = "dead_letter.jsonl"):
        self.dosya_yolu = Path(dosya_yolu)
        
    def kaydet(self, kayit: Any, hata_mesaji: str) -> None:
        # Hatalı satırı sistemi durdurmadan karantina dosyasına ekler
        with open(self.dosya_yolu, "a", encoding="utf-8") as dosya:
            hata_raporu = {"hata": hata_mesaji, "veri": str(kayit)}
            dosya.write(json.dumps(hata_raporu) + "\n")