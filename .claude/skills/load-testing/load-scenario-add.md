# Load Scenario Add — Yeni Locust Senaryosu Ekleme Skill'i

> **Slash Komutu**: `/Insider-load-scenario-add`
> **Amac**: Mevcut Locust mimarisine yeni bir kullanıcı tipi (HttpUser + TaskSet) ve test verisi ekler. Modüler tasarıma uygun olarak yalnızca yeni dosyalar oluşturur; mevcut senaryolara dokunmaz.

---

## Referanslar

- `../project-config.md` → Dizin yapısı, ortam değişkenleri
- `load-test.md` → Mevcut senaryo örnekleri, çalıştırma komutları, eşik değerleri
- `../reporting/report-analyze.md` → Senaryo sonrası analiz

---

## Kullanım

Kullanıcı şu bilgilerden birini sağlar:
1. **Senaryo adı + hedef URL** (örnek: "Checkout akışı, /sepet → /odeme")
2. **Yük profili** (örnek: "weight=2, 10 user, 120s")
3. **Test verisi** (örnek: "şu keyword'leri kullan: ['laptop', 'telefon']")

---

## Agent Çalışma Akışı

```
INPUT: Senaryo adı + endpoint + yük profili
   |
[ADIM 1] Mevcut Yapıyı Kontrol Et
   |
[ADIM 2] Test Verisi Dosyası Oluştur / Güncelle
   |
[ADIM 3] Validator Fonksiyonu Ekle (gerekiyorsa)
   |
[ADIM 4] Senaryo Dosyası Oluştur
   |
[ADIM 5] __init__.py Güncelle
   |
[ADIM 6] Doğrula
   |
OUTPUT: Senaryo hazır, /Insider-load-test ile çalıştırılabilir
```

---

## ADIM 1 — Mevcut Yapıyı Kontrol Et

```bash
ls load_tests/scenarios/
cat load_tests/scenarios/__init__.py
cat load_tests/config.py
ls load_tests/data/
cat load_tests/utils/response_validator.py
```

Kontrol:
- `{scenario}.py` zaten var mı? → Varsa güncelle, yoksa oluştur
- `config.py`'de hedef URL tanımlı mı? → Yoksa ortam bloğuna ekle
- Yeni endpoint için validator gerekiyor mu?

---

## ADIM 2 — Test Verisi Dosyası Oluştur / Güncelle

Mevcut `data/search_data.py` kapsamı dışındaysa yeni dosya oluştur.
Aynı domain içindeyse (örn. ek arama terimleri) mevcut dosyaya ekle.

**Yeni dosya gerekiyorsa**: `load_tests/data/{domain}_data.py`

```python
{DOMAIN}_QUERIES: list[str] = [
    "{keyword1}",
    "{keyword2}",
    "{keyword3}",
]

{DOMAIN}_PATHS: list[str] = [
    "/{path1}",
    "/{path2}",
]
```

**Kural**: Sabit string değerler buraya, threshold ve config değerleri `config.py`'e.

---

## ADIM 3 — Validator Fonksiyonu Ekle (Koşullu)

Yeni endpoint için özel doğrulama gerekmiyorsa bu adımı atla.
Gerekiyorsa `load_tests/utils/response_validator.py`'e ekle:

```python
def validate_{scenario}_response(resp: ResponseContextManager) -> None:
    if resp.status_code != 200:
        resp.failure(f"Expected 200, got {resp.status_code}")
        return
    if len(resp.content) < 500:
        resp.failure(f"Response too small: {len(resp.content)} bytes")
        return
    _check_p95_threshold(resp)
    resp.success()
```

**Mevcut validatorlar** (yeniden yazma):
- `validate_search_response` → 200 + body ≥ 500 bytes + P95
- `validate_category_response` → 200 + body ≥ 500 bytes
- `validate_homepage_response` → 200
- `validate_edge_case_response` → sadece P95

---

## ADIM 4 — Senaryo Dosyası Oluştur

**Dosya**: `load_tests/scenarios/{scenario_name}.py`

### TaskSet Türü Seçimi

| Kullanım | Tür |
|----------|-----|
| Bağımsız, tekrar eden görevler | `BaseTaskSet(TaskSet)` |
| Sıralı adımlar (checkout, login→işlem) | `SequentialTaskSet` |

### TaskSet(BaseTaskSet) Şablonu

