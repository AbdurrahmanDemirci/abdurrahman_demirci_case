# Data Katmanı

> **Kapsam**: `ui_tests/data/`
> **Dosya**: `expected_content.py`

---

## Amaç

Test assertion'larında kullanılan beklenen değerler (string sabitler) test dosyasına gömülmez.
Bunun yerine `ui_tests/data/expected_content.py`'de merkezi olarak tutulur.

---

## Mevcut Sabitler

```python
# ui_tests/data/expected_content.py

EXPECTED_HOME_TITLE_KEYWORD      = "Insider"
EXPECTED_JOB_DEPARTMENT          = "Quality Assurance"
EXPECTED_JOB_POSITION_KEYWORDS   = ("Quality Assurance", "QA")
EXPECTED_JOB_LOCATION            = "Istanbul"
```

---

## Kullanım

```python
from ui_tests.data.expected_content import (
    EXPECTED_HOME_TITLE_KEYWORD,
    EXPECTED_JOB_DEPARTMENT,
    EXPECTED_JOB_POSITION_KEYWORDS,
    EXPECTED_JOB_LOCATION,
)

assert EXPECTED_JOB_DEPARTMENT in first["department"]
assert any(kw in first["position"] for kw in EXPECTED_JOB_POSITION_KEYWORDS)
```

---

## Kural

| Buraya girer | Buraya girmez |
|--------------|---------------|
| Assertion'da karşılaştırılan string sabitler | URL'ler (`config.py`'da) |
| Keyword tuple'ları | Browser / wait ayarları |
| Başlık keyword'leri | Selector / locator |

URL'ler `.env` destekli olduğu için `config.py`'da kalır — `data/` katmanına taşınmaz.

---

## Yeni Sabit Eklerken

1. `ui_tests/data/expected_content.py`'e sabiti ekle
2. Test dosyasında import et — inline string yazma
