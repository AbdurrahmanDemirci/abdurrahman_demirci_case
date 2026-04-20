# Bug Report — Bug Raporlama Skill'i

> **Slash Komutu**: `/Insider-bug-report`
> **Amac**: Test failure'larindan yapısal bug raporu olusturur. Bug ile Test Issue arasinda ayrım yapar.

---

## Referanslar

- `../project-config.md` → Proje ve ortam bilgisi
- `../test-execution/test-fix.md` → UI failure kategori tanimlari (Selenium/browser hatalar)
- `../api-testing/test-fix.md` → API failure kategori tanimlari (HTTP/contract hatalar)

**Hangi test tipini raporluyorsun?**
- UI bug → test-execution/test-fix.md kategorilerini uygula
- API bug → api-testing/test-fix.md kategorilerini uygula (HTTP Status Mismatch, Response Field, API Kontrat Degisimi)

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **pytest terminal ciktisi** veya fail mesaji
2. **Allure results dizini**
3. **Screenshot yolu** (`automation-test-results/screenshots/`)
4. **Manuel gozlem** (ornek: "Su sayfada su oluyor, bug gibi gorunuyor")
5. **test-fix sonucu** (ornek: "Fix denedim ama site bug'i cikti")

---

## Bug vs Test Issue Karar Matrisi

| Durum | Bug mu? | Test Issue mu? |
|-------|---------|----------------|
| Element bulunamiyor, DOM'da yok (yeni HTML incelendi) | Belki (site degisti) | Belki (locator eski) |
| Assertion fail, gercek deger yanlis (site yanlis veri donuyor) | EVET | — |
| Assertion fail, beklenen deger yanlis (test guncellenmeli) | — | EVET |
| Sayfa yuklenmiyor / 4xx-5xx donuyor | EVET | — |
| Beklenmedik yonlendirme (yanlis URL) | EVET | — |
| Form gecersiz veriyi kabul ediyor | EVET | — |
| Job listesi gosterilmiyor / bos liste | EVET | — |
| Timeout, sayfa cok yavash | Belki (performans) | Belki (wait kisa) |
| Sadece Firefox'ta fail | Belki (browser bug) | Belki (browser-specific selector) |
| Driver/Selenium hatasi | — | EVET (infra sorunu) |

**Karar verilemiyorsa**: Her iki olasiligi kullaniciya sun, karar vermesini iste.

---

## Islem Adimlari

### Adim 1: Veriyi Topla

```bash
# Fail ciktisini oku
# pytest terminal outputu veya:
find automation-test-results/allure-results/ -name "*-result.json" | xargs grep -l '"status":"failed"\|"status":"broken"'

# Screenshot varsa listele
ls automation-test-results/screenshots/
```

**Her fail icin toplanacak bilgi:**
- Test metodu adi ve browser
- Hata mesaji (tam)
- Stack trace (ilk 5 satir)
- Screenshot (varsa yolu)
- Hangi sayfa / URL'de fail etti

### Adim 2: Bug vs Test Issue Karar Ver

Karar matrisini uygula. Kategori 6 (Site Bug) veya net site hatasi → BUG raporu yaz.

### Adim 3: Gruplama

Ayni kok nedeni paylasan failure'lari tek BUG altinda topla.
Oncelik ata (Severity rehberi asagida).

### Adim 4: Raporu Olustur ve Kaydet

Dosya adi formati:
```
.generate/bug-report-{GG-AA-YYYY}.md
```

Ornek: `.generate/bug-report-19-04-2026.md`

---

## Rapor Yapisi

```
1. Baslik + Ortam Bilgisi
2. Ozet Metrikler
3. Failure Ozet Tablosu
4. Detayli Bug Raporlari (BUG-01, BUG-02, ...)
5. Oncelikli Aksiyon Listesi
```

### 1. Baslik Blogu

```markdown
# Test Failure Analiz Raporu
**Tarih**: {GG Ay YYYY}
**Browser(lar)**: Chrome, Firefox
**Test Suite**: {smoke / regression / full}
**Kaynak**: pytest + Selenium 4, {proje-sitesi}
```

### 2. Ozet Metrikler

```markdown
## Ozet Metrikler

| Metrik | Deger |
|--------|-------|
| Toplam Test | {total} |
| Basarili | {passed} |
| Basarisiz | {failed} |
| Pass Rate | %{rate} |
```

### 3. Failure Ozet Tablosu

```markdown
## Failure Ozet Tablosu

| # | Kategori | Severity | Tur | Etkilenen |
|---|----------|----------|-----|-----------|
| BUG-01 | {baslik} | P{n} | Bug / Test Issue | {n} test |
```

---

## Bug Raporu Formati (Her BUG-N)

```markdown
---

## BUG-{N} — [{Modul/Sayfa}]: {Kisa aciklama}

**Baslik**: [{Browser}] {Sayfa} — {Net aciklama}

**Etkilenen Testler**:
- `{test_metodu}` [{browser}] — {kisa aciklama}

**Beklenen**: {Ne olmasi gerekiyordu}

**Gercek**: {Ne oldu}

**Analiz**: {Screenshot, hata mesaji ve stack trace'e dayali yorum.
Sayfanin hangi noktasinda ne oldugu, kullanicinin ekranda ne gorecegi aciklanir.
Sadece hata kodunu tekrar etme — davranis ve olasi neden yorumlanir.}

---

| Ortam | Deger |
|-------|-------|
| Browser | {Chrome / Firefox / Her ikisi} |
| URL | {fail olan sayfa URL'i} |
| Test Metodu | {tam metod adi} |
| Screenshot | {varsa dosya yolu} |

| Severity | Oncelik | Tekrar | Cross-Browser |
|----------|---------|--------|---------------|
| {Critical/High/Medium/Low} | P{1-4} | {Her seferinde/Bazen/Nadiren} | {Evet/Hayir/Kontrol edilmeli} |

### Adimlar (Reproduce)

1. {Adim 1}
2. {Adim 2}
3. {Adim 3 — fail olan nokta}

### Kok Neden
{Hata mesaji ve stack trace'e dayali net aciklama.}

### Aksiyon
- [ ] {Somut adim}
- [ ] {Somut adim 2}
```

---

## Severity Rehberi

### Critical (P1)
- Ana sayfa yuklenmiyor
- Login / navigasyon tamamen calismiyor
- Butun testler fail

### High (P2)
- Onemli sayfa veya ozellik calismiyor (Careers, Job Listing)
- Yanlis icerik gosteriliyor (yanlis is ilanlari, yanlis filtre sonucu)
- Her iki browser'da fail

### Medium (P3)
- Belirli filtreleme senaryosunda hata
- Sadece bir browser'da fail (browser-specific)
- Cookie banner gozukmüyor / gizlenemiyor

### Low (P4)
- Edge case'de hata
- Kozmetik sorun (yanlis baslik, kucuk metin hatasi)
- Flaky test (bazen fail bazen pass)

---

## Cikti

1. `.generate/bug-report-{GG-AA-YYYY}.md` dosyasina kaydet
2. Ekrana markdown formatinda yaz
3. Kullaniciya: "Rapor `.generate/` klasorune kaydedildi"
