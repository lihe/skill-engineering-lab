PYTHON ?= python3
SKILL ?= ai-video-creator-style
CASES ?= evals/cases.json
RUN ?= iteration-001
SAMPLE_OUTPUT ?= runs/$(RUN)/core-skill-eval-lab/with_skill_v2/output.md

.PHONY: eval report verify check all

all: eval verify check

eval:
	$(PYTHON) scripts/run_eval.py --skill $(SKILL) --cases $(CASES) --iteration $(RUN)

report:
	$(PYTHON) scripts/summarize_report.py runs/$(RUN)

verify:
	$(PYTHON) skills/ai-video-creator-style/scripts/validate_package.py $(SAMPLE_OUTPUT)

check:
	$(PYTHON) -c "import ast, pathlib; files=['scripts/run_eval.py','scripts/grade_output.py','scripts/summarize_report.py','skills/ai-video-creator-style/scripts/validate_package.py']; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'), filename=p) for p in files]; print('syntax ok')"
