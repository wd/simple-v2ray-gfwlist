.PHONY: test

Release_tag := $(shell grep '__VERSION__ =' src/svgfw | awk -F"'" '{print $$2}')
Package_name := 'svgfw-$(Release_tag).zip'

test:
	pytest -v

update:
	./src/svgfw.py update_list -d

package:
	$(info Make pakcage for $(Release_tag))
	$(eval TMP := $(shell mktemp -d))
	git clone https://github.com/wd/simple-v2ray-gfwlist $(TMP)
	cd $(TMP) && git checkout tags/$(Release_tag) && mkdir package
	cd $(TMP) && cp -r src/{config_sample.ini,svgfw,lists} package
	cd $(TMP)/package && zip -r $(Package_name) config_sample.ini svgfw lists
	cp $(TMP)/package/$(Package_name) ./
	md5 $(Package_name) > $(Package_name).md5
	rm -rf $(TMP)
