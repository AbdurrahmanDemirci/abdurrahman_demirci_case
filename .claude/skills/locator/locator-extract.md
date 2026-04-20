# Locator Extract — Web Locator Cikarma Skill'i

> **Slash Komutu**: `/Insider-locator-extract`
> **Amac**: Kullanicinin verdigi sayfa bilgisine (URL, HTML snippet, screenshot) gore proje konvansiyonuna uygun Selenium locator'lari cikarir ve ilgili `*_locators.py` dosyasina yazar.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, naming convention, sayfa kontekstleri
- `references/locator-strategy.md` → CSS/XPath oncelik sirasi, Locator sinifi, kontrol listesi

---

## Giris Tipleri

Kullanici asagidakilerden birini verebilir:

| Giris | Nasil Kullanilir |
|-------|-----------------|
| URL | Sayfayi tara, hangi elementlere locator lazim oldugunu sor |
| HTML snippet | Snippeti analiz et, uygun selector'lari cikar |
| Screenshot | Gorsel uzerinden element bolgelerini tespit et |
| Serbest aciklama | "Careers sayfasindaki filtre dropdown'u" gibi — hangi sayfada ne oldugunu sor |

Giris belirsizse su soruyu sor:
> "Hangi sayfa, hangi elementler icin locator lazim?"

---

## Islem Adimlari

### Adim 1: Hangi Sayfaya Ait?

Mevcut sayfa kontekstleri → `project-config.md` → "Dizin Yapisi" bolumunden oku.

Her proje icin `ui_tests/locators/` altindaki dosyalar ve sinif isimleri farklidir.
Yeni bir sayfa icin locator yaziliyorsa → yeni `{sayfa_adi}_locators.py` dosyasi olusturulur.

**Bu Projede (InsiderOne):**

| Kontekst | Dosya |
|----------|-------|
| `homePage` | `ui_tests/locators/home_page_locators.py` |
| `careersPage` | `ui_tests/locators/careers_page_locators.py` |
| `jobListingPage` | `ui_tests/locators/job_listing_page_locators.py` |

### Adim 2: Mevcut Locator'lari Oku

Ilgili `*_locators.py` dosyasini oku:
- Hangi locator'lar zaten var?
- Yeni ekleneceklerle cakisma var mi?

### Adim 3: CSS Selector Oncelik Sirasi

> Tam kural seti ve ornekler: `references/locator-strategy.md` → "CSS mi, XPath mi?" bolumu

**Oncelik sirasi** (en kararli → en kirigan):
`ID` → `data-*` → `CSS class` → `href` → `XPath` (sadece metin eslestirme)

Kacin: pozisyon bazli (`nth-child`, `//div[3]`), dinamik class (`.elementor-repeater-item-56ca501`), cok genel tag (`button`, `div`).

### Adim 4: Locator Key Isimlendir

Format: `{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}`

Element tipleri:
| Tip | Ne zaman |
|-----|----------|
| `_btn` | Tiklanabilir buton |
| `_link` | Navigasyon linki |
| `_input` | Metin girisi |
| `_dropdown` | Acilir liste / secim kutusu |
| `_text` | Sadece okunacak metin / baslik |
| `_section` | Sayfa bolumu |
| `_card` | Tekrar eden kart ogesi |
| `_container` | Genel wrapper |
| `_list` | Liste / koleksiyon |
| `_item` | Liste icindeki tekil oge |
| `_modal` | Modal / dialog penceresi |
| `_checkbox` | Onay kutusu |
| `_label` | Form etiketi |
| `_icon` | Ikon elementi |

### Adim 5: Kodu Uret

```python
from selenium.webdriver.common.by import By
from ui_tests.locators.locator import Locator

class {SayfaAdi}Locators:
    {key} = Locator(By.CSS_SELECTOR, "{selector}")
```

**Yalnizca** test adimlari icin gercekten kullanilacak locator'lar eklenir — "lazim olur" diye onceden yazilmaz.

### Adim 6: Dosyaya Yaz

- Mevcut dosyaya ekleme yapiliyorsa → `Edit` ile ilgili sinifin sonuna ekle
- Yeni sayfa icin → yeni `*_locators.py` dosyasi olustur, import satirlari dahil

### Adim 7: Kontrol Listesi

Yazmadan once dogrula:
- [ ] Format dogru mu? `sayfaAdi_elementAciklamasi_tip`
- [ ] Bu adimlarda gercekten kullanilacak mi?
- [ ] Pozisyona degil anlama dayali mi?
- [ ] Dinamik class icermiyor mu?
- [ ] `Locator(By.X, "...")` ile tanimlandi mi — duz tuple degil?
- [ ] Dogru locator dosyasinda mi?
- [ ] Mevcut locator'larla cakismiyor mu?

### Adim 8: Sonucu Bildir

```
3 locator eklendi → ui_tests/locators/careers_page_locators.py

careersPage_locationFilter_dropdown  = Locator(By.CSS_SELECTOR, "[data-select='location']")
careersPage_departmentFilter_dropdown = Locator(By.CSS_SELECTOR, "[data-select='department']")
careersPage_jobCards_list            = Locator(By.CSS_SELECTOR, ".position-list-item")
```

---

## Onemli Kurallar

1. **Sadece kullanilacak locator**: Test adimlari yoksa locator yazilmaz
2. **CSS oncelikli**: XPath sadece metin eslestirme icin kullanilir
3. **Stabil selector**: Deploy'da degismeyecek attribute'lar secilir
4. **pages/ katmanina dokunma**: Locator eklemek page object'i degistirmez — sayfa yeni metod gerektiriyorsa ayri belirt
5. **Locator sinifi zorunlu**: Duz `(By.X, "...")` tuple degil, `Locator(By.X, "...")` kullanilir

---

## Buyume Prensibi — Locator Katmaninin Rolu

> Detay: `../project-config.md` → "Buyumeye Acik Mimari"

`Locator.__set_name__` sayesinde:
- Yeni locator = **1 satir** `*_locators.py`'de — baska hicbir dosya degismez
- pages/, tests/, flows/ **dokunulmaz**
- Log'larda `By.CSS_SELECTOR '#btn'` yerine `homePage_cookieAccept_btn` gorunur — debug kolayligi

Yeni sayfa eklendiginde:
- `{yeniSayfa}_locators.py` olustur, `class {YeniSayfa}Locators` tanimla
- `pages/{yeni_sayfa}.py`'de `from ui_tests.locators.{yeni_sayfa}_locators import {YeniSayfa}Locators as L` ile import et
- Baska hicbir dosyaya dokunma

Bu kalip projenin herhangi bir sayfasına locator eklemesini tek-satir operasyonu yapar.
