# Code Clean — Python Format ve Mimari Kontrol Skill'i

> **Slash Komutu**: `/Insider-code-clean`
> **Amac**: Commit oncesi degisen Python dosyalarinda format, stil ve mimari kurallari kontrol eder; otomatik duzeltir veya raporlar.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, katman kurallari, naming convention
- `commit.md` → Commit oncesi bu skill calistirilir

---

## Tetikleme

- `/Insider-code-clean` ile manuel calistirilir
- `/Insider-commit` oncesinde otomatik tetiklenebilir (kullanici tercihine gore)

---

## Kontrol Edilecek Dosyalar

```bash
git diff --name-only HEAD
git diff --name-only --staged
```

Degisen dosyalar taranir. Kapsam:
- `ui_tests/**/*.py`
- `utils/**/*.py`
- `conftest.py`

`.venv/`, `__pycache__/`, `automation-test-results/` KAPSAM DISI.

---

## Adim 1: Otomatik Araclar

### flake8

```bash
flake8 <degisen-dosyalar>
```

Konfigurasyon (`setup.cfg`):
- `max-line-length = 100`
- `extend-ignore = E221` (hizalama amaçli çoklu bosluk — locator tanimlari için izinli)
- exclude: `.git`, `__pycache__`, `.env`, `automation-test-results`, `venv`, `.venv`

**Sik Karsilasilan Hatalar ve Duzeltme**:

| Kod | Hata | Duzeltme |
|-----|------|----------|
| E501 | Satir 100+ karakter | Satiri böl veya kısalt |
| F401 | Import edilip kullanilmayan modul | Import satirini sil |
| E302 | 2 bos satir bekleniyor | Sinif/fonksiyon oncesi 2 bos satir ekle |
| E303 | Fazla bos satir | Fazla satirlari sil |
| W291 | Trailing whitespace | Satir sonu bosluklarini sil |
| W292 | Dosya sonu newline yok | Dosya sonuna newline ekle |
| E711 | `== None` yerine `is None` | `is None` / `is not None` kullan |
| F811 | Tekrar tanimlanan isim | Duplicate tanimlamayi sil |

**KRITIK**: flake8 hatasi varsa duzelt, commit'e gecme.

### pre-commit (varsa kurulu)

```bash
pre-commit run --files <degisen-dosyalar>
```

Aktif hook'lar:
- `trailing-whitespace` — satir sonu bosluklari
- `end-of-file-fixer` — dosya sonu newline
- `check-yaml` — YAML syntax
- `debug-statements` — unutulan `breakpoint()`, `pdb.set_trace()` tespiti

**`debug-statements` KRITIK**: Test dosyalarinda `breakpoint()` veya `import pdb` varsa commit EDILMEZ — sil.

---

## Adim 2: Mimari Katman Kurallari

### Kural 1: Selector Katman Ihlali

`pages/**` veya `tests/**` icinde asagidakiler OLMAMALI:

```python
# YASAK — pages/ veya tests/ icinde:
By.CSS_SELECTOR
By.XPATH
By.ID
By.CLASS_NAME
(By.
```

Tespit edilirse: selector'i ilgili `*_locators.py` dosyasina tasi, sayfadan `L.` ile referans ver.

### Kural 2: Locator Dosyasinda Duz Tuple

`locators/**` icinde duz `(By.X, "...")` tuple OLMAMALI, `Locator(By.X, "...")` kullanilmali:

```python
# YANLIS:
some_element = (By.CSS_SELECTOR, ".btn")

# DOGRU:
some_element = Locator(By.CSS_SELECTOR, ".btn")
```

### Kural 3: Test Assertion Sabitleri

`tests/**` icinde hardcoded string assertion OLMAMALI, `data/expected_content.py`'den gelmeli:

```python
# YANLIS:
assert "Quality Assurance" in text

# DOGRU:
from ui_tests.data.expected_content import ExpectedContent as E
assert E.DEPARTMENT_NAME in text
```

**Not**: Basit `assert driver.title` gibi assertions bu kurala girmez. Yalnizca is tanimina ait sabit string degerler `data/` katmanina tasınır.

### Kural 4: config.py Kapsami

`ui_tests/config.py` SADECE env/altyapi ayarlari icermeli:
- Browser tipi, URL'ler, timeout, dizin yollari

**OLMAMALI**:
- Test assertion sabitleri → `data/expected_content.py`
- Selector / locator → `locators/*_locators.py`

### Kural 5: Locator Naming Convention

`locators/**` icindeki key'ler `{sayfaKonteksti}_{elementBetimlemesi}_{elementTipi}` formatinda olmali:

```python
# DOGRU:
homePage_cookieAccept_btn
careersPage_departmentCards_section
jobListingPage_jobItems_list

# YANLIS:
btn1, acceptButton, COOKIE_BTN, careers_filter
```

---

## Adim 3: Python Genel Kalite Kontrolleri

- **Kullanilmayan import**: `F401` flake8 yakalar, sil
- **Duplicate import**: Ayni modul iki kez import edilmis, tekrari sil
- **Gereksiz yorum**: Sadece kodu tekrar eden yorumlar (`# click the button` gibi) — sil
- **Magic number**: Test kodunda aciklamasiz sabit sayi varsa `expected_content.py`'e tasi
- **Type hint tutarliligi**: Mevcut metodlarda tip hint varsa yeni metodlarda da olmali

---

## Adim 4: Sonuc Raporu

```
Code Clean Sonucu:
✓ ui_tests/locators/careers_page_locators.py — sorun yok
✓ ui_tests/pages/careers_page.py — 1 trailing whitespace duzeltildi
✗ ui_tests/tests/test_insider_careers.py — flake8 E302 (2 bos satir eksik, duzeltildi)
⚠ ui_tests/pages/home_page.py — katman ihlali: By.CSS_SELECTOR bulundu (manuel mudahale gerekli)
```

Semboller:
- `✓` — temiz veya otomatik duzeltildi
- `✗` — sorun vardi, otomatik duzeltildi
- `⚠` — manuel mudahale gerekiyor, commit'e gecme

---

## Onemli Kurallar

1. **flake8 hatasi varsa commit YAPMA** — once duzelt
2. **debug-statements commit EDILMEZ** — `breakpoint()`, `pdb` bulunursa sil
3. **Selector katman ihlali** — pages/ veya tests/ icinde selector varsa locators/ katmanina tasi
4. **Otomatik duzeltme**: trailing whitespace, end-of-file newline, flake8 E302/E303 → otomatik duzelt
5. **Manuel mudahale gerektiren**: katman ihlali, assertion sabiti — raporla, kullaniciya birak
6. **Format degisikligi ayri commit OLMAZ** — diger degisikliklerle birlikte commit edilir
