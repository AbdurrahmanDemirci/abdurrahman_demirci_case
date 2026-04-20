# Code Clean — Python Format ve Mimari Kontrol Skill'i

> **Slash Komutu**: `/Insider-code-clean`
> **Amac**: Commit oncesi degisen Python dosyalarinda format, stil ve mimari kurallari kontrol eder; otomatik duzeltir veya raporlar.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, katman kurallari, naming convention
- `commit.md` → Commit oncesi bu skill calistirilir

---

## Tetikleme

- `/Insider-code-clean` ile manuel calistirilir
- `/Insider-commit` oncesinde otomatik tetiklenebilir (kullanici tercihine gore)

---

## Kontrol Edilecek Dosyalar

```bash
git diff --name-only HEAD
git diff --name-only --staged
```

Degisen dosyalar taranir. Kapsam:
- `ui_tests/**/*.py`
- `api_tests/**/*.py`
- `load_tests/**/*.py`
- `conftest.py`

`.venv/`, `__pycache__/`, `automation-test-results/` KAPSAM DISI.

---

## Adim 1: Otomatik Araclar

### flake8

```bash
flake8 <degisen-dosyalar>
```

Konfigurasyon (`setup.cfg`):
- `max-line-length = 100`
- `extend-ignore = E221` (hizalama amaçli çoklu bosluk — locator tanimlari için izinli)
- exclude: `.git`, `__pycache__`, `.env`, `automation-test-results`, `venv`, `.venv`

**Sik Karsilasilan Hatalar ve Duzeltme**:

| Kod | Hata | Duzeltme |
|-----|------|----------|
| E501 | Satir 100+ karakter | Satiri böl veya kısalt |
| F401 | Import edilip kullanilmayan modul | Import satirini sil |
| E302 | 2 bos satir bekleniyor | Sinif/fonksiyon oncesi 2 bos satir ekle |
| E303 | Fazla bos satir | Fazla satirlari sil |
| W291 | Trailing whitespace | Satir sonu bosluklarini sil |
| W292 | Dosya sonu newline yok | Dosya sonuna newline ekle |
| E711 | `== None` yerine `is None` | `is None` / `is not None` kullan |
| F811 | Tekrar tanimlanan isim | Duplicate tanimlamayi sil |

**KRITIK**: flake8 hatasi varsa duzelt, commit'e gecme.

---

## Adim 2: Mimari Katman Kurallari

### Kural 1: Selector Katman Ihlali

`pages/**` veya `tests/**` icinde asagidakiler OLMAMALI:

```python
# YASAK — pages/ veya tests/ icinde:
By.CSS_SELECTOR
By.XPATH
By.ID
By.CLASS_NAME
(By.
```

Tespit edilirse: selector'i ilgili `*_locators.py` dosyasina tasi, sayfadan `L.` ile referans ver.

### Kural 2: Locator Dosyasinda Duz Tuple

`locators/**` icinde duz `(By.X, "...")` tuple OLMAMALI, `Locator(By.X, "...")` kullanilmali:

```python
# YANLIS:
some_element = (By.CSS_SELECTOR, ".btn")

# DOGRU:
some_element = Locator(By.CSS_SELECTOR, ".btn")
```

### Kural 3: Test Assertion Sabitleri

`tests/**` icinde hardcoded string assertion OLMAMALI, `data/expected_content.py`'den gelmeli:

```python
# YANLIS:
assert "Quality Assurance" in text

# DOGRU:
from ui_tests.data.expected_content import ExpectedContent as E
assert E.DEPARTMENT_NAME in text
```

**Not**: Basit `assert driver.title` gibi assertions bu kurala girmez. Yalnizca is tanimina ait sabit string degerler `data/` katmanina tasınır.

### Kural 4: config.py Kapsami

`ui_tests/config.py` SADECE env/altyapi ayarlari icermeli:
- Browser tipi, URL'ler, timeout, dizin yollari

**OLMAMALI**:
- Test assertion sabitleri → `data/expected_content.py`
- Selector / locator → `locators/*_locators.py`

### Kural 5: Locator Naming Convention

`locators/**` icindeki key'ler `{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}` formatinda olmali:

```python
# DOGRU:
homePage_cookieAccept_btn
careersPage_departmentCards_section
jobListingPage_jobItems_list

# YANLIS:
btn1, acceptButton, COOKIE_BTN, careers_filter
```

---

## Adim 3: Python Genel Kalite Kontrolleri

- **Kullanilmayan import**: `F401` flake8 yakalar, sil
- **Duplicate import**: Ayni modul iki kez import edilmis, tekrari sil
- **Gereksiz yorum**: Sadece kodu tekrar eden yorumlar (`# click the button` gibi) — sil
- **Magic number**: Test kodunda aciklamasiz sabit sayi varsa `expected_content.py`'e tasi
- **Type hint tutarliligi**: Mevcut metodlarda tip hint varsa yeni metodlarda da olmali

---

## Adim 2c: Load Test Katman Kurallari (`load_tests/**`)

### Kural L1: Senaryo Dosyasinda Hardcoded URL/String Yasak

`load_tests/scenarios/**` icinde inline URL veya arama terimi OLMAMALI:

