# CI — GitHub Actions Konfigürasyon Skill'i

> **Slash Komutu**: `/Insider-ci`
> **Amac**: GitHub Actions workflow tasariminda dogru pattern'leri uygular; dis bagimliliklar, matrix job, artifact ve tetikleyici konfigürasyonunu yonetir.

---

## Referanslar

- `../project-config.md` → Proje dizin yapisi
- `.github/workflows/tests.yml` → Mevcut workflow

---

## Temel Kurallar

### 1. Dis Siteye Bagli Job — `continue-on-error: true`

Hedef site CI IP'lerini bloklayabilir (bot protection, rate limiting). Bu durumda job fail olur ama pipeline'i kirmamali.

```yaml
load-tests:
  name: Load Tests
  runs-on: ubuntu-latest
  continue-on-error: true   # ← dis siteye bagli her job icin
```

**Ne zaman kullanilir**: Kendi kontrolunde olmayan bir sistemi test eden her job.
**Ne zaman kullanilmaz**: Kendi kodunu/servisini test eden job (UI, unit, API testleri).

---

### 2. `--exit-code-on-error` — Locust Icin

```bash
# YANLIS — dis siteye karsi (n11.com gibi)
locust --headless --exit-code-on-error 1

# DOGRU — dis siteye karsi
locust --headless   # sadece Python/import hatalarinda fail olur

# DOGRU — kendi servisine karsi (staging/local)
locust --headless --exit-code-on-error 1
```

**Kural**: `--exit-code-on-error 1` sadece test edilen servis kendi kontrolundeyse kullanilir.

---

### 3. Path Trigger — Gereksiz CI Calismasini Onle

```yaml
on:
  push:
    paths:
      - 'ui_tests/**'
      - 'load_tests/**'
      - 'locust.conf'
      - 'requirements.txt'
      - '.github/workflows/tests.yml'
```

**Kural**: Hangi job hangi dosyaya baglidir → sadece o path'ler tetikleyici olur. README, skill dosyalari CI'yi tetiklememeli.

---

### 4. Matrix Job — Cross-Browser / Cross-Version

```yaml
strategy:
  fail-fast: false    # ← bir browser fail olursa digeri durmaz
  matrix:
    browser: [chrome, firefox]
```

**`fail-fast: false` zorunlu**: Aksi halde Chrome fail olduğunda Firefox koşmaz, veri kaybolur.

---

### 5. Artifact Upload — Her Zaman `if: always()`

```yaml
- name: Upload results
  if: always()        # ← fail olsa da rapor yuklenir
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: automation-test-results/
    retention-days: 7
```

**Kural**: Test fail oldugunda rapor en cok gereklidir. `if: always()` olmadan fail durumunda artifact yuklenmez.

---

### 6. Locust on_start — Exception Handling (KRITIK)

CI ortaminda `on_start` icinde HTTP cagrisi yapiliyorsa exception yakalanmalidir:

```python
# YANLIS — CI'da hedef site TCP reset yaparsa user crash olur, 0 istek yapilir
def on_start(self) -> None:
    with self.client.get("/", catch_response=True) as resp:
        validate_homepage_response(resp)

# DOGRU
def on_start(self) -> None:
    try:
        with self.client.get("/", catch_response=True) as resp:
            validate_homepage_response(resp)
    except Exception as e:
        logger.warning(f"on_start skipped: {e}")
```

**Neden**: Locust, user class'inda yakalanmamis exception varsa exit code 1 ile cikiyor — `--exit-code-on-error` olmasa bile.

---

### 7. pip Cache — Her Job Icin

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: pip          # ← her job'a ekle, CI suresi yarilir
```

---

## Mevcut Workflow Ozeti

```
tests.yml
├── ui-tests (matrix: chrome, firefox)
│   ├── fail-fast: false
│   ├── path trigger: ui_tests/**, requirements.txt
│   └── artifact: allure-results-ui-{browser} (7 gun)
│
└── load-tests
    ├── continue-on-error: true    ← dis site (n11.com) bloklayabilir
    ├── path trigger: load_tests/**, locust.conf
    └── artifact: locust-results (7 gun)
```

---

## Yeni Job Ekleme Sablonu

```yaml
my-job:
  name: My Job Name
  runs-on: ubuntu-latest
  continue-on-error: false   # kendi servisin ise false, dis site ise true

  steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"
        cache: pip

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests
      run: <komut>

    - name: Upload results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: my-job-results
        path: <rapor-dizini>/
        retention-days: 7
```

---

## Sik Karsilasilan Hatalar

| Hata | Sebep | Cozum |
|------|-------|-------|
| Load test job fail, pipeline kirmizi | Dis site CI IP'lerini blokladi | `continue-on-error: true` |
| Locust 0 istek yapti, exit code 1 | `on_start`'ta exception yakalanmadi | `try/except` ekle |
| Firefox job calistı ama Chrome fail olunca durdu | `fail-fast: true` (default) | `fail-fast: false` ekle |
| Fail durumunda artifact yok | `if: always()` eksik | Her upload step'e ekle |
| Her commit'te CI calisiyor | Path trigger yok | `paths:` filtresi ekle |
