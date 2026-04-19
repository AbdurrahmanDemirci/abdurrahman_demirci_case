# Pre-commit — Pre-commit Hook Kaldirma Skill'i

> **Slash Komutu**: `/Insider-pre-commit`
> **Amac**: Projeden pre-commit hook altyapisini temiz bir sekilde kaldirir; bagli tum dosya ve skill referanslarini gunceller.

---

## Ne Zaman Kullanilir

- Pre-commit hook'lar CI'da calismiyor veya conflict cikariyor
- Takim pre-commit kullanmama karari alindi
- `pre-commit install` yerine manual format kontrolu tercih ediliyor
- `.pre-commit-config.yaml` mevcut, kaldirilmak isteniyor

---

## Etki Analizi — Kaldirmadan Once Kontrol Et

```bash
# pre-commit referanslarini bul
grep -rn "pre-commit" . \
  --include="*.yaml" \
  --include="*.yml" \
  --include="*.txt" \
  --include="*.md" \
  --include="*.toml" \
  --include="*.cfg" \
  --exclude-dir=.git
```

Tipik etkilenen yerler:

| Dosya | Ne Yapilir |
|-------|-----------|
| `.pre-commit-config.yaml` | Sil |
| `requirements-dev.txt` | `pre-commit==X.Y.Z` satirini kaldir |
| `requirements.txt` | Eger varsa `pre-commit` satirini kaldir |
| `Makefile` | pre-commit target'i varsa kaldir |
| `.claude/skills/dev-ops/code-clean.md` | pre-commit bolumunu kaldir, kontroller manuel yap |
| `.claude/skills/dev-ops/commit.md` | pre-commit hook kuralini kaldir |
| `CLAUDE.md` | pre-commit referansi varsa kaldir |
| CI workflow (`tests.yml`) | pre-commit install adimi varsa kaldir |

---

## Islem Adimlari

### Adim 1: Config Dosyasini Sil

```bash
rm .pre-commit-config.yaml
```

### Adim 2: Bagimliligi Kaldir

**requirements-dev.txt varsa:**
```bash
# pre-commit satirini kaldir
# Dosya bos kaliyorsa (sadece -r requirements.txt kaldiysa) dosyayi da sil
```

**requirements.txt'te varsa:**
`pre-commit` satirini sil.

### Adim 3: Yuklu Hook'u Kaldır (Varsa)

```bash
# pre-commit daha once kurulduysa git hook'u kaldir
pre-commit uninstall 2>/dev/null || true

# .git/hooks/ altindaki pre-commit dosyasini kontrol et
ls .git/hooks/pre-commit 2>/dev/null && echo "Hook mevcut, kaldirildi" || echo "Hook kurulu degil"
```

### Adim 4: Skill Referanslarini Guncelle

**code-clean.md:**
- `pre-commit run --files ...` komutunu kaldir
- Aktif hook listesini (`trailing-whitespace`, `end-of-file-fixer` vb.) kaldir
- `debug-statements` kontrolu kaldir ya da "Manuel kontrol gerekli" olarak isaretle
- flake8 Adim 1 kismi kalir — pre-commit olmadan da calisir

**commit.md:**
- "pre-commit hook: aktifse calisir, basarisiz olursa coz" kuralini kaldir

### Adim 5: Dogrulama

```bash
# Hic pre-commit referansi kalmamali
grep -rn "pre-commit" . \
  --include="*.yaml" --include="*.yml" \
  --include="*.txt" --include="*.md" \
  --exclude-dir=.git
```

Cikti bos olmali.

### Adim 6: Manuel Kontrol Listesi (Pre-commit'in Yaptigini Ella Yap)

Pre-commit kalkinca su kontroller commit oncesi manuel yapilmali:

| pre-commit Hook | Manuel Karsiligi |
|-----------------|-----------------|
| `trailing-whitespace` | flake8 `W291` yakalar |
| `end-of-file-fixer` | flake8 `W292` yakalar |
| `check-yaml` | CI'da YAML syntax hatasi gorulur |
| `debug-statements` | code-clean.md Adim 3'te `breakpoint()`/`pdb` grep |
| `flake8` | `flake8 <dosyalar>` → code-clean Adim 1 |

---

## Bu Projede Yapilan (Referans)

| Dosya | Yapilan |
|-------|---------|
| `.pre-commit-config.yaml` | Silindi |
| `requirements-dev.txt` | Tum dosya silindi (icerik kalmadi) |
| `code-clean.md` | pre-commit bolumu (Adim 1 alti) kaldirildi |
| `commit.md` | Kural 9 (pre-commit hook) kaldirildi |

---

## Onemli Notlar

1. **flake8 kalir** — pre-commit olmadan `flake8 <dosyalar>` ile ayni sekilde calisir
2. **CI etkilenmez** — workflow'da `pre-commit install` adimi yoksa CI degismez
3. **debug-statements kontrolu** — pre-commit kalkinca `grep -rn "breakpoint\|pdb" ui_tests/ load_tests/` ile manuel kontrol yap
4. **Geriye donus** — `.pre-commit-config.yaml`'i git'ten geri getirebilirsin; `pre-commit install` ile yeniden aktif edilir
