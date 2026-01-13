.PHONY: help install upscayl-single upscayl-batch example clean

# Default target
help:
	@echo "Upscayl Image Upscaler - Available commands:"
	@echo ""
	@echo "  install          - Install Upscayl and dependencies"
	@echo "  upscayl-single   - Upscale a single image"
	@echo "  upscayl-batch    - Upscale images in batch mode"
	@echo "  example          - Run example upscaling operation"
	@echo "  clean            - Remove example files"
	@echo ""
	@echo "Usage examples:"
	@echo "  make install"
	@echo "  make upscayl-single INPUT=image.png OUTPUT=upscaled.png SCALE=2"
	@echo "  make upscayl-batch INPUT_DIR=images OUTPUT_DIR=upscaled SCALE=3"
	@echo "  make example"

# Install Upscayl
install:
	chmod +x setup.sh
	./setup.sh

# Upscale single image
upscayl-single:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ] || [ -z "$(SCALE)" ]; then \
		echo "Usage: make upscayl-single INPUT=input_file OUTPUT=output_file SCALE=scale_factor"; \
		exit 1; \
	fi
	python upscaler.py -i "$(INPUT)" -o "$(OUTPUT)" -s "$(SCALE)"

# Upscale batch of images
upscayl-batch:
	@if [ -z "$(INPUT_DIR)" ] || [ -z "$(OUTPUT_DIR)" ] || [ -z "$(SCALE)" ]; then \
		echo "Usage: make upscayl-batch INPUT_DIR=input_dir OUTPUT_DIR=output_dir SCALE=scale_factor"; \
		exit 1; \
	fi
	python upscaler.py -d "$(INPUT_DIR)" -o "$(OUTPUT_DIR)" -s "$(SCALE)"

# Run example
example:
	python example_usage.py

# Clean example files
clean:
	rm -f example_input.png example_output.png
	@echo "Example files removed."

# Install Python dependencies
deps:
	pip install -r requirements.txt