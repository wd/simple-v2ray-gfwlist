.PHONY: test
test:
	env PYTHONPATH=./src pytest

update:
	cd src && ./svgfw.py update_list --debug
package:
	echo "package"
