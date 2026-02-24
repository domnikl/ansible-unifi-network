
SHELL := bash
.PHONY: install

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt -r requirements-dev.txt

lint: venv
	venv/bin/pylint plugins

install:
	mkdir -p ~/ansible/collections/ansible_collections/domnikl/unifi_network
	cp -r * ~/ansible/collections/ansible_collections/domnikl/unifi_network

lint-docs: venv
	venv/bin/antsibull-docs lint-collection-docs \
		--plugin-docs \
		--validate-collection-refs self \
		--check-extra-docs-refs \
		.

clean:
	git clean -xdf

sanity:
	ansible-test sanity --color --truncate 0 -v \
		--docker default \
		--allow-disabled

units:
	ansible-test units --color --truncate 0 -v \
		--docker default

integration:
	ansible-test integration --color --truncate 0 -v \
		--docker default \
		--allow-disabled