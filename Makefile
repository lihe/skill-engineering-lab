PYTHON ?= python3
SKILL ?= ai-video-creator-style
CASES ?= evals/cases.json
RUN ?= iteration-001
PROVIDER ?= mock
MODEL ?=
SAMPLE_OUTPUT ?= runs/$(RUN)/core-skill-eval-lab/with_skill_v2/output.md

.PHONY: eval report dashboard-data skill-diff verify check site-check all

all: eval dashboard-data skill-diff verify check site-check

eval:
	$(PYTHON) scripts/run_eval.py --skill $(SKILL) --cases $(CASES) --iteration $(RUN) --provider $(PROVIDER) $(if $(MODEL),--model $(MODEL),)

report:
	$(PYTHON) scripts/summarize_report.py runs/$(RUN)

dashboard-data:
	$(PYTHON) scripts/build_dashboard_data.py --run-dir runs/$(RUN) --output dashboard/data.js

skill-diff:
	$(PYTHON) scripts/build_skill_diff.py --skill $(SKILL) --output dashboard/skill_diff.js

verify:
	$(PYTHON) skills/ai-video-creator-style/scripts/validate_package.py $(SAMPLE_OUTPUT)

check:
	$(PYTHON) -c "import ast, pathlib; files=['scripts/run_eval.py','scripts/grade_output.py','scripts/summarize_report.py','scripts/build_dashboard_data.py','scripts/build_skill_diff.py','providers/__init__.py','providers/base.py','providers/routing.py','providers/mock.py','providers/openai.py','providers/anthropic.py','skills/ai-video-creator-style/scripts/validate_package.py']; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'), filename=p) for p in files]; print('syntax ok')"

site-check:
	node --check dashboard/app.js
	node --check dashboard/data.js
	node --check dashboard/skill_diff.js
	node --check site/app.js
	$(PYTHON) -c "from pathlib import Path; import json; required=['index.html','vercel.json','dashboard/index.html','dashboard/style.css','dashboard/app.js','dashboard/data.js','dashboard/skill_diff.js','site/index.html','site/styles.css','site/app.js','docs/ai-agent-skill-engineering.html','docs/evaluation-report.html','skills/ai-video-creator-style/current/SKILL.md']; missing=[p for p in required if not Path(p).exists()]; assert not missing, missing; json.loads(Path('vercel.json').read_text(encoding='utf-8')); print('static site assets ok')"