```python
# YANLIS — senaryo icinde:
resp = self.client.get("/arama?q=laptop")

# DOGRU:
from load_tests.data.search_data import POPULAR_QUERIES
query = random.choice(POPULAR_QUERIES)
resp = self.client.get(f"/arama", params={"q": query})
```

### Kural L2: Senaryo Dosyasinda Inline Validasyon Yasak

`load_tests/scenarios/**` icinde `if resp.status_code != 200` gibi inline kontrol OLMAMALI:

```python
# YANLIS:
if resp.status_code != 200:
    resp.failure(...)

# DOGRU:
from load_tests.utils.response_validator import validate_search_response
validate_search_response(resp)
```

### Kural L3: locustfile.py'e Senaryo Kodu Eklenmez

`load_tests/locustfile.py` sadece import icermeli. Task veya user logic buraya gelmez.

### Kural L4: config.py Salt Okunur

`load_tests/config.py` sadece import edilir, degistirilmez. Ortam degeri → `.env` uzerinden degistir.

---

## Adim 2b: API Katman Kurallari (`api_tests/**`)

### Kural A: client/ icinde raw HTTP yasak

`api_tests/client/**` icinde `requests.get(...)`, `requests.Session()` direkt cagrisi OLMAMALI:

```python
# YANLIS — client dosyasinda:
resp = requests.get(f"{BASE_URL}/pet/{pet_id}")

# DOGRU — BaseAPI metodlarini kullan:
return self._get(f"/pet/{pet_id}")
```

### Kural B: Test dosyasinda hardcoded payload yasak

`api_tests/tests/**` icinde duz dict payload OLMAMALI, `{Resource}Builder` kullanilmali:

```python
# YANLIS:
payload = {"id": 12345, "name": "Buddy", "status": "available", "photoUrls": []}

# DOGRU:
payload = PetBuilder.full(name="Buddy", status="available")
```

### Kural C: Test dosyasinda hardcoded ID yasak

`api_tests/tests/**` icinde sabit ID sayisi OLMAMALI, `data/{resource}_data.py` sabitleri kullanilmali:

```python
# YANLIS:
resp = self.client.get_by_id(999999999999)

# DOGRU:
from api_tests.data.pet_data import INVALID_PET_ID
resp = self.client.get_by_id(INVALID_PET_ID)
```

### Kural D: Pozitif testlerde schema dogrulama zorunlu

`api_tests/tests/test_{resource}_{create|read|update}.py` icindeki 200 donduran her pozitif test `validate(instance=body, schema=...)` cagirmali:

```python
# ZORUNLU — her pozitif test dosyasinda:
from jsonschema import validate
from api_tests.schemas.pet_schema import PET_RESPONSE_SCHEMA

validate(instance=body, schema=PET_RESPONSE_SCHEMA)
```

Eksikse: testi guncelle, validate cagrisi ekle.

---

### Kural 6: yield Kullanan Fixture Donus Tipi

`@pytest.fixture` icinde `yield` varsa donus tipi `-> dict` / `-> webdriver.Remote` OLMAZ:

```python
# YANLIS — Pylance sarı cizgi:
@pytest.fixture
def created_pet(client: PetClient) -> dict:
    ...
    yield pet

# DOGRU:
from collections.abc import Generator

@pytest.fixture
def created_pet(client: PetClient) -> Generator[dict, None, None]:
    ...
    yield pet
```

**Kural**: `yield` li her fixture → `Generator[YieldType, None, None]`
- `YieldType`: fixture'in yield ettigi deger tipi (`dict`, `webdriver.Remote`, ...)
- `send_type` ve `return_type`: pytest fixture'larinda her zaman `None`
- `from collections.abc import Generator` — Python 3.9+, harici paket gerekmez

---

## Adim 4: Sonuc Raporu

```
Code Clean Sonucu:
✓ ui_tests/locators/careers_page_locators.py — sorun yok
✓ ui_tests/pages/careers_page.py — 1 trailing whitespace duzeltildi
✗ ui_tests/tests/test_insider_careers.py — flake8 E302 (2 bos satir eksik, duzeltildi)
⚠ ui_tests/pages/home_page.py — katman ihlali: By.CSS_SELECTOR bulundu (manuel mudahale gerekli)
```

Semboller:
- `✓` — temiz veya otomatik duzeltildi
- `✗` — sorun vardi, otomatik duzeltildi
- `⚠` — manuel mudahale gerekiyor, commit'e gecme

---

## Onemli Kurallar

1. **flake8 hatasi varsa commit YAPMA** — once duzelt
2. **debug-statements commit EDILMEZ** — `breakpoint()`, `pdb` bulunursa sil
3. **Selector katman ihlali** — pages/ veya tests/ icinde selector varsa locators/ katmanina tasi
4. **Otomatik duzeltme**: trailing whitespace, end-of-file newline, flake8 E302/E303 → otomatik duzelt
5. **Manuel mudahale gerektiren**: katman ihlali, assertion sabiti — raporla, kullaniciya birak
6. **Format degisikligi ayri commit OLMAZ** — diger degisikliklerle birlikte commit edilir

## Sonraki Adim

Bu kontrol sorunsuz tamamlandiysa → `/Insider-commit` ile commit at.
