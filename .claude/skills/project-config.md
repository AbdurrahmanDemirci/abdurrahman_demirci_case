# Project Config

Bu dosya proje-spesifik ayarları içerir. Bütün skill dosyaları buradan okur.

---

## Proje Bilgileri

- **Proje Adı**: InsiderOne QA Assessment
- **Platform**: Web (Desktop Browser)
- **Dil / Framework**: Python 3.10+ + Selenium 4 + pytest
- **Test Türü**: UI (Selenium, 5-katmanlı POM)

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
│   │   └── driver_factory.py   ← Chrome/Firefox, Selenium Manager
│   ├── tests/
│   │   ├── test_home_page.py
│   │   └── test_insider_careers.py
│   ├── conftest.py             ← pytest_generate_tests, driver fixture, screenshot hook
│   └── config.py               ← env-driven (BASE_URL, HEADLESS, EXPLICIT_WAIT …)
├── utils/
│   └── logger.py               ← Paylaşılan logger (colorlog)
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
| `CAREERS_URL` | `https://insiderone.com/careers/#open-roles` | Kariyer sayfası URL |
| `EXPLICIT_WAIT` | `30` | Selenium bekleme süresi (saniye) |
| `SCREENSHOTS_DIR` | `automation-test-results/screenshots` | Screenshot klasörü |

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
