.PHONY: help ui ui-chrome ui-firefox ui-all \
        ui-chrome-headless ui-firefox-headless ui-all-headless \
        ui-parallel ui-all-parallel \
        load-test load-test-smoke load-test-scale \
        test-all report report-open clean

ALLURE_DIR  := automation-test-results/allure-results
REPORT_DIR  := automation-test-results/allure-report
LOCUST_DIR  := automation-test-results/locust

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
	pytest ui_tests/tests/ --browser=chrome

ui-firefox:
	pytest ui_tests/tests/ --browser=firefox

ui-all:
	pytest ui_tests/tests/

ui-chrome-headless:
	pytest ui_tests/tests/ --browser=chrome --headless=true

ui-firefox-headless:
	pytest ui_tests/tests/ --browser=firefox --headless=true

ui-all-headless:
	pytest ui_tests/tests/ --headless=true

ui-parallel:
	pytest ui_tests/tests/ --browser=chrome -n auto

ui-all-parallel:
	pytest ui_tests/tests/ -n auto

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
report:
	allure generate $(ALLURE_DIR) --clean -o $(REPORT_DIR)

report-open:
	allure serve $(ALLURE_DIR)

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf automation-test-results/
