.PHONY: test

Release_tag := 0.1
Package_name := 'svgfw-$(Release_tag).zip'

test:
	env PYTHONPATH=./src pytest

update:
	cd src && ./svgfw.py update_list --debug

package:
	$(eval TMP := $(shell mktemp -d))
	git clone https://github.com/wd/simple-v2ray-gfwlist $(TMP)
	cd $(TMP) && git checkout tags/$(Release_tag) && mkdir package
	cd $(TMP) && cp -r src/{config_sample.ini,svgfw,lists} package
	cd $(TMP)/package && zip -r $(Package_name) config_sample.ini svgfw lists
	cp $(TMP)/package/$(Package_name) ./
	md5 $(Package_name) > $(Package_name).md5
	rm -rf $(TMP)
