# Load Test — Locust Senaryo Skill'i

> **Slash Komutu**: `/Insider-load-test`
> **Amac**: Herhangi bir web uygulamasinda davranis odakli yukle testi calistirir ve sonuclari analiz eder.

---

## Referanslar

- `../project-config.md` → Proje dizin yapisi

---

## Mimari — Buyumeye Acik Tasarim

Bu mimari herhangi bir projeye uygulanabilir. `load_tests/` altindaki her katman tek sorumludur.

```
load_tests/
├── locustfile.py              ← Giris noktasi (ince, senaryo icermez)
├── locust.conf                ← Varsayilan CLI parametreleri (project root'ta)
├── config.py                  ← Ortamlar, esik degerler, think time
├── data/
│   └── <domain>_data.py       ← Tum test verisi ve assertion sabitleri
├── utils/
│   ├── base_task_set.py       ← BaseTaskSet: on_start + on_stop (paylasimlari)
│   ├── logger.py              ← Bagimsiz logger (sys.path catismasini onler)
│   └── response_validator.py  ← Merkezi validasyon + P95 esik kontrolleri
└── scenarios/
    ├── __init__.py            ← Senaryo siniflarini kayit eder
    └── <senaryo_adi>.py       ← Her kullanici tipi ayri dosya
```

**Yeni senaryo**: `scenarios/` altina yeni dosya + `__init__.py`'e 1 import. Baska dosya degismez.

**Yeni ortam**: `config.py`'deki `ENVIRONMENTS` dict'ine 1 satir + `LOAD_TEST_ENV=staging`.

**Yeni test verisi / assertion sabiti**: `data/<domain>_data.py`'e 1 satir.

---

## BaseTaskSet Kalıbı

Tum `TaskSet` siniflari `BaseTaskSet`'ten miras alir — `on_start` ve `on_stop` tekrar yazılmaz.

```python
# load_tests/utils/base_task_set.py
class BaseTaskSet(TaskSet):
    def on_start(self) -> None:
        try:
            with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
                validate_homepage_response(resp)
        except Exception as e:
            logger.warning(f"on_start homepage check skipped: {e}")

    def on_stop(self) -> None:
        logger.info(f"{self.__class__.__name__} session ended.")
```

**Neden try/except**: CI ortamlarinda hedef site baglantıyı reddedebilir. Exception `on_start`'ta yakalanmazsa user crash olur, hic task calismaz.

**SequentialTaskSet icin**: `BaseTaskSet(TaskSet)`'ten miras alinamaz. Ayri `BaseSequentialTaskSet(SequentialTaskSet)` yapilir ya da on_start/on_stop yazilmaz (ilk @task zaten setup gorevi gorur).

---

## Senaryo Sablonu

```python
# load_tests/scenarios/my_scenario.py
import random
from locust import HttpUser, between, tag, task
from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.utils.base_task_set import BaseTaskSet
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import validate_search_response

logger = get_logger(__name__)


class MyScenarioTasks(BaseTaskSet):

    @tag("smoke")
    @task
    def my_action(self) -> None:
        with self.client.get(
            "/path",
            headers=DEFAULT_HEADERS,
            name="/[my-action]",    # raporda gorulecek isim
            catch_response=True,
        ) as resp:
            validate_search_response(resp)
            logger.info(f"Action | status={resp.status_code} | {resp.elapsed.total_seconds():.2f}s")


class MyScenarioUser(HttpUser):
    host      = BASE_URL
    weight    = 1
    tasks     = [MyScenarioTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
```

```python
# load_tests/scenarios/__init__.py — sadece bu satiri ekle:
from load_tests.scenarios.my_scenario import MyScenarioUser  # noqa: F401
```

---

## Bu Projede Kullanilan Senaryolar (n11.com)

| Sinif | Tags | Flow |
|-------|------|------|
| `CategorySearchUser` (weight=1) | smoke | `/` → `/bilgisayar` |
| `ProductSearchUser` (weight=3) | smoke+regression | `/` → `/arama?q=<keyword>` (popular×5, tech×2, edge×1) |
| `UserJourneyUser` (weight=1) | — | `/` → `/arama?q=<keyword>` → interrupt |

---

## Calistirma Komutlari

```bash
# Default (locust.conf'tan: 1 user, 60s)
locust --headless

# Scale
locust --headless -u 10 -r 2 --run-time 120s

# Smoke tag
locust --headless --tags smoke

# Baska ortam
LOAD_TEST_ENV=staging locust --headless

# HTML rapor
locust --headless --html automation-test-results/locust/locust_report.html --csv automation-test-results/locust/locust

# Web UI (canli grafik)
locust
```

---

## Sonuc Analizi

| Metrik | Kabul Edilebilir | Dikkat |
|--------|-----------------|--------|
| Failure rate | %0 | >%1 |
| Homepage avg | <2000ms | >3000ms |
| Arama avg | <1500ms | >3000ms |
| P95 (genel) | <3000ms | >5000ms |

---

## Onemli Kurallar

1. **locustfile.py ince kalir** — senaryo kodu buraya girmez
2. **config.py** — ortam, esik degerleri, think time; test verisi buraya gelmez
3. **Hardcoded string yasak** — response body'de aranan sabitler `data/` katmanina yazilir
4. **Her senaryo bagimsiz dosya** — tek sorumluluk prensibi
5. **Response validation merkezi** — `utils/response_validator.py`; senaryo dosyasinda inline kontrol yok
6. **BaseTaskSet kullan** — `on_start`/`on_stop` her senaryoda tekrar yazilmaz
7. **on_start'ta try/except** — CI'da hedef site baglantıyı reddedebilir; exception yakalanmazsa user crash olur
