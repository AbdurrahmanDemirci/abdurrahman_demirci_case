# Flows Katmanı

> **Kapsam**: `ui_tests/flows/`
> **Dosya**: `site_flow.py`

---

## Amaç

Birden fazla sayfayı kapsayan tekrar eden adım dizilerini ve sayfadan bağımsız (cross-cutting) işlemleri
page object içine gömmek yerine ayrı bir `flows/` katmanında toplar.

---

## `SiteFlow` — Mevcut Metodlar

```python
from ui_tests.flows.site_flow import SiteFlow

flow = SiteFlow(driver)
```

### `handle_cookie_banner(action="accept_all")`

Cookie banner'ını kapatır. Banner yoksa sessizce geçer.

```python
flow.handle_cookie_banner()                  # accept_all (varsayılan)
flow.handle_cookie_banner("only_necessary")  # sadece gerekli çerezler
flow.handle_cookie_banner("decline_all")     # reddet
```

Desteklenen action değerleri: `"accept_all"`, `"only_necessary"`, `"decline_all"`

### `navigate_to_qa_jobs(home_page) -> JobListingPage`

Home → Careers → QA Open Positions akışını tek satıra indirir.

```python
job_page = flow.navigate_to_qa_jobs(self.home)
```

İçeride yaptıkları:
1. `home_page.go_to_careers()`
2. `CareersPage.click_see_all_teams()`
3. `CareersPage.click_qa_open_positions()` → `JobListingPage` döner

---

## Test'te Kullanım

```python
@pytest.fixture(autouse=True)
def setup(self, driver):
    self.driver = driver
    self.flow = SiteFlow(driver)
    self.home = HomePage(self.driver)
    self.home.open()
    self.flow.handle_cookie_banner()        # ← cookie page-agnostic

def test_03_qa_jobs_listed(self):
    job_page = self.flow.navigate_to_qa_jobs(self.home)  # ← tek satır
    assert job_page.is_job_list_present()
```

---

## Kural

| Flows'a girer | Flows'a girmez |
|---------------|----------------|
| Birden fazla sayfayı kapsayan akış | Tek sayfaya özgü işlem → page object |
| Tekrar eden navigasyon dizisi | Element locator mantığı → locators |
| Banner / popup gibi her sayfada çıkabilecek işlem | Assertion → test dosyası |

---

## Yeni Flow Eklerken

1. `ui_tests/flows/site_flow.py`'e metod ekle
2. Metodun döndürdüğü page object'i type hint'e yaz
3. `ui-testing/flows-layer.md`'i yeni metodun ornegi ile guncelle
