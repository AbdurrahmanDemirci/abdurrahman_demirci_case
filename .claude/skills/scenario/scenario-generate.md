# Scenario Generate — pytest Test Senaryosu Uretme Skill'i

> **Slash Komutu**: `/Insider-scenario-generate`
> **Amac**: ISTQB standartlarina uygun, duplikasyonsuz, projenin 5-katmanli POM yapısına uygun pytest test metodlari uretir.

---

## Referanslar

- `../project-config.md` → Naming convention, dizin yapisi, katman kurallari
- `../ui-testing/test-structure.md` → pytest class yapisi, setup fixture, marker kurallari
- `../ui-testing/flows-layer.md` → Cross-page navigasyon; test birden fazla sayfayi kapsiyorsa SiteFlow'dan gecmeli
- `references/istqb-principles.md` → Test tasarim teknikleri
- `references/test-strategy.md` → Smoke/regression stratejisi, mevcut test kapsamı

---

## Temel Prensipler (ASLA Ihlal Edilmez)

### 1. Sifir Duplikasyon
Mevcut testlerde zaten dogrulanan bir davranis icin yeni test yazilmaz.
Yeni assertion gerekiyorsa → mevcut metoda eklenir.

### 2. Katman Kurali
- Selector → `locators/*_locators.py`
- Etkilesim → `pages/*.py`
- Akis → `flows/site_flow.py`
- Sabitler → `data/expected_content.py`
- Senaryo → `tests/test_*.py`

Test metodunda `By.CSS_SELECTOR` veya selector string OLMAZ.
Test metodunda hardcoded assertion string OLMAZ — `expected_content.py`'den gelir.

### 3. ISTQB Maliyet-Etkinlik
- **EP**: Ayni partition'dan 1 test degeri yeterli, her deger icin ayri test yazma
- **BVA**: Sadece sayisal limit olan alanlarda uygulanir
- **Risk-Based**: Kritik akislar (ana sayfa, job listing) → smoke + regression

---

## Agent Calisma Akisi

```
INPUT: Sayfa/ozellik aciklamasi
   |
[ADIM 1] Kapsam & Risk Analizi
   |
[ADIM 2] Mevcut Testleri Kontrol Et (Duplikasyon Kontrolu)
   |
[ADIM 3] Locator Kontrolu
   |
[ADIM 4] ISTQB Teknik Secimi
   |
[ADIM 5] Senaryo Uretimi
   |
[ADIM 6] Completeness Self-Check
   |
OUTPUT: pytest test metodlari → dosyaya yaz
```

---

## ADIM 1 — Kapsam & Risk Analizi

Kullanicidan cikar:

```
Sayfa / Ozellik  : [Hangi sayfa veya akis]
Test Amaci       : [Ne dogrulanacak]
Marker           : [smoke / regression / her ikisi]
Bagimlilıklar    : [Hangi sayfalardan geciliyor]
```

**Risk Skoru (1-5):**
- 5 → Ana akis (ana sayfa, is ilanları) → smoke + regression
- 3-4 → Yardimci sayfa/ozellik → regression
- 1-2 → Edge case / kosmetik → regression (opsiyonel)

---

## ADIM 2 — Mevcut Testleri Kontrol Et

```bash
# Mevcut test metodlarini listele
grep -n "def test_" ui_tests/tests/*.py

# Spesifik sayfayi oku
cat ui_tests/tests/test_{sayfa}.py
```

Mevcut testlerle karsilastir:

