# Report Analyze — Allure Rapor Analiz Skill'i

> **Slash Komutu**: `/Insider-report-analyze`
> **Amac**: pytest/Allure sonuc raporunu okur, pattern tespit eder, oncelikli aksiyon onerileri sunar.

---

## Referanslar

- `../project-config.md` → Rapor dizin yapisi
- `../test-execution/test-fix.md` → Failure kategori tanimlari

---

## Kullanim

Kullanici su kaynaklardan birini saglar:
1. **Allure results dizini** (`automation-test-results/allure-results/`)
2. **pytest terminal ciktisi** (kopyala-yapistir)
3. **Genel talep** (ornek: "son test kosusunu analiz et")

---

## Islem Adimlari

### Adim 1: Veriyi Oku

**Allure JSON dosyalari:**
```bash
# Result dosyalarini listele
ls automation-test-results/allure-results/

# JSON result'lari oku
find automation-test-results/allure-results/ -name "*-result.json"
```

**Allure result JSON yapisi:**
```json
{
  "name": "test_01_home_page_is_opened_and_loaded[chrome]",
  "status": "passed|failed|broken|skipped",
  "statusDetails": { "message": "hata mesaji", "trace": "stack trace" },
  "labels": [{"name": "suite", "value": "..."}, {"name": "tag", "value": "..."}],
  "start": 1234567890,
  "stop": 1234567900
}
```

**pytest terminal ciktisinden:**
- `PASSED` / `FAILED` / `ERROR` satirlarini parse et
- `short test summary info` bolumundeki FAILED listesini cikar
- Toplam sure ve sayilari oku

**Screenshot dizini:**
```bash
ls automation-test-results/screenshots/
```
Her fail icin `{test_adi}_{browser}_{timestamp}.png` formatinda screenshot varsa belirt.

### Adim 2: Ozet Metrikleri Hesapla

```
## Test Kosu Ozeti

- **Tarih**: {tarih}
- **Browser(lar)**: Chrome, Firefox
- **Suite**: {smoke / regression / full}
- **Toplam Test**: {total}
- **Basarili**: {passed} (%{rate})
- **Basarisiz**: {failed}
- **Hata**: {error/broken}
- **Atlanan**: {skipped}
- **Toplam Sure**: {sure}
```

### Adim 3: Failure Analizi

Her fail olan test icin:
1. **Test metodu adi ve browser**
2. **Hata mesaji** (statusDetails.message'in ilk satiri)
3. **Fail olan satir** (stack trace'den)
4. **Screenshot** — `automation-test-results/screenshots/` altinda var mi?
5. **Hata kategorisi** (`test-fix.md` kategorilerine gore):
   - Locator Gecersiz
   - Element Kaldirildi
   - Timing / Wait Sorunu
   - Assertion Fail — Icerik Degismis
   - Sayfa Akisi Degismis
   - Site Bug

### Adim 4: Pattern Tespiti

**Test Bazli Analiz:**
```
| Test Metodu | Chrome | Firefox | Hata Tipi |
|-------------|--------|---------|-----------|
| test_01     | PASS   | PASS    | —         |
| test_02     | PASS   | FAIL    | Locator   |
| test_03     | FAIL   | FAIL    | Assertion |
```

**Browser Bazli Dagilim:**
```
| Browser | Toplam | Pass | Fail | Pass Rate |
|---------|--------|------|------|-----------|
| Chrome  | 6      | 5    | 1    | %83       |
| Firefox | 6      | 4    | 2    | %67       |
```

**Hata Tipi Dagilimi:**
```
| Hata Tipi          | Sayi | Oran |
|--------------------|------|------|
| Locator Gecersiz   | 2    | %50  |
| Assertion Fail     | 1    | %25  |
| Timing Sorunu      | 1    | %25  |
```

**Cross-browser analiz:**
- Sadece Firefox'ta fail → browser-specific locator veya rendering sorunu
- Her iki browser'da fail → gercek bir sorun (locator, assertion, site degisimi)
- Flaky (bazen pass, bazen fail) → timing/wait sorunu

**Regression tespiti:**
- Yeni eklenen kod veya site degisikligiyle eslesen fail → potansiyel regression

### Adim 5: Aksiyon Onerileri

```
## Oncelikli Aksiyonlar

### Yuksek Oncelik
1. [Her iki browser'da fail] test_03 — Assertion fail, site icerigi degismis → /Insider-test-fix
2. [Locator] test_02 [Firefox] — CSS selector gecersiz → /Insider-locator-extract

### Orta Oncelik
3. [Timing] test_04 [Chrome] — Bekleme suresi yetersiz → /Insider-test-fix

### Dusuk Oncelik
4. [Skip] test_05 — Manuel olarak skip edilmis, sebep kontrol edilmeli
```

---

## Cikti Formati

### Kisa Ozet (Varsayilan)
```
## Son Test Kosu Analizi

Sonuclar: 10/12 passed (%83 pass rate)
Fail: 2 test — 1 locator, 1 assertion
Kritik: Her iki browser'da fail olan test_03 (regression riski)
Flaky: test_04 Chrome'da 1/3 denemede pass (timing sorunu)

Sonraki Adim: /Insider-test-fix ile test_03 ve test_04'u duzelt
```

### Detayli Rapor (Istenirse)
Tum metrikler, browser bazli tablo, her failure detayi, pattern analizi ve oncelikli aksiyon listesi.

---

## Locust Raporu Analizi

Kullanici su kaynaklardan birini saglar:
1. **`locust_report.html`** (CI artifact veya `make load-test` sonrasi)
2. **`locust_stats.csv` / `locust_stats_history.csv`** (CSV artifacts)
3. **Locust terminal ciktisi** (kopyala-yapistir)

### Adim 1: Temel Metrikleri Oku

```
## Locust Kosu Ozeti

- **Tarih**: {tarih}
- **Kullanici Sayisi**: {users}
- **Spawn Rate**: {spawn-rate}/s
- **Sure**: {run-time}
- **Toplam Istek**: {total_requests}
- **Hata Sayisi**: {failures}
- **Failure Rate**: %{rate}
```

### Adim 2: Endpoint Bazli Analiz

| Endpoint | Req/s | Avg (ms) | P95 (ms) | Failure |
|----------|-------|----------|----------|---------|
| / (homepage) | — | — | — | — |
| /arama?q=[popular] | — | — | — | — |
| /arama?q=[tech] | — | — | — | — |
| /arama?q=[edge_case] | — | — | — | — |
| /[category-slug] | — | — | — | — |

### Adim 3: Esik Deger Kontrolu

| Metrik | Kabul Edilebilir | Dikkat | Kritik |
|--------|-----------------|--------|--------|
| Failure rate | %0 | >%1 | >%5 |
| Homepage avg | <2000ms | >3000ms | >5000ms |
| Kategori avg | <500ms | >1000ms | >2000ms |
| Arama avg | <1500ms | >3000ms | >5000ms |
| P95 (genel) | <3000ms | >5000ms | >8000ms |

**Not**: Kategori sayfasi genellikle <200ms gelir (CDN cache) — normal ve beklenen.

### Adim 4: Aksiyon Onerileri

```
## Locust Analiz Sonucu

Failure rate: %{rate} — {kabul edilebilir / dikkat / kritik}
En yavas endpoint: {endpoint} avg={avg}ms P95={p95}ms
Kapasite: {req/s} istek/saniye — {yeterli / yetersiz}

Sonraki Adim: {öneri}
```
