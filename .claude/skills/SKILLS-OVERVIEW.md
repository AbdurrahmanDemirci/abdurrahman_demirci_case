# Skills Sistemi — Genel Bakış

> **Son Güncelleme**: 2026-04-19

---

## Dosya Yapısı

```
.claude/skills/
├── SKILLS-OVERVIEW.md              ← Bu dosya
├── project-config.md               ← Merkez config (herkes buradan okur)
├── locator/
│   └── locator-strategy.md         ← Locator isimlendirme, Locator sınıfı, CSS/XPath kuralları
└── ui-testing/
    ├── test-structure.md           ← autouse setup, test isimlendirme, yeni test yazma kuralı
    ├── data-layer.md               ← expected_content.py, assertion sabitleri, kural
    └── flows-layer.md              ← SiteFlow, handle_cookie_banner, navigate_to_qa_jobs
```

---

## Skill Özeti

| Skill | Dosya | İçerik |
|-------|-------|--------|
| **project-config** | `project-config.md` | Dizin yapısı, test komutları, naming convention, ortam değişkenleri |
| **locator-strategy** | `locator/locator-strategy.md` | `sayfaAdı_element_tip` kuralı, `Locator` sınıfı, CSS/XPath seçimi |
| **test-structure** | `ui-testing/test-structure.md` | `autouse` setup fixture, `self.driver`, test isimlendirme, yeni test ekleme akışı |
| **data-layer** | `ui-testing/data-layer.md` | `expected_content.py`, assertion sabitleri, neyin buraya girip girmeyeceği |
| **flows-layer** | `ui-testing/flows-layer.md` | `SiteFlow`, cookie handling, çok sayfalı navigasyon akışları |

---

## Güncelleme Rehberi

| Durum | Ne Güncellenmeli |
|-------|-----------------|
| Yeni skill eklendi | Bu dosyadaki tablo + dosya yapısı |
| Locator kuralı değişti | `locator/locator-strategy.md` |
| Proje dizini / komut değişti | `project-config.md` |
| Yeni test adımı eklendi | İlgili `*_locators.py` |
