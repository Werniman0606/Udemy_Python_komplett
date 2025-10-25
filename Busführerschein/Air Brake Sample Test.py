import random


def run_bilingual_quiz(fragen, titel_en, titel_de):
    """
    Führt ein zweisprachiges Multiple-Choice-Quiz durch (Englisch und Deutsch).
    """
    falsche_antworten = 0
    gesamt_fragen = len(fragen)
    # Mapping für die Antworten des Benutzers (A=0, B=1, C=2, D=3)
    antwort_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    optionen_labels = ['A', 'B', 'C', 'D']

    print(f"=== {titel_en} / {titel_de} ({gesamt_fragen} Questions/Fragen) ===")
    print(
        "Please enter the correct answer (A, B, C, or D). / Bitte geben Sie die korrekte Antwort (A, B, C oder D) ein.")
    print("-" * 80)

    for i, (frage_en, frage_de, optionen_en, optionen_de, korrekter_index) in enumerate(fragen, 1):

        # Zeigt nur die tatsächlich vorhandenen Optionen an
        aktuelle_labels = optionen_labels[:len(optionen_en)]

        print(f"\n--- Question/Frage {i} ---")

        # ENGLISCHER BLOCK
        print(f"\n[ENGLISH ORIGINAL]")
        print(f"{i}) {frage_en}")
        for label, option in zip(aktuelle_labels, optionen_en):
            print(f"  {label}. {option}")

        # DEUTSCHER BLOCK
        print(f"\n[DEUTSCHE ÜBERSETZUNG]")
        print(f"{i}) {frage_de}")
        for label, option in zip(aktuelle_labels, optionen_de):
            print(f"  {label}. {option}")

        while True:
            benutzer_eingabe = input("\nYour Answer (A, B, C, D): ").strip().upper()

            # Überprüft, ob die Eingabe gültig ist
            if benutzer_eingabe in aktuelle_labels:
                benutzer_index = antwort_mapping[benutzer_eingabe]
                break
            else:
                print(f"Invalid input. Please enter {', '.join(aktuelle_labels)}.")

        # Antwort prüfen
        if benutzer_index == korrekter_index:
            print("✅ Correct! / Korrekt!")
        else:
            falsche_antworten += 1
            korrekte_antwort_label = optionen_labels[korrekter_index]
            # Sicherstellen, dass der Index nicht außerhalb der Bounds liegt
            korrekte_antwort_text_en = optionen_en[korrekter_index] if korrekter_index < len(optionen_en) else "Unknown"
            print(f"❌ Wrong. The correct answer is **{korrekte_antwort_label}**: {korrekte_antwort_text_en}")
            print(f"❌ Falsch. Die richtige Antwort ist **{korrekte_antwort_label}**.")

        print("-" * 80)

    # Zusammenfassung
    print(f"\n=== {titel_en} / {titel_de} Quiz Finished ===")
    richtige_antworten = gesamt_fragen - falsche_antworten
    print(f"Result: {richtige_antworten} out of {gesamt_fragen} questions answered correctly.")

    # Passing score for Air Brakes is often 80% (20/25)
    required_to_pass = int(gesamt_fragen * 0.80)
    print(f"Ergebnis: {richtige_antworten} von {gesamt_fragen} Fragen richtig beantwortet.")
    if richtige_antworten / gesamt_fragen >= 0.8:
        print(f"🎉 **PASS!** (You needed {required_to_pass}/{gesamt_fragen} correct answers) / **BESTANDEN!**")
    else:
        print(
            f"😢 **FAIL.** You need {required_to_pass}/{gesamt_fragen} to pass. Keep practicing. / **NICHT BESTANDEN.**")


