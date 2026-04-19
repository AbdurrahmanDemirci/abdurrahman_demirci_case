# Locator Stratejisi

> **Kapsam**: insiderone.com UI otomasyonu — Python + Selenium 4
> **Prensip**: Bir locator değiştiğinde sadece locator dosyası güncellenir; page object'e, teste, hiçbir yere dokunulmaz.

---

## Temel Kural: Locator Katmanı

```
ui_tests/locators/   ← SADECE selector tanımları
ui_tests/pages/      ← SADECE etkileşim mantığı (click, find, wait)
ui_tests/tests/      ← SADECE assertion ve senaryo akışı
```

- `pages/` içinde `By.CSS_SELECTOR`, `By.XPATH` veya herhangi bir selector string **asla** bulunmaz.
- `tests/` içinde locator tuple **asla** bulunmaz.
- Selector değişikliği → sadece ilgili `*_locators.py` güncellenir.

---

## İsimlendirme Kuralı

### Format

```
{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}
```

### Bu Projede Kullanılan Sayfa Kontekstleri

| Kontekst | Dosya |
|----------|-------|
| `homePage` | `home_page_locators.py` |
| `careersPage` | `careers_page_locators.py` |
| `jobListingPage` | `job_listing_page_locators.py` |

### Element Tipleri

| Tip | Ne zaman |
|-----|----------|
| `_btn` | Tıklanabilir buton |
| `_link` | Navigasyon linki |
| `_input` | Metin girişi |
| `_dropdown` | Açılır liste / seçim kutusu |
| `_text` | Sadece okunacak metin / başlık |
| `_section` | Sayfa bölümü |
| `_card` | Tekrar eden kart öğesi |
| `_container` | Genel wrapper |
| `_list` | Liste / koleksiyon |
| `_item` | Liste içindeki tekil öğe |

### Bu Projeden Örnekler

```python
# ✅ Projede mevcut locatorlar — tüm liste
homePage_cookieAccept_btn           # Cookie banner kabul butonu
homePage_cookieOnlyNecessary_btn    # Sadece gerekli çerezler
homePage_cookieDecline_btn          # Reddet
homePage_mainNavigation_container   # Header / nav wrapper
homePage_heroSection_section        # Hero bölümü
homePage_careersNavigation_link     # Careers sayfasına giden link

careersPage_departmentCards_section # Departman kartları grid alanı
careersPage_seeAllTeams_btn         # "Tüm ekipleri gör" butonu
careersPage_qaOpenPositions_btn     # QA açık pozisyonlar linki (Lever'a gider)

leverPage_jobItems_list             # Lever iş ilanı posting öğeleri
```

```python
# ❌ Kötü isimlendirme örnekleri
btn1
careers_filter
ACCEPT
cookieBtn
```

---

## `Locator` Sınıfı

`ui_tests/locators/locator.py` içinde tanımlı. Selenium'un beklediği `(by, value)` tuple'ı gibi davranır; ek olarak `.name` özelliği taşır.

```python
class Locator(tuple):
    def __new__(cls, by: str, value: str) -> "Locator":
        instance = super().__new__(cls, (by, value))
        instance.name = f"{by} '{value}'"  # fallback
        return instance

    def __set_name__(self, _owner: type, name: str) -> None:
        self.name = name  # Python class body işlenirken otomatik çağrılır
```

### Nasıl Çalışır?

```python
class HomePageLocators:
    homePage_cookieAccept_btn = Locator(By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
    # Python → __set_name__ → homePage_cookieAccept_btn.name = "homePage_cookieAccept_btn"
```

### Log Farkı

```
# Locator sınıfı olmadan:
CLICK (optional) → css selector '#wt-cli-accept-all-btn'

# Locator sınıfı ile:
CLICK (optional) → homePage_cookieAccept_btn
```

### Selenium Uyumluluğu

`tuple` alt sınıfı olduğundan Selenium API'si değişmez:

```python
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(locator))
driver.find_element(*locator)
```

---

## CSS mi, XPath mi?

### Öncelik Sırası

```
1. ID       → By.CSS_SELECTOR, "#element-id"
2. data-*   → By.CSS_SELECTOR, "[data-department='Quality Assurance']"
3. CSS      → By.CSS_SELECTOR, ".insiderone-icon-cards-grid"
4. href     → By.CSS_SELECTOR, "a[href='/careers/']"
5. XPath    → By.XPATH — sadece metin eşleştirme gerektiğinde
```

### Bu Projeden Örnekler

```python
# CSS — stabil, hızlı (projede kullanılan yöntem)
Locator(By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
Locator(By.CSS_SELECTOR, "a[href='/careers/']")
Locator(By.CSS_SELECTOR, ".insiderone-icon-cards-grid")
Locator(By.CSS_SELECTOR, "a.inso-btn.see-more")
Locator(By.CSS_SELECTOR, "a[href*='lever.co'][href*='Quality']")
Locator(By.CSS_SELECTOR, ".postings-group .posting")

# XPath — metin eşleştirme gerektiğinde kullanılır (bu projede gerek duyulmadı)
# Locator(By.XPATH, "//button[contains(text(), 'Accept')]")
```

### Kaçınılacaklar

```python
# ❌ Pozisyona dayalı
Locator(By.XPATH, "//div[3]/ul/li[2]/a")

# ❌ Elementor dinamik class'ı — deploy'da değişir
Locator(By.CSS_SELECTOR, ".elementor-repeater-item-56ca501")

# ❌ Çok genel
Locator(By.CSS_SELECTOR, "button")
```

---

## Ne Kadar Locator Yazılmalı?

O test adımında **gerçekten kullanılacak** locatorlar yazılır. "Lazım olur" diye önceden yazılmaz.

```python
# ❌ Yanlış — hiçbir test adımında kullanılmayan locatorlar eklendi
class CareersPageLocators:
    careersPage_departmentCards_section = ...
    careersPage_locationSlider_left     = ...  # test adımı yok, gereksiz
    careersPage_teamSection_container   = ...  # test adımı yok, gereksiz

# ✅ Doğru — sadece gerçekten kullanılan locatorlar (bu projedeki gerçek hali)
class CareersPageLocators:
    careersPage_departmentCards_section = Locator(By.CSS_SELECTOR, ".insiderone-icon-cards-grid")
    careersPage_seeAllTeams_btn         = Locator(By.CSS_SELECTOR, "a.inso-btn.see-more")
    careersPage_qaOpenPositions_btn     = Locator(By.CSS_SELECTOR, "a[href*='lever.co'][href*='Quality']")
```

---

## BasePage Entegrasyonu

`base_page.py` içindeki `_name()` helper'ı locator'ın adını loglar:

```python
@staticmethod
def _name(locator: tuple) -> str:
    return getattr(locator, "name", f"{locator[0]} '{locator[1]}'")
```

Her `_click`, `_find`, `_click_if_exists` metodu bu helper'ı kullanır.

---

## Kontrol Listesi

- [ ] Format doğru mu? `sayfaAdı_elementAçıklaması_tip`
- [ ] Bu adımda gerçekten kullanılacak mı?
- [ ] Pozisyona değil anlama dayalı mı?
- [ ] Dinamik class içermiyor mu?
- [ ] `Locator(By.X, "...")` ile tanımlandı mı — düz tuple değil?
- [ ] Doğru locator dosyasında mı?
