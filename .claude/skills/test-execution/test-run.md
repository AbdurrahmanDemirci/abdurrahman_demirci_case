# Test Run — pytest Test Kosturma Skill'i

> **Slash Komutu**: `/Insider-test-run`
> **Amac**: pytest testlerini kosturur, ciktiyi yorumlar, Allure raporu uretir.

---

## Referanslar

- `../project-config.md` → Test kosma komutlari, dizin yapisi

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **Test dosyasi** (ornek: `test_insider_careers.py`)
2. **Tek test metodu** (ornek: `test_02_careers_page_loads`)
3. **Marker** (ornek: "smoke testleri kos")
4. **Browser** (ornek: "Firefox'ta kos")
5. **Genel talep** (ornek: "tum testleri kos")

---

## Islem Adimlari

### Adim 1: Test Komutunu Olustur

> Tum komutlarin tam listesi: `../project-config.md` → "Test Calistirma Komutlari"

**Hizli referans:**

```bash
# Tum testler
make ui-all

# Headless (CI uyumlu)
make ui-all-headless

# Tek browser
make ui-chrome
make ui-firefox

# Marker bazli
pytest ui_tests/tests/ -m smoke
pytest ui_tests/tests/ -m regression

# Tek dosya
pytest ui_tests/tests/test_insider_careers.py -v

# Tek test metodu
pytest ui_tests/tests/test_insider_careers.py::TestInsiderCareers::test_02_careers_page_loads -v

# Browser ve headless override
pytest ui_tests/tests/ --browser=firefox --headless=true
```

### Adim 2: Testi Kos

Komutu calistir ve ciktiyi canli izle.

**Timeout**: Tek test icin 2 dakika, tam suite icin 15 dakika.

Eger `WebDriverException: Chrome not reachable` veya `geckodriver not found` hatasi cikiyorsa:
```bash
# Selenium Manager otomatik driver indirmeli, ama eksikse:
pip install --upgrade selenium
```

### Adim 3: Ciktiyi Yorumla

**Basarili cikti:**
```
PASSED ui_tests/tests/test_home_page.py::TestHomePage::test_01 [chrome]
PASSED ui_tests/tests/test_home_page.py::TestHomePage::test_01 [firefox]
2 passed in 18.43s
```

**Basarisiz — Element Bulunamadi:**
```
selenium.common.exceptions.TimeoutException: Message: element not interactable
NoSuchElementException: Unable to locate element: {"method":"css selector","selector":".btn"}
```
→ Locator gecersiz veya sayfa degismis

**Basarisiz — Assertion Fail:**
```
AssertionError: assert "Quality Assurance" in []
AssertionError: Expected page title "X" but got "Y"
```
→ Beklenen icerik degismis veya sayfa yuklenmemis

**Basarisiz — Timeout:**
```
TimeoutException: Timed out after 30 seconds waiting for element
```
→ Sayfa yavash yükleniyor, wait suresi yetersiz veya element artik yok

**Basarisiz — Browser/Driver:**
```
WebDriverException: Message: session not created
```
→ ChromeDriver/GeckoDriver versiyonu uyumsuz, `pip install --upgrade selenium` dene

**Flaky (reruns):**
```
FAILED ui_tests/tests/test_home_page.py::TestHomePage::test_01 [chrome] — 1 failed, 2 rerun
PASSED (rerun 1)
```
→ pytest.ini'deki `--reruns=2` devreye girdi, timing sorunu olabilir

### Adim 4: Allure Raporu Uret

```bash
allure serve automation-test-results/allure-results/
```

Veya HTML olarak kaydet:
```bash
allure generate automation-test-results/allure-results/ -o automation-test-results/allure-report/ --clean
```

---

## Cikti Formati

```
## Test Sonucu

- **Browser(lar)**: Chrome, Firefox
- **Suite**: Full regression
- **Toplam**: 6 test (3 dosya x 2 browser)
- **Basarili**: 5
- **Basarisiz**: 1
- **Pass Rate**: %83

### Basarisiz Testler:
1. test_03_filter_jobs [firefox] → AssertionError: "Quality Assurance" not in job list

### Oneri:
- /Insider-test-fix ile analiz et
```

---

## Onemli Kurallar

1. **Headless tercih et** — CI ortaminda ve hizli kontrol icin `--headless=true`
2. **Her iki browser'da kos** — Sadece Chrome'da pass etmek yetmez
3. **Screenshot on failure** — `conftest.py`'deki hook otomatik kaydeder (`automation-test-results/screenshots/`)
4. **Reruns normal** — `--reruns=2` flaky korumasi icin, ama 3 denemede de fail ise gercek sorun var
5. **`allure serve` sadece lokal** — CI'da `allure generate` kullan
