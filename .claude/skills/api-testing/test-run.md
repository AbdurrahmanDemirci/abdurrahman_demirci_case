# API Test Run — pytest API Test Kosturma Skill'i

> **Slash Komutu**: `/Insider-api-test-run`
> **Amac**: API testlerini kosturur, HTTP hata tiplerini yorumlar, Allure raporu uretir.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, test kosma komutlari

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **Test dosyasi** (ornek: `test_pet.py`)
2. **Tek test metodu** (ornek: `test_03_find_by_valid_status_returns_200`)
3. **Marker** (ornek: "smoke testleri kos", "regression")
4. **Genel talep** (ornek: "tum api testleri kos")

---

## Islem Adimlari

### Adim 1: Test Komutunu Olustur

**Make hedefleri (tercihli):**

```bash
# Tum API testleri
make api-test

# Sadece smoke
make api-smoke
```

**Direkt pytest — ince kontrol:**

```bash
# Tum API testleri (verbose)
pytest api_tests/tests/ -v --alluredir=automation-test-results/api/allure-results

# Marker bazli
pytest api_tests/tests/ -m smoke --alluredir=automation-test-results/api/allure-results
pytest api_tests/tests/ -m regression --alluredir=automation-test-results/api/allure-results

# Tek dosya (6-file yapisi)
pytest api_tests/tests/test_pet_create.py -v --alluredir=automation-test-results/api/allure-results
pytest api_tests/tests/test_pet_negative.py -v --alluredir=automation-test-results/api/allure-results

# Tek test metodu
pytest api_tests/tests/test_pet_create.py::TestPetCreate::test_create_pet_returns_200_and_correct_fields -v

# Kaynak filtresi
pytest api_tests/tests/ -k "create or delete" -v

# Rerun olmadan (flaky debug)
pytest api_tests/tests/ -p no:rerunfailures -v
```

**Allure dizini**: `automation-test-results/api/allure-results/`
**UI allure dizininden FARKLI** — karistirma.

### Adim 2: Testi Kos

Timeout: Tek test icin 30 saniye, tam suite icin 3 dakika.

`API_BASE_URL` veya `API_TIMEOUT` override gerekiyorsa:
```bash
API_BASE_URL=https://petstore.swagger.io/v2 API_TIMEOUT=15 pytest api_tests/tests/ -v
```

### Adim 3: Ciktiyi Yorumla

**Basarili cikti:**
```
PASSED api_tests/tests/test_pet.py::TestPetCrud::test_01_create_pet_returns_200_and_correct_fields
PASSED api_tests/tests/test_pet.py::TestPetCrud::test_02_get_pet_by_id_returns_correct_pet
13 passed in 4.21s
```

**Basarisiz — HTTP Status Mismatch:**
```
AssertionError: assert 500 == 200
AssertionError: assert 200 in (400, 404, 405)
```
→ API davranisi degismis veya beklenti yanlis

**Basarisiz — Response Field:**
```
KeyError: 'id'
AssertionError: assert body["name"] == "Buddy"
assert "UpdatedBuddy" == "UpdatedBuddy" → body["name"] != "UpdatedBuddy"
```
→ Response schema degismis veya test data uyumsuz

**Basarisiz — Fixture Setup:**
```
AssertionError: Pet creation failed: {"code":400,"message":"..."}
```
→ `created_pet` fixture'i basarisiz; API erisilebilir mi kontrol et

**Basarisiz — Connection:**
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='petstore.swagger.io', port=443)
```
→ API_BASE_URL kontrol et, internet baglantisi kontrol et

**Basarisiz — Timeout:**
```
requests.exceptions.ReadTimeout: HTTPSConnectionPool read timed out. (read timeout=10)
```
→ `.env`'de `API_TIMEOUT` degerini artir veya API gecikmeli

**Flaky (reruns):**
```
FAILED ... — 1 failed, 2 rerun → PASSED (rerun 1)
```
→ Petstore public API'si zaman zaman gecikir; `--reruns=2` normal

### Adim 4: Allure Raporu Uret

```bash
# Lokal izleme
make report-open-api
# veya:
allure serve automation-test-results/api/allure-results

# CI icin HTML raporu
make report-api
# veya:
allure generate automation-test-results/api/allure-results --clean -o automation-test-results/allure-report/api
```

---

## Cikti Formati

```
## API Test Sonucu

- **Suite**: Full / Smoke / Regression
- **Endpoint Grubu**: Pet API
- **Toplam**: 15 test (6 dosya)
- **Basarili**: 12
- **Basarisiz**: 1
- **Pass Rate**: %92

### Basarisiz Testler:
1. test_10_delete_nonexistent_pet_returns_404
   → AssertionError: assert 200 == 404 (API davranisi degismis)

### Oneri:
- /Insider-api-test-fix ile analiz et
```

---

## Onemli Kurallar

1. **Allure dizinini karistirma** — UI: `allure-results/ui/`, API: `allure-results/api/`
2. **Rerun normal** — `--reruns=2` Petstore kararsizligini karsilar; 3'te de fail gercek sorun
3. **Fixture sorununu once coz** — `created_pet` fail → tum bag test'ler skip olur; once temel CRUD duzelt
4. **Public API bilinci** — `petstore.swagger.io` public; baska takim test verileri biriktirebilir, `INVALID_PET_ID = 999_999_999_999` bunu yonetir
5. **`-p no:rerunfailures`** — Debug sirasinda kesin hata gormek icin rerun'i kapat
