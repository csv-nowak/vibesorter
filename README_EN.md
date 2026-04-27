> 🇬🇧 English (this file) · 🇩🇪 [Deutsch](README.md)

# 🗂 VibeSorter

**Local AI file sorting — 100% GDPR-compliant.**

An AI analyses your filenames and sorts them into the right folder structure.
No cloud uploads. No API keys. No data-protection headaches.
Everything runs locally on your machine.

Developed by [Constance Nowak](https://constancenowak.de)

---

## What VibeSorter does

1. You choose a profile: **Business** or **Personal**
2. You tell it which folder to tidy up
3. The local AI analyses each filename and suggests the matching destination folder
4. You see a **preview** — nothing is moved without your confirmation
5. Only after your "yes" are the files moved

---

## Requirements

### 1. Install Python
If you don't already have it: [python.org/downloads](https://www.python.org/downloads/)
Recommended: Python 3.10 or newer

### 2. Install Ollama
Ollama is the local AI framework that keeps everything on your machine.

→ [ollama.com](https://ollama.com) → Download → Install

Then in your terminal:
```bash
ollama pull mistral
```
This downloads the AI model (~4 GB). You only need to do this once.

### 3. Set up VibeSorter

```bash
# Switch into the VibeSorter directory
cd path/to/vibesorter

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python vibesorter.py
```

That's it. VibeSorter will guide you through the rest.

---

## Customising the configuration (`config.yaml`)

The `config.yaml` is the heart of the tool. This is where you define your folder structure:

```yaml
model: "mistral"   # AI model: mistral | llama3 | phi3

profiles:
  business:
    base_structure:
      - "Finance/Invoices/Incoming"
      - "Projects/Active"
      # ... add your own folders here

  personal:
    base_structure:
      - "Media/Photos"
      - "Documents/Insurance"
      # ... add your own folders here
```

Simply adapt the structure to match your own folder names.

---

## Why local?

Most AI tools send your data to the cloud.
That means filenames, document contents and — in the worst case — entire files end up on servers in the United States, often without it being prominently mentioned in the terms and conditions.

VibeSorter uses **Ollama**, a framework for local AI models.
The AI runs on `localhost:11434` — your machine, your network, your data.

---

## Supported models

| Model | Size | Best for |
|-------|------|----------|
| `mistral` | ~4 GB | Recommended for most use cases |
| `llama3` | ~4.7 GB | Slightly more accurate with English filenames |
| `phi3` | ~2.3 GB | Faster, good for lower-spec hardware |

Change the model in `config.yaml`. Download a model with `ollama pull <model-name>`.

---

## Privacy in plain words

- The AI never sees your files — only their **names**.
- Filenames are processed in memory by your local Ollama instance and discarded afterwards.
- No internet connection is required after the model has been downloaded once.
- No analytics, no telemetry, no account.

---

## Licence

MIT — free to use, adapt and share with attribution.

---

*Questions or feedback? → [constancenowak.de](https://constancenowak.de)*
