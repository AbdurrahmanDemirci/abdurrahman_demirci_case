# API Scenario Generate — API Test Senaryosu Uretme Skill'i

> **Slash Komutu**: `/Insider-api-scenario-generate`
> **Amac**: ISTQB standartlarina uygun, duplikasyonsuz, projenin 4-katmanli API yapisina uygun pytest test metodlari uretir.

---

## Referanslar

- `../project-config.md` → Naming convention, dizin yapisi
- `references/istqb-api-principles.md` → API icin 6 ISTQB teknigi
- `references/api-test-strategy.md` → Mevcut kapsam, smoke/regression stratejisi

---

## Temel Prensipler (ASLA Ihlal Edilmez)

### 1. Sifir Duplikasyon
Mevcut testlerde zaten dogrulanan bir HTTP davranisi icin yeni test yazilmaz.
Yeni assertion gerekiyorsa → mevcut metoda eklenir.

### 2. Katman Kurali

| Ne | Nereye |
|----|--------|
| HTTP cagrilari | `client/{resource}_client.py` — `BaseAPI`'yi extend eder |
| Test verisi builder | `models/{resource}_model.py` — `{Resource}Builder` sinifi |
| Test sabitleri | `data/{resource}_data.py` — `INVALID_`, `VALID_`, `NEGATIVE_` |
| Schema dogrulama | `schemas/{resource}_schema.py` — `{RESOURCE}_RESPONSE_SCHEMA` |
| Test senaryolari | `tests/test_{resource}_{crud}.py` — 6 dosya (create/read/update/delete/lifecycle/negative) |

Test metodunda `requests.get(...)` veya URL string OLMAZ.
Test metodunda hardcoded payload OLMAZ — `{Resource}Builder.full()` kullanilir.
Test metodunda hardcoded ID OLMAZ — `data/{resource}_data.py` sabitleri kullanilir.
Test metodunda `validate()` cagrisi OLMAZ — pozitif testlerin tamaminda schema dogrulama ZORUNLU.

### 3. ISTQB Maliyet-Etkinlik
- **EP**: Ayni partition'dan 1 deger yeterli; her gecerli status icin ayri pozitif test yerine `@pytest.mark.parametrize` kullan
- **BVA**: Sayisal sinir olan alanlarda (ID min/max, negatif) uygula
- **State Transition**: Lifecycle testi — tam CRUD dongusu tek test metodunda
- **Error Guessing**: Eksik body, yanlis tip, null deger, negatif ID

---

## Agent Calisma Akisi

```
INPUT: Endpoint / resource aciklamasi
   |
[ADIM 1] Kapsam & Risk Analizi
   |
[ADIM 2] Mevcut Testleri Kontrol Et (Duplikasyon Kontrolu)
   |
[ADIM 3] Katman Hazirlik Kontrolu (Builder + Schema)
   |
[ADIM 4] ISTQB Teknik Secimi
   |
[ADIM 5] Senaryo Uretimi
   |
[ADIM 6] Completeness Self-Check
   |
OUTPUT: pytest test metodlari → dogru dosyaya yaz
```

---

## ADIM 1 — Kapsam & Risk Analizi

Kullanicidan cikar:

```
Resource / Endpoint : [Hangi API kaynagi — Pet, User, Store, ...]
HTTP Metodlari      : [CRUD'un hangi kismi — POST, GET, PUT, DELETE, ...]
Marker              : [smoke / regression / her ikisi]
Oncelik             : [Kritik akis mi? Yardimci mi?]
```

**Risk Skoru (1-5):**
- 5 → Temel CRUD (create + get + delete) → smoke + regression
- 3-4 → Filtreleme, arama, soft validation → regression
- 1-2 → Edge case, tuhaf input → regression (opsiyonel)

---

## ADIM 2 — Mevcut Testleri Kontrol Et

```bash
# Tum API test metodlarini listele (6 dosya)
grep -rn "def test_" api_tests/tests/

# Spesifik resource'un tum test dosyalarini oku
ls api_tests/tests/test_{resource}_*.py
grep -rn "def test_" api_tests/tests/test_{resource}_*.py
```

Mevcut testlerle karsilastir:

```
DEDUPLICATION KONTROLU — [{Resource}/{Endpoint}]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dogrulanacak Davranis              | Mevcut Dosya             | Aksiyon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POST 200 + schema validate         | test_pet_create.py       | Mevcut → YAZMA
GET 200 + schema validate          | test_pet_read.py         | Mevcut → YAZMA
GET 404 nonexistent                | test_pet_negative.py     | Mevcut → YAZMA
Persistence (GET after PUT)        | HAYIR                    | Yeni yaz
Idempotency (duplicate DELETE)     | HAYIR                    | Yeni yaz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ADIM 3 — Katman Hazirlik Kontrolu

```bash
# Model builder var mi?
ls api_tests/models/{resource}_model.py 2>/dev/null || echo "YOK — /Insider-api-client-add cagir"

# Builder metodlari
grep -n "def " api_tests/models/{resource}_model.py

# Schema var mi?
ls api_tests/schemas/{resource}_schema.py 2>/dev/null || echo "YOK — /Insider-api-client-add cagir"

# Client BaseAPI'den mi miras alıyor?
grep -n "class.*Client\|from.*base_api\|BaseAPI" api_tests/client/{resource}_client.py

# Gerekli sabitler var mi?
grep -n "INVALID_\|VALID_\|NEGATIVE_" api_tests/data/{resource}_data.py
```

Yoksa: `/Insider-api-client-add` ile once katmanlar olusturulmasi gerektigini bildir.

**Builder + Schema hazirsa devam:**

```bash
# conftest fixture var mi?
grep -n "def client\|def created_" api_tests/conftest.py
```

---

## ADIM 4 — ISTQB Teknik Secimi

| Senaryo Tipi | Birincil Teknik | Ikincil |
|---|---|---|
| Status kodu dogrulama | Use Case | EP |
| Gecerli/gecersiz parametreler | EP | Error Guessing |
| ID siniri (min/max/negatif) | BVA | EP |
| Zorunlu alan eksik | Error Guessing | EP |
| CRUD lifecycle akisi | State Transition | Use Case |
| Filtreleme / coklu deger | EP + Parametrize | Decision Table |
| Tip hatasi (string → int) | Error Guessing | EP |
| Persistence dogrulama | State Transition | Use Case |
| Idempotency | State Transition | Error Guessing |

---

## ADIM 5 — Senaryo Uretimi

### Test Sinifi Yapisi (Her Dosya)

```python
@allure.parent_suite("API Tests")
@allure.suite("{Resource}")
@allure.feature("{Resource} API")
@allure.story("{Create|Read|Update|Delete|Lifecycle}")  # dosyaya gore sabit
class Test{Resource}{CrudType}:

    @pytest.fixture(autouse=True)
    def setup(self, client: {Resource}Client) -> None:
        self.client = client
```

**setup'a dokunma** — mevcut `client` fixture'ini degistirme.

---

### Positive Test Pattern (Schema Dogrulama ZORUNLU)

```python
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.api
@allure.story("Create")
@allure.title("POST /{resource} — valid payload returns 200 with correct fields")
def test_create_{resource}_returns_200_and_correct_fields(self) -> None:
    payload = {Resource}Builder.full(name="Buddy", status="available")

    resp = self.client.create(payload)

    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == payload["id"]
    assert body["name"] == payload["name"]
    assert body["status"] == payload["status"]
    validate(instance=body, schema={RESOURCE}_RESPONSE_SCHEMA)

    self.client.delete(body["id"])
