# API Client Add — Yeni API Kaynagi Ekleme Skill'i

> **Slash Komutu**: `/Insider-api-client-add`
> **Amac**: Yeni bir API resource'u (User, Store, Order, ...) icin BaseAPI client, PetBuilder pattern model, schema ve conftest fixture'ini projenin mevcut mimarisine uygun sekilde olusturur.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, naming convention
- `scenario-generate.md` → Olusturduktan sonra test senaryosu uretimi icin

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **Resource adi** (ornek: "User", "Store", "Order")
2. **Endpoint bilgisi** (ornek: "POST /user, GET /user/{username}, DELETE /user/{username}")
3. **Swagger/OpenAPI linki** (ornek: "petstore.swagger.io User endpoints")

---

## Agent Calisma Akisi

```
INPUT: Resource adi + endpoint bilgisi
   |
[ADIM 1] Mevcut Yapiyi Kontrol Et
   |
[ADIM 2] BaseAPI Client Olustur
   |
[ADIM 3] Model Builder Olustur (models/)
   |
[ADIM 4] Response Schema Olustur (schemas/)
   |
[ADIM 5] Data Sabitleri Olustur (data/)
   |
[ADIM 6] conftest.py Guncelle
   |
[ADIM 7] Dogrula
   |
OUTPUT: 5 dosya hazir, /Insider-api-scenario-generate kullanilabilir
```

---

## ADIM 1 — Mevcut Yapiyi Kontrol Et

```bash
# Mevcut katman dosyalari
ls api_tests/client/
ls api_tests/models/
ls api_tests/schemas/
ls api_tests/data/

# Mevcut fixture'lar
grep -n "@pytest.fixture" api_tests/conftest.py

# BaseAPI varligi
cat api_tests/api/base_api.py
```

Kontrol: `{resource}_client.py` veya `{resource}_model.py` zaten var mi?
Varsa → onceden olusturulmus, gerekirse guncelle.

---

## ADIM 2 — BaseAPI Client Olustur

**Dosya**: `api_tests/client/{resource}_client.py`

**PetClient'i taklit et** — `BaseAPI`'den miras al:

```python
import requests

from api_tests.api.base_api import BaseAPI


class {Resource}Client(BaseAPI):

    def create(self, payload: dict | None) -> requests.Response:
        return self._post("/{resource}", json=payload)

    def get_by_{id_field}(self, {id_field}: int | str) -> requests.Response:
        return self._get(f"/{resource}/{{{id_field}}}")

    def update(self, payload: dict) -> requests.Response:
        return self._put("/{resource}", json=payload)

    def delete(self, {id_field}: int | str) -> requests.Response:
        return self._delete(f"/{resource}/{{{id_field}}}")
```

**Sadece gercekten var olan endpoint'leri ekle** — Swagger schema'yı baz al.
Yoksa metodu ekleme; olmayan endpoint'i stub etme.

**Filtreleme / arama endpoint'i varsa:**
```python
def find_by_{param}(self, {param}: str) -> requests.Response:
    return self._get(f"/{resource}/findBy{Param}", params={{"{param}": {param}}})
```

**`BaseAPI` ne saglar**: `self.session` (headers dahil), `self._get/_post/_put/_delete`, otomatik logging.
Client metodlarinda `requests.Session()` veya URL string OLMAZ.

---

## ADIM 3 — Model Builder Olustur

**Dosya**: `api_tests/models/{resource}_model.py`

```python
import time


def _new_id() -> int:
    return int(time.time() * 1000) % 10**9


class {Resource}Builder:

    @staticmethod
    def full(name: str = "Test{Resource}", status: str = "{default_status}") -> dict:
        return {{
            "id": _new_id(),
            "name": name,
            "status": status,
            "photoUrls": ["https://example.com/photo.jpg"],  # API zorunlu kiliyorsa
            "category": {{"id": 1, "name": "Default"}},      # API zorunlu kiliyorsa
            "tags": [{{"id": 1, "name": "test"}}],           # API zorunlu kiliyorsa
        }}

    @staticmethod
    def minimal(name: str = "Test{Resource}") -> dict:
        return {{
            "id": _new_id(),
            "name": name,
            "photoUrls": [],  # zorunlu minimum alan
        }}

    @staticmethod
    def without_name() -> dict:
        payload = {Resource}Builder.full()
        del payload["name"]
        return payload

    @staticmethod
    def without_photo_urls() -> dict:
        payload = {Resource}Builder.full()
        del payload["photoUrls"]
        return payload

    @staticmethod
    def invalid_body() -> dict:
        return {{"id": "not-a-number", "name": "Ghost", "status": "available", "photoUrls": []}}
```

**Kurallar:**
- `_new_id()` → ms cozunurluklu, 9 haneli ID, public API catismalarini minimize eder
- Sadece API'nin gercekten beklediği alanlari ekle — tahmini alan ekleme
- Her builder metodu bagimsiz bir payload sablonunu temsil eder

---

## ADIM 4 — Response Schema Olustur

**Dosya**: `api_tests/schemas/{resource}_schema.py`

```python
{RESOURCE}_RESPONSE_SCHEMA: dict = {{
    "type": "object",
    "required": ["id", "name", "photoUrls"],  # API'nin zorunlu dondurmesi gereken alanlar
    "additionalProperties": False,
    "properties": {{
        "id": {{"type": "integer"}},
        "name": {{"type": "string"}},
        "status": {{"type": "string"}},
        "photoUrls": {{
            "type": "array",
            "items": {{"type": "string"}},
        }},
        "category": {{
            "type": "object",
            "additionalProperties": True,
            "properties": {{
                "id": {{"type": "integer"}},
                "name": {{"type": "string"}},
            }},
        }},
        "tags": {{
            "type": "array",
            "items": {{
                "type": "object",
                "additionalProperties": True,
                "properties": {{
                    "id": {{"type": "integer"}},
                    "name": {{"type": "string"}},
                }},
            }},
        }},
    }},
}}
```

