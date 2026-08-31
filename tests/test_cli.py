import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typer.testing import CliRunner
from src.mini_etl.cli import app

runner = CliRunner()

def test_cli_basarili_calisma():
    # Terminal komutunu simüle ederek tüm CLI sürecini baştan sona test eder
    sonuc = runner.invoke(app, ["run", "--config", "pipeline.yaml"])
    
    assert sonuc.exit_code == 0
    assert "başarıyla tamamlandı" in sonuc.stdout
    assert os.path.exists("sonuc_dinamik.csv")