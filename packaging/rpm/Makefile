PACKAGE_NAME?=	redborder-webui-node-modules

#VERSION?=	$(shell git describe --tags --long | sed 's/-/_/g')
VERSION?=	$(shell git describe --abbrev=6 --tags HEAD --always | sed 's/-/_/g')

BUILD_NUMBER?= 1

MOCK_CONFIG?=default

RESULT_DIR?=pkgs

PUPPETEER_VERSION?= 19.5.2

CHROMIUM_VERSION?= 1069273

all: rpm

SOURCES:
	mkdir -p SOURCES

archive: SOURCES
	cd ../../ && \
	git archive --prefix=$(PACKAGE_NAME)-$(VERSION)/ \
		-o packaging/rpm/SOURCES/$(PACKAGE_NAME)-$(VERSION).tar.gz HEAD

build_prepare: archive
	mkdir -p $(RESULT_DIR)
	rm -f $(RESULT_DIR)/$(PACKAGE_NAME)*.rpm

srpm: build_prepare
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)" \
		--define "__release $(BUILD_NUMBER)" \
		--define "__puppeteer_version $(PUPPETEER_VERSION)" \
		--define "__chromium_version $(CHROMIUM_VERSION)" \
		--resultdir=$(RESULT_DIR) \
		--buildsrpm \
		--spec=${PACKAGE_NAME}.spec \
		--sources=SOURCES
	@echo "======= Source RPM now available in $(RESULT_DIR) ======="

rpm: srpm
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)"\
		--define "__release $(BUILD_NUMBER)"\
		--define "__puppeteer_version $(PUPPETEER_VERSION)" \
		--define "__chromium_version $(CHROMIUM_VERSION)" \
		--resultdir=$(RESULT_DIR) \
		--rebuild $(RESULT_DIR)/$(PACKAGE_NAME)*.src.rpm
	@echo "======= Binary RPMs now available in $(RESULT_DIR) ======="

clean:
	rm -rf SOURCES pkgs

distclean: clean
	rm -f build.log root.log state.log available_pkgs installed_pkgs \
		*.rpm *.tar.gz
