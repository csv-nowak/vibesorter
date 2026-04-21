# 🗂 VibeSorter

**Lokale KI-Dateisortierung — 100% DSGVO-konform.**

Deine Dateien werden von einer KI analysiert und in die richtige Ordnerstruktur sortiert.
Kein Cloud-Upload. Kein API-Key. Kein Datenschutzproblem.
Alles läuft lokal auf deinem Rechner.

Entwickelt von [Constance Nowak](https://constancenowak.de)

---

## Was VibeSorter macht

1. Du wählst ein Profil: **Business** oder **Privat**
2. Du gibst an, welchen Ordner aufgeräumt werden soll
3. Die lokale KI analysiert jeden Dateinamen und schlägt den passenden Zielordner vor
4. Du siehst eine **Vorschau** — nichts wird ohne deine Bestätigung verschoben
5. Erst nach deinem "Ja" werden die Dateien verschoben

---

## Voraussetzungen

### 1. Python installieren
Falls noch nicht vorhanden: [python.org/downloads](https://www.python.org/downloads/)
Empfohlen: Python 3.10 oder neuer

### 2. Ollama installieren
Ollama ist das lokale KI-Framework, das alles auf deinem Rechner hält.

→ [ollama.com](https://ollama.com) → Download → Installieren

Danach im Terminal:
```bash
ollama pull mistral
```
Das lädt das KI-Modell (~4 GB). Nur einmal nötig.

### 3. VibeSorter einrichten

```bash
# Ins VibeSorter-Verzeichnis wechseln
cd pfad/zum/vibesorter

# Abhängigkeiten installieren
pip install -r requirements.txt
```

---

## Verwendung

```bash
python vibesorter.py
```

Das war's. VibeSorter führt dich durch den Rest.

---

## Konfiguration anpassen (`config.yaml`)

Die `config.yaml` ist das Herzstück. Hier legst du deine Ordnerstruktur fest:

```yaml
model: "mistral"   # KI-Modell: mistral | llama3 | phi3

profiles:
  business:
    base_structure:
      - "Finanzen/Rechnungen/Eingang"
      - "Projekte/Aktiv"
      # ... eigene Ordner ergänzen

  privat:
    base_structure:
      - "Medien/Fotos"
      - "Dokumente/Versicherungen"
      # ... eigene Ordner ergänzen
```

Passe die Struktur einfach an deine eigenen Ordnernamen an.

---

## Warum lokal?

Die meisten KI-Tools schicken deine Daten in die Cloud.
Das bedeutet: Dateinamen, Dokumenteninhalte, im schlimmsten Fall ganze Dateien landen auf Servern in den USA — oft ohne dass es in den AGB groß hervorgehoben wird.

VibeSorter nutzt **Ollama**, ein Framework für lokale KI-Modelle.
Die KI läuft auf `localhost:11434` — dein Rechner, dein Netzwerk, deine Daten.

---

## Unterstützte Modelle

| Modell | Größe | Eignung |
|--------|-------|---------|
| `mistral` | ~4 GB | Empfohlen für die meisten Anwendungsfälle |
| `llama3` | ~4.7 GB | Etwas präziser bei englischen Dateinamen |
| `phi3` | ~2.3 GB | Schneller, gut für schwächere Hardware |

Modell in `config.yaml` anpassen. Modell mit `ollama pull <modellname>` herunterladen.

---

## Lizenz

MIT — frei nutzbar, anpassbar, weitergeben mit Namensnennung.

---

*Fragen oder Feedback? → [constancenowak.de](https://constancenowak.de)*