```python
import random

from locust import HttpUser, between, tag, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.data.{domain}_data import {DOMAIN}_QUERIES
from load_tests.utils.base_task_set import BaseTaskSet
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import validate_{scenario}_response

logger = get_logger(__name__)


class {Scenario}Tasks(BaseTaskSet):

    @tag("smoke", "regression")
    @task({weight})
    def {primary_action}(self) -> None:
        query = random.choice({DOMAIN}_QUERIES)
        with self.client.get(
            "/path",
            params={"q": query},
            headers=DEFAULT_HEADERS,
            name="/[{scenario}-primary]",
            catch_response=True,
        ) as resp:
            validate_{scenario}_response(resp)
            logger.info(f"{Scenario} | q={query} | {resp.status_code} | {resp.elapsed.total_seconds():.2f}s")

    @tag("regression")
    @task(1)
    def {secondary_action}(self) -> None:
        path = random.choice({DOMAIN}_PATHS)
        with self.client.get(
            path,
            headers=DEFAULT_HEADERS,
            name="/[{scenario}-secondary]",
            catch_response=True,
        ) as resp:
            validate_{scenario}_response(resp)


class {Scenario}User(HttpUser):
    host      = BASE_URL
    weight    = {weight}   # toplam user dağılımındaki oran
    tasks     = [{Scenario}Tasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
```

### SequentialTaskSet Şablonu

```python
from locust import HttpUser, SequentialTaskSet, between, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import validate_homepage_response, validate_{scenario}_response

logger = get_logger(__name__)


class {Scenario}Tasks(SequentialTaskSet):
    _state: str = ""

    @task
    def step_one(self) -> None:
        with self.client.get(
            "/",
            headers=DEFAULT_HEADERS,
            name="/[{scenario}-step1]",
            catch_response=True,
        ) as resp:
            validate_homepage_response(resp)
            self._state = "step1_done"

    @task
    def step_two(self) -> None:
        with self.client.get(
            "/next-path",
            headers=DEFAULT_HEADERS,
            name="/[{scenario}-step2]",
            catch_response=True,
        ) as resp:
            validate_{scenario}_response(resp)
            self.interrupt(reschedule=True)  # döngüyü yeniden başlat


class {Scenario}User(HttpUser):
    host      = BASE_URL
    weight    = {weight}
    tasks     = [{Scenario}Tasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
```

**Önemli kurallar:**
- `locustfile.py`'e dokunma — senaryo otomatik yüklenir
- `config.py`'e dokunma — sadece `config.py`'deki sabitleri import et
- `name="/[...]"` → Locust raporunda okunabilir endpoint ismi
- `catch_response=True` → validator içinde `resp.failure()` / `resp.success()` çağrısı zorunlu

---

## ADIM 5 — __init__.py Güncelle

`load_tests/scenarios/__init__.py` dosyasına sadece şu satırı ekle:

```python
from load_tests.scenarios.{scenario_name} import {Scenario}User  # noqa: F401
```

Başka hiçbir dosyaya dokunmak gerekmez.

---

## ADIM 6 — Doğrula

```bash
# Import kontrolü
.venv/bin/python -c "from load_tests.scenarios.{scenario_name} import {Scenario}User; print('OK')"

# Locust collect kontrolü (senaryoları listeler)
.venv/bin/locust --list 2>&1

# Kısa smoke çalıştırması
locust --headless -u 1 -r 1 --run-time 10s --tags smoke 2>&1 | tail -20
```

`--list` çıktısında `{Scenario}User` görünmeli.

---

## Çıktı Formatı

```
## Load Senaryo Ekleme Raporu

### Oluşturulan / Güncellenen Dosyalar
- `load_tests/data/{domain}_data.py`          — {N} sabit
- `load_tests/utils/response_validator.py`    — validate_{scenario}_response eklendi  [koşullu]
- `load_tests/scenarios/{scenario_name}.py`   — {Scenario}User (weight={W}), {N} task
- `load_tests/scenarios/__init__.py`          — 1 import eklendi

### Senaryo Profili
| Sınıf | Weight | Task Sayısı | Tags |
|-------|--------|-------------|------|
| {Scenario}User | {W} | {N} | smoke, regression |

### Doğrulama
- Import: OK
- Locust list: OK
- Sonraki adım: /Insider-load-test ile çalıştır
```

---

## Önemli Kurallar

1. **locustfile.py ince kalır** — senaryo kodu buraya girmez
2. **config.py salt okunur** — sadece import et, değiştirme
3. **BaseTaskSet miras al** — `on_start`/`on_stop` her senaryoda tekrar yazılmaz
4. **SequentialTaskSet'te BaseTaskSet kullanma** — miras uyumsuzluğu; on_start/on_stop gerekiyorsa manuel yaz
5. **Hardcoded string yasak** — arama terimleri `data/` katmanına, URL'ler `config.py`'e
6. **Validator merkezi** — senaryo dosyasında inline `if resp.status_code != 200` kontrolü yok
7. **`name=` parametresi zorunlu** — Locust raporunda endpoint'in okunabilir görünmesi için
