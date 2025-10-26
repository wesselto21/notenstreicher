from itertools import product
from collections import defaultdict

class Fach:
    _next_id = 1
    
    def __init__(self, name, note, ects, modulkategorie):
        """
            name (str): Name des Fachs
            note (float): Note (0 wenn unbenotet, sonst 1.0 bis 6.0)
            ects (int): ECTS-Punkte
            modulkategorie (str): Kategorie (wiwi, nawi, iwi)
        """
        self.name = name
        self.id_nummer = Fach._next_id
        Fach._next_id += 1
        self.note = note
        self.ects = ects
        self.modulkategorie = modulkategorie
    
    def __str__(self):
        note_str = "unbenotet" if self.note == None else f"{self.note}"
        return f"Fach: {self.name} (ID: {self.id_nummer}, Note: {note_str}, ECTS: {self.ects}, Kategorie: {self.modulkategorie})"

def calculate_weighted_average(fächer):
    """
    Berechnet den ECTS-gewichteten Notendurchschnitt für eine Liste von Fächern
    """
    if not fächer:
        return 0.0
    
    total_weighted_sum = sum(f.note * f.ects for f in fächer)
    total_ects = sum(f.ects for f in fächer)
    return total_weighted_sum / total_ects if total_ects > 0 else 0.0

def filter_graded_subjects(fächer, cancellable_only=False):
    """
    Filtert benotete Fächer aus der Liste
    cancellable_only: Wenn True, nur Fächer mit modulkategorie (kündbar)
    """
    filtered = [f for f in fächer if f.note is not None and f.note > 0]
    if cancellable_only:
        filtered = [f for f in filtered if f.modulkategorie is not None]
    return filtered

def optimize_subject_cancellation(fächer):
    """
    Linear Programming Optimization to find best subjects to cancel
    Rules:
    - Max 1 subject per category (wiwi, nawi, iwi)
    - Max 15 ECTS total cancellation
    - Goal: Maximize ECTS-weighted average
    - Fächer ohne Modulbereich (None) können nicht gestrichen werden
    """
    # Filter subjects using helper functions
    benotete_fächer = filter_graded_subjects(fächer, cancellable_only=True)
    unkündbare_fächer = filter_graded_subjects(fächer, cancellable_only=False)
    unkündbare_fächer = [f for f in unkündbare_fächer if f.modulkategorie is None]
    
    if not benotete_fächer:
        print("Keine kündbaren benoteten Fächer gefunden!")
        return
    
    # Group by category using defaultdict
    kategorien = defaultdict(list)
    for fach in benotete_fächer:
        kategorien[fach.modulkategorie].append(fach)
    
    print(f"\n=== LP OPTIMIERUNG: BESTE FÄCHER ZUM STREICHEN ===")
    
    # Create all possible combinations
    best_combination = None
    best_average = float('inf')
    best_ects_cancelled = 0
    
    # Generate all possible combinations
    
    # Create lists of subjects for each category
    category_lists = []
    for kategorie in ['wiwi', 'nawi', 'iwi']:
        if kategorie in kategorien:
            # Add None option (no cancellation in this category)
            category_lists.append([None] + kategorien[kategorie])
        else:
            category_lists.append([None])
    
    print(f"\nPrüfe alle möglichen Kombinationen...")
    
    for combination in product(*category_lists):
        # Calculate ECTS to be cancelled
        cancelled_ects = sum(f.ects for f in combination if f is not None)
        
        # Check ECTS constraint (max 15)
        if cancelled_ects > 15:
            continue
        
        # Calculate new average after cancellation
        remaining_fächer = [f for f in benotete_fächer if f not in combination]
        
        if not remaining_fächer:
            continue
        
        # Include unkündbare Fächer in the average calculation
        all_remaining_fächer = remaining_fächer + unkündbare_fächer
            
        # Calculate ECTS-weighted average using helper function
        new_average = calculate_weighted_average(all_remaining_fächer)
        
        # Check if this is better (lower is better for grades)
        if new_average < best_average:
            best_average = new_average
            best_combination = combination
            best_ects_cancelled = cancelled_ects
    
    if best_combination is None:
        print("Keine gültige Kombination gefunden!")
        return
    
    # Display results
    print(f"\n=== OPTIMALE LÖSUNG ===")
    print(f"NEUER ECTS-gewichteter Durchschnitt: {best_average:.2f}")
    print(f"Gestrichene ECTS: {best_ects_cancelled}")
    print(f"Gestrichene Fächer:")
    
    for fach in best_combination:
        if fach is not None:
            print(f"  - {fach.name} (Note: {fach.note}, ECTS: {fach.ects}, Kategorie: {fach.modulkategorie})")
    
    # Show improvement using helper function
    all_original_fächer = benotete_fächer + unkündbare_fächer
    original_average = calculate_weighted_average(all_original_fächer)
    improvement = original_average - best_average
    print(f"\nVerbesserung: {improvement:.2f} Notenpunkte")
    
    return best_combination, best_average