```

**Import satiri (her pozitif test dosyasinda):**
```python
from jsonschema import validate
from api_tests.models.{resource}_model import {Resource}Builder
from api_tests.schemas.{resource}_schema import {RESOURCE}_RESPONSE_SCHEMA
```

---

### Persistence Verification Pattern (PUT sonrasi GET)

```python
@pytest.mark.regression
@pytest.mark.api
@allure.story("Update")
@allure.title("PUT /{resource} — update persists on subsequent GET")
def test_update_{resource}_persists_on_get(self, created_{resource}: dict) -> None:
    updated = {{**created_{resource}, "name": "PersistName", "status": "sold"}}

    self.client.update(updated)
    verify_resp = self.client.get_by_id(created_{resource}["id"])

    assert verify_resp.status_code == 200
    assert verify_resp.json()["name"] == "PersistName"
    assert verify_resp.json()["status"] == "sold"
```

---

### Lifecycle Pattern (State Transition — E2E)

```python
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.api
@allure.story("Lifecycle")
@allure.title("{Resource} full lifecycle — Create → Read → Update → Verify → Delete → 404")
def test_full_{resource}_lifecycle(self) -> None:
    payload = {Resource}Builder.full(name="LifecyclePet", status="available")

    # Create
    create_resp = self.client.create(payload)
    assert create_resp.status_code == 200
    {resource} = create_resp.json()
    {resource}_id = {resource}["id"]

    # Read
    get_resp = self.client.get_by_id({resource}_id)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "LifecyclePet"

    # Update
    updated = {{**{resource}, "name": "UpdatedLifecycle", "status": "sold"}}
    update_resp = self.client.update(updated)
    assert update_resp.status_code == 200

    # Verify persistence
    verify_resp = self.client.get_by_id({resource}_id)
    assert verify_resp.json()["name"] == "UpdatedLifecycle"
    assert verify_resp.json()["status"] == "sold"

    # Delete
    delete_resp = self.client.delete({resource}_id)
    assert delete_resp.status_code == 200

    # Verify 404
    assert self.client.get_by_id({resource}_id).status_code == 404
```

---

### Negative Test Pattern

```python
@pytest.mark.regression
@pytest.mark.api
@allure.story("Read")
@allure.title("GET /{resource}/{{id}} — non-existent ID returns 404")
def test_get_nonexistent_{resource}_returns_404(self) -> None:
    resp = self.client.get_by_id(INVALID_{RESOURCE}_ID)

    assert resp.status_code == 404
```

**Esnek status beklentisi** — API quirk varsa yorum ekle:
```python
# Petstore returns 404 for string IDs instead of 400 (lenient validation)
assert resp.status_code in (400, 404)
```

---

### Parametrize Pattern (EP icin)

```python
@pytest.mark.regression
@pytest.mark.api
@allure.story("Read")
@allure.title("GET /{resource}/findByStatus — valid status returns 200 with a list")
@pytest.mark.parametrize("status", VALID_{RESOURCE}_STATUSES)
def test_find_by_valid_status_returns_200(self, status: str) -> None:
    resp = self.client.find_by_status(status)

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
```

---

### Opsiyonel Assertions (Eklenebilir, Zorunlu Degil)

```python
# Response time
assert resp.elapsed.total_seconds() < 2.0

# Content-Type header
assert "application/json" in resp.headers.get("Content-Type", "")

