# API Test Stratejisi — Mevcut Kapsam ve Kurallar

> Bu dosya `scenario-generate.md`'nin referansidir.
> Son Guncelleme: 2026-04-20

---

## Mevcut Kapsam

### Pet API — 6 dosya, 15 test

| Dosya | Test Metodlari | HTTP | Tip | Marker |
|-------|----------------|------|-----|--------|
| `test_pet_create.py` | test_create_pet_returns_200_and_correct_fields | POST /pet | Pozitif | smoke, regression |
| `test_pet_create.py` | test_create_minimal_pet_returns_200 | POST /pet | Pozitif | regression |
| `test_pet_read.py` | test_get_pet_by_id_returns_correct_pet | GET /pet/{id} | Pozitif | smoke, regression |
| `test_pet_read.py` | test_find_by_valid_status_returns_200[available] | GET /pet/findByStatus | Pozitif (param) | regression |
| `test_pet_read.py` | test_find_by_valid_status_returns_200[pending] | GET /pet/findByStatus | Pozitif (param) | regression |
| `test_pet_read.py` | test_find_by_valid_status_returns_200[sold] | GET /pet/findByStatus | Pozitif (param) | regression |
| `test_pet_update.py` | test_update_pet_returns_200_with_updated_fields | PUT /pet | Pozitif | regression |
| `test_pet_delete.py` | test_delete_pet_returns_200_then_get_returns_404 | DELETE /pet/{id} | Pozitif + State | smoke, regression |
| `test_pet_lifecycle.py` | test_full_pet_lifecycle | POST+GET+PUT+GET+DELETE+GET | E2E | smoke, regression |
| `test_pet_negative.py` | test_get_nonexistent_pet_returns_404 | GET /pet/{id} | Negatif | regression |
| `test_pet_negative.py` | test_get_pet_with_string_id_returns_client_error | GET /pet/{id} | Negatif (tip) | regression |
| `test_pet_negative.py` | test_create_pet_with_no_body_returns_error | POST /pet | Negatif | regression |
| `test_pet_negative.py` | test_update_with_invalid_id_type_returns_error | PUT /pet | Negatif (tip) | regression |
| `test_pet_negative.py` | test_delete_nonexistent_pet_returns_404 | DELETE /pet/{id} | Negatif | regression |
| `test_pet_negative.py` | test_find_by_invalid_status_returns_empty_list | GET /pet/findByStatus | Negatif | regression |

**Toplam**: 15 test (4 smoke + 15 regression — overlap var)
**Coverage**: Tum CRUD + findByStatus pozitif + negatif + E2E lifecycle + schema validation

---

## Completeness Self-Check Durumu

| Kategori | Mevcut | Eksik |
|---|---|---|
| POST pozitif + schema | ✓ test_create_pet_returns_200... | — |
| POST minimal payload | ✓ test_create_minimal_pet... | — |
| GET id ile pozitif + schema | ✓ test_get_pet_by_id... | — |
| GET findByStatus parametrize | ✓ test_find_by_valid_status... | — |
| PUT pozitif + schema | ✓ test_update_pet... | — |
| PUT persistence verify | — | Henuz yazilmadi |
| DELETE 200 + GET 404 | ✓ test_delete_pet... | — |
| E2E lifecycle | ✓ test_full_pet_lifecycle | — |
| GET var olmayan ID — 404 | ✓ test_get_nonexistent... | — |
| GET string ID — 400/404 | ✓ test_get_pet_with_string_id... | — |
| GET negatif ID (-1) | — | Henuz yazilmadi |
| POST bos body — 4xx | ✓ test_create_pet_with_no_body... | — |
| PUT gecersiz ID tipi — 4xx | ✓ test_update_with_invalid_id_type... | — |
| DELETE var olmayan — 404 | ✓ test_delete_nonexistent... | — |
| findByStatus gecersiz deger | ✓ test_find_by_invalid_status... | — |

**Mevcut**: 13/15 kategori karsilandi. Eksik: persistence verify + negatif ID (-1).

---

## Smoke Stratejisi