def main():

    fächer = [
        # DEMO-DATEN: Ersetze diese mit deinen eigenen Fächern!
        Fach("Höhere Mathematik 1", 1.7, 8, "nawi"),
        Fach("Höhere Mathematik 2", 1.3, 8, "nawi"),
        Fach("Höhere Mathematik 3", 2.0, 8, "nawi"),
        Fach("Physik", 2.7, 5, "nawi"),
        Fach("Statistik für Studierende des Wirtschaftsingenieurwesens", 1.0, 6, "nawi"),
        Fach("Elektrizitätsversorgungssysteme", 1.3, 5, "iwi"),
        Fach("Grundgebiete der Elektrotechnik 1 - Einführung in die Schaltungsanalyse", 1.7, 7, "iwi"),
        Fach("Grundgebiete der Elektrotechnik 2 - Modellierung und Analyse elektrischer Komponenten und Schaltungen", 3.0, 8, "iwi"),
        Fach("Grundgebiete der Elektrotechnik 3 - Signale und Systeme", 1.3, 8, "iwi"),
        Fach("Grundgebiete der Elektrotechnik 4 - Einführung in die elektromagnetischen Felder", 1.7, 8, "iwi"),
        Fach("Grundgebiete der Informatik 1 - Programmierung, Algorithmen und Datenstrukturen", 2.0, 4, "iwi"),
        Fach("Praktikum IT 1", None, 3, "iwi"),
        Fach("Praktikum IT 2", None, 3, "iwi"),
        Fach("Systemtheorie 1", 2.3, 5, "iwi"),
        Fach("Hoch- und Mittelspannungsschaltgeräte und -anlagen", 1.0, 5, "iwi"),
        Fach("Planung und Betrieb von Elektrizitätsversorgungssystemen", 1.3, 5, "iwi"),
        Fach("Absatz und Beschaffung", 1.0, 5, "wiwi"),
        Fach("Buchführung und Internes Rechnungswesen", 1.0, 5, "wiwi"),
        Fach("Einführung in die Empirische Wirtschaftsforschung", 1.7, 5, "wiwi"),
        Fach("Entscheidungslehre", 1.0, 5, "wiwi"),
        Fach("Grundlagen des Management", 1.3, 5, "wiwi"),
        Fach("Investition und Finanzierung", 2.3, 5, "wiwi"),
        Fach("Organisation und Personal", 1.7, 5, "wiwi"),
        Fach("Produktion und Logistik", 1.0, 5, "wiwi"),
        Fach("Quantitative Methoden der Wirtschaftswissenschaften", 1.7, 5, "wiwi"),
        Fach("VWL: Einführung", 1.0, 5, "wiwi"),
        Fach("VWL: Märkte und strategisches Entscheiden", 1.0, 5, "wiwi"),
        Fach("Strategisches Management", 1.0, 5, "wiwi"),
        Fach("Industrie Praktikum", None, 12, None),
        Fach("Bachelorarbeit", 1.0, 12, None)
    ]
    
    # Alle Fächer ausgeben
    print("=== TRANSCRIPT FÄCHER ===\n")
    for fach in fächer:
        print(fach)
    
    # Statistiken berechnen
    print(f"\n=== STATISTIKEN ===")
    print(f"Anzahl Fächer: {len(fächer)}")
    
    # ECTS gesamt
    total_ects = sum(fach.ects for fach in fächer)
    print(f"Gesamt ECTS: {total_ects}")
    
    # Notendurchschnitt berechnen (nur benotete Fächer)
    benotete_fächer = filter_graded_subjects(fächer)
    if benotete_fächer:
        gewichteter_durchschnitt = calculate_weighted_average(benotete_fächer)
        print(f"ECTS-gewichteter Notendurchschnitt: {gewichteter_durchschnitt:.2f}")
    
    # LP Optimization für beste Fächer zum Streichen
    optimize_subject_cancellation(fächer)
    

if __name__ == "__main__":
    main()