# Required fields batch check
assert all(k in body for k in ["id", "name", "status", "photoUrls"])
```

---

## ADIM 6 — Completeness Self-Check

```
COMPLETENESS SELF-CHECK — [{Resource} API]
═══════════════════════════════════════════════════════════════════════════════
| Kategori                    | Teknik        | Min | Sayi | Dosya           |
|═════════════════════════════|═══════════════|═════|══════|═════════════════|
| POST pozitif + schema       | Use Case      | 1   |      | _create.py      |
| POST minimal payload        | EP            | 1   |      | _create.py      |
| GET id ile pozitif + schema | Use Case      | 1   |      | _read.py        |
| GET findByStatus parametrize| EP + Param    | 1   |      | _read.py        |
| PUT pozitif + schema        | Use Case      | 1   |      | _update.py      |
| PUT persistence verify      | State Trans   | 1   |      | _update.py      |
| DELETE 200 + GET 404        | State Trans   | 1   |      | _delete.py      |
| E2E lifecycle               | State Trans   | 1   |      | _lifecycle.py   |
| GET var olmayan ID — 404    | Error Guess   | 1   |      | _negative.py    |
| GET string ID — 400/404     | Error Guess   | 1   |      | _negative.py    |
| GET negatif ID (-1)         | BVA           | 1   |      | _negative.py    |
| POST bos body — 4xx         | Error Guess   | 1   |      | _negative.py    |
| PUT gecersiz ID tipi — 4xx  | Error Guess   | 1   |      | _negative.py    |
| DELETE var olmayan — 404    | Error Guess   | 1   |      | _negative.py    |
| findByStatus gecersiz deger | EP            | 1   |      | _negative.py    |
═══════════════════════════════════════════════════════════════════════════════
Eksik kategori varsa kullaniciya bildir, eklemesini iste.
```

**Minimum**: 15 test metodu (3 smoke + 12 regression).

---

## ADIM 7 — Dogru Dosyaya Yaz

### 6-File Routing Kurali

| Test Tipi | Dosya |
|-----------|-------|
| POST senaryolari | `api_tests/tests/test_{resource}_create.py` |
| GET senaryolari | `api_tests/tests/test_{resource}_read.py` |
| PUT senaryolari | `api_tests/tests/test_{resource}_update.py` |
| DELETE senaryolari | `api_tests/tests/test_{resource}_delete.py` |
| Tam yasam dongusu (E2E) | `api_tests/tests/test_{resource}_lifecycle.py` |
| Negatif / hata senaryolari | `api_tests/tests/test_{resource}_negative.py` |

### Yeni Resource Dosya Sablonu

```python
import pytest
import allure
from jsonschema import validate

from api_tests.client.{resource}_client import {Resource}Client
from api_tests.models.{resource}_model import {Resource}Builder
from api_tests.schemas.{resource}_schema import {RESOURCE}_RESPONSE_SCHEMA


@allure.parent_suite("API Tests")
@allure.suite("{Resource}")
@allure.feature("{Resource} API")
@allure.story("{Create|Read|Update|Delete|Lifecycle}")
class Test{Resource}{CrudType}:

    @pytest.fixture(autouse=True)
    def setup(self, client: {Resource}Client) -> None:
        self.client = client
```

**Negative dosya sablonu** (coklu story):

```python
@allure.parent_suite("API Tests")
@allure.suite("{Resource}")
@allure.feature("{Resource} API")
class Test{Resource}Negative:

    @pytest.fixture(autouse=True)
    def setup(self, client: {Resource}Client) -> None:
        self.client = client

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /{resource}/{{id}} — ...")
    def test_...(self) -> None:
        ...
```

---

## Coverage Raporu (Her Uretim Sonunda)

```
COVERAGE RAPORU — [{Resource} API]
══════════════════════════════════════════════════════
Toplam Yeni Metod    : {N}
  - smoke + regression: {N}
  - regression only   : {N}

ISTQB Teknikler      : {EP, State Transition, Error Guessing, BVA, ...}
Onlenen Duplikasyon  : {N} metod tasarruf edildi
Completeness         : {N}/15 kategori karsilandi
Yazilan Dosyalar     : {dosya listesi}
══════════════════════════════════════════════════════
```

---

## Buyume Prensibi — Her Uretimde Kontrol Et

Yeni test metodu yazarken sor:
**"Bu degisiklik baska bir dosyaya cascade eder mi?"**

- **Yeni resource testi** → `models/`, `schemas/`, `client/`, `data/` katmanlari hazir olmali; yoksa once `api-client-add` cagir
- **Yeni sabit** → `data/{resource}_data.py`'e ekle, test metodunda import et
- **Yeni client metodu** → `client/{resource}_client.py`'e ekle (BaseAPI metodu kullanarak)
- **Yeni builder** → `models/{resource}_model.py`'e ekle
- **Yeni fixture** → `api_tests/conftest.py`'e ekle, baska conftest'e ekleme

Cascade eden degisiklik mimari ihlalidir.
