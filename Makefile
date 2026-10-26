PROTO_DIR := proto
BUILD_DIR := build
PROTO_FILES := $(shell find $(PROTO_DIR) -name '*.proto')

.PHONY: validate-dictionary proto clean

validate-dictionary:
	python scripts/validate_dictionary.py

proto:
	mkdir -p $(BUILD_DIR)
	protoc -I=$(PROTO_DIR) -I=/usr/include \
	  --include_imports \
	  --descriptor_set_out=$(BUILD_DIR)/contracts.pb \
	  $(PROTO_FILES)

clean:
	rm -rf $(BUILD_DIR)
