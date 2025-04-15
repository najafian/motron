# 🚀 Motron Framework – Publish & Usage Guide

Motron is a Spring Boot–inspired Python framework that brings component scanning, annotation-based injection, scheduling, REST routing, configuration binding, and more — all with a simple developer experience.

---

## 🧱 Project Structure (Motron)



```markdown
motron/
├── pyproject.toml
├── setup.py
├── requirements.txt
└── src/main/motron/...
```

---

## 🔖 1. Publish a New Version

1. Update the version in `pyproject.toml` and `setup.py` (e.g., `v0.1.4`)
2. Push the new version tag:

```bash
git add .
git commit -m "release: v0.1.4"
git push
git tag -d v0.0.1
git push --delete origin v0.0.1
git tag v0.0.1
git push origin v0.0.1
```

---

## 📦 2. Install Motron in Any Project

### Option A: Add to `requirements.txt`

```
git+ssh://git@gitlab.dev.motrada.net:5922/researching/motron.git@v0.1.4#egg=motron
```

### Option B: Install directly with pip

```bash
pip install --upgrade \
  git+ssh://git@gitlab.dev.motrada.net:5922/researching/motron.git@v0.1.4#egg=motron
```

---

## 🗂 Sample Project Structure

```
sampleProject/
├── requirements.txt
├── src/main/resources/
│   ├── application.yml
│   └── key/public_key.pem
└── src/main/example/
```

---

## ♻️ 3. Clean Virtual Environment (if needed)

If you have conflicting or outdated packages inside `.venv`:

### ✅ Option 1: Recreate `.venv` (Recommended)

```bash
rm -rf .venv                # Remove old virtual environment
python -m venv .venv        # Create a new one
source .venv/bin/activate   # Activate it (Linux/macOS)
# OR
.venv\Scripts\activate      # Activate it (Windows)
```

### ✅ Option 2: Uninstall All Packages Manually

```bash
source .venv/bin/activate
pip freeze | xargs pip uninstall -y
```

---

## 📥 4. Install Dependencies

Once `.venv` is clean or recreated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ 5. Sample `application.yml`

```yaml
motron:
  title: Motron Rules!
  debug: true
  port: 9000

  logging:
    level:
      python.presentation.reset.controllers.FooRestController: INFO
      example.service.MyService: DEBUG

  security:
    oauth2:
      resourceserver:
        jwt:
          public-key-location: classpath:key/public_key.pem
```
