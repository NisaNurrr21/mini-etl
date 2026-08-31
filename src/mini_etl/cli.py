import typer
import yaml
from typing import Any
from .source import DosyaKaynagi
from .transform import Filter, Rename, Cast
from .sink import DosyaHedefi
from .engine import boru_hattini_calistir

app = typer.Typer(help="Mini ETL Framework CLI Aracı")

@app.callback()
def callback() -> None:
    """Ana CLI Giriş Noktası"""
    pass

@app.command()
def run(config: str = typer.Option(..., "--config", help="YAML yapılandırma dosyası yolu")) -> None:
    typer.echo(f"ETL süreci başlatılıyor... Okunan ayar dosyası: {config}")
    
    with open(config, "r", encoding="utf-8") as dosya:
        ayarlar = yaml.safe_load(dosya)
    
    adimlar: list[Any] = []
    
    # 1. Kaynak (Source)
    adimlar.append(DosyaKaynagi(ayarlar["source"]["path"]))
    
    # 2. Dönüşümler (Transforms)
    for ayar in ayarlar.get("transforms", []):
        if ayar["type"] == "filter":
            sart = str(ayar["condition"])
            
            # Lambda yerine tam tipli alt fonksiyon tanımlandı (Mypy hatasını çözer)
            def filtre_kurali(x: dict[str, Any], s: str = sart) -> bool:
                temiz_veri = {k: int(v) if str(v).isdigit() else v for k, v in x.items()}
                return bool(eval(s, {}, temiz_veri))
                
            adimlar.append(Filter(filtre_kurali))
            
        elif ayar["type"] == "cast":
            tip_haritasi = {alan: eval(tip) for alan, tip in ayar["fields"].items()}
            adimlar.append(Cast(tip_haritasi))
            
        elif ayar["type"] == "rename":
            adimlar.append(Rename(ayar["mapping"]))
            
    # 3. Hedef (Sink)
    adimlar.append(DosyaHedefi(ayarlar["sink"]["path"]))
    
    # 4. Motoru Ateşleme
    pipeline = adimlar[0]
    for adim in adimlar[1:]:
        pipeline = pipeline >> adim
        
    try:
        boru_hattini_calistir(pipeline)
        typer.echo(f"ETL süreci başarıyla tamamlandı! Çıktı: {ayarlar['sink']['path']}")
    except Exception as e:
        typer.echo(f"Süreç sırasında hata oluştu: {str(e)}", err=True)

if __name__ == "__main__":
    app()