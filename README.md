## 🎯 Was macht das Tool?

**Das Tool berechnet die optimale Streichung von Fächern für den RWTH Aachen Wirtschaftsingenieurwesen Bachelor, aber universell einsetzbar!-> eventuelle gelten andere Notenstreichungsregelungen für euren Studiengang und ihr müsst den code leicht anpassen. Schaut dafür am besten mal in eure Prüfungsordnung!**

Die Ausgabe zeigt:
1. **Alle Fächer** mit Details (ID, Note, ECTS, Kategorie)
2. **Statistiken** (Anzahl Fächer, Gesamt-ECTS, aktueller Durchschnitt)
3. **Optimale Lösung** (neuer Durchschnitt, gestrichene ECTS)
4. **Empfohlene Streichungen** mit Begründung
5. **Verbesserung** in Notenpunkten


## 🚀 Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/wesselto21/notenstreicher.git
cd Notenstreicher
```

### 2. Python-Abhängigkeiten installieren
```bash
pip install itertools collections
```
*(Das Tool verwendet nur Standard-Bibliotheken)*

### 3. ⚠️ **Fächer eintragen** ⚠️ 
Öffne `notenstreicher.py` und trage deine Fächer in der `main()` Funktion ein (Zeilen 139-170).

### 4. Tool ausführen
```bash
python notenstreicher.py
```

## 📝 Wie trage ich meine Fächer ein?

### Schritt-für-Schritt Anleitung:

1. **Datei öffnen**: `notenstreicher.py` in einem Texteditor öffnen
2. **Zur main() Funktion scrollen**: Zeile 139-170 finden
3. **Demo-Daten ersetzen**: Die `fächer` Liste mit deinen eigenen Fächern ersetzen
4. **Fach-Format**: Jedes Fach folgt diesem Format:
   ```python
   Fach("Fachname", Note, ECTS, "Kategorie")
   ```

### Fach-Parameter:
- **Fachname** (String): Name des Fachs
- **Note** (Float oder None): 
  - `1.0` bis `6.0` für benotete Fächer
  - `None` für unbenotete Fächer (z.B. Praktika)
- **ECTS** (Integer): ECTS-Punkte des Fachs
- **Kategorie** (String oder None):
  - `"wiwi"` für Wirtschaftswissenschaften
  - `"nawi"` für Naturwissenschaften  
  - `"iwi"` für Ingenieurswissenschaften
  - `None` für nicht streichbare Fächer (z.B. Bachelorarbeit)

### Beispiel:
```python
fächer = [
    Fach("Mathematik 1", 2.3, 8, "nawi"),
    Fach("Physik", 2.7, 5, "nawi"),
    Fach("Praktikum", None, 3, "iwi"),
    Fach("Bachelorarbeit", 1.0, 12, None)
]
```