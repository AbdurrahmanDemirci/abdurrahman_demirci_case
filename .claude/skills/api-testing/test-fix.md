# API Test Fix — Hata Duzeltme Skill'i

> **Slash Komutu**: `/Insider-api-test-fix`
> **Amac**: Fail olan API testini 7 kategoriye gore siniflandirir, kok nedeni tespit eder, fix uygular.

---

## Referanslar

- `../project-config.md` → Dizin yapisi
- `test-run.md` → Dogrulama icin test kosma
- `../reporting/bug-report.md` → API davranis hatasi cikarsa bug raporlama

---

## Kullanim

Kullanici su bilgilerden birini saglar:
1. **pytest terminal ciktisi** (fail mesaji + stack trace)
2. **Fail olan test metodu adi**
3. **Genel talep** (ornek: "api testleri fail oluyor")

---

## Failure Kategorileri ve Fix Stratejileri

### Kategori 1: HTTP Status Mismatch

**Belirti:**
```
AssertionError: assert resp.status_code == 200
assert 500 == 200
assert 200 in (400, 404, 405)
```

**Fix Stratejisi:**
1. Hangi endpoint ve metod (GET/POST/PUT/DELETE) fail etti tespit et
2. `api_tests/tests/test_pet.py` ilgili testi oku — beklenti ne?
3. Gercek response'u incele: `resp.text` mesajina bak (stack trace'de varsa)
4. Karar matrisi:
   - Beklenti yanlis, API dogru → testi guncelle (yeni status kodu ekle veya degistir)
   - API yanlis, beklenti dogru → Bug raporu yaz (`/Insider-api-bug-report`)
   - Petstore quirk (belgelenmis) → yorumu guncelle, beklentiyi genislet
5. Fix: `assert resp.status_code in (400, 404)` gibi genisletilmis beklenti ekle

**Dikkat:** Petstore bazi senaryolarda standart HTTP kodlarini vermez.
Mevcut testte yorumlar var (`# Petstore returns 404 instead of 400`) — bu yorum pattern'ini koru.

---

### Kategori 2: Response Field Hatasi

**Belirti:**
```
KeyError: 'id'
AssertionError: assert body["name"] == "Buddy"
assert body["status"] == "available" — body["status"] is "pending"
```

**Fix Stratejisi:**
1. Hangi alan fail etti tespit et
2. `api_tests/data/pet_data.py`'deki `build_pet()` ile gonulen payload'i kontrol et
3. Donulen response schema'yi anlamak icin:
   ```bash
   # Endpoint'i curl ile test et (dogrudan)
   curl -s https://petstore.swagger.io/v2/pet -X POST \
     -H "Content-Type: application/json" \
     -d '{"id":1,"name":"Buddy","status":"available","photoUrls":["x"]}' | python3 -m json.tool
   ```
4. Karar:
   - Alan yok / yeniden adlandirildi → `client/pet_client.py` veya test assertion guncelle
   - Alan degeri yanlis donuyor → test data builder'i (`build_pet`) incele; ID catismasi mi?
   - API degisti, alan kaldirildi → Bug raporu yaz

---

### Kategori 3: Fixture Kurulum Hatasi

**Belirti:**
```
AssertionError: Pet creation failed: {"code":400,"message":"bad input"}
AssertionError: Pet creation failed: {"code":500,"message":"..."}
ERROR api_tests/conftest.py::created_pet — setup failed
```

**Fix Stratejisi:**
1. `api_tests/conftest.py`'deki `created_pet` fixture'ini oku
2. `build_pet()` payload'ini kontrol et — zorunlu alan eksik mi?
   ```bash
   grep -n "def " api_tests/models/pet_model.py
   ```
3. API erisilebilirligini dogrula:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://petstore.swagger.io/v2/pet/1
   ```
4. ID catismasi: `int(time.time() * 1000) % 10**9` dogru ID uretimi sagliyor mu?
5. Fixture'da `yield` oncesi assert fail → tum bagimli testler ERROR olarak isaretlenir
   → Once `test_01_create_pet` calisiyor mu kontrol et (izole calistir)

---

### Kategori 4: Baglanti Hatasi

**Belirti:**
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='petstore.swagger.io')
requests.exceptions.SSLError: ...
socket.gaierror: [Errno 8] nodename nor servname provided
```

