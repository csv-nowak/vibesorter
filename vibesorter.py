"""
VibeSorter — Lokale KI-Dateisortierung
Entwickelt von Constance Nowak | constancenowak.de

100% DSGVO-konform: Alle Daten bleiben auf deinem Rechner.
Kein Cloud-Upload. Kein API-Key. Keine externen Server.
"""

import yaml
import os
import shutil
import json
from pathlib import Path

try:
    import ollama
except ImportError:
    print("❌ Fehlende Bibliothek: 'ollama'")
    print("   Bitte ausführen: pip install ollama pyyaml")
    exit(1)


# ─────────────────────────────────────────────
# KONFIGURATION LADEN
# ─────────────────────────────────────────────

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        print(f"❌ Konfigurationsdatei nicht gefunden: {config_path}")
        exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────
# PROFIL AUSWÄHLEN
# ─────────────────────────────────────────────

def get_profile(config):
    profiles = list(config["profiles"].keys())

    print("\n" + "═" * 50)
    print("  🗂   V I B E S O R T E R")
    print("  Lokale KI-Sortierung — powered by Ollama")
    print("═" * 50)
    print("\nWelches Profil möchtest du verwenden?\n")
    for i, p in enumerate(profiles, 1):
        print(f"  {i}. {p.capitalize()}")

    while True:
        choice = input("\nDeine Wahl (Nummer): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            selected = profiles[int(choice) - 1]
            print(f"\n✅ Profil gewählt: {selected.capitalize()}")
            return selected
        print("  Bitte eine gültige Nummer eingeben.")


# ─────────────────────────────────────────────
# ORDNER AUSWÄHLEN
# ─────────────────────────────────────────────

def get_source_folder():
    print("\nWelchen Ordner soll VibeSorter analysieren?")
    print("(Tipp: Pfad einfach aus dem Finder in dieses Fenster ziehen)\n")
    folder = input("Ordnerpfad: ").strip()

    # Anführungszeichen entfernen (falls vorhanden)
    if len(folder) >= 2 and folder[0] in ('"', "'") and folder[-1] == folder[0]:
        folder = folder[1:-1]

    # Backslash-Escapes entfernen (macOS fügt diese beim Drag & Drop ein)
    # z.B. "Constances\ Chaos" → "Constances Chaos"
    import re
    folder = re.sub(r'\\(.)', r'\1', folder)

    # Tilde (~) durch echten Home-Pfad ersetzen
    folder = os.path.expanduser(folder)

    if not folder:
        print("❌ Kein Pfad eingegeben.")
        return None

    if not os.path.exists(folder):
        print(f"❌ Ordner nicht gefunden: {folder}")
        print("   Tipp: Ordner direkt aus dem Finder ins Terminal-Fenster ziehen.")
        return None

    if not os.access(folder, os.R_OK):
        print(f"❌ Kein Zugriff auf: {folder}")
        print("   Fix: Systemeinstellungen → Datenschutz & Sicherheit → Festplattenvollzugriff → Terminal hinzufügen")
        return None

    return folder


# ─────────────────────────────────────────────
# OLLAMA — DATEI ANALYSIEREN
# ─────────────────────────────────────────────

def ask_ollama(filename, structure, model="mistral"):
    structure_str = "\n".join(f"- {s}" for s in structure)

    prompt = f"""Du bist ein präziser Datei-Sortierer.
Antworte AUSSCHLIESSLICH mit dem exakten Ordnerpfad aus der Liste unten. Keine Erklärung, kein Text drumherum.

Dateiname: {filename}

Verfügbare Zielordner:
{structure_str}

Welcher Ordner passt am besten?"""

    try:
        response = ollama.generate(model=model, prompt=prompt)
        answer = response["response"].strip().split("\n")[0].strip()

        # Besten Match aus der Struktur finden
        answer_lower = answer.lower()
        for folder in structure:
            if folder.lower() in answer_lower or answer_lower in folder.lower():
                return folder

        # Fallback: "Sonstiges" wenn kein Match
        for folder in structure:
            if "sonstiges" in folder.lower():
                return folder

        return structure[-1]

    except Exception as e:
        return f"[Fehler: {e}]"


# ─────────────────────────────────────────────
# SIMULATION
# ─────────────────────────────────────────────

def run_simulation(source_folder, profile_config, model):
    structure = profile_config["base_structure"]

    # Nur Dateien (keine Unterordner)
    files = [
        f for f in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, f))
        and not f.startswith(".")  # versteckte Dateien überspringen
    ]

    if not files:
        print("\n📂 Keine Dateien im Ordner gefunden.")
        return []

    print(f"\n🔍 Analysiere {len(files)} Datei(en) mit lokaler KI ({model})...")
    print("   Deine Daten verlassen deinen Rechner nicht.\n")

    plan = []
    for i, filename in enumerate(files, 1):
        print(f"  [{i:>2}/{len(files)}] {filename[:45]:<45}", end=" ", flush=True)
        target_folder = ask_ollama(filename, structure, model)
        target_path = os.path.join(source_folder, target_folder, filename)
        plan.append({
            "filename": filename,
            "source": os.path.join(source_folder, filename),
            "target_folder": target_folder,
            "target_path": target_path,
        })
        print(f"→  {target_folder}")

    return plan


