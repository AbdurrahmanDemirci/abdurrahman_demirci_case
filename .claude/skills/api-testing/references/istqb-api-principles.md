# ISTQB API Test Prensipleri

> Bu dosya `scenario-generate.md`'nin referansidir.
> Web UI testleri icin: `../../scenario/references/istqb-principles.md`

---

## API Testine Ozel 6 ISTQB Teknigi

### 1. Equivalence Partitioning (EP) — Denklik Bolgulemesi

**Ne zaman**: Parametre, payload alan veya query string birden fazla gecerli/gecersiz degeri kabul ediyorsa.

**API'de uygulama:**
- Status parametresi: `["available", "pending", "sold"]` → 3 partition, her birinden 1 test
- ID tipi: `int` (gecerli) vs `string` (gecersiz) → 2 partition, her birinden 1 test
- Body varligi: dolu body vs bos body → 2 partition

**Kural**: Ayni partition icindeki degerler ayni davranisi tetikler — sadece birini test et.

**Yanlis:**
```python
def test_find_by_available(self): ...  # ayri
def test_find_by_pending(self): ...    # ayri  ← YANLIS
def test_find_by_sold(self): ...       # ayri
```

**Dogru:**
```python
@pytest.mark.parametrize("status", VALID_STATUSES)  # tek metod, parametrize
def test_find_by_valid_status_returns_200(self, status): ...
```

---

### 2. Boundary Value Analysis (BVA) — Sinir Degeri Analizi

**Ne zaman**: Sayisal ID, offset, limit, page gibi siniri olan parametreler.

**API'de uygulama:**
- ID min: `0` veya `1` (ge?erli min)
- ID max: `999_999_999_999` (gecersiz, cok buyuk)
- Negatif ID: `-1` (gecersiz)
- Limit: `0` (bos liste), `1` (en az 1), `max_limit + 1` (limit asimi)

**Kural**: BVA sadece somut sayisal sinir varsa uygula; status string gibi alanlarda UYGULAMA.

---

### 3. Decision Table (Karar Tablosu)

**Ne zaman**: Birden fazla parametre kombinasyonunun sonucu belirlediginde.

**API'de uygulama:**
```
| status    | category | Beklenti          |
|-----------|----------|-------------------|
| available | Dogs     | 200, dolu liste   |
| available | (bos)    | 200, tum liste    |
| gecersiz  | Dogs     | 200, bos liste    |
| gecersiz  | (bos)    | 200, bos liste    |
```

**Kural**: Kombinasyon sayisi fazlaysa EP ile kirp — her kombinasyonu test etme.

---

### 4. State Transition (Durum Gecisi)

**Ne zaman**: Resource'un yasam dongusu (lifecycle) varsa.

**Pet API ornegi:**
```
[Yok] →[POST /pet]→ [Var: available]
              ↓
         [PUT /pet]
              ↓
      [Var: sold/pending]
              ↓
      [DELETE /pet/{id}]
              ↓
          [Silinmis]
              ↓
        [GET /pet/{id}]
              ↓
            404
```

**Test:** `test_05_delete_pet_returns_200_then_get_returns_404` bu teknigin ornegi.

---

### 5. Error Guessing (Hata Tahmini)

**Ne zaman**: API'nin hata yonetimini, edge case'leri test ederken.

**API'de uygulama — yaygin hatalar:**

| Senaryo | Beklenti |
|---------|----------|
| Bos body (None) | 400, 405, 415 |
| Yanlis Content-Type (text/plain) | 415, 400 |
| ID yerine string ("abc") | 400, 404 |
| Cok buyuk ID (999_999_999_999) | 404 |
| Negatif ID (-1) | 400, 404 |
| Eksik zorunlu alan (photoUrls yok) | 400, 500 |
| ID tipi yanlis body'de (string ID) | 400, 500 |

**Kural**: Petstore gibi lenient API'lerde beklentiler esnek olmali → `in (400, 404, 500)`.

---

### 6. Use Case Testing (Kullanim Senaryosu)

**Ne zaman**: Bastan sona is akislari.

**API'de uygulama:**
- Tam CRUD lifecycle: Olustur → Oku → Guncelle → Sil
- Sadece okuma: Oluştur (fixture) → Listele → Dogrula
- Arama akisi: Statuse gore filtrele → Sonu dogrula

**Kural**: Her use case bir veya birkac test metoduna denk gelir; tek metoda sikilmak zorunda degilsin.

---

## Teknik Secim Rehberi

| Senaryo Tipi                     | Birincil    | Ikincil         |
|----------------------------------|-------------|-----------------|
| Status kodu dogrulama (pozitif)  | Use Case    | EP              |
| Coklu gecerli parametre degeri   | EP          | Parametrize     |
| ID sinir testi                   | BVA         | EP              |
| Bos / null body                  | Error Guess | EP              |
| Yanlis tip (str yerine int)      | Error Guess | EP              |
| Tam CRUD akisi                   | State Trans | Use Case        |
| Coklu parametre kombinasyonu     | Decision T. | EP              |
| Var olmayan resource             | Error Guess | Use Case        |

---

## API Test Maliyeti vs. Degeri

```
Yuksek deger:
  ✓ Temel CRUD (create + get + delete)      → smoke + regression
  ✓ Status kodu dogrulama (200/404/400)     → regression
  ✓ Response field dogrulama               → regression

Orta deger:
  ~ Filtreleme / arama                     → regression
  ~ Parametrik status testleri             → regression

Dusuk deger (yine de yazilmali):
  ~ Tip hatasi senaryolari                → regression
  ~ Bos body / eksik alan                 → regression

Yazilmamali:
  ✗ Ayni partition'dan birden fazla test
  ✗ Fixture'nin saglayacagini tekrar test etmek
  ✗ Petstore veritabanini dogtan kurtarmaya calismak (external state)
```
