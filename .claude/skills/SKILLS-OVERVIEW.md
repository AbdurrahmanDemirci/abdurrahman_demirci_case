# Skills Sistemi — Genel Bakis

> **Son Guncelleme**: 2026-04-20
> **Not**: Yeni skill, referans veya flow eklendiginde bu dosya da guncellenmelidir.

---

## Bu Sistem Ne Yapar?

InsiderOne QA Assessment projesi icin tasarlanmis, buyumeye acik bir skill mimarisidir.
**Temel prensip**: Her skill bagimsiz calisabilir; hepsi `project-config.md`'den (merkez config) beslenir.

> Bu proje bir case study olarak baslamis olsa da global olcekte buyumeye hazir tasarlanmistir.
> Tum skill'ler bu buyume felsefesini koda yansitirak uretiim yapar — detay: `project-config.md` → "Buyumeye Acik Mimari" bolumu.

---

## Dosya Yapisi

```
.claude/
├── skills/
│   ├── SKILLS-OVERVIEW.md              ← Bu dosya
│   ├── project-config.md               ← Merkez config + buyume mimarisi (herkes okur)
│   │
│   ├── locator/
│   │   ├── locator-extract.md          ← /Insider-locator-extract
│   │   └── references/
│   │       └── locator-strategy.md     ← CSS/XPath kurallari, Locator sinifi
│   │
│   ├── scenario/
│   │   ├── scenario-generate.md        ← /Insider-scenario-generate
│   │   └── references/
│   │       ├── istqb-principles.md     ← Web icin 6 ISTQB teknigi
│   │       └── test-strategy.md        ← Smoke/regression stratejisi, mevcut kapsam
│   │
│   ├── test-execution/
│   │   ├── test-run.md                 ← /Insider-test-run
│   │   └── test-fix.md                 ← /Insider-test-fix
│   │
│   ├── reporting/
│   │   ├── report-analyze.md           ← /Insider-report-analyze
│   │   └── bug-report.md               ← /Insider-bug-report
│   │
│   ├── load-testing/
│   │   ├── load-test.md                ← /Insider-load-test
│   │   └── load-scenario-add.md        ← /Insider-load-scenario-add
│   │
│   ├── dev-ops/
│   │   ├── commit.md                   ← /Insider-commit
│   │   ├── code-clean.md               ← /Insider-code-clean
│   │   └── ci.md                       ← /Insider-ci
│   │
│   ├── api-testing/
│   │   ├── test-run.md                 ← /Insider-api-test-run
│   │   ├── test-fix.md                 ← /Insider-api-test-fix
│   │   ├── scenario-generate.md        ← /Insider-api-scenario-generate
│   │   ├── client-add.md               ← /Insider-api-client-add
│   │   └── references/
│   │       ├── istqb-api-principles.md ← API icin 6 ISTQB teknigi
│   │       └── api-test-strategy.md    ← Mevcut kapsam, smoke/regression stratejisi
│   │
│   └── ui-testing/                     ← Referans dokumanlari (slash komutu yok)
│       ├── page-add.md                 ← /Insider-page-add
│       ├── test-structure.md
│       ├── data-layer.md
│       └── flows-layer.md
│
└── commands/
    ├── Insider-locator-extract.md
    ├── Insider-page-add.md
    ├── Insider-scenario-generate.md
    ├── Insider-test-run.md
    ├── Insider-test-fix.md
    ├── Insider-report-analyze.md
    ├── Insider-bug-report.md
    ├── Insider-load-test.md
    ├── Insider-load-scenario-add.md
    ├── Insider-code-clean.md
    ├── Insider-commit.md
    ├── Insider-ci.md
    ├── Insider-api-test-run.md
    ├── Insider-api-test-fix.md
    ├── Insider-api-scenario-generate.md
    └── Insider-api-client-add.md
```

---

## Skill Ozeti

| Skill | Slash Komutu | Ne Yapar |
|-------|-------------|----------|
| **locator-extract** | `/Insider-locator-extract` | URL/HTML/screenshot'tan proje konvansiyonuna uygun Selenium locator uretir, `*_locators.py`'e yazar |
| **page-add** | `/Insider-page-add` | Yeni UI sayfasi icin locator dosyasi, Page Object sinifi ve gerekiyorsa SiteFlow metodunu 5-katmanli POM mimarisine uygun olusturur |
| **scenario-generate** | `/Insider-scenario-generate` | ISTQB standartlarina uygun, duplikasyonsuz pytest test metodlari uretir |
| **test-run** | `/Insider-test-run` | pytest testlerini kosturur, ciktiyi yorumlar, Allure raporu uretir |
| **test-fix** | `/Insider-test-fix` | Fail olan testi kategorize eder (6 kategori), kok nedenini bulur, fix uygular |
| **report-analyze** | `/Insider-report-analyze` | Allure/pytest raporunu okur (UI veya API context), pattern tespit eder, aksiyon onerir; Locust HTML raporunu da analiz eder |
| **bug-report** | `/Insider-bug-report` | Bug vs Test Issue ayirt eder, yapısal bug raporu olusturur, `.generate/`'a yazar |
| **load-test** | `/Insider-load-test` | Locust load testini calistirir, P95 esigi analiz eder, sonuclari raporlar |
| **load-scenario-add** | `/Insider-load-scenario-add` | Mevcut Locust mimarisine yeni HttpUser + TaskSet senaryosu ekler; data, validator ve __init__ kaydini gunceller |
| **code-clean** | `/Insider-code-clean` | Commit oncesi Python format ve mimari kural kontrolu yapar, duzeltir |
| **commit** | `/Insider-commit` | Conventional Commits formatinda degisiklikleri gruplar, commit atar, push eder |
| **ci** | `/Insider-ci` | GitHub Actions workflow tasariminda dogru pattern uygular; dis bagimlilık, matrix, artifact ve tetikleyici konfigürasyonunu yonetir |
| **api-test-run** | `/Insider-api-test-run` | API testlerini kosturur, HTTP hata tiplerini yorumlar, Allure raporu uretir |
| **api-test-fix** | `/Insider-api-test-fix` | Fail olan API testini 7 kategoriye gore siniflandirir, kok nedenini bulur, fix uygular |
| **api-scenario-generate** | `/Insider-api-scenario-generate` | ISTQB standartlarina uygun, duplikasyonsuz API pytest test metodlari uretir |
| **api-client-add** | `/Insider-api-client-add` | Yeni API resource icin client, data builder ve conftest fixture'ini PetClient mimarisine uygun olusturur |

