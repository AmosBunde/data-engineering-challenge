# Variables (customize paths as needed)
PYTHON      = python
PIP         = pip
PROJECT_DIR = .
TEST_DIR    = tests
REQUIREMENTS_FILE = requirements.txt
IMAGE_NAME  = data-pipeline-sftp
IMAGE_TAG   = latest
DOCKERFILE  = docker/Dockerfile

.PHONY: install lint test docker-build docker-run clean

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS_FILE)

lint:
	@echo "Running pylint..."
	pylint $(PROJECT_DIR)/data-processing-pipeline $(PROJECT_DIR)/main.py

test:
	@echo "Running pytest..."
	pytest --maxfail=1 --disable-warnings -v $(TEST_DIR)

docker-build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) .

docker-run:
	@echo "Running Docker container..."
	docker run -p 8000:8000 --env-file .env $(IMAGE_NAME):$(IMAGE_TAG)

clean:
	@echo "Cleaning up caches, __pycache__ folders..."
	find . -type d -name "__pycache__" -exec rm -rf {} +