# ISTQB Test Tasarim Teknikleri — Web UI Referansi

> Bu dosya `scenario-generate.md` tarafindan okunur.

---

## Equivalence Partitioning (EP)

Girdi uzayini partition'lara bol; ayni sonucu ureten gruptan 1 test degeri yeterli.

**Web'de kullanim:**
- Filtre dropdown'i: gecerli secim (1 test) + gecersiz/bos (1 test)
- Arama kutusu: gecerli keyword (1 test) + sonucsuz keyword (1 test)
- Form alanlari: gecerli format (1 test) + gecersiz format (1 test)

**Yanlis (EP ihlali):**
```python
# Her location icin ayri test — YAPMA
def test_filter_istanbul(self): ...
def test_filter_ankara(self): ...
def test_filter_izmir(self): ...
```

**Dogru:**
```python
# Gecerli location partition'indan 1 test yeterli
def test_filter_by_location_shows_results(self): ...
```

---

## Boundary Value Analysis (BVA)

Sayisal sinirlar veya uzunluk kisitlari olan alanlarda: min-1, min, max, max+1.

**Web'de kullanim:**
- Karakter limiti olan input alanlari
- Sayfa pagination (0 sonuc, 1 sonuc, n sonuc)
- Liste eleman sayisi kontrolleri

**Web'de gereksiz:**
- Etiket, baslik, ikon kontrolleri — BVA gerekmez
- Sadece gorunurluk kontrolleri — BVA gerekmez

---

## State Transition Testing

Sistemin durumundan duruma gecisini test eder.

**Web'de kullanim:**
- Sayfadan sayfaya navigasyon akisi
- Filtre uygulanmis → temizlenmis durumlari
- Login → logout durumlari
- Sekme/modal acik → kapali

---

## Decision Table Testing

Birden fazla kosulun kombinasyonunu test eder.

**Web'de kullanim:**
- Birden fazla filtre birlikte uygulandiginda
- Farkli kullanici rolleri + farkli yetkiler
- Form validasyonunda birden fazla alan kombine kontrol

---

## Use Case / Scenario Testing

Kullanicinin gercek kullanim senaryosunu basa-sona test eder.

**Web'de kullanim:**
- Ana akis: Ana sayfa → Careers → Filtre → Job detay
- Kritik path testi (smoke senaryolari)

---

## Error Guessing

Deneyim ve sezgiye dayali; hata yapilmasi muhtemel noktalari test eder.

**Web'de kullanim:**
- 3. parti sayfa yonlendirmeleri (Lever, LinkedIn)
- Cookie banner kapanmadan yapilan islemler
- Sayfa tam yuklenmeden tiklama
- Bos/null deger durumlarinda liste gosterimi
