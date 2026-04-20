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

## Önemli Kurallar

1. Commit atmadan önce `/Insider-code-clean` çalıştır
2. Commit için `/Insider-commit` kullan — Conventional Commits standardı
3. Yeni page object yazmadan önce locator dosyasını oluştur (`/Insider-locator-extract`)
4. `BasePage` metodlarını (`_click`, `_find`, vb.) sayfa sınıflarında yeniden yazma
5. `BaseAPI` metodlarını (`_get`, `_post`, vb.) client sınıflarında yeniden yazma
6. Test assertion sabitleri `data/expected_content.py`'e gider, test dosyasına hardcode etme
7. Load test verisi `load_tests/data/` katmanına gider, senaryo dosyasına hardcode etme