# ─────────────────────────────────────────────
# SIMULATION ANZEIGEN & SPEICHERN
# ─────────────────────────────────────────────

def show_simulation(plan):
    print("\n" + "═" * 50)
    print("  📋 SIMULATION — Vorschau der Verschiebungen")
    print("═" * 50 + "\n")

    # Gruppiert nach Zielordner
    grouped = {}
    for item in plan:
        grouped.setdefault(item["target_folder"], []).append(item["filename"])

    for folder, files in sorted(grouped.items()):
        print(f"  📁 {folder}/")
        for f in files:
            print(f"     └─ {f}")
        print()


def save_simulation_json(plan, source_folder):
    output_path = os.path.join(source_folder, "vibesorter_simulation.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"  💾 Simulation gespeichert: vibesorter_simulation.json\n")


# ─────────────────────────────────────────────
# AUSFÜHREN
# ─────────────────────────────────────────────

def execute_plan(plan):
    print("\n🚀 Verschiebe Dateien...\n")
    moved, errors = 0, 0

    for item in plan:
        target_dir = os.path.dirname(item["target_path"])
        os.makedirs(target_dir, exist_ok=True)
        try:
            shutil.move(item["source"], item["target_path"])
            print(f"  ✅ {item['filename']}")
            moved += 1
        except Exception as e:
            print(f"  ❌ {item['filename']}: {e}")
            errors += 1

    print(f"\n✨ Fertig! {moved} Datei(en) verschoben.", end="")
    if errors:
        print(f" {errors} Fehler.")
    else:
        print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    config = load_config()
    model = config.get("model", "mistral")

    profile_name = get_profile(config)
    profile_config = config["profiles"][profile_name]

    source_folder = get_source_folder()
    if not source_folder:
        return

    plan = run_simulation(source_folder, profile_config, model)
    if not plan:
        return

    show_simulation(plan)
    save_simulation_json(plan, source_folder)

    print("═" * 50)
    print("  Keine Datei wurde bisher verschoben.")
    print("  Bitte prüfe die Vorschau oben sorgfältig.")
    print("═" * 50)

    while True:
        confirm = input("\n  Dateien jetzt wirklich verschieben? Tippe j + Enter für Ja, n + Enter für Nein: ").strip().lower()
        if confirm in ["j", "ja", "y", "yes"]:
            execute_plan(plan)
            break
        elif confirm in ["n", "nein", "no"]:
            print("\n⏹  Abgebrochen. Keine Dateien wurden verschoben.")
            print("   Die Simulation liegt als 'vibesorter_simulation.json' im Ordner.\n")
            break
        else:
            print("  ↩  Bitte nur 'j' (ja) oder 'n' (nein) eingeben.")


if __name__ == "__main__":
    main()
