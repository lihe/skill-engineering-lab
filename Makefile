PYTHON ?= python3
SKILL ?= ai-video-creator-style
CASES ?= evals/cases.json
RUN ?= iteration-001
SAMPLE_OUTPUT ?= runs/$(RUN)/core-skill-eval-lab/with_skill_v2/output.md

.PHONY: eval report dashboard-data verify check site-check all

all: eval dashboard-data verify check site-check

eval:
	$(PYTHON) scripts/run_eval.py --skill $(SKILL) --cases $(CASES) --iteration $(RUN)

report:
	$(PYTHON) scripts/summarize_report.py runs/$(RUN)

dashboard-data:
	$(PYTHON) scripts/build_dashboard_data.py --run-dir runs/$(RUN) --output dashboard/data.js

verify:
	$(PYTHON) skills/ai-video-creator-style/scripts/validate_package.py $(SAMPLE_OUTPUT)

check:
	$(PYTHON) -c "import ast, pathlib; files=['scripts/run_eval.py','scripts/grade_output.py','scripts/summarize_report.py','scripts/build_dashboard_data.py','skills/ai-video-creator-style/scripts/validate_package.py']; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'), filename=p) for p in files]; print('syntax ok')"

site-check:
	node --check dashboard/app.js
	node --check dashboard/data.js
	node --check site/app.js
	$(PYTHON) -c "from pathlib import Path; required=['dashboard/index.html','dashboard/style.css','dashboard/app.js','dashboard/data.js','site/index.html','site/styles.css','site/app.js','docs/ai-agent-skill-engineering.html']; missing=[p for p in required if not Path(p).exists()]; assert not missing, missing; print('static site assets ok')"
