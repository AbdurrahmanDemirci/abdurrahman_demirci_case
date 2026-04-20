# InsiderOne QA Assessment

Senior QA Engineer case study — Python tabanlı 3 katmanlı test otomasyon framework.

---

## Stack

| Katman | Teknoloji |
|--------|-----------|
| UI | Python 3.10+, Selenium 4.18.1, pytest 8.1.1, Allure |
| API | requests 2.32.3, jsonschema 4.23.0, pytest |
| Load | Locust 2.32.3 |
| CI | GitHub Actions (Chrome × Firefox matrix) |

---

## Kurulum

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## Test Çalıştırma

```bash
make ui-chrome          # Chrome UI testleri
make ui-firefox         # Firefox UI testleri
make ui-all-headless    # Her iki browser, headless
make api-test           # API testleri
make load-test          # Load testi (1 user, 60s)
make run-all            # Tüm suite paralel
make open-reports       # Allure UI:4040, API:4041
```

---

## Hedef Siteler

| Test Türü | Site |
|-----------|------|
| UI | https://insiderone.com |
| API | https://petstore.swagger.io/v2 |
| Load | https://www.n11.com |

---

## Mimari

```
ui_tests/
  locators/   ← WHAT to find (Locator sınıfı, *_locators.py)
  pages/      ← HOW to interact (BasePage miras zinciri)
  flows/      ← WHICH sequence (cross-page navigasyon)
  data/       ← WHAT to expect (assertion sabitleri)
  tests/      ← WHAT to verify (test mantığı)

api_tests/
  api/        ← BaseAPI (session, logging)
  client/     ← Resource client'ları (PetClient pattern)
  models/     ← Builder sınıfları (PetBuilder)
  schemas/    ← jsonschema kontrat tanımları
  data/       ← Sabit test verileri
  tests/      ← 6 dosya: create/read/update/delete/lifecycle/negative

load_tests/
  config.py   ← Ortam, threshold, think time
  data/       ← Test verileri (query'ler, path'ler)
  scenarios/  ← HttpUser sınıfları (her senaryo ayrı dosya)
  utils/      ← BaseTaskSet, logger, response_validator
  locustfile.py ← İnce entry point (sadece import)
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEST FRAMEWORK                              │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │   UI Tests     │  │   API Tests    │  │   Load Tests     │   │
│  │                │  │                │  │                  │   │
│  │ 1. locators/   │  │ api/           │  │ config.py        │   │
│  │ 2. pages/      │  │ client/        │  │ data/            │   │
│  │ 3. flows/      │  │ models/        │  │ scenarios/       │   │
│  │ 4. data/       │  │ schemas/       │  │ utils/           │   │
│  │ 5. tests/      │  │ data/ tests/   │  │ locustfile.py    │   │
│  └───────┬────────┘  └───────┬────────┘  └────────┬─────────┘   │
│          │                   │                     │             │
│  ┌───────▼───────────────────▼─────────────────────▼──────────┐  │
│  │              pytest / Locust runner                         │  │
│  └───────────────────────────┬────────────────────────────────┘  │
│                               │                                  │
│  ┌────────────────────────────▼────────────────────────────────┐  │
│  │  automation-test-results/                                    │  │
│  │    ui/allure-results/   api/allure-results/   locust/html   │  │
│  └────────────────────────────┬────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │         GitHub Actions CI           │
              │   chrome × firefox + API + Load    │
              │   (paralel job'lar, 7-day artifact)│
              └───────────────────────────────────┘
```

## Skill Workflow Diagram

```
Yeni UI Sayfası:
  /Insider-locator-extract → /Insider-page-add → /Insider-scenario-generate
    → /Insider-test-run → [fail?] /Insider-test-fix → /Insider-code-clean
    → /Insider-commit

Yeni API Resource:
  /Insider-api-client-add → /Insider-api-scenario-generate
    → /Insider-api-test-run → [fail?] /Insider-api-test-fix → /Insider-code-clean
    → /Insider-commit

Yeni Load Senaryosu:
  /Insider-load-scenario-add → /Insider-load-test
    → /Insider-report-analyze → /Insider-code-clean → /Insider-commit

Her commit için:
  /Insider-code-clean → /Insider-commit
```

## Skill Sistemi

Tüm slash komutları `.claude/skills/SKILLS-OVERVIEW.md` dosyasında belgelidir.

### Yeni İçerik Eklerken

| Ne Eklenecek | Skill |
|-------------|-------|
| Yeni UI sayfası (locator + page object) | `/Insider-page-add` |
| Yeni UI testi | `/Insider-scenario-generate` |
| Yeni API resource | `/Insider-api-client-add` |
| Yeni load senaryosu | `/Insider-load-scenario-add` |

### Sorun Giderme

| Sorun | Skill |
|-------|-------|
| UI testi fail | `/Insider-test-fix` |
| API testi fail | `/Insider-api-test-fix` |
| Rapor analizi | `/Insider-report-analyze` |
| Bug raporu | `/Insider-bug-report` |

### Commit Akışı (HER ZAMAN)

```
/Insider-code-clean → /Insider-commit
```

---

## Naming Convention

```
Locator  : {sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}
           örnek: careersPage_seeAllTeams_btn

Test     : test_NN_ne_dogrulaniyor
           örnek: test_03_qa_jobs_listed

Page     : eylem → go_to_X(), click_X()
           doğrulama → is_page_loaded(), is_X()
           veri → get_X(), get_all_Xs()
```

---

## Ortam Değişkenleri

> Tüm değişkenler **zorunludur** — eksik değişken `None` döner ve test crash eder. Hiçbir `config.py`'de default değer kullanılmaz.

| Değişken | Örnek | Açıklama |
|----------|-------|----------|
| `BASE_URL` | `https://insiderone.com` | UI hedef URL |
| `BROWSER` | `chrome` | `chrome` / `firefox` |
| `HEADLESS` | `false` | `true` / `false` |
| `EXPLICIT_WAIT` | `30` | Selenium wait (saniye) |
| `API_BASE_URL` | `https://petstore.swagger.io/v2` | API hedef URL |
| `API_TIMEOUT` | `10` | HTTP timeout (saniye) |
| `LOAD_TEST_ENV` | `production` | `production` / `staging` / `local` |
| `MIN_RESPONSE_BODY_SIZE` | `500` | Minimum response body boyutu (byte) |
| `P95_THRESHOLD_MS` | `3000` | P95 eşiği (ms) |
| `THINK_TIME_MIN` | `2` | Locust min think time (saniye) |
| `THINK_TIME_MAX` | `5` | Locust max think time (saniye) |

---

## Önemli Kurallar

1. Commit atmadan önce `/Insider-code-clean` çalıştır
2. Commit için `/Insider-commit` kullan — Conventional Commits standardı
3. Yeni page object yazmadan önce locator dosyasını oluştur (`/Insider-locator-extract`)
4. `BasePage` metodlarını (`_click`, `_find`, vb.) sayfa sınıflarında yeniden yazma
5. `BaseAPI` metodlarını (`_get`, `_post`, vb.) client sınıflarında yeniden yazma
6. Test assertion sabitleri `data/expected_content.py`'e gider, test dosyasına hardcode etme
7. Load test verisi `load_tests/data/` katmanına gider, senaryo dosyasına hardcode etme
8. `os.getenv("KEY")` çağrısı asla default almaz — yeni env var eklendiyse `.env`, `.env.example` ve `project-config.md` tablosunu güncelle
