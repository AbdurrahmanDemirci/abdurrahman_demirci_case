# Page Add — Yeni UI Sayfa Ekleme Skill'i

> **Slash Komutu**: `/Insider-page-add`
> **Amac**: Yeni bir UI sayfası için locator dosyası, Page Object sınıfı ve gerekiyorsa SiteFlow metodunu projenin 5-katmanlı POM mimarisine uygun şekilde oluşturur.

---

## Referanslar

- `../project-config.md` → Dizin yapısı, naming convention, BasePage API
- `../locator/locator-extract.md` → Locator dosyası zaten oluşturulduysa bu adımı atla
- `../scenario/scenario-generate.md` → Oluşturduktan sonra test senaryosu üretimi için
- `flows-layer.md` → SiteFlow'a ne zaman metod eklenir

---

## Kullanım

Kullanıcı şu bilgilerden birini sağlar:
1. **Sayfa adı + URL** (örnek: "About sayfası, /about/")
2. **Screenshot veya HTML** (locator çıkarımı için)
3. **Mevcut locator dosyası** (zaten `/Insider-locator-extract` çalıştırıldıysa)

---

## Agent Çalışma Akışı

```
INPUT: Sayfa adı + URL/HTML/screenshot
   |
[ADIM 1] Mevcut Yapıyı Kontrol Et
   |
[ADIM 2] Locator Dosyası Oluştur / Doğrula
   |
[ADIM 3] Page Object Sınıfı Oluştur
   |
[ADIM 4] SiteFlow Güncellemesi (gerekiyorsa)
   |
[ADIM 5] expected_content.py Güncellemesi (gerekiyorsa)
   |
[ADIM 6] Doğrula
   |
OUTPUT: Sayfa hazır, /Insider-scenario-generate kullanılabilir
```

---

## ADIM 1 — Mevcut Yapıyı Kontrol Et

```bash
ls ui_tests/locators/
ls ui_tests/pages/
grep -n "def " ui_tests/flows/site_flow.py
cat ui_tests/data/expected_content.py
```

Kontrol: `{page}_locators.py` veya `{page}_page.py` zaten var mı?
Varsa → mevcut dosyayı oku, eksik parçaları ekle.

---

## ADIM 2 — Locator Dosyası Oluştur / Doğrula

Locator dosyası varsa (locator-extract çalıştırıldıysa) doğrula ve ADIM 3'e geç.
Yoksa oluştur:

**Dosya**: `ui_tests/locators/{page}_locators.py`

```python
from selenium.webdriver.common.by import By

from ui_tests.locators.locator import Locator


class {Page}Locators:
    {pageName}_{elementDescription}_{elementType} = Locator((By.CSS_SELECTOR, "..."))
    {pageName}_{elementDescription}_{elementType} = Locator((By.XPATH, "..."))
```

**Naming convention** (`project-config.md`):
```
{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}
```
- sayfaKonteksti: `aboutPage`, `contactPage`, `blogPage`
- elementTipi: `btn`, `link`, `input`, `dropdown`, `text`, `section`, `card`, `container`, `list`, `item`
- Örnek: `aboutPage_heroTitle_text`, `contactPage_submitForm_btn`

**Locator seçim önceliği:**
1. `data-testid`, `data-cy` → değişmez, tercih et
2. Benzersiz CSS class → sınıf değişmezse kullanılabilir
3. ARIA rolü + metin → erişilebilir, kararlı
4. XPath — son çare; sadece CSS erişilmez olduğunda

---

## ADIM 3 — Page Object Sınıfı Oluştur

**Dosya**: `ui_tests/pages/{page}_page.py`

```python
from selenium.webdriver.remote.webdriver import WebDriver

from ui_tests.config import BASE_URL
from ui_tests.locators.{page}_locators import {Page}Locators as L
from ui_tests.pages.base_page import BasePage


class {Page}Page(BasePage):
    PAGE_URL = BASE_URL + "/{path}/"

    def is_page_loaded(self) -> bool:
        return self._is_visible(L.{pageName}_{mainSection}_section)

    def {action_method}(self) -> "{ReturnPage}Page":
        self._click(L.{pageName}_{element}_btn)
        return {ReturnPage}Page(self.driver)

    def get_{data_name}(self) -> str:
        return self._find(L.{pageName}_{element}_text).text
```