**Fix Stratejisi:**
1. `api_tests/config.py`'deki `BASE_URL` degerini kontrol et
2. `.env` dosyasinda `API_BASE_URL` override var mi?
3. Internet baglantisi ve DNS kontrol:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://petstore.swagger.io/v2/pet/1
   ```
4. Petstore gecici downtime: 5 dakika sonra tekrar dene
5. SSL hatasi: Python certifi paketi guncel mi?
   ```bash
   pip install --upgrade certifi requests
   ```

---

### Kategori 5: Timeout

**Belirti:**
```
requests.exceptions.ReadTimeout: HTTPSConnectionPool read timed out. (read timeout=10)
requests.exceptions.ConnectTimeout: ...
```

**Fix Stratejisi:**
1. Mevcut timeout degerini kontrol et: `api_tests/config.py`'de `API_TIMEOUT`
2. `.env`'de `API_TIMEOUT=20` olarak artir (gecici)
3. Ayni endpoint'i manual curl ile test et:
   ```bash
   time curl -s https://petstore.swagger.io/v2/pet/findByStatus?status=available | head -c 100
   ```
4. Sonuc: API gecikmeli → `.env` degerini artir; sistemli gecikme → Bug raporu

---

### Kategori 6: Veri Catismasi (ID Collision)

**Belirti:**
```
# Test gecti ama yanlis pet verisi dondu (baska taraf ayni ID'yi kullanmis)
assert body["name"] == "TestPet"  →  body["name"] == "SomeoneElsesPet"
```

**Fix Stratejisi:**
1. Petstore public API — baska kullanicilar ayni ID'yi kullanabilir
2. `api_tests/data/pet_data.py`'deki ID uretim mekanizmasini kontrol et:
   ```python
   int(time.time() * 1000) % 10**9  # millisaniye bazli — cakisma dusuk ihtimal
   ```
3. Daha benzersiz ID gerekiyorsa:
   ```python
   import random
   random.randint(10**8, 10**9 - 1)  # 9 haneli rastgele
   ```
4. Saat bazli cakisma (parallel testler): pytest-xdist kullanimdaysa her worker farkli ID uretmeli

---

### Kategori 7: API Kontrat Degisimi

**Belirti:**
- Yeni zorunlu alan eklendi (request body'de eksik → 400)
- Alan tipi degisti (string → integer)
- Endpoint kaldirildi veya tasinidi (404 her seferinde)

**Fix Stratejisi:**
1. Petstore Swagger UI'da guncel schema bak:
   `https://petstore.swagger.io/#/pet`
2. Degisen alanlari tespit et
3. `api_tests/data/pet_data.py` → `build_pet()` fonksiyonunu guncelle
4. `api_tests/client/pet_client.py` → URL degistiyse URL'i guncelle
5. Etkilenen tum test assertionlarini guncelle
6. Kontrat degisimi buyukse (`/Insider-api-client-add` ile yeni resource mimarisi kur)

---

## Islem Adimlari

### Adim 1: Failure Analizi

```bash
# Fail ciktisini topla
pytest api_tests/tests/ -v -p no:rerunfailures 2>&1 | tail -50

# Tek fail testi izole calistir
pytest api_tests/tests/test_pet.py::TestPetCrud::{test_metodu} -v -s
```

Yukaridaki 7 kategoriden hangisine girdigini tespit et.

### Adim 2: Bilgi Toplama

```bash
# Ilgili testi oku
grep -rn "def {test_metodu}" api_tests/tests/

# Data builder'i oku
cat api_tests/data/pet_data.py

# Client metodunu oku
cat api_tests/client/pet_client.py

# Config'i oku
cat api_tests/config.py
```

### Adim 3: Fix Uygula

**Onemli**: Ayni kosustaki TUM hatalari tek seferde tespit et ve duzelt.

Fix kontrol listesi:
- [ ] Degisiklik dogru dosyada mi? (data → `data/pet_data.py`, client → `client/pet_client.py`)
- [ ] Diger testler etkilendi mi? (`grep` ile kontrol)
- [ ] Yorum eklenmesi gereken API quirk var mi?

### Adim 4: Dogrulama

```bash
# Sadece fix uygulanan test
pytest api_tests/tests/test_pet.py::TestPetCrud::{test_metodu} -v

# Tam suite — regresyon yok mu?
make api-test
```

---

## Retry Politikasi

- **Maksimum 3 deneme**: Fix → kos → fail → fix → kos → fail → fix → kos
- 3 denemede hala fail: **Manuel inceleme** — kullaniciya bildir
- Kategori 4 (Connection) veya 5 (Timeout): Infra sorunu olabilir, testi beklet

---

## Cikti Formati

```
## API Fix Raporu

### Fail Eden Test
- **Metod**: test_07_get_pet_with_string_id_returns_client_error
- **Hata**: AssertionError: assert 200 in (400, 404)

### Kok Neden
- **Kategori**: HTTP Status Mismatch
- **Detay**: Petstore artik string ID'ye 200 donuyor (onceki davranis 404'du)

### Uygulanan Fix
- **Dosya**: api_tests/tests/test_pet.py
- **Degisiklik**: Beklenti `(400, 404)` → `(200, 400, 404)` genisletildi
- **Yorum eklendi**: "Petstore now returns 200 for string IDs (upsert behavior)"

### Dogrulama
- **Izole**: PASS
- **Tam Suite**: 13/13 PASS
```
