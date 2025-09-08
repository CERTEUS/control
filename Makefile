SHELL := /usr/bin/env bash

.PHONY: setup token token-json login list clone secret-pack secret-write lint agent-install agent-once agent-loop agent-stop help \
	codex-build codex-start codex-stop codex-shell codex-status codex-exec

help:
	@echo "Dostępne cele: setup, token, token-json, login, list, clone owner=<o> repo=<r>, secret-pack, secret-write"
	@echo "               lint, agent-install issue=<nr> [dry=0|1], agent-once, agent-loop, agent-stop"
	@echo "               codex-build, codex-start, codex-stop, codex-shell, codex-status, codex-exec cmd=\"...\""

setup:
	@tools/remote-bot/setup.sh

token:
	@tools/remote-bot/gh_app_token.sh

token-json:
	@tools/remote-bot/gh_app_token.sh --json | sed 's/.*/&/'

login:
	@tools/remote-bot/with-gh.sh gh auth status || true

list:
	@tools/remote-bot/list-repos.sh


clone:
	@if [ -z "$$owner" ] || [ -z "$$repo" ]; then \
		echo "Użycie: make clone owner=<owner> repo=<repo> [dir=<katalog>]"; exit 2; \
	fi; \
	tools/remote-bot/clone-repo.sh $$owner/$$repo $$dir

secret-pack:
	@tools/remote-bot/pack-secret.sh

secret-write:
	@tools/remote-bot/pack-secret.sh --write

lint:
	@bash tools/verify-markdown.sh && echo "Markdown OK"
	@which shellcheck >/dev/null 2>&1 && shellcheck -S style tools/*.sh tools/remote-bot/*.sh tools/remote-agent/*.sh || echo "(pomijam shellcheck)"
	@which cspell >/dev/null 2>&1 && cspell --no-progress "**/*.md" || echo "(pomijam cspell)"

agent-install:
	@[ -n "$(issue)" ] || (echo "Użycie: make agent-install issue=<NR> [dry=0|1]"; exit 2)
	@tools/remote-agent/install.sh --issue $(issue) $(if $(dry),$(if $(filter 0,$(dry)),--no-dry-run,))

agent-once:
	@tools/remote-agent/agent.sh --once

agent-loop:
	@tools/remote-agent/agent.sh --loop

agent-stop:
	@systemctl --user stop certeus-remote-agent.service || true

# ========================
# Codex dev container
# ========================

CONTROL_VOL ?= /f/projekty/control
CODEX_HOME_VOL ?= /f/projekty/codex_home
IMAGE ?= codex-ubuntu
CONTAINER ?= codex

codex-build:
	@docker build -t $(IMAGE) -f devops/Dockerfile.codex .

codex-start: codex-build
	@docker stop $(CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(CONTAINER) >/dev/null 2>&1 || true
	@docker run -d --name $(CONTAINER) -p 1455:1455 \
		-v $(CONTROL_VOL):/workspace/control \
		-v $(CODEX_HOME_VOL):/root/.codex \
		$(IMAGE) bash -lc "sleep infinity"
	@docker exec $(CONTAINER) git config --global --add safe.directory /workspace/control || true
	@docker exec $(CONTAINER) git config --global --add safe.directory /workspace/control/certeus || true
	@docker exec $(CONTAINER) codex login status || true

codex-stop:
	@docker stop $(CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(CONTAINER) >/dev/null 2>&1 || true

codex-shell:
	@docker exec -it $(CONTAINER) bash

codex-status:
	@docker exec $(CONTAINER) codex login status

codex-exec:
	@[ -n "$(cmd)" ] || (echo "Użycie: make codex-exec cmd=\"cd /workspace/control && codex /status\""; exit 2)
	@docker exec $(CONTAINER) bash -lc "$(cmd)"
