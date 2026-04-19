# Test Fix — Hata Duzeltme Skill'i

> **Slash Komutu**: `/Insider-test-fix`
> **Amac**: Fail olan Selenium testini kategorize eder, kok nedeni tespit eder, otomatik fix uygular.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, katman kurallari
- `test-run.md` → Dogrulama test kosmasi icin
- `../locator/locator-extract.md` → Locator guncellemesi gerekiyorsa
- `../locator/references/locator-strategy.md` → CSS/XPath oncelik kurallari

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **Fail ciktisi** (terminal log veya pytest output)
2. **Fail olan test metodu** (ornek: "test_03 fail oluyor")
3. **Allure rapor dizini** (`automation-test-results/allure-results/`)
4. **Genel talep** (ornek: "fail olan testleri duzelt")

---

## Failure Kategorileri ve Fix Stratejileri

### Kategori 1: Locator Gecersiz

**Belirti:**
```
NoSuchElementException: Unable to locate element: css selector '.old-class'
TimeoutException: element not interactable after 30s
```

**Fix Stratejisi:**
1. Fail olan locator key'ini tespit et
2. Mevcut selector'u oku:
   ```bash
   grep -rn "selector_degeri" ui_tests/locators/
   ```
3. Kullanicidan sayfanin guncel HTML'ini veya screenshot'ini iste
4. `../locator/references/locator-strategy.md`'deki CSS oncelik sirasina gore yeni selector bul
5. Ilgili `*_locators.py` dosyasini guncelle
6. Testi tekrar kos

### Kategori 2: Element DOM'dan Kaldirildi

**Belirti:** Element hicbir sekilde bulunamiyor, sayfa HTML'inde yok

**Fix Stratejisi:**
1. Sayfanin guncel HTML'ini incele — element gercekten kalkti mi?
2. Kullaniciya sor: Element kaldirildi mi, yoksa baska bir yere mi tasindi?
3. Kaldirildiysa: Ilgili test adimini veya testi guncelle/kaldir
4. Tasindiysa: Yeni locator cikar, test akisini guncelle

### Kategori 3: Timing / Wait Sorunu

**Belirti:**
```
TimeoutException: Timed out after 30 seconds
StaleElementReferenceException: element is not attached to the page
```

**Fix Stratejisi:**
1. `base_page.py`'deki `_find()` metodunun implicit wait'ini kontrol et
2. `config.py`'deki `EXPLICIT_WAIT` degerine bak (varsayilan 30s)
3. Sayfa yeniden yuklenme sonrasi element araniyorsa `StaleElementReference` normal — `try/retry` mantigi ekle
4. Cookie banner gibi dinamik elemanlar icin `_click_if_exists()` pattern'i kullan
5. Gerekirse `EXPLICIT_WAIT` degerini `.env` uzerinden artir

### Kategori 4: Assertion Fail — Icerik Degismis

**Belirti:**
```
AssertionError: assert "Quality Assurance" in []
AssertionError: "Insider." not in "useinsider.com - Leader in Individualized..."
```

**KRITIK — Sifir Gereksiz Kosma Prensibi:**
Assertion fail'de gercek deger zaten hata mesajinda yazilidir. Test tekrar kosulmadan fix yapilabilir.

**Fix Stratejisi:**
1. Hata mesajindan gercek degeri oku
2. Degerin `ui_tests/data/expected_content.py`'de mi yoksa test dosyasinda mi oldugunu belirle
3. Eger `expected_content.py`'deyse → orada guncelle
4. Eger test dosyasindaysa → `expected_content.py`'e tasi, oradan import et (katman kurali)
5. Ayni degeri kullanan diger testleri de kontrol et:
   ```bash
   grep -rn "eski_deger" ui_tests/tests/
   ```
6. TUM etkilenen testleri tek seferde guncelle, sonra bir kez kos

**Ornek — Dogru Yaklasim:**
```
Hata: AssertionError: "Insider." not in "useinsider.com - Leader..."
→ expected_content.py'de HOME_TITLE = "Insider." guncellenmeli
→ Ayni sabiti kullanan diger testler de kontrol edilmeli
→ Hepsini duzelt, 1 kez kos → PASS
```

### Kategori 5: Sayfa Akisi Degismis