---

## Skill Zincirleri

```
Yeni UI sayfasi ekleme:
  locator-extract → page-add → scenario-generate → test-run → test-fix

UI fail analizi:
  test-run → test-fix → report-analyze [UI context] → bug-report

Yeni API resource:
  api-client-add → api-scenario-generate → api-test-run → api-test-fix

API fail analizi:
  api-test-run → api-test-fix → report-analyze [API context] → bug-report

Yeni load senaryosu:
  load-scenario-add → load-test → report-analyze [Locust bolumu]

Commit akisi (hepsi icin):
  code-clean → commit

CI/CD:
  ci (workflow tasarimi / yeni job ekleme)
```

### Hangi Sorun → Hangi Skill?

| Sorun | Skill |
|-------|-------|
| Yeni UI elementi lazim | `/Insider-locator-extract` |
| Yeni UI sayfasi ekleyecegim | `/Insider-page-add` |
| Yeni UI test yazacagim | `/Insider-scenario-generate` |
| UI testleri fail oluyor | `/Insider-test-fix` |
| Yeni API resource ekleyecegim | `/Insider-api-client-add` |
| API test yazacagim | `/Insider-api-scenario-generate` |
| API testleri fail oluyor | `/Insider-api-test-fix` |
| Yeni load senaryosu ekleyecegim | `/Insider-load-scenario-add` |
| Load test calistiracagim | `/Insider-load-test` |
| Test raporunu analiz etmek istiyorum | `/Insider-report-analyze` |
| Bug raporu yazmak istiyorum | `/Insider-bug-report` |
| Commit atacagim | `/Insider-commit` |
| CI/CD degisiklik yapacagim | `/Insider-ci` |

---

## Buyume Kaliplari — Her Skill Bunlara Uyar

Asagidaki kaliplar kodun her katmanina islenmi? olup her skill bu felsefeve gore uretim yapar.
Detayli aciklama: `project-config.md` → "Buyumeye Acik Mimari" bolumu.

### UI Test Katmanindaki Kaliplar

```
BasePage mirasi     → Yeni sayfa = class XPage(BasePage), baska kod degismez
Locator.__set_name__ → Yeni locator = 1 satir, kayit gerekmez
env-driven config   → Ortam degisimi = env var, kod dokunulmaz
pytest matrix       → Yeni browser = conftest'e 1 satir
5-katman POM        → UI degisimi sadece 1 katmani etkiler
expected_content.py → Icerik degisimi = 1 dosya
```

### Load Test Katmanindaki Kaliplar

```
scenarios/ klasoru        → Yeni senaryo = yeni dosya + 1 import
config.py merkezi         → Yeni ortam = 1 satir
locustfile.py ince        → Entry point'e hic dokunulmaz
LOAD_TEST_ENV             → Ortam gecisi = env var
data/search_data.py       → Yeni assertion sabiti = 1 satir, validator'e dokunulmaz
utils/response_validator  → Validation merkezi; senaryo dosyasinda inline kontrol yok
load_tests/utils/logger   → Bagimsiz logger; proje root utils/ ile sys.path catismasi yok
```

### Skill Uretiminde Buyume Prensibi

Yeni kod yazarken her skill su soruyu sorar:
> "Bu degisiklik baska bir dosyaya cascade eder mi?"
- Eder → Katman ihlali, yapiyi gozden gecir
- Etmez → Dogru katmana yazilmis

---

## Guncelleme Rehberi

| Durum | Ne Guncellenmeli |
|-------|-----------------|
| Yeni skill eklendi | Bu dosya (dosya yapisi + ozet tablo + zincirler) |
| Yeni referans dosyasi | Bu dosya + ilgili skill'in referanslar bolumu |
| Proje dizini / komut degisti | `project-config.md` |
| Yeni browser destegi | `project-config.md` + `conftest.py` |
| Yeni load test senaryosu | `load_tests/scenarios/` + `__init__.py` |
| Buyume mimarisi degisti | `project-config.md` → "Buyumeye Acik Mimari" |