Smoke = Kritik akisin calisiyor olmasi:
- `test_create_pet_returns_200...` — POST, olusturabilir miyiz?
- `test_get_pet_by_id...` — GET, okuyabilir miyiz?
- `test_delete_pet...` — DELETE + state gecisi dogru mu?
- `test_full_pet_lifecycle` — E2E akis calisiyor mu?

Smoke'a EKLENMEMESI gerekenler:
- Parametrize testler (3 kosma = 3x yavaslatma)
- Negatif testler (kritik akis degil)
- Minimal/edge case testler

---

## Regression Stratejisi

Regression = Tum pozitif + negatif + edge case:
- Tum smoke testleri regression'a da dahil
- Parametrize `findByStatus` → 3 status x 1 metod
- Tip hatasi, bos body, var olmayan ID → her CRUD icin 1'er negatif
- Schema dogrulama her pozitif testte

---

## Allure Hiyerarsisi

```
parent_suite = "API Tests"       ← Allure sol panel ust baslik
suite        = "Pet"             ← Resource adi (User, Store, ...)
feature      = "Pet API"         ← Feature panel
story        = "Create/Read/Update/Delete/Lifecycle"
title        = "HTTP METOD /path — aciklama"
```

Yeni resource eklendiginde:
- `parent_suite` ayni kalir: `"API Tests"`
- `suite` yeni resource: `"User"`, `"Store"`, ...
- `feature` yeni resource API: `"User API"`, `"Store API"`, ...

---

## Petstore API Bilinen Davranislar (Quirks)

| Durum | Beklenen (RFC) | Petstore Gercegi | Yorum Ekle |
|-------|---------------|------------------|------------|
| String ID → GET | 400 | 404 | Evet |
| String ID → PUT body | 400 | 400 / 500 | Evet |
| Bos body → POST | 400 / 415 | 400 / 405 / 500 | Evet |
| Gecersiz status → findByStatus | 400 | 200 + bos liste | Evet |
| Var olmayan ID → DELETE | 404 | 404 (tutarli) | Hayir |

**Yorum pattern'i:**
```python
# Petstore returns 200 + empty list for unknown status (lenient validation)
assert resp.status_code == 200
assert resp.json() == []
```

---

## Yeni Resource Kapsam Rehberi

Yeni bir resource (User, Store) eklendiginde minimum kapsam:

| Kategori | Min Test Sayisi | Marker | Dosya |
|----------|-----------------|--------|-------|
| POST pozitif + schema | 1 | smoke + regression | _create.py |
| POST minimal | 1 | regression | _create.py |
| GET id ile pozitif + schema | 1 | smoke + regression | _read.py |
| GET findByX (varsa) | 1 parametrize | regression | _read.py |
| PUT pozitif + schema | 1 | regression | _update.py |
| PUT persistence verify | 1 | regression | _update.py |
| DELETE 200 + GET 404 | 1 | smoke + regression | _delete.py |
| E2E lifecycle | 1 | smoke + regression | _lifecycle.py |
| GET var olmayan | 1 | regression | _negative.py |
| GET gecersiz tip | 1 | regression | _negative.py |
| GET negatif ID (-1) | 1 | regression | _negative.py |
| POST bos body | 1 | regression | _negative.py |
| PUT gecersiz tip | 1 | regression | _negative.py |
| DELETE var olmayan | 1 | regression | _negative.py |
| findByX gecersiz deger | 1 | regression | _negative.py |

**Minimum**: 15 test metodu yeni bir resource icin.

---

## Fixture Kullanim Kurali

| Duruma gore | Ne Kullan |
|-------------|-----------|
| Test kendi verisini olusturuyor, siliyor | Inline: `self.client.create(...)` + `self.client.delete(...)` |
| Test mevcut veriyi okuyor/guncelliyor | `created_{resource}` fixture (otomatik teardown) |
| Sadece okuma (GET) | `created_{resource}` fixture tercihli |

**Kural**: `created_{resource}` fixture kullanan testler silme yapmaz — fixture teardown eder.
Inline olusturulan resource → test sonunda silme zorunlu.
