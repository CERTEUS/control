SHELL := /usr/bin/env bash

.PHONY: setup token token-json login list clone secret-pack secret-write help

help:
	@echo "Dostępne cele: setup, token, token-json, login, list, clone owner=<o> repo=<r>, secret-pack, secret-write"

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
