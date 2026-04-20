.PHONY: help \
        ui-chrome ui-firefox ui-all ui-all-headless ui-fast \
        api-test api-smoke \
        load-test load-test-smoke load-test-scale \
        run-all \
        open-reports stop-reports report-ui report-api \
        clean

ALLURE_UI_DIR  := automation-test-results/ui/allure-results
ALLURE_API_DIR := automation-test-results/api/allure-results
REPORT_DIR     := automation-test-results/allure-report
LOCUST_DIR     := automation-test-results/locust
LOG_DIR        := automation-test-results/logs

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  UI Tests"
	@echo "    make ui-chrome        → Chrome (görünür, debug)"
	@echo "    make ui-firefox       → Firefox (görünür, debug)"
	@echo "    make ui-all           → Chrome + Firefox (görünür, tam kapsam)"
	@echo "    make ui-all-headless  → Chrome + Firefox (headless, CI standard)"
	@echo "    make ui-fast          → Chrome + Firefox (headless + paralel, CI turbo)"
	@echo ""
	@echo "  API Tests"
	@echo "    make api-test         → Tüm API testleri"
	@echo "    make api-smoke        → Sadece smoke"
	@echo ""
	@echo "  Load Tests"
	@echo "    make load-test        → 1 user, 60s (assessment default)"
	@echo "    make load-test-smoke  → Smoke task'ları"
	@echo "    make load-test-scale  → 10 user, 120s"
	@echo ""
	@echo "  Full Suite"
	@echo "    make run-all          → UI + API + Load (paralel, headless)"
	@echo ""
	@echo "  Reports"
	@echo "    make open-reports     → UI:4040 + API:4041 Allure + Locust HTML"
	@echo "    make stop-reports     → Allure server'ları durdur"
	@echo "    make report-ui        → UI Allure HTML oluştur (CI artifact)"
	@echo "    make report-api       → API Allure HTML oluştur (CI artifact)"
	@echo ""
	@echo "  Cleanup"
	@echo "    make clean            → Tüm test sonuçlarını sil"
	@echo ""

# ── UI ────────────────────────────────────────────────────────────────────────
ui-chrome:
	pytest ui_tests/tests/ --browser=chrome --alluredir=$(ALLURE_UI_DIR)

ui-firefox:
	pytest ui_tests/tests/ --browser=firefox --alluredir=$(ALLURE_UI_DIR)

ui-all:
	pytest ui_tests/tests/ --alluredir=$(ALLURE_UI_DIR)

ui-all-headless:
	pytest ui_tests/tests/ --headless=true --alluredir=$(ALLURE_UI_DIR)

ui-fast:
	pytest ui_tests/tests/ --headless=true -n auto --alluredir=$(ALLURE_UI_DIR)

# ── API ───────────────────────────────────────────────────────────────────────
api-test:
	pytest api_tests/tests/ --alluredir=$(ALLURE_API_DIR)

api-smoke:
	pytest api_tests/tests/ -m smoke --alluredir=$(ALLURE_API_DIR)

# ── Load ──────────────────────────────────────────────────────────────────────
load-test:
	@mkdir -p $(LOCUST_DIR)
	locust --headless --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

load-test-smoke:
	@mkdir -p $(LOCUST_DIR)
	locust --headless --tags smoke --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

load-test-scale:
	@mkdir -p $(LOCUST_DIR)
	locust --headless -u 10 -r 2 --run-time 120s --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

# ── Run All (paralel) ─────────────────────────────────────────────────────────
run-all:
	@mkdir -p $(ALLURE_UI_DIR) $(ALLURE_API_DIR) $(LOCUST_DIR) $(LOG_DIR)
	@echo ""
	@echo "UI + API + Load testleri paralel başlatılıyor..."
	@echo ""
	@( pytest ui_tests/tests/ --headless=true --alluredir=$(ALLURE_UI_DIR) \
	     --tb=short -q > $(LOG_DIR)/ui.log 2>&1; echo $$? > $(LOG_DIR)/ui.exit ) & \
	 ( pytest api_tests/tests/ --alluredir=$(ALLURE_API_DIR) \
	     --tb=short -q > $(LOG_DIR)/api.log 2>&1; echo $$? > $(LOG_DIR)/api.exit ) & \
	 ( locust --headless \
	     --html $(LOCUST_DIR)/locust_report.html \
	     --csv  $(LOCUST_DIR)/locust \
	     > $(LOG_DIR)/load.log 2>&1; echo $$? > $(LOG_DIR)/load.exit ) & \
	 wait
	@echo ""
	@echo "────────────── Sonuçlar ──────────────"
	@[ "$$(cat $(LOG_DIR)/ui.exit)"   = "0" ] && echo "✓ UI Testleri   — PASS" \
	  || { echo "✗ UI Testleri   — FAIL"; echo ""; tail -20 $(LOG_DIR)/ui.log; }
	@[ "$$(cat $(LOG_DIR)/api.exit)"  = "0" ] && echo "✓ API Testleri  — PASS" \
	  || { echo "✗ API Testleri  — FAIL"; echo ""; tail -20 $(LOG_DIR)/api.log; }
	@[ "$$(cat $(LOG_DIR)/load.exit)" = "0" ] && echo "✓ Load Testi    — PASS" \
	  || { echo "✗ Load Testi    — FAIL"; echo ""; tail -10 $(LOG_DIR)/load.log; }
	@echo "──────────────────────────────────────"
	@echo ""
	@echo "Raporlar için: make open-reports"
	@echo ""
	@exit $$(( $$(cat $(LOG_DIR)/ui.exit) | $$(cat $(LOG_DIR)/api.exit) | $$(cat $(LOG_DIR)/load.exit) ))

# ── Reports ───────────────────────────────────────────────────────────────────
open-reports:
	@lsof -ti tcp:4040 | xargs kill -9 2>/dev/null || true
	@lsof -ti tcp:4041 | xargs kill -9 2>/dev/null || true
	@allure serve $(ALLURE_UI_DIR)  --port 4040 > /dev/null 2>&1 &
	@allure serve $(ALLURE_API_DIR) --port 4041 > /dev/null 2>&1 &
	@sleep 2
	@open $(LOCUST_DIR)/locust_report.html 2>/dev/null || true
	@echo ""
	@echo "  UI  Allure → http://localhost:4040"
	@echo "  API Allure → http://localhost:4041"
	@echo "  Load       → $(LOCUST_DIR)/locust_report.html"
	@echo ""
	@echo "  Durdurmak için: make stop-reports"
	@echo ""

stop-reports:
	@lsof -ti tcp:4040 | xargs kill -9 2>/dev/null && echo "✓ Port 4040 kapatıldı" || echo "  Port 4040 zaten kapalı"
	@lsof -ti tcp:4041 | xargs kill -9 2>/dev/null && echo "✓ Port 4041 kapatıldı" || echo "  Port 4041 zaten kapalı"

report-ui:
	allure generate $(ALLURE_UI_DIR) --clean -o $(REPORT_DIR)/ui

report-api:
	allure generate $(ALLURE_API_DIR) --clean -o $(REPORT_DIR)/api

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf automation-test-results/
