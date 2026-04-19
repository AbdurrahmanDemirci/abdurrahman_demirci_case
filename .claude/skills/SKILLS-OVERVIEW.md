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
│   │   └── load-test.md                ← /Insider-load-test
│   │
│   ├── dev-ops/
│   │   ├── commit.md                   ← /Insider-commit
│   │   └── code-clean.md               ← /Insider-code-clean
│   │
│   └── ui-testing/                     ← Referans dokumanlari (slash komutu yok)
│       ├── test-structure.md
│       ├── data-layer.md
│       └── flows-layer.md
│
└── commands/
    ├── Insider-locator-extract.md
    ├── Insider-scenario-generate.md
    ├── Insider-test-run.md
    ├── Insider-test-fix.md
    ├── Insider-report-analyze.md
    ├── Insider-bug-report.md
    ├── Insider-load-test.md
    ├── Insider-code-clean.md
    └── Insider-commit.md
```

---

## Skill Ozeti

| Skill | Slash Komutu | Ne Yapar |
|-------|-------------|----------|
| **locator-extract** | `/Insider-locator-extract` | URL/HTML/screenshot'tan proje konvansiyonuna uygun Selenium locator uretir, `*_locators.py`'e yazar |
| **scenario-generate** | `/Insider-scenario-generate` | ISTQB standartlarina uygun, duplikasyonsuz pytest test metodlari uretir |
| **test-run** | `/Insider-test-run` | pytest testlerini kosturur, ciktiyi yorumlar, Allure raporu uretir |
| **test-fix** | `/Insider-test-fix` | Fail olan testi kategorize eder (6 kategori), kok nedenini bulur, fix uygular |
| **report-analyze** | `/Insider-report-analyze` | Allure/pytest raporunu okur, pattern tespit eder, aksiyon onerir |
| **bug-report** | `/Insider-bug-report` | Bug vs Test Issue ayirt eder, yapısal bug raporu olusturur, `.generate/`'a yazar |
| **load-test** | `/Insider-load-test` | n11.com search modulu load testini calistirir, sonuclari analiz eder |
| **code-clean** | `/Insider-code-clean` | Commit oncesi Python format ve mimari kural kontrolu yapar, duzeltir |
| **commit** | `/Insider-commit` | Conventional Commits formatinda degisiklikleri gruplar, commit atar, push eder |

---

## Skill Zincirleri

```
Yeni test yazma:
  locator-extract → scenario-generate → test-run → test-fix

Fail analizi:
  test-run → test-fix → report-analyze → bug-report

Commit akisi:
  code-clean → commit

Load test:
  load-test (bagimsiz)
```

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
| Yeni skill eklendi | Bu dosya (dosya yapisi + ozet tablo) |
| Yeni referans dosyasi | Bu dosya + ilgili skill'in referanslar bolumu |
| Proje dizini / komut degisti | `project-config.md` |
| Yeni browser destegi | `project-config.md` + `conftest.py` |
| Yeni load test senaryosu | `load_tests/scenarios/` + `__init__.py` |
| Buyume mimarisi degisti | `project-config.md` → "Buyumeye Acik Mimari" |
