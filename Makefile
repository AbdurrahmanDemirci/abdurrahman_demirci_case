.PHONY: help ui ui-chrome ui-firefox ui-all \
        ui-chrome-headless ui-firefox-headless ui-all-headless \
        ui-parallel ui-all-parallel \
        api-test api-smoke \
        load-test load-test-smoke load-test-scale \
        test-all report-ui report-api report-open-ui report-open-api clean

ALLURE_UI_DIR  := automation-test-results/ui/allure-results
ALLURE_API_DIR := automation-test-results/api/allure-results
REPORT_DIR     := automation-test-results/allure-report
LOCUST_DIR     := automation-test-results/locust

# ── default ───────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  UI Tests"
	@echo "    make ui                    → Chrome (default)"
	@echo "    make ui-chrome             → Chrome"
	@echo "    make ui-firefox            → Firefox"
	@echo "    make ui-all                → Chrome + Firefox (sequential)"
	@echo "    make ui-chrome-headless    → Chrome (headless)"
	@echo "    make ui-firefox-headless   → Firefox (headless)"
	@echo "    make ui-all-headless       → Chrome + Firefox headless (sequential)"
	@echo "    make ui-parallel           → Chrome — parallel workers"
	@echo "    make ui-all-parallel       → Chrome + Firefox — parallel workers"
	@echo ""
	@echo "  Load Tests"
	@echo "    make load-test             → 1 user, 60s — assessment default"
	@echo "    make load-test-smoke       → smoke-tagged tasks only"
	@echo "    make load-test-scale       → 10 users, 120s — scale test"
	@echo ""
	@echo "  All Tests"
	@echo "    make test-all       → UI (Chrome) + Load Tests"
	@echo ""
	@echo "  Reports"
	@echo "    make report         → Generate Allure HTML report"
	@echo "    make report-open    → Generate + open in browser"
	@echo ""
	@echo "  Cleanup"
	@echo "    make clean          → Delete test-result artefacts"
	@echo ""

# ── UI ────────────────────────────────────────────────────────────────────────
ui: ui-chrome

ui-chrome:
	pytest ui_tests/tests/ --browser=chrome --alluredir=$(ALLURE_UI_DIR)

ui-firefox:
	pytest ui_tests/tests/ --browser=firefox --alluredir=$(ALLURE_UI_DIR)

ui-all:
	pytest ui_tests/tests/ --alluredir=$(ALLURE_UI_DIR)

ui-chrome-headless:
	pytest ui_tests/tests/ --browser=chrome --headless=true --alluredir=$(ALLURE_UI_DIR)

ui-firefox-headless:
	pytest ui_tests/tests/ --browser=firefox --headless=true --alluredir=$(ALLURE_UI_DIR)

ui-all-headless:
	pytest ui_tests/tests/ --headless=true --alluredir=$(ALLURE_UI_DIR)

ui-parallel:
	pytest ui_tests/tests/ --browser=chrome -n auto --alluredir=$(ALLURE_UI_DIR)

ui-all-parallel:
	pytest ui_tests/tests/ -n auto --alluredir=$(ALLURE_UI_DIR)

# ── API ───────────────────────────────────────────────────────────────────────
api-test:
	pytest api_tests/tests/ --alluredir=$(ALLURE_API_DIR)

api-smoke:
	pytest api_tests/tests/ -m smoke --alluredir=$(ALLURE_API_DIR)

# ── Load ──────────────────────────────────────────────────────────────────────
load-test:
	mkdir -p $(LOCUST_DIR)
	locust --headless --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

load-test-smoke:
	mkdir -p $(LOCUST_DIR)
	locust --headless --tags smoke --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

load-test-scale:
	mkdir -p $(LOCUST_DIR)
	locust --headless -u 10 -r 2 --run-time 120s --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

# ── All ───────────────────────────────────────────────────────────────────────
test-all:
	pytest ui_tests/tests/ --browser=chrome
	mkdir -p $(LOCUST_DIR)
	locust --headless --html $(LOCUST_DIR)/locust_report.html --csv $(LOCUST_DIR)/locust

# ── Reports ───────────────────────────────────────────────────────────────────
report-ui:
	allure generate $(ALLURE_UI_DIR) --clean -o $(REPORT_DIR)/ui

report-api:
	allure generate $(ALLURE_API_DIR) --clean -o $(REPORT_DIR)/api

report-open-ui:
	allure serve $(ALLURE_UI_DIR)

report-open-api:
	allure serve $(ALLURE_API_DIR)

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf automation-test-results/
