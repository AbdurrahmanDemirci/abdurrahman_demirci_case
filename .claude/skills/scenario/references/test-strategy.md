# Test Stratejisi Referansi

> Bu dosya `scenario-generate.md` tarafindan okunur.

---

## Marker Stratejisi

| Marker | Ne Zaman | Ornek |
|--------|----------|-------|
| `@pytest.mark.smoke` | Kritik akis — her deployment oncesi kosulur | Ana sayfa yuklendi, QA ilanlar var |
| `@pytest.mark.regression` | Tam test seti — PR'larda kosulur | Tum sayfa ve filtre testleri |
| `@pytest.mark.ui` | Tarayici gerektiren testler — varsayilan | Tum UI testleri |

**Kural**: `smoke` her zaman `regression` ile birlikte kullanilir. Smoke = regression'un altkumesi.

---

## Katman Bazli Test Kapsamı

### Neyi test ederiz?

| Katman | Ne Test Edilir |
|--------|---------------|
| **Sayfa Yuklenmesi** | URL dogru mu? Kritik elementler gorunuyor mu? |
| **Navigasyon** | Sayfalar arasi gecis dogru calisıyor mu? |
| **Icerik Dogrulama** | Dogru veriler mi gorunuyor? (baslik, departman, konum) |
| **Filtre / Interaksiyon** | Kullanici etkilesimi beklenen sonucu veriyor mu? |
| **3. Parti Entegrasyon** | Lever, dis URL yonlendirmeleri dogru mu? |

### Neyi test ETMEYIZ?

- Gorsel detaylar (renk, font, padding) — visual test scope'unda
- Backend API yanit icerigi — API test scope'unda
- Performance / sayfa hizi — ayri scope

---

## Mevcut Test Kaplaması

| Test Metodu | Marker | Ne Test Eder |
|-------------|--------|-------------|
| `test_01_home_page_is_opened_and_loaded` | smoke, regression | Ana sayfa URL + header + hero section |
| `test_02_careers_page_is_opened_and_loaded` | regression | Careers URL + departman kartlari |
| `test_03_qa_jobs_listed` | smoke, regression | Lever job board + liste varligi |
| `test_04_first_qa_job_details_are_correct` | regression | Ilk isin departman + konum + pozisyon icerigni |

---

## Yeni Senaryo Yazarken Karar Agaci

```
Yeni test metodu yazmak istiyorum...
        |
Bu davranis mevcut bir test metodunda zaten dogrulanıyor mu?
   ├── EVET → Yeni metod YAZMA, mevcut metodun assertion'ini guncelle
   └── HAYIR
        |
Bu smoke mi yoksa regression mi?
   ├── Kritik akis / her deployment oncesi → smoke + regression
   └── Detay dogrulama → regression
        |
Hangi sayfada? Mevcut test dosyasi mi yoksa yeni dosya mi?
   ├── Mevcut sayfa → ayni test dosyasina ekle
   └── Yeni sayfa → yeni test_{sayfa}.py olustur
```

---

## Smoke Test Kriteri

Smoke test olmasi icin:
1. Uygulamanin ayakta oldugunu kanitlamali
2. Ana kullanici akisinin calistıgini dogrulamali
3. 2 dakika icinde bitebilmeli (headless)
4. Flaky OLMAMALI — her kosuda ayni sonucu vermeli
