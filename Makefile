.PHONY: build-image
build-image:
	$(eval VERSION := $(shell cat CANARY_VERSION))
	$(eval IMAGE_PREFIX := $(shell cat PRIVATE_IMAGE_PREFIX))
	$(eval NEW_VERSION := $(shell echo $(VERSION) | awk -F. '{print $$1"."$$2"."$$3+1}'))
	echo $(NEW_VERSION)
	docker build -t $(IMAGE_PREFIX)$(NEW_VERSION) --platform=linux/amd64 .
	@echo $(NEW_VERSION) > VERSION
	docker push $(IMAGE_PREFIX)$(NEW_VERSION)

.PHONY: fmt
fmt:
	black .
	isort .