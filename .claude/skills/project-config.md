# Project Config

Bu dosya proje-spesifik ayarları içerir. Bütün skill dosyaları buradan okur.

---

## Proje Bilgileri

- **Proje Adı**: InsiderOne QA Assessment
- **Platform**: Web (Desktop Browser)
- **Dil / Framework**: Python 3.10+ + Selenium 4 + pytest
- **Test Türü**: UI (Selenium, 5-katmanlı POM)

---

## Buyumeye Acik Mimari — Temel Prensipler

Bu proje bir case study olarak baslamis olsa da **global olcekte buyumeye hazir** tasarlanmistir.
Asagidaki kaliplar kodun her katmanina islenmi? olup yeni ozellik, sayfa veya ortam eklemek minimum degisiklik gerektirir.

### UI Test Katmani

| Kalip | Nerede | Buyumeye Katkisi |
|-------|--------|-----------------|
| **BasePage mirası** | `pages/base_page.py` | Yeni sayfa = sadece `class XPage(BasePage)`. Wait, click, scroll, log ucretsiz gelir. |
| **Locator.__set_name__** | `locators/locator.py` | Locator kendini otomatik isimlendirir. Yeni locator = 1 satir, kayit gerekmez. |
| **env-driven config** | `ui_tests/config.py` | `BASE_URL`, `HEADLESS`, `EXPLICIT_WAIT`, `BROWSER` `.env`'den okunur. Ortam degisimi = env var degisimi, kod dokunulmaz. |
| **pytest_generate_tests** | `conftest.py` | Cross-browser otomatik parametrize. Yeni browser = liste'ye 1 eleman. |
| **driver_factory soyutlama** | `ui_tests/utils/driver_factory.py` | Tum browser olusturma tek yerde. Safari/Edge eklemek = 1 if blogu. |
| **SiteFlow._COOKIE_ACTIONS dict** | `flows/site_flow.py` | Yeni cookie aksiyonu = dict'e 1 satir, cagiran kod degismez. |
| **_click_if_exists / _navigate_via_href** | `pages/base_page.py` | Dinamik ve SPA sayfalar icin savunmaci kaliplar, brittle wait gerektirmez. |
| **5-katmanli POM ayirimi** | `locators/ pages/ flows/ data/ tests/` | UI degisimi sadece 1 katmani etkiler. Cascading degisiklik olmaz. |
| **expected_content.py** | `data/expected_content.py` | Tum assertion sabitleri tek dosyada. Icerik degisimi = 1 dosya guncelleme. |
| **GitHub Actions matrix** | `.github/workflows/tests.yml` | Chrome + Firefox CI'da tanimlı. Yeni browser = matrix'e 1 satir. |

### Load Test Katmani

| Kalip | Nerede | Buyumeye Katkisi |
|-------|--------|-----------------|
| **Modular senaryolar** | `load_tests/scenarios/` | Yeni senaryo = yeni dosya + `__init__.py`'e 1 import. Baska hicbir sey degismez. |
| **Merkezi config** | `load_tests/config.py` | Ortam, test verisi, esik degerleri tek yerde. Yeni ortam = 1 satir. |
| **Ince entry point** | `load_tests/locustfile.py` | Sadece import. Senaryo eklemek locustfile.py'e dokunmak gerektirmez. |
| **env-var ortam secimi** | `LOAD_TEST_ENV` | `LOAD_TEST_ENV=staging locust ...` ile ortam gecisi, kod degismez. |

### Bu Prensiplere Uyarak Kod Yazma Kurali

Yeni bir senaryo, sayfa, locator veya test yazarken su soruyu sor:
> **"Bu degisiklik baska bir dosyaya cascade eder mi?"**

- Eder → Katman ihlali var, yapiyi gozden gecir
- Etmez → Dogru yerde yazilmis demektir

Tum skill'ler bu prensibi pekistirerek kod uretir.

---

## Dizin Yapısı

```
insiderone2/
├── .github/
│   └── workflows/
│       └── tests.yml           ← CI: Chrome + Firefox matrix
├── ui_tests/
│   ├── locators/               ← WHAT to find (* _locators.py)
│   │   ├── locator.py          ← Locator sınıfı (tuple wrapper)
│   │   ├── home_page_locators.py
│   │   ├── careers_page_locators.py
│   │   └── job_listing_page_locators.py
│   ├── pages/                  ← HOW to interact
│   │   ├── base_page.py        ← open(), wait_for_document_ready(), _click(), _find()
│   │   ├── home_page.py
│   │   ├── careers_page.py
│   │   └── job_listing_page.py
│   ├── flows/                  ← WHICH sequence (cross-page)
│   │   └── site_flow.py        ← handle_cookie_banner(), navigate_to_qa_jobs()
│   ├── data/                   ← WHAT to expect (assertion constants)
│   │   └── expected_content.py
│   ├── utils/
│   │   ├── driver_factory.py   ← Chrome/Firefox, Selenium Manager
│   │   └── logger.py           ← Structured logger (colorlog, pytest-aware)
│   ├── tests/
│   │   ├── test_home_page.py
│   │   └── test_insider_careers.py
│   ├── conftest.py             ← pytest_generate_tests, driver fixture, screenshot hook
│   └── config.py               ← env-driven (BASE_URL, HEADLESS, EXPLICIT_WAIT …)
├── .env                        ← Lokal overrides (gitignored)
├── .env.example                ← Template
├── .pre-commit-config.yaml     ← flake8 + trailing-whitespace
├── Makefile                    ← Kısa komutlar
├── pytest.ini
├── setup.cfg
└── requirements.txt
```

---

## Test Çalıştırma Komutları

```bash
# Tek browser
make ui-chrome
make ui-firefox

# Cross-browser (otomatik parametrize)
make ui-all
make ui-all-headless

# Paralel
make ui-parallel
make ui-all-parallel

# Marker bazlı
pytest ui_tests/tests/ -m smoke       # test_01, test_03
pytest ui_tests/tests/ -m regression  # tüm testler

# Tek test
pytest ui_tests/tests/test_home_page.py::TestHomePage::test_01_home_page_is_opened_and_loaded
```

---

## Naming Convention'lar

### Locator Key Formatı
```
{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}
```
- **sayfaKonteksti**: `homePage`, `careersPage`, `jobListingPage`
- **elementTipi**: `btn`, `link`, `input`, `dropdown`, `text`, `section`, `card`, `container`, `list`, `item`
- **Örnek**: `homePage_cookieAccept_btn`, `careersPage_seeAllTeams_btn`

### Test Metodu Formatı
```
test_NN_açıklama
```
- **Örnek**: `test_01_home_page_is_opened_and_loaded`

### Page Object Metodu Formatı
- Eylem: `go_to_careers()`, `click_see_all_teams()`
- Doğrulama: `is_page_loaded()`, `is_on_correct_page()`
- Veri çekme: `get_all_job_details()`

---

## Ortam Değişkenleri (.env)

| Değişken | Varsayılan | Açıklama |
|----------|-----------|----------|
| `BROWSER` | `chrome` | Varsayılan browser (chrome / firefox) |
| `HEADLESS` | `false` | Headless mod |
| `BASE_URL` | `https://insiderone.com` | Ana sayfa URL |
| `EXPLICIT_WAIT` | `30` | Selenium bekleme süresi (saniye) |

---

## config.py Kapsamı

`config.py` sadece **ortam / altyapı** ayarlarını içerir:
- Browser tipi, URL'ler, timeout değerleri, dizin yolları

**Buraya KOYMA:**
- Test assertion sabitleri → `ui_tests/data/expected_content.py`'e gider
- Selector / locator → `ui_tests/locators/*_locators.py`'e gider

---

## Hedef Site

| Test Türü | Site |
|-----------|------|
| UI | https://insiderone.com |
