# Test Yapısı

> **Kapsam**: `ui_tests/tests/` içindeki test dosyaları
> **Dosyalar**: `test_home_page.py`, `test_insider_careers.py`

---

## Temel Yapı

Her test class'ı `autouse=True` fixture ile başlar. Bu fixture WebdriverIO'nun `beforeEach` karşılığıdır — her test metodundan önce otomatik çalışır.

```python
import pytest
from ui_tests.flows.site_flow import SiteFlow
from ui_tests.pages.home_page import HomePage

class TestHomePage:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Her testten önce: browser aç, ana sayfaya git, cookie banner'ı kapat."""
        self.driver = driver
        self.flow = SiteFlow(driver)
        self.home = HomePage(self.driver)
        self.home.open()
        self.flow.handle_cookie_banner()

    def test_01_home_page_is_opened_and_loaded(self):
        # self.driver, self.home, self.flow hazır gelir
        assert self.home.is_on_correct_page()
```

`driver` fixture'ı `conftest.py`'deki `pytest_generate_tests` tarafından browser parametresiyle inject edilir — test class'ı hangi browser'da çalıştığını bilmez.

---

## Kural: `setup`'ta Ne Olur?

`setup` fixture'ına yalnızca **her testin ortak başlangıç noktası** girer:

| Setup'ta olur | Setup'ta olmaz |
|---------------|----------------|
| `driver` → `self.driver` atama | Test'e özgü navigasyon |
| Ana sayfayı açma (`home.open()`) | Assertion |
| Cookie banner kapatma | Sayfaya özgü filtre/tıklama |

---

## `setup` vs `setup_method`

Bu projede `@pytest.fixture(autouse=True)` kullanılır — pytest fixture zinciriyle (`driver` fixture'ından `self.driver`'a) entegrasyon sağlar.

`setup_method` pytest fixture'larına doğrudan erişemez, bu yüzden kullanılmaz.

---

## Test Metodu İsimlendirmesi

```
test_NN_ne_dogrulaniyor
```

```python
# test_home_page.py
def test_01_home_page_is_opened_and_loaded(self):   # smoke + regression

# test_insider_careers.py
def test_02_careers_page_is_opened_and_loaded(self): # regression
def test_03_qa_jobs_listed(self):                    # smoke + regression
def test_04_first_qa_job_details_are_correct(self):  # regression
```

Numara sırası test akışını gösterir — her test bir öncekinin bıraktığı yerden mantıksal olarak devam eder.

---

## Yeni Test Yazarken

1. `setup` fixture'a dokunma — ortak başlangıç noktası sabit kalır
2. Test metoduna sadece o adıma özel navigasyon ve assertion girer
3. Yeni sayfaya geçiliyorsa ilgili page object import edilir
4. Yeni locator gerekiyorsa önce `*_locators.py` dosyasına eklenir, sonra test yazılır