# --- Air Brake Test Fragen (25 Fragen) ---
# Format: (Fragentext EN, Fragentext DE, [Optionen EN], [Optionen DE], Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen_air_brake = [
    ("The driver must be able to see a low pressure warning which comes on before pressure in the service air tanks falls below ___ psi.",
     "Der Fahrer muss eine Warnung bei niedrigem Druck sehen können, die aufleuchtet, bevor der Druck in den Betriebs-Lufttanks unter ___ psi fällt.",
     ["20", "40", "60", "80"],
     ["20", "40", "60", "80"],
     2),
    ("All air brake equipped vehicles have:",
     "Alle mit Druckluftbremsen ausgestatteten Fahrzeuge haben:",
     ["An air use gauge", "At least one brake heater", "A supply pressure gauge", "A backup hydraulic system"],
     ["Eine Luftverbrauchsanzeige", "Mindestens eine Bremsenheizung",
      "Ein Vorratsdruckmessgerät (Supply Pressure Gauge)", "Ein hydraulisches Backup-System"],
     2),
    ("The supply pressure gauge shows how much pressure:",
     "Das Vorratsdruckmessgerät zeigt, wie viel Druck:",
     ["You have used in this trip", "Is in the air tanks", "Is going to brake chambers", "The air can take"],
     ["Sie auf dieser Fahrt verbraucht haben", "In den Lufttanks ist", "Zu den Bremskammern geleitet wird",
      "Die Luft verträgt"],
     1),
    ("The brake system that applies and releases the brakes when the driver uses the brake pedal is the ___ brake system.",
     "Das Bremssystem, das die Bremsen anlegt und löst, wenn der Fahrer das Bremspedal betätigt, ist das ___ Bremssystem.",
     ["Emergency", "Service", "Parking", "None of the above"],
     ["Notfall- (Emergency)", "Betriebs- (Service)", "Feststell- (Parking)", "Keines der oben genannten"],
     1),
    ("To test air service brakes, you should brake firmly when moving slowly forward. The brakes are ok if you notice:",
     "Um die Betriebs-Druckluftbremsen zu testen, sollten Sie beim langsamen Vorwärtsfahren fest bremsen. Die Bremsen sind in Ordnung, wenn Sie Folgendes bemerken:",
     ["A delayed stopping action", "An unusual feel", "The vehicle pulls to one side", "None of the above"],
     ["Eine verzögerte Bremswirkung", "Ein ungewöhnliches Gefühl", "Das Fahrzeug zieht zu einer Seite",
      "Keines der oben genannten"],
     3),
    ("Total stopping distance for air brakes is longer than that for hydraulic brakes due to ___ distance.",
     "Der gesamte Anhalteweg bei Druckluftbremsen ist länger als bei hydraulischen Bremsen aufgrund der ___ Distanz.",
     ["Perception", "Reaction", "Brake lag", "Effective braking"],
     ["Wahrnehmungs-", "Reaktions-", "Bremsverzögerungs- (Brake Lag)", "Effektive Brems-"],
     2),
    ("Brakes that are overheated can:",
     "Überhitzte Bremsen können:",
     ["Wear out", "Stop working", "Cause you to lose power", "All of the above"],
     ["Verschleißen", "Aufhören zu funktionieren", "Dazu führen, dass Sie Leistung verlieren",
      "Alle der oben genannten"],
     1),
    ("The most common type of foundation brake found on heavy vehicles is the:",
     "Der gängigste Typ der Grundbremse, die in schweren Fahrzeugen zu finden ist, ist die:",
     ["Disc", "Wedge drum", "S-cam drum", "None of the above"],
     ["Scheiben- (Disc)", "Keil-Trommel- (Wedge drum)", "S-Nocken-Trommel- (S-cam drum)", "Keines der oben genannten"],
     2),
    ("At what psi does the safety valve usually open?",
     "Bei welchem psi öffnet sich das Sicherheitsventil normalerweise?",
     ["90", "120", "150", "65"],
     ["90", "120", "150", "65"],
     2),
    ("The brake pedal in an air brake system:",
     "Das Bremspedal in einem Druckluftbremssystem:",
     ["Controls the speed of the air compressor", "Is seldom used",
      "Controls the air pressure applied to put on the brakes", "Is connected to slack adjusters by rods and linkages"],
     ["Steuert die Geschwindigkeit des Luftkompressors", "Wird selten benutzt",
      "Steuert den angewendeten Luftdruck, um die Bremsen zu betätigen",
      "Ist über Stangen und Gestänge mit den Gestängestellern verbunden"],
     2),
    ("With air brake vehicles, the parking brakes should be used:",
     "Bei Druckluftbremsfahrzeugen sollten die Feststellbremsen verwendet werden:",
     ["Whenever you leave the vehicle unattended", "To hold speed downhill", "As little as possible",
      "Only during inspection"],
     ["Immer wenn Sie das Fahrzeug unbeaufsichtigt lassen", "Um die Geschwindigkeit bergab zu halten",
      "So wenig wie möglich", "Nur während der Inspektion"],
     0),
    ("On long downhill grades, experts recommend using a low gear and light, steady pedal pressure instead of on-again off-again braking. Why?",
     "Auf langen Gefällen empfehlen Experten, einen niedrigen Gang und leichten, gleichmäßigen Pedaldruck zu verwenden, anstatt die Bremsen ständig anzulegen und zu lösen. Warum?",
     ["Air usage is less", "Brake linings heat less", "You can keep speed constant", "All of the above"],
     ["Der Luftverbrauch ist geringer", "Die Bremsbeläge erhitzen sich weniger",
      "Sie können die Geschwindigkeit konstant halten", "Alle der oben genannten"],
     3),
    ("Why should you drain water from compressed air tanks?",
     "Warum sollten Sie Wasser aus den Drucklufttanks ablassen?",
     ["Boiling reduces braking power", "Water can freeze and cause brake failure", "Water cools compressor too much",
      "To make room for oil"],
     ["Kochen reduziert die Bremskraft", "Wasser kann gefrieren und Bremsversagen verursachen",
      "Wasser kühlt den Kompressor zu stark", "Um Platz für Öl zu schaffen"],
     1),
    ("If your vehicle has an alcohol evaporator, everyday during cold weather you should:",
     "Wenn Ihr Fahrzeug einen Alkohol-Verdampfer hat, sollten Sie bei kaltem Wetter täglich:",
     ["Check and fill the alcohol level", "Change the alcohol", "Clean air filter", "Check oil for alcohol"],
     ["Den Alkoholstand prüfen und auffüllen", "Den Alkohol wechseln", "Den Luftfilter reinigen",
      "Das Öl auf Alkohol prüfen"],
     0),
    ("To check the play of manual slack adjusters of S-cam brakes, you should park:",
     "Um das Spiel manueller Gestängesteller von S-Nocken-Bremsen zu überprüfen, sollten Sie parken:",
     ["On level ground and apply parking brake", "On level ground, chock wheels, and release parking brake",
      "On level ground and drain air pressure", "On slight grade, release parking brakes and apply service brakes"],
     ["Auf ebener Fläche und die Feststellbremse anziehen",
      "Auf ebener Fläche, Räder verkeilen und die Feststellbremse lösen",
      "Auf ebener Fläche und den Luftdruck ablassen",
      "Auf leichtem Gefälle, Feststellbremsen lösen und Betriebsbremsen anziehen"],
     1),
    ("The most important thing to do when a low air pressure warning comes on is:",
     "Das Wichtigste, was zu tun ist, wenn eine Warnung bei niedrigem Luftdruck aufleuchtet, ist:",
     ["Upshift", "Downshift", "Adjust brake pedal", "Stop and safely park ASAP"],
     ["Hochschalten", "Herunterschalten", "Bremspedal einstellen", "So schnell wie möglich anhalten und sicher parken"],
     3),
    ("The braking power of the spring brakes:",
     "Die Bremskraft der Federspeicherbremsen:",
     ["Increases when service brakes are hot", "Depends on service brakes being in adjustment",
      "Is not affected by condition", "Can only be tested by experts"],
     ["Nimmt zu, wenn die Betriebsbremsen heiß sind", "Hängt von der Einstellung der Betriebsbremsen ab",
      "Wird durch den Zustand nicht beeinflusst", "Kann nur von Experten getestet werden"],
     1),
    ("If your vehicle has an alcohol evaporator, it is there to:",
     "Wenn Ihr Fahrzeug einen Alkohol-Verdampfer hat, dient er dazu:",
     ["Rid the wet tank of alcohol", "Eliminate tank draining", "Boost tank pressure", "Reduce risk of ice in valves"],
     ["Den Nass-Tank von Alkohol zu befreien", "Das tägliche Ablassen des Tanks zu eliminieren",
      "Den Tankdruck zu erhöhen", "Das Risiko von Eis in Ventilen zu verringern"],
     3),
    ("Your truck or bus has a dual air brake system. If a low air pressure warning comes on for only one system, what should you do?",
     "Ihr Lkw oder Bus hat ein Dual-Druckluftbremssystem. Wenn eine Warnung bei niedrigem Luftdruck nur für ein System aufleuchtet, was sollten Sie tun?",
     ["Reduce speed, drive to garage", "Reduce speed, test remaining system", "Continue normally",
      "Stop and safely park until fixed"],
     ["Geschwindigkeit reduzieren, zur Werkstatt fahren", "Geschwindigkeit reduzieren, verbleibendes System testen",
      "Normal weiterfahren", "Anhalten und sicher parken, bis es behoben ist"],
     3),
    ("During normal driving, spring brakes are usually held back by:",
     "Beim normalen Fahren werden die Federspeicherbremsen normalerweise zurückgehalten durch:",
     ["Air pressure", "Spring pressure", "Centrifugal force", "Bolts or clamps"],
     ["Luftdruck", "Federdruck", "Zentrifugalkraft", "Bolzen oder Klammern"],
     0),
    ("The air compressor governor controls:",
     "Der Luftkompressor-Regler (Governor) steuert:",
     ["Compressor speed", "Air pressure applied to brakes", "When air is pumped into tanks",
      "When brake chambers release pressure"],
     ["Die Kompressorgeschwindigkeit", "Den auf die Bremsen angewendeten Luftdruck",
      "Wann Luft in die Tanks gepumpt wird", "Wann die Bremskammern Druck ablassen"],
     2),
    ("For emergency stab braking, you should:",
     "Für das Notfall-Stoßbremsen (Stab Braking) sollten Sie:",
     ["Pump pedal rapidly", "Press hard, release when wheels lock, then reapply",
      "Brake hard until wheels lock then release for same time", "Press hard and use hand valve"],
     ["Das Pedal schnell pumpen", "Fest drücken, loslassen, wenn die Räder blockieren, dann erneut anwenden",
      "Hart bremsen, bis die Räder blockieren, dann für die gleiche Zeit loslassen",
      "Fest drücken und das Handventil verwenden"],
     1),
    ("The air loss rate for a straight truck or bus with the engine off and service brake released is:",
     "Die Luftverlustrate für einen Lastwagen oder Bus mit ausgeschaltetem Motor und gelöster Betriebsbremse beträgt:",
     ["1 psi in 30 seconds", "2 psi in 1 minute", "2 psi in 45 seconds", "3 psi in 1 minute"],
     ["1 psi in 30 Sekunden", "2 psi in 1 Minute", "2 psi in 45 Sekunden", "3 psi in 1 Minute"],
     1),
    ("Your brakes are fading when:",
     "Ihre Bremsen lassen nach (Fading), wenn:",
     ["You have to push harder to control speed downhill", "Pedal feels spongy", "Releasing pressure increases speed",
      "Less pressure needed"],
     ["Sie bergab härter drücken müssen, um die Geschwindigkeit zu kontrollieren", "Das Pedal sich schwammig anfühlt",
      "Das Lösen des Drucks die Geschwindigkeit erhöht", "Weniger Druck benötigt wird"],
     0),
    ("Why should the air brake system be balanced?",
     "Warum sollte das Druckluftbremssystem ausgewogen (balanced) sein?",
     ["To give enough stopping power to all wheels", "For a smoother ride", "To allow better slack adjustment",
      "All of the above"],
     ["Um allen Rädern genügend Bremskraft zu verleihen", "Für eine sanftere Fahrt",
      "Um eine bessere Gestängesteller-Einstellung zu ermöglichen", "Alle der oben genannten"],
     0)
]

# Start des zweisprachigen Air Brake Quiz
if __name__ == "__main__":
    run_bilingual_quiz(quiz_fragen_air_brake, "Air Brake Test", "Druckluftbremsen Test")