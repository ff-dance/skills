SHELL := /bin/zsh

MODEL ?= gpt-5.4
RUN_NAME ?= make-$(shell date +%Y%m%d_%H%M%S)

.PHONY: skillopt-help skillopt-env skillopt-install skillopt-smoke skillopt-verify skillopt-upgrade skillopt-train

skillopt-help:
	@echo "skillopt-env      Copy .env.skillopt.local.example to .env.skillopt.local if missing"
	@echo "skillopt-install  Install repo overlay into the local SkillOpt checkout"
	@echo "skillopt-smoke    Sync + precheck + verify, no training, 1 repeat"
	@echo "skillopt-verify   Sync + precheck + verify, no training, 3 repeats"
	@echo "skillopt-upgrade  Stable full cycle with training and 3-repeat gates"
	@echo "skillopt-train    Alias of skillopt-upgrade"

skillopt-env:
	@if [[ -f .env.skillopt.local ]]; then \
		echo ".env.skillopt.local already exists"; \
	else \
		cp .env.skillopt.local.example .env.skillopt.local; \
		echo "Created .env.skillopt.local"; \
	fi

skillopt-install:
	@./scripts/install_skillopt_overlay.sh

skillopt-smoke:
	@RUN_NAME="$(RUN_NAME)-smoke" \
	MODEL="$(MODEL)" \
	RUN_TRAIN=0 \
	PROMOTE_TO_REPO=1 \
	PRECHECK_REPEATS=1 \
	VERIFY_REPEATS=1 \
	SELECTION_REPEATS=1 \
	TEST_REPEATS=1 \
	./scripts/run_skillopt_upgrade_cycle.sh

skillopt-verify:
	@RUN_NAME="$(RUN_NAME)-verify" \
	MODEL="$(MODEL)" \
	RUN_TRAIN=0 \
	PROMOTE_TO_REPO=1 \
	PRECHECK_REPEATS=3 \
	VERIFY_REPEATS=3 \
	SELECTION_REPEATS=3 \
	TEST_REPEATS=1 \
	./scripts/run_skillopt_upgrade_cycle.sh

skillopt-upgrade:
	@RUN_NAME="$(RUN_NAME)-upgrade" \
	MODEL="$(MODEL)" \
	RUN_TRAIN=1 \
	PROMOTE_TO_REPO=1 \
	PRECHECK_REPEATS=3 \
	VERIFY_REPEATS=3 \
	SELECTION_REPEATS=3 \
	TEST_REPEATS=1 \
	TRAIN_NUM_EPOCHS=1 \
	FAILURE_ONLY=true \
	./scripts/run_skillopt_upgrade_cycle.sh

skillopt-train: skillopt-upgrade