```
DEDUPLICATION KONTROLU — [{Sayfa/Ozellik}]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dogrulanacak Davranis       | Zaten Var? | Aksiyon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sayfa URL dogrulama         | test_02    | Mevcut metodda var, YAZMA
Departman kartlari gorunuyor| test_02    | Mevcut metodda var, YAZMA
Is listesi bos degil        | test_03    | Mevcut metodda var, YAZMA
Filtre sonucu konum dogrula | HAYIR      | Yeni test yaz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ADIM 3 — Locator Kontrolu

```bash
# Kullanilacak locator'larin mevcut olup olmadigini kontrol et
grep -n "locator_key" ui_tests/locators/*.py
```

Yoksa: `/Insider-locator-extract` ile once locator olusturulmasi gerektigini bildir.
Page Object sinifi da yoksa: once `/Insider-page-add` calistir, sonra buraya don.

---

## ADIM 4 — ISTQB Teknik Secimi

> Detay: `references/istqb-principles.md`

| Sayfa/Ozellik Tipi | Birincil Teknik | Ikincil |
|---|---|---|
| Sayfa yuklenmesi / gorunurluk | Use Case | EP |
| Navigasyon akisi | State Transition | Use Case |
| Filtre / dropdown | EP | Decision Table |
| Form / input | EP + BVA | Error Guessing |
| Liste / arama | EP + BVA | State Transition |
| 3. parti yonlendirme | Use Case | Error Guessing |
| Icerik dogrulama | Use Case | EP |

---

## ADIM 5 — Senaryo Uretimi

### Test Metodu Kurallari

**Isimlendirme:**
```python
def test_NN_ne_dogrulaniyor(self):
```
- `NN`: mevcut en yuksek numaranin devami
- Kucuk harf, snake_case, aciklayici

**Marker:**
```python
@pytest.mark.smoke
@pytest.mark.regression
def test_NN_...(self):
```

**Yapı:**
```python
@pytest.mark.regression
def test_05_filter_by_location_shows_results(self):
    """
    Step 5: Apply location filter on job listing page and verify
    results are displayed for the selected location.
    """
    job_page = self.flow.navigate_to_qa_jobs(self.home)

    job_page.select_location_filter(E.FILTER_LOCATION)

    jobs = job_page.get_all_job_details()
    assert len(jobs) > 0, "No jobs found after applying location filter"
    assert all(E.EXPECTED_JOB_LOCATION in j["location"] for j in jobs), (
        f"Some jobs do not have location '{E.EXPECTED_JOB_LOCATION}'"
    )
```

**Katman kurali — ne nereye gider:**

| Ne | Nereye |
|----|--------|
| `driver.find_element(By.CSS...)` | `pages/*.py` metoduna |
| `"Quality Assurance"` sabiti | `data/expected_content.py`'e |
| `home → careers → jobs` akisi | `flows/site_flow.py`'e |
| `By.CSS_SELECTOR, ".selector"` | `locators/*_locators.py`'e |

### Tek Sayfa Pozitif + Negatif Birlestirme (EP Kurali)

```python
# DOGRU — Ayni sayfanin tum pozitif kontrolleri TEK metodda
@pytest.mark.regression
def test_05_job_listing_page_elements_present(self):
    job_page = self.flow.navigate_to_qa_jobs(self.home)
    assert job_page.is_job_list_present()
    assert job_page.is_filter_panel_visible()
    assert job_page.get_job_count() > 0

# YANLIS — Her element icin ayri test
def test_05_job_list_present(self): ...     # YAPMA
def test_06_filter_panel_visible(self): ... # YAPMA
def test_07_job_count_positive(self): ...   # YAPMA
```

### Yeni Page Object Metodu Gerekiyorsa

Test metodu yazarken ilgili `pages/*.py`'de henuz olmayan metod gerekiyorsa:
1. Once `pages/*.py`'e metodu ekle
2. Gerekirse `locators/*.py`'e locator ekle
3. Sonra testi yaz

Metod isimlendirme kuralı:
- Eylem: `go_to_X()`, `click_X()`, `select_X_filter()`
- Dogrulama: `is_X_visible()`, `is_X_loaded()`
- Veri: `get_X()`, `get_all_X()`

---

## ADIM 6 — Completeness Self-Check

```
COMPLETENESS SELF-CHECK — [{Sayfa/Ozellik}]
=======================================================================
| Kategori           | Teknik        | Min | Sayi | Test Metodlari    |
| Sayfa Yuklenmesi   | Use Case      | 1   |      |                   |
| Navigasyon         | State Trans.  | 1   |      |                   |
| Icerik Dogrulama   | Use Case + EP | 1   |      |                   |
| Filtre/Etkilesim   | EP            | 1   |      |                   |
| Edge Cases         | Error Guess.  | 1   |      |                   |
| Regression (Smoke) | Risk-Based    | 1   |      |                   |
=======================================================================
```

Eksik kategori varsa kullaniciya bildir.

---

## ADIM 7 — Dosyaya Yaz

- **Mevcut sayfanin testi**: `ui_tests/tests/test_{mevcut}.py` dosyasina ekle
- **Yeni sayfa**: Yeni `ui_tests/tests/test_{yeni_sayfa}.py` olustur — import'lar dahil

**Yeni dosya sablonu:**
```python
import pytest

from ui_tests.flows.site_flow import SiteFlow
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.{yeni_sayfa} import {YeniSayfa}
from ui_tests.data.expected_content import (
    EXPECTED_X,
    EXPECTED_Y,
)


class Test{YeniSayfa}:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.flow = SiteFlow(driver)
        self.home = HomePage(self.driver)
        self.home.open()
        self.flow.handle_cookie_banner()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_NN_...(self):
        ...
```

---

## Coverage Raporu (Her Uretim Sonunda)

```
COVERAGE RAPORU — [{Sayfa/Ozellik}]
══════════════════════════════════════════
Toplam Yeni Metod    : {N}
  - smoke + regression: {N}
  - regression         : {N}

ISTQB Teknikler      : EP, State Transition, Use Case
Onlenen Duplikasyon  : {N} metod tasarruf edildi
Completeness         : {N}/6 kategori karsilandi
══════════════════════════════════════════
```

---

## Onemli Kurallar

1. **Duplikasyon yok**: Mevcut test varsa yeni yazma, assertion ekle
2. **Katman ihlali yok**: Test metodunda selector, driver API OLMAZ
3. **Sabit degerler data katmaninda**: `expected_content.py`'de tanimla, test metodunda import et
4. **Flaky test yazma**: Her kosuda ayni sonucu verecek test yaz — timing varsa page object'te wait uygula
5. **setup'a dokunma**: Ortak baslangic noktasi sabit kalir
6. **Locator once, test sonra**: Locator yoksa once `/Insider-locator-extract` cagir

---

## Buyume Prensibi — Her Uretimde Kontrol Et

> Detay: `../project-config.md` → "Buyumeye Acik Mimari"

Yeni test metodu yazarken su soruyu sor:
**"Bu degisiklik baska bir dosyaya cascade eder mi?"**

- **Yeni sayfa testi**: `class XPage(BasePage)` — base_page.py'e dokunma
- **Yeni assertion**: `expected_content.py`'e sabit ekle, test'te import et
- **Yeni browser**: `conftest.py`'deki `browsers` listesine 1 eleman — test metodlarina dokunma
- **Ortam degisimi**: `.env`'de `BASE_URL` degistir — kod degismez
- **Yeni locator**: `*_locators.py`'e 1 satir — pages/ veya tests/ degismez

Bu kaliplara uymayan kod uretme. Cascade eden degisiklik mimari ihlalidir.
