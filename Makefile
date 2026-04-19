.PHONY: help ui ui-chrome ui-firefox ui-all \
        ui-chrome-headless ui-firefox-headless ui-all-headless \
        ui-parallel ui-all-parallel \
        test-all report report-open clean

ALLURE_DIR := automation-test-results/allure-results
REPORT_DIR := automation-test-results/allure-report

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
	@echo "  All Tests"
	@echo "    make test-all       → UI (Chrome) full suite"
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

# ── All ───────────────────────────────────────────────────────────────────────
test-all:
	pytest ui_tests/tests/ --browser=chrome

# ── Reports ───────────────────────────────────────────────────────────────────
report:
	allure generate $(ALLURE_DIR) --clean -o $(REPORT_DIR)

report-open:
	allure serve $(ALLURE_DIR)

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf automation-test-results/
