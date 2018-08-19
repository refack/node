# Default to verbose builds.
# To do quiet/pretty builds, run `make V=` to set V to an empty string,
# or set the V environment variable to an empty string.
V ?= 1

.PHONY: help
# To add a target to the help, add a double comment (##) on the target line.
help: ## Print help for targets with comments.
	@printf "For more targets and info see the comments in the Makefile.\n\n"
	@grep -E '^[a-zA-Z0-9._-]+:.*?## .*$$' Makefile | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

NODE ?= ./node
NPM ?= ./deps/npm/bin/npm-cli.js

# Google Analytics ID used for tracking API docs page views, empty
# DOCS_ANALYTICS means no tracking scripts will be included in the
# generated .html files
DOCS_ANALYTICS ?=

run-npm-ci = $(abspath $(NODE) $(NPM)) ci

test/addons/.docbuildstamp: \
	tools/doc/addon-verify.js \
	doc/api/addons.md         \
	tools/doc/node_modules
	$(RM) -r test/addons/??_*/
	$(NODE) $<
	touch $@

ADDONS_BINDING_GYPS := \
	$(filter-out test/addons/??_*/binding.gyp, \
		$(wildcard test/addons/*/binding.gyp))

ADDONS_BINDING_SOURCES := \
	$(filter-out test/addons/??_*/*.cc, $(wildcard test/addons/*/*.cc)) \
	$(filter-out test/addons/??_*/*.h, $(wildcard test/addons/*/*.h))

ADDONS_PREREQS :=            \
	config.gypi                \
	deps/npm/node_modules/node-gyp/package.json \
	tools/build-addons.js      \
	deps/uv/include/*.h        \
	deps/v8/include/*.h        \
	src/node.h                 \
	src/node_buffer.h          \
	src/node_object_wrap.h     \
	src/node_version.h

# function used to build native addons
define run_build_addons
	env \
			npm_config_loglevel=$(LOGLEVEL)   \
			npm_config_nodedir="$$PWD"        \
			npm_config_python="$(PYTHON)"     \
		$(NODE) \
			tools/build-addons \
			deps/npm/node_modules/node-gyp/bin/node-gyp.js \
			$1
endef

ADDONS_BUILD_PREQS :=            \
 	$(ADDONS_PREREQS)            \
	$(ADDONS_BINDING_GYPS)       \
	$(ADDONS_BINDING_SOURCES)    \
	test/addons/.docbuildstamp
test/addons/.buildstamp: $(ADDONS_BUILD_PREQS)
	$(call run_build_addons, test/addons)
	touch $@


ADDONS_NAPI_BINDING_GYPS := \
	$(filter-out test/addons-napi/??_*/binding.gyp, \
		$(wildcard test/addons-napi/*/binding.gyp))

ADDONS_NAPI_BINDING_SOURCES := \
	$(filter-out test/addons-napi/??_*/*.c, $(wildcard test/addons-napi/*/*.c)) \
	$(filter-out test/addons-napi/??_*/*.cc, $(wildcard test/addons-napi/*/*.cc)) \
	$(filter-out test/addons-napi/??_*/*.h, $(wildcard test/addons-napi/*/*.h))

BUILD_NAPI_ADDONS_PREREQS :=          \
	$(ADDONS_PREREQS)                 \
	$(ADDONS_NAPI_BINDING_GYPS)       \
	$(ADDONS_NAPI_BINDING_SOURCES)    \
	src/node_api.h                    \
	src/node_api_types.h
test/addons-napi/.buildstamp: $(BUILD_NAPI_ADDONS_PREREQS)
	$(call run_build_addons, test/addons-napi)
	touch $@


apidoc_dirs = out/doc out/doc/api out/doc/api/assets
apidoc_sources = $(wildcard doc/api/*.md)
apidocs_html = $(addprefix out/,$(apidoc_sources:.md=.html))
apidocs_json = $(addprefix out/,$(apidoc_sources:.md=.json))

apiassets = $(subst api_assets,api/assets,$(addprefix out/,$(wildcard doc/api_assets/*)))

out/doc:
	mkdir -p $@

# If it's a source tarball, doc/api already contains the generated docs.
# Just copy everything under doc/api over.
out/doc/api: doc/api
	mkdir -p $@
	cp -r doc/api out/doc

# If it's a source tarball, assets are already in doc/api/assets
out/doc/api/assets:
	mkdir -p $@
	if [ -d doc/api/assets ]; then cp -r doc/api/assets out/doc/api; fi;

# If it's not a source tarball, we need to copy assets from doc/api_assets
out/doc/api/assets/%: doc/api_assets/% out/doc/api/assets
	@cp $< $@

out/doc/api/%.json out/doc/api/%.html: \
	doc/api/%.md                       \
	tools/doc/generate.js              \
	tools/doc/html.js                  \
	tools/doc/json.js                  \
	out/doc/api
	$(NODE) tools/doc/generate.js   \
	--node-version=$(FULLVERSION)   \
	--analytics=$(DOCS_ANALYTICS)   \
	--output-directory=$>           \
	$<

out/doc/api/all.html: tools/doc/allhtml.js $(apidocs_html)
	$(NODE) $<

out/doc/api/all.json: tools/doc/alljson.js $(apidocs_json)
	$(NODE) $<


tools/remark-cli/node_modules: tools/remark-cli/package.json
	@echo "Markdown linter: installing remark-cli into tools/"
	cd tools/remark-cli && $(run-npm-ci)

tools/remark-preset-lint-node/node_modules: \
	tools/remark-preset-lint-node/package.json
	@echo "Markdown linter: installing remark-preset-lint-node into tools/"
	cd tools/remark-preset-lint-node && $(run-npm-ci)

tools/doc/node_modules: tools/doc/package.json
	cd tools/doc && $(run-npm-ci)

LINT_MD_DOC_FILES = $(shell ls doc/*.md doc/**/*.md)
# Lint all changed markdown files under doc/
tools/.doc_mdlint_stamp: $(LINT_MD_DOC_FILES)
	$(NODE) tools/remark-cli/cli.js -q -f $?
	touch $@

LINT_MD_DIRS = src lib benchmark test tools/doc tools/icu
LINT_MD_MISC_FILES := $(shell \
		find $(LINT_MD_DIRS) -type f -not -path '*node_modules*' -name '*.md' \
	) \
	$(wildcard *.md)
# Lint other changed markdown files maintained by us
tools/.misc_mdlint_stamp: $(LINT_MD_MISC_FILES)
	$(NODE) tools/remark-cli/cli.js -q -f $?
	touch $@

tools/.mdlint_stamp: tools/.misc_mdlint_stamp tools/.doc_mdlint_stamp
	touch $@

tools/clang-format/node_modules: tools/clang-format/package.json
	cd tools/clang-format && $(run-npm-ci)