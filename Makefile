.PHONY: build-docker
build-docker:
	rm -rf ./appimage-build
	docker build -t facial-detection . -f ./Dockerfile.txt

.PHONY: run-docker
run-docker:
	docker run --rm -it -v "${PWD}":/module -w /module facial-detection "/bin/bash"

.PHONY: appimage
appimage: 
	/usr/local/bin/appimage-builder --recipe ./etc/appimage-`uname -m`.yml

.PHONY: appimage-docker
appimage-docker: build-docker
	docker run --rm -it -v "${PWD}":/module -w /module facial-detection "/bin/bash" "-c" "make appimage"