**Belirti:** Element var ama test yanlis sayfada veya akis farklilasti

**Fix Stratejisi:**
1. Sayfanin guncel akisini anla (kullanicidan bilgi al)
2. Cookie banner, pop-up, redirect gibi yeni eklenen engeller var mi?
3. `flows/site_flow.py`'yi guncelle — yeni akis adimini ekle
4. Gereksiz adimi kaldir
5. Testi tekrar kos

**Ornek:** Cookie banner konumu degismis, `handle_cookie_banner()` metodu eski locator'i ariyor.

### Kategori 6: Site Bug (Gercek Bug)

**Belirti:** Uygulama beklenmedik davranis gosteriyor, site cevap vermiyor

**Fix Stratejisi:**
1. Bug olup olmadigini dogrula — test kodu mu hatali, site mi?
2. Kullaniciya bildir: "Bu bir site bug'i, `/Insider-bug-report` ile rapor olusturabilirsiniz"
3. Testi `@pytest.mark.skip(reason="site-bug: #JIRA-XXX")` ile gecici isaretle

---

## Islem Adimlari

### Adim 1: Failure Analizi

1. Hata mesajini ve stack trace'i oku
2. Fail olan test metodunu ve satir numarasini tespit et
3. Hangi assertion veya `find()` cagrisinin fail ettini belirle
4. **Screenshot'u incele** — `automation-test-results/screenshots/` altinda
5. Yukaridaki 6 kategoriden hangisine ait oldugunu belirle

### Adim 2: Bilgi Toplama

```bash
# Fail olan locator degerini bul
grep -rn "css_selector_degeri" ui_tests/locators/

# Fail olan test metodunu oku
cat ui_tests/tests/{test_dosyasi}.py

# Ilgili page object'i oku
cat ui_tests/pages/{sayfa}.py

# expected_content'i oku
cat ui_tests/data/expected_content.py
```

### Adim 3: Fix Uygula

**ONEMLI**: Ayni test kosusundaki TUM hatalari tespit et ve tek seferde duzelt.

Kategoriye gore uygun fix uygula. Fix sonrasi kontrol listesi:
- [ ] Degisiklik dogru katmanda mi? (locator → locators/, sabit → data/)
- [ ] `pages/` veya `tests/` icinde selector kalmadi mi?
- [ ] Diger testler etkilendi mi? (`grep` ile kontrol)

### Adim 4: Dogrulama

Fix sonrasi fail olan testi kos:
```bash
pytest {test_dosyasi}::{TestClass}::{test_metodu} -v --browser=chrome
```

Birden fazla fix varsa hepsini tek komutla kos:
```bash
pytest ui_tests/tests/ -k "test_01 or test_03" -v
```

**Her iki browser'da kos** — Chrome fix Chrome fix degil, Firefox'ta da gecmeli.

### Adim 5: Cross-Browser Kontrol

Chrome'da fix yapildiysa Firefox'ta da test kos:
```bash
pytest {test_dosyasi}::{test_metodu} --browser=firefox -v
```

---

## Retry Politikasi

- **Maksimum 3 deneme**: Fix → kos → fail → tekrar fix → kos → fail → tekrar fix → kos
- 3 denemede hala fail: **Manuel inceleme** olarak isaretle
- Kullaniciya bildir: "3 deneme sonrasi hala basarisiz. Manuel inceleme gerekiyor."

---

## Cikti Formati

```
## Fix Raporu

### Fail Eden Test
- **Metod**: test_03_filter_jobs_by_department [chrome, firefox]
- **Hata**: AssertionError: "Quality Assurance" not in []

### Kok Neden
- **Kategori**: Assertion Fail — Icerik Degismis
- **Detay**: Lever job listing sayfasinda QA pozisyonu artik farkli bir URL altinda

### Uygulanan Fix
- **Dosya**: ui_tests/locators/careers_page_locators.py
- **Degisiklik**: `careersPage_qaOpenPositions_btn` selector guncellendi
- **Eski**: `a[href*='lever.co'][href*='Quality']`
- **Yeni**: `a[href*='jobs.lever.co'][href*='QA']`

### Dogrulama
- **Chrome**: PASS ✓
- **Firefox**: PASS ✓
```
