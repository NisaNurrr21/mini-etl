from typing import Any, Iterable, Generator, Protocol

# Tüm dönüştürücülerin uyması gereken zorunlu şablon (Protocol)
class TransformProtocol(Protocol):
    def isle(self, veri: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        ...

# >> operatörü ile ETL adımlarını birbirine zincirleyen temel sınıf
class Baglanabilir:
    def __rshift__(self, sonraki_adim: Any) -> Any:
        # Kendisini ve sonraki adımı bir Pipeline içinde birleştirir
        return Pipeline(self, sonraki_adim)

class Pipeline:
    def __init__(self, mevcut_adim: Any, sonraki_adim: Any):
        self.adımlar: list[Any] = []
        
        # Eğer mevcut adım zaten bir zincirse, onu genişlet
        if isinstance(mevcut_adim, Pipeline):
            self.adımlar.extend(mevcut_adim.adımlar)
        else:
            self.adımlar.append(mevcut_adim)
            
        self.adımlar.append(sonraki_adim)

    def __rshift__(self, sonraki_adim: Any) -> 'Pipeline':
        # Yeni eklenen adımları zincire dahil etmeye devam eder
        return Pipeline(self, sonraki_adim)