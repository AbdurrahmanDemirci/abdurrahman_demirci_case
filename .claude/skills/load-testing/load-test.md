# Load Test — Locust Senaryo Skill'i

> **Slash Komutu**: `/Insider-load-test`
> **Amac**: n11.com search modulu uzerinde davranis odakli yukle testi calistirir ve sonuclari analiz eder.

---

## Referanslar

- `../project-config.md` → Proje dizin yapisi

---

## Mimari — Buyumeye Acik Tasarim

```
load_tests/
├── locustfile.py              ← Giris noktasi (ince, senaryo icermez)
├── locust.conf                ← Varsayilan CLI parametreleri
├── config.py                  ← Ortamlar, esik degerler, think time
├── data/
│   └── search_data.py         ← Tum test verisi ve assertion sabitleri
├── utils/
│   ├── base_task_set.py       ← BaseTaskSet: on_start (homepage) + on_stop (log)
│   └── response_validator.py  ← Merkezi validasyon + P95 esik kontrolleri
└── scenarios/
    ├── __init__.py            ← Senaryo siniflarini kayit eder
    ├── category_search.py     ← Senaryo A: kategori sayfasina gitme   [smoke]
    ├── product_search.py      ← Senaryo B: urun arama → /arama?q=    [smoke+regression]
    └── user_journey.py        ← Senaryo C: sirali kullanici yolculugu
```

**Yeni senaryo eklemek**: `scenarios/` altina yeni dosya + `__init__.py`'e 1 import satiri. Baska hicbir dosya degismez.

**Yeni ortam eklemek**: `config.py`'deki `ENVIRONMENTS` dict'ine 1 satir. Komuta `LOAD_TEST_ENV=staging` ekle.

**Yeni test verisi veya assertion sabiti eklemek**: `data/search_data.py`'e 1 satir.

---

## Senaryolar

### Senaryo A — CategorySearchUser `[smoke]`
Kullanici arama kutusuna yazar, autocomplete'den kategori onerisi secer.
```
Homepage (/) → /bilgisayar veya /telefon-ve-aksesuarlari
```

### Senaryo B — ProductSearchUser `[smoke+regression]`
Kullanici arama kutusuna urun adi yazar, direkt sonuc sayfasina gider.
Agirlikli task'lar: popular(5) → tech(2) → edge_case(1)
```
Homepage (/) → /arama?q=<keyword>
```

### Senaryo C — UserJourneyUser
Sirayla: anasayfa → arama → sonuclari goruntule.
```
/ → /arama?q=<keyword> → interrupt(reschedule=True)
```

---

## Calistirma Komutlari

```bash
# Assessment default — 1 kullanici, 60 saniye (locust.conf varsayilanlari)
locust --headless

# Olcekleme — 10 kullanici
locust --headless -u 10 -r 2 --run-time 120s

# Sadece smoke tag'li task'lar
locust --headless --tags smoke

# Baska ortam
LOAD_TEST_ENV=staging locust --headless

# Web UI (gercek zamanli grafik)
locust
```

---

## Sonuc Analizi

Raporda izlenecek metrikler:

| Metrik | Kabul Edilebilir | Dikkat Gerektiren |
|--------|-----------------|-------------------|
| Failure rate | %0 | >%1 |
| Homepage avg | <2000ms | >3000ms |
| Kategori avg | <500ms | >1000ms (CDN sorunu?) |
| Arama avg | <1500ms | >3000ms (sunucu agrisi) |
| 95. percentil | <3000ms | >5000ms |

**Kategori sayfasi cok hizli (<200ms)**: CDN cache'den geliyor — normal ve beklenen.
**Arama sayfasi daha yavash**: Sunucu tarafli isleme var — kabul edilebilir.

---

## Yeni Senaryo Ekleme Adimlari

1. `load_tests/scenarios/` altinda yeni `.py` dosyasi olustur
2. TaskSet sinifini `BaseTaskSet`'ten miras al (`on_start`/`on_stop` otomatik gelir), `HttpUser` ayri tanimla
3. `load_tests/scenarios/__init__.py`'e import satirini ekle
4. `locustfile.py`'e dokunma — otomatik kesfedilir

**Ornek — Yeni senaryo: urun detay sayfasi:**
```python
# load_tests/scenarios/product_detail.py
from locust import HttpUser, TaskSet, between, task
from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.utils.response_validator import validate_homepage_response
from load_tests.utils.logger import get_logger

logger = get_logger(__name__)

PRODUCT_SLUGS = ["/urun-adi-p-123456789", "/baska-urun-p-987654321"]

class ProductDetailTasks(TaskSet):

    def on_start(self):
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            validate_homepage_response(resp)

    @task
    def view_product(self):
        import random
        slug = random.choice(PRODUCT_SLUGS)
        with self.client.get(
            slug,
            headers=DEFAULT_HEADERS,
            name="/[product-detail]",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Unexpected status {resp.status_code}")
            logger.info(f"Product | slug='{slug}' | status={resp.status_code}")

class ProductDetailUser(HttpUser):
    host      = BASE_URL
    weight    = 1
    tasks     = [ProductDetailTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
```

```python
# load_tests/scenarios/__init__.py — sadece bu satiri ekle:
from load_tests.scenarios.product_detail import ProductDetailUser  # noqa: F401
```

---

## Onemli Kurallar

1. **locustfile.py ince kalir** — senaryo kodu buraya girmez
2. **config.py** — ortam, esik degerleri, think time; test verisi buraya gelmez
3. **Hardcoded string yasak** — response body'de aranan metinler (orn. hata mesajlari) `data/search_data.py`'e sabit olarak yazilir, validator dosyasinda inline string kullanilmaz
4. **Her senaryo bagimsiz dosya** — tek sorumluluk prensibi
5. **Ortam degiskeni ile calistir** — `LOAD_TEST_ENV=staging` gibi
6. **Response validation merkezi** — `utils/response_validator.py` kullanilir, senaryo dosyasinda inline `if status != 200` yazilmaz