**Kurallar:**
- `"required"` → sadece API'nin her zaman dondurdugu alanlari koy
- `"additionalProperties": False` → beklenmedik yeni alan eklenirse test fail eder (kontrat ihlali yakalanir)
- Nested objeler icin `"additionalProperties": True` → daha toleranli
- `jsonschema` kutuphanesi `requirements.txt`'te olmali: `jsonschema==4.23.0`

---

## ADIM 5 — Data Sabitleri Olustur

**Dosya**: `api_tests/data/{resource}_data.py`

```python
VALID_{RESOURCE}_STATUSES: list[str] = ["{status1}", "{status2}", "{status3}"]

INVALID_{RESOURCE}_ID: int = 999_999_999_999
NEGATIVE_{RESOURCE}_ID: int = -1
INVALID_STRING_ID: str = "not-a-valid-id"
```

**Kurallar:**
- `INVALID_..._ID = 999_999_999_999` — buyuk ve anlamsiz, catisma olasiligi neredeyse sifir
- `NEGATIVE_..._ID = -1` — BVA icin sinir degeri testi
- `INVALID_STRING_ID` — tip hatasi testi icin
- `build_{resource}()` FONKSIYON EKLEME — Builder pattern artik `models/` katmaninda

---

## ADIM 6 — conftest.py Guncelle

**Dosya**: `api_tests/conftest.py`

Mevcut fixture'larin ALTINA ekle:

```python
from api_tests.client.{resource}_client import {Resource}Client
from api_tests.models.{resource}_model import {Resource}Builder


@pytest.fixture(scope="session")
def {resource}_client() -> {Resource}Client:
    return {Resource}Client()


@pytest.fixture
def created_{resource}({resource}_client: {Resource}Client) -> dict:
    payload = {Resource}Builder.full()
    resp = {resource}_client.create(payload)
    assert resp.status_code == 200, f"{Resource} creation failed: {resp.text}"
    resource_data = resp.json()
    yield resource_data
    {resource}_client.delete(resource_data["{id_field}"])
```

**Onemli kurallar:**
- `{resource}_client` → `scope="session"` (baglanti havuzu yeniden kullanilir)
- `created_{resource}` → `scope` belirtme (varsayilan = function; her test icin temiz resource)
- Teardown: `yield` sonrasinda delete — API temizligi garanti altinda
- `{Resource}Builder.full()` kullan, hardcoded payload OLMAZ

---

## ADIM 7 — Dogrula

### Dosya Varlik Kontrolu

```bash
ls api_tests/client/{resource}_client.py
ls api_tests/models/{resource}_model.py
ls api_tests/schemas/{resource}_schema.py
ls api_tests/data/{resource}_data.py
grep -n "{resource}_client\|created_{resource}" api_tests/conftest.py
```

### Import Kontrolu

```bash
.venv/bin/python -c "from api_tests.client.{resource}_client import {Resource}Client; print('client OK')"
.venv/bin/python -c "from api_tests.models.{resource}_model import {Resource}Builder; print('model OK')"
.venv/bin/python -c "from api_tests.schemas.{resource}_schema import {RESOURCE}_RESPONSE_SCHEMA; print('schema OK')"
```

### Collect Kontrolu

```bash
.venv/bin/pytest api_tests/ --collect-only -q 2>&1 | head -20
```

Hata yoksa: "`/Insider-api-scenario-generate` ile test senaryolari yazilabilir`" mesaji ver.

---

## Cikti Formati

```
## API Client Ekleme Raporu

### Olusturulan Dosyalar
- `api_tests/client/{resource}_client.py`  — BaseAPI extend, {N} endpoint metodu
- `api_tests/models/{resource}_model.py`   — {Resource}Builder: full, minimal, without_name, without_photo_urls, invalid_body
- `api_tests/schemas/{resource}_schema.py` — {RESOURCE}_RESPONSE_SCHEMA (jsonschema)
- `api_tests/data/{resource}_data.py`      — {N} sabit (INVALID, NEGATIVE, VALID)
- `api_tests/conftest.py`                  — 2 fixture eklendi ({resource}_client, created_{resource})

### Mevcut Endpoint'ler
| HTTP | Path | Metod |
|------|------|-------|
| POST | /{resource} | create(payload) |
| GET  | /{resource}/{id} | get_by_{id_field}(id) |
| PUT  | /{resource} | update(payload) |
| DELETE | /{resource}/{id} | delete(id) |

### Dogrulama
- Import: OK
- Collect: OK
- Sonraki adim: /Insider-api-scenario-generate ile test yaz
```

---

## Onemli Kurallar

1. **BaseAPI extend et** — `requests.Session()` direkt kullanma; `self._get/_post/_put/_delete` kullan
2. **Sadece var olan endpoint** — Swagger'da olmayan metodu stub etme
3. **Builder pattern** — `models/{resource}_model.py`'de sinif; `data/{resource}_data.py`'de sadece sabitler
4. **Schema zorunlu** — Her pozitif testte `validate(instance=body, schema=...)` kullanilacak
5. **`__init__.py` ekleme** — `api_tests/` namespace package; `__init__.py` gereksiz
6. **conftest genisletme** — Mevcut fixture'lara dokunma, sadece yenilerini ekle