**BasePage'den ücretsiz gelen metodlar — yeniden yazmak YASAK:**
- `open()` → PAGE_URL'e git, document.readyState bekle
- `_find(locator)` → element presence bekler, döndürür
- `_click(locator)` → clickable bekler, scroll, tıkla (JS fallback)
- `_click_if_exists(locator, timeout=5)` → varsa tıkla, bool döndür
- `_is_visible(locator, timeout=5)` → görünür mü, bool döndür
- `_navigate_via_href(locator)` → href oku, doğrudan navigate (SPA linkler için)
- `get_current_url()`, `get_title()`, `is_on_correct_page()`

**Metod isimlendirme:**
- Eylem: `go_to_{target}()`, `click_{element}()`
- Doğrulama: `is_page_loaded()`, `is_{condition}()`
- Veri çekme: `get_{data_name}()`, `get_all_{data_name}s()`

**Dönüş tipi kuralı:**
- Aynı sayfada kalıyorsa → `return self`
- Başka sayfaya geçiyorsa → `return {TargetPage}(self.driver)`
- Veri döndürüyorsa → `str`, `list[dict]`, vb.

---

## ADIM 4 — SiteFlow Güncellemesi (Koşullu)

Yeni sayfaya giden yol **birden fazla sayfayı kapsıyorsa** `site_flow.py`'e metod ekle.
Tek sayfadan erişiliyorsa (örn. direkt URL) SiteFlow'a dokunma.

**Kural (flows-layer.md):**
| Flows'a girer | Flows'a girmez |
|---------------|----------------|
| Birden fazla sayfayı kapsayan navigasyon | Tek sayfaya özgü işlem → page object |
| Her sayfada çıkabilecek popup/banner | Locator mantığı → locators |

Gerekiyorsa:
```python
# ui_tests/flows/site_flow.py — mevcut metodların ALTINA ekle

def navigate_to_{target}(self, start_page: {StartPage}) -> {TargetPage}:
    start_page.{step_one_method}()
    intermediate = {IntermediatePage}(self.driver)
    return intermediate.{step_two_method}()
```

---

## ADIM 5 — expected_content.py Güncellemesi (Koşullu)

Test assertion'larında kullanılacak sabit stringler varsa ekle:

```python
# ui_tests/data/expected_content.py — mevcut sabitlerin ALTINA ekle

{PAGE_NAME}_TITLE_KEYWORD = "{keyword}"
EXPECTED_{PAGE_NAME}_{FIELD} = "{value}"
```

Sadece **sabit içerik** buraya gider. Locator ve URL buraya GELMEz.

---

## ADIM 6 — Doğrula

```bash
# Dosya varlık kontrolü
ls ui_tests/locators/{page}_locators.py
ls ui_tests/pages/{page}_page.py

# Import kontrolü
.venv/bin/python -c "from ui_tests.pages.{page}_page import {Page}Page; print('Page OK')"
.venv/bin/python -c "from ui_tests.locators.{page}_locators import {Page}Locators; print('Locators OK')"

# Collect kontrolü
.venv/bin/pytest ui_tests/ --collect-only -q 2>&1 | head -20
```

Hata yoksa: "`/Insider-scenario-generate` ile test senaryoları yazılabilir" mesajı ver.

---

## Çıktı Formatı

```
## Sayfa Ekleme Raporu

### Oluşturulan / Güncellenen Dosyalar
- `ui_tests/locators/{page}_locators.py`  — {N} locator tanımı
- `ui_tests/pages/{page}_page.py`         — {Page}Page(BasePage), {N} metod
- `ui_tests/flows/site_flow.py`           — navigate_to_{target}() eklendi  [koşullu]
- `ui_tests/data/expected_content.py`     — {N} sabit eklendi               [koşullu]

### Sayfanın Metodları
| Metod | Döndürür | Açıklama |
|-------|----------|----------|
| is_page_loaded() | bool | {main_section} görünür mü |
| {method_name}() | {ReturnType} | {açıklama} |

### Doğrulama
- Import: OK
- Collect: OK
- Sonraki adım: /Insider-scenario-generate ile test yaz
```

---

## Önemli Kurallar

1. **BasePage extend et** — `__init__`, `open()`, `_find()`, `_click()` yeniden yazma
2. **Locator dosyasına bak** — locator-extract çalıştırıldıysa yeniden üretme
3. **PAGE_URL zorunlu** — `BasePage.open()` ve `is_on_correct_page()` buna bağlı
4. **SiteFlow koşullu** — tek sayfadan erişilen sayfalar için SiteFlow gereksiz
5. **`__init__.py` ekleme** — `ui_tests/` namespace package; `__init__.py` gereksiz
6. **Cascade yok** — yeni sayfa sadece kendi dosyasını ve varsa SiteFlow'u etkiler
