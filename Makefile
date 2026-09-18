.PHONY: help install lint test format clean

help:
	@echo "AstroGit-OS - Comandos de desarrollo"
	@echo "  make install    Instala dependencias de desarrollo"
	@echo "  make lint       Ejecuta el linter (ruff)"
	@echo "  make format     Formatea el código con ruff"
	@echo "  make test       Ejecuta la suite de pruebas (pytest)"
	@echo "  make clean      Limpia residuos de compilación y caché"

install:
	pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format .

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache src/*.egg-info