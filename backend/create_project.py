from pathlib import Path

PROJECT_FOLDERS = [
    "app",
    "app/api",
    "app/core",
    "app/config",
    "app/models",
    "app/repositories",
    "app/schemas",
    "app/services",
    "app/utils",
    "tests",
]

PROJECT_FILES = {
    "app/__init__.py": "",
    "app/api/__init__.py": "",
    "app/core/__init__.py": "",
    "app/config/__init__.py": "",
    "app/models/__init__.py": "",
    "app/repositories/__init__.py": "",
    "app/schemas/__init__.py": "",
    "app/services/__init__.py": "",
    "app/utils/__init__.py": "",
    "tests/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI

app = FastAPI(
    title="FinInsight AI",
    description="Enterprise Financial Document Intelligence Platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to FinInsight AI"}


@app.get("/health")
def health():
    return {"status": "UP"}
""",
    ".env": """AWS_PROFILE=rag-project
AWS_REGION=us-east-1
""",
    ".gitignore": """.venv/
__pycache__/
*.pyc
.env
.vscode/
.idea/
""",
}


def create_project() -> None:
    base_path = Path(__file__).parent

    for folder in PROJECT_FOLDERS:
        (base_path / folder).mkdir(parents=True, exist_ok=True)

    for file_name, content in PROJECT_FILES.items():
        file_path = base_path / file_name

        if file_path.exists():
            print(f"Skipped existing file: {file_name}")
            continue

        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_name}")

    print("\nFinInsight AI backend structure created successfully.")


if __name__ == "__main__":
    create_project()
