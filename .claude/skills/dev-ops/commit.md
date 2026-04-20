# Commit — Conventional Commits Standartinda Git Commit Skill'i

> **Slash Komutu**: `/commit`
> **Amac**: Degisiklikleri analiz eder, Conventional Commits standardina uygun mesajlarla commit atar.

---

## Referanslar

- `../project-config.md` → Dizin yapisi, naming convention

---

## Commit Mesaj Formati — Conventional Commits

```
<type>(<scope>): <description>
```

Zorunlu alan: `type` ve `description`.
Tavsiye edilen alan: `scope` — degisen katmayi (layer) belirtir.

### `type` Alani

| Type | Ne Zaman |
|------|----------|
| `test` | Test senaryosu ekleme, duzeltme, silme |
| `fix` | Basarısız testi, yanlis locator'u, hatalı assertion'ı duzeltme |
| `feat` | Yeni page object, yeni helper method, yeni test kapasitesi |
| `refactor` | Davranis degismeden yapisal iyilestirme |
| `chore` | Bagimlılık guncelleme, config, tooling, .claude degisiklikleri |
| `ci` | GitHub Actions workflow degisiklikleri |
| `perf` | Wait suresi, parallel config optimizasyonu |
| `docs` | Dokumantasyon, skill, README degisiklikleri |
| `style` | Yalnizca formatlamayi etkileyen degisiklikler (flake8, whitespace) |

### `scope` Alani — Degisen Katman

| Dosya Konumu | Scope Degeri |
|---|---|
| `ui_tests/tests/**` | `tests` |
| `ui_tests/pages/**` | `pages` |
| `ui_tests/locators/**` | `locators` |
| `ui_tests/flows/**` | `flows` |
| `ui_tests/data/**` | `data` |
| `ui_tests/conftest.py` | `conftest` |
| `ui_tests/config.py` | `config` |
| `utils/**` | `utils` |
| `api_tests/tests/**` | `api-tests` |
| `api_tests/client/**` | `api-client` |
| `api_tests/models/**` | `api-models` |
| `api_tests/schemas/**` | `api-schemas` |
| `api_tests/data/**` | `api-data` |
| `api_tests/conftest.py` | `api-conftest` |
| `api_tests/config.py` | `api-config` |
| `api_tests/api/**` | `api-base` |
| `load_tests/**` | `load` |
| `.github/workflows/**` | `ci` |
| `pytest.ini`, `setup.cfg`, `requirements.txt`, `Makefile` | `config` |
| `.claude/**` | `claude` |

**NOT**: Birden fazla scope etkileniyorsa AYRI commit olur. Tek commit'te birden fazla scope karistirilmaz.

### `description` Alani

- Kucuk harfle baslar, imperative mood (emir kipi) kullanilir
- Ingilizce yazar
- 72 karakteri gecmez
- Nokta ile bitmez

**YASAK — Generic/lazy mesajlar**:
- ~~edited~~, ~~updated~~, ~~changes~~, ~~fix applied~~, ~~fixed~~

**DOGRU — Ne yapildigini anlatan mesajlar**:

| Durum | Ornek |
|---|---|
| Locator xpath degisti | `fix(locators): update careers nav link selector` |
| Yeni locator eklendi | `feat(locators): add job listing filter locators` |
| Page method eklendi | `feat(pages): add get_job_count method to listing page` |
| Test eklendi | `test(tests): add qa jobs filter and listing assertions` |
| Test duzeltildi | `fix(tests): correct expected job count assertion` |
| Flow guncellendi | `refactor(flows): simplify cookie banner handler` |
| Assertion sabiti degisti | `fix(data): update expected department filter text` |
| conftest degisti | `feat(conftest): add screenshot on failure hook` |
| Config degisti | `chore(config): increase explicit wait to 45 seconds` |
| Dependency guncellendi | `chore(config): upgrade selenium to 4.20.0` |
| CI degisti | `ci: add firefox to browser test matrix` |
| Skill eklendi | `docs(claude): add conventional commits skill` |
| API test eklendi | `test(api-tests): add pet update persistence verify test` |
| API client metodu eklendi | `feat(api-client): add find_by_status method to pet client` |
| API schema guncellendi | `fix(api-schemas): add tags field to pet response schema` |
| API model builder guncellendi | `feat(api-models): add without_photo_urls builder method` |
| API data sabiti eklendi | `feat(api-data): add NEGATIVE_PET_ID constant for BVA test` |
| Load senaryo eklendi | `feat(load): add category search scenario with smoke tag` |
| Makefile guncellendi | `chore(config): add ui-smoke make target` |

---

## Ayri Commit Kurali (KRITIK)

Her **scope** ayri commit olur. Ayni anda hem locator hem test degismisse:

```bash
# 1. commit — locators
git add ui_tests/locators/
git commit -m "fix(locators): update careers nav link selector"

# 2. commit — pages
git add ui_tests/pages/
git commit -m "feat(pages): add get_job_count method to listing page"

# 3. commit — tests
git add ui_tests/tests/
git commit -m "test(tests): add qa jobs filter and listing assertions"
```

---

## Islem Adimlari

### Adim 1: Degisiklikleri Analiz Et
```bash
git status
git diff --name-only HEAD
git diff --staged --name-only
```
- Hangi dosyalar degismis?
- Hangi scope'lar etkilenmis?
- `??` (untracked) dosyalari da incele — yeni eklenen dosyalar bunlara dahildir.

### Adim 2: Degisiklikleri Grupla
Scope'lara gore grupla. Her gruba uygun `type` ve `scope` belirle.

### Adim 3: Commit Listesini Goster ve Direkt Ilerle
Kullaniciya atilacak commit'leri goster ve **onay beklemeden devam et**:
```
Atilacak commit'ler:
1. fix(locators): update careers nav link selector  (1 dosya)
2. fix(tests): correct expected job count assertion  (2 dosya)
```

**KRITIK**: "Onayliyor musun?" diye SORMA — listele ve devam et.

### Adim 4: Sirali Commit At
```bash
git add <grup-dosyalari>
git commit -m "<mesaj>"
```

### Adim 5: Push At
Tum commit'ler atildiktan sonra push et:
```bash
git push
```

**Push ZORUNLUDUR** — commit sonrasi her zaman push atilir, ayri onay beklenmez.

### Adim 6: Sonuc Bildir
```
2 commit basariyla atildi ve push edildi:
1. fix(locators): update careers nav link selector
2. fix(tests): correct expected job count assertion
```

---

## Onemli Kurallar

1. **Push zorunlu**: Tum commit'ler atildiktan sonra `git push` atilir — ayri onay beklenmez
2. **Her scope ayri commit**: locators, pages, tests, flows, data — hepsi ayri commit
3. **Generic mesaj yasak**: "edited", "updated", "changes" gibi anlamsiz mesajlar kullanilmaz
4. **Imperative mood**: "add", "fix", "update", "remove" — "added", "fixed" degil
5. **Hassas dosyalar**: `.env`, credential iceren dosyalar ASLA commit edilmez
6. **Staging secici**: `git add -A` yerine degisen dosyalari scope'a gore ekle
7. **Amend yerine yeni commit**: Hook fail olursa amend yapma, yeni commit olustur
8. **Co-Authored-By YASAK**: Commit mesajina `Co-Authored-By` satiri EKLENMEZ
