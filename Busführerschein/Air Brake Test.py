import time

# Die Fragen, Optionen und korrekten Antworten (als 0-basierter Index)
# *** WICHTIG: Die Reihenfolge und Indizes wurden anhand der Quelldatei "Air Brake Test.pdf" verifiziert. ***
# Format: (Fragentext (EN), [Option A, Option B, Option C, Option D] (EN), Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen = [
    # Q1: Air loss in a straight truck... -> D (Index 3)
    ("Air loss in a straight truck or bus should not be more than ___ with the engine off and the brakes on.",
     ["1 PSI in 30 seconds", "1 PSI in one minute", "2 PSI in 45 seconds", "3 PSI in one minute"], 3),
    # Q2: You should know that your brakes are fading when: -> A (Index 0)
    ("You should know that your brakes are fading when:",
     ["You have to push harder on the brake pedal to control your speed on a downgrade",
      "The brake pedal feels spongy when pressure is applied",
      "Pressure on the brake pedal is released and speed increases",
      "Less pressure is needed on the brake pedal for each stop"], 0),
    # Q3: The supply pressure gauge shows the driver how much pressure: -> B (Index 1)
    ("The supply pressure gauge shows the driver how much pressure:",
     ["Has been used in this trip", "Is in the air tanks", "Is being sent to the brake chambers",
      "The air can tolerate"], 1),
    # Q4: The brake system that applies and releases the brakes... is the: -> B (Index 1)
    ("The brake system that applies and releases the brakes when the driver uses the brake pedal is the:",
     ["Emergency brake system", "Service brake system", "Parking brake system", "None of the above"], 1),
    # Q5: If your vehicle has an alcohol evaporator, every day during cold weather you should: -> A (Index 0)
    ("If your vehicle has an alcohol evaporator, every day during cold weather you should:",
     ["Check and fill the alcohol level", "Change the alcohol from a new bottle", "Clean the air filter with alcohol",
      "Check the oil for alcohol content"], 0),
    # Q6: Why should you drain water from compressed air tanks? -> B (Index 1)
    ("Why should you drain water from compressed air tanks?",
     ["The different boiling points reduce braking power", "Water can freeze in cold weather and cause brake failure",
      "Water cools the compressor too much", "To make room for the oil that should be there instead"], 1),
    # Q7: If the air compressor should develop a leak, what keeps the air in the tanks? -> D (Index 3)
    ("If the air compressor should develop a leak, what keeps the air in the tanks?",
     ["The air compressor governor", "The tractor protection valve", "The emergency relay valve",
      "The one-way check valve"], 3),
    # Q8: On long downhill grades experts recommend light steady pedal pressure... Why? -> D (Index 3)
    ("On long downhill grades experts recommend light steady pedal pressure instead of on-again off-again braking. Why?",
     ["Air usage is less with light steady pressure", "Brake linings do not heat up as much with light pressure",
      "It is easier to keep vehicle speed constant in a low gear", "All of the above"], 3),
    # Q9: Your truck or bus has a dual air brake system. If a low air pressure warning comes on... -> D (Index 3)
    ("Your truck or bus has a dual air brake system. If a low air pressure warning comes on for only one system, what should you do?",
     ["Reduce your speed and drive to the nearest garage for repairs",
      "Reduce your speed and test the remaining system while under way",
      "Continue at normal speed and find a garage before the brakes lock",
      "Stop, safely park, and continue only after the system is fixed"], 3),
    # Q10: During normal driving, spring brakes are usually held back by: -> A (Index 0)
    ("During normal driving, spring brakes are usually held back by:",
     ["Air pressure", "Spring pressure", "Centrifugal force", "Bolts or clamps"], 0),
    # Q11: Which of the following makes the total stopping distance for air brakes longer... -> C (Index 2)
    ("Which of the following makes the total stopping distance for air brakes longer than that for hydraulic brakes?",
     ["Perception distance", "Reaction distance", "Brake lag distance", "Effective braking distance"], 2),
    # Q12: The most common type of foundation brake found on heavy vehicles is the: -> C (Index 2)
    ("The most common type of foundation brake found on heavy vehicles is the:",
     ["Disc", "Wedge drum", "S-cam drum", "None of the above"], 2),
    # Q13: In air brake vehicles the parking brakes should be used: -> A (Index 0)
    ("In air brake vehicles the parking brakes should be used:",
     ["Whenever the vehicle is parked", "To hold your speed when going downhill", "As little as possible",
      "Only during pre- and post - trip inspections"], 0),
    # Q14: To make an emergency stop with air brakes, using the stab braking method, you should: -> B (Index 1)
    ("To make an emergency stop with air brakes, using the stab braking method, you should:",
     ["Pump the brake pedal rapidly and lightly",
      "Brake as hard as you can, get off the brakes when the wheels lock, get back on the brakes when the wheels start rolling again",
      "Brake hard until the wheels lock, then get off the brakes for as much time as the wheels were locked",
      "Press hard on the brake pedal and apply full hand valve until you stop"], 1),
    # Q15: Parking or emergency brakes of trucks and buses can be legally held on by ___ pressure -> A (Index 0)
    ("Parking or emergency brakes of trucks and buses can be legally held on by ___ pressure",
     ["Spring", "Fluid", "Air", "Atmospheric"], 0),
    # Q16: The driver must be able to see a warning that is given before air pressure... falls below -> C (Index 2)
    ("The driver must be able to see a warning that is given before air pressure in the service air tanks falls below",
     ["20 psi", "40 psi", "60 psi", "80 psi"], 2),
    # Q17: If your vehicle has an alcohol evaporator, it is there to: -> D (Index 3)
    ("If your vehicle has an alcohol evaporator, it is there to:",
     ["Rid the wet tank of alcohol that condenses and sits at the bottom", "Eliminate the need for daily tank draining",
      "Boost tank pressure the same way that turbochargers boost engines",
      "Reduce the risk of ice in air brake valves in cold weather"], 3),
    # Q18: The brake pedal in an air brake system: -> C (Index 2)
    ("The brake pedal in an air brake system:",
     ["Controls the speed of the air compressor", "Is seldom used, compared to hydraulic systems",
      "Controls the air pressure applied to put on the brakes",
      "Is connected to slack adjusters by a series of rods and linkages"], 2),
    # Q19: If your truck or bus has dual parking control valves... pressure from a separate tank to: -> C (Index 2)
    ("If your truck or bus has dual parking control valves it means that you can use pressure from a separate tank to:",
     ["Balance the service brake system while you are driving", "Stay parked without using up service air pressure",
      "Release the spring brakes to move a short distance", "Brake harder if the main tank is getting low"], 2),
    # Q20: To check the free play of manual slack adjusters of S-cam brakes, you should: -> B (Index 1)
    ("To check the free play of manual slack adjusters of S-cam brakes, you should:",
     ["Stop on level ground and apply the parking brakes",
      "Park on level ground, chock the wheels, and release the parking brakes",
      "Park on level ground and drain off air pressure before checking the adjustment",
      "Park on a slight grade, release the parking brakes, and apply the service brakes, check for vehicle movement"],
     1),
    # Q21: Of the choices below, the first thing to do when a low air pressure warning comes on is: -> D (Index 3)
    ("Of the choices below, the first thing to do when a low air pressure warning comes on is:",
     ["Upshift", "Downshift", "Adjust the brake pedal for more travel", "Stop and safely park as soon as possible"], 3),
    # Q22: The air compressor governor controls: -> C (Index 2)
    ("The air compressor governor controls:",
     ["The speed of the air compressor", "Air pressure applied to the brakes", "When air is pumped into the air tanks",
      "When the brake chambers release pressure"], 2),
    # Q23: The braking power of the spring brakes: -> B (Index 1)
    ("The braking power of the spring brakes:",
     ["Increases when the service brakes are hot", "Depends on the adjustment of the service brakes",
      "Is not affected by the condition of the service brakes",
      "Can only be tested by highly-trained brake service people"], 1),
    # Q24: Air brake equipped vehicles must have: -> B (Index 1)
    ("Air brake equipped vehicles must have:",
     ["An air use gauge", "A supply pressure gauge", "At least two brake heaters", "A backup hydraulic system"], 1),
    # Q25: If you must make an emergency stop, you should brake so that you: -> C (Index 2)
    ("If you must make an emergency stop, you should brake so that you:",
     ["Use the hand brake first", "Can steer hard while braking hard", "Stay in a straight line and can steer",
      "Use the full power of the brakes and lock them"], 2)
]


def get_german_translation(index):
    """
    Manuell erstellte deutsche Übersetzungen für die Fragen und Optionen.
    """
    translations = {
        0: {
            "q": "Luftverlust in einem geraden LKW oder Bus sollte nicht mehr als ___ betragen, wenn der Motor aus und die Bremsen angezogen sind.",
            "o": ["1 PSI in 30 Sekunden", "1 PSI in einer Minute", "2 PSI in 45 Sekunden", "3 PSI in einer Minute"]},
        1: {"q": "Sie sollten wissen, dass Ihre Bremsen nachlassen (fading), wenn:", "o": [
            "Sie das Bremspedal stärker drücken müssen, um Ihre Geschwindigkeit bei einem Gefälle zu kontrollieren",
            "Das Bremspedal sich schwammig anfühlt, wenn Druck ausgeübt wird",
            "Der Druck auf das Bremspedal gelöst wird und die Geschwindigkeit zunimmt",
            "Für jeden Stopp weniger Druck auf das Bremspedal benötigt wird"]},
        2: {"q": "Das Vorratsdruckmanometer (Supply Pressure Gauge) zeigt dem Fahrer an, wie viel Druck:",
            "o": ["Auf dieser Fahrt verbraucht wurde", "Sich in den Lufttanks befindet",
                  "An die Bremskammern gesendet wird", "Die Luft vertragen kann"]},
        3: {"q": "Das Bremssystem, das die Bremsen anlegt und löst, wenn der Fahrer das Bremspedal betätigt, ist das:",
            "o": ["Notbremssystem (Emergency)", "Betriebsbremssystem (Service)", "Feststellbremssystem (Parking)",
                  "Keine der oben genannten"]},
        4: {
            "q": "Wenn Ihr Fahrzeug über einen Alkohol-Verdampfer (Alcohol Evaporator) verfügt, sollten Sie jeden Tag bei kaltem Wetter:",
            "o": ["Den Alkoholspiegel prüfen und auffüllen", "Den Alkohol aus einer neuen Flasche wechseln",
                  "Den Luftfilter mit Alkohol reinigen", "Den Ölstand auf Alkoholgehalt prüfen"]},
        5: {"q": "Warum sollten Sie Wasser aus Druckluftbehältern ablassen?",
            "o": ["Die unterschiedlichen Siedepunkte reduzieren die Bremskraft",
                  "Wasser kann bei kaltem Wetter gefrieren und zu Bremsversagen führen",
                  "Wasser kühlt den Kompressor zu stark ab",
                  "Um Platz für das Öl zu schaffen, das stattdessen dort sein sollte"]},
        6: {"q": "Wenn der Luftkompressor ein Leck entwickeln sollte, was hält die Luft in den Tanks?",
            "o": ["Der Luftkompressor-Regler (Governor)", "Das Sattelzug-Schutzventil", "Das Notfall-Relaisventil",
                  "Das Einweg-Rückschlagventil (One-Way Check Valve)"]},
        7: {
            "q": "Bei langen Gefällstrecken empfehlen Experten leichten, gleichmäßigen Pedaldruck anstelle von abwechselndem Bremsen. Warum?",
            "o": ["Der Luftverbrauch ist bei leichtem, gleichmäßigem Druck geringer",
                  "Bremsbeläge heizen sich bei leichtem Druck nicht so stark auf",
                  "Es ist einfacher, die Fahrzeuggeschwindigkeit in einem niedrigen Gang konstant zu halten",
                  "Alles oben Genannte"]},
        8: {
            "q": "Ihr LKW oder Bus verfügt über ein Zweikreis-Druckluftbremssystem. Wenn eine Warnung für niedrigen Luftdruck nur für einen Kreis aufleuchtet, was sollten Sie tun?",
            "o": ["Reduzieren Sie Ihre Geschwindigkeit und fahren Sie zur nächsten Werkstatt für Reparaturen",
                  "Reduzieren Sie Ihre Geschwindigkeit und testen Sie das verbleibende System während der Fahrt",
                  "Fahren Sie mit normaler Geschwindigkeit weiter und finden Sie eine Werkstatt, bevor die Bremsen blockieren",
                  "Halten Sie sicher an, parken Sie und fahren Sie erst weiter, nachdem das System repariert wurde"]},
        9: {
            "q": "Während der normalen Fahrt werden Federspeicherbremsen (Spring Brakes) normalerweise zurückgehalten durch:",
            "o": ["Luftdruck", "Federdruck", "Zentrifugalkraft", "Bolzen oder Klemmen"]},
        10: {
            "q": "Was von den folgenden Faktoren führt dazu, dass der gesamte Bremsweg bei Druckluftbremsen länger ist als bei hydraulischen Bremsen?",
            "o": ["Wahrnehmungsdistanz (Perception distance)", "Reaktionsdistanz (Reaction distance)",
                  "Bremsverzögerungsdistanz (Brake lag distance)",
                  "Tatsächliche Bremsdistanz (Effective braking distance)"]},
        11: {"q": "Der am häufigsten bei schweren Fahrzeugen verwendete Typ der Betriebsbremse ist die:",
             "o": ["Scheibenbremse", "Keil-Trommelbremse", "S-Nocken-Trommelbremse (S-cam drum)",
                   "Keine der oben genannten"]},
        12: {"q": "Bei Fahrzeugen mit Druckluftbremsen sollte die Feststellbremse verwendet werden:",
             "o": ["Immer, wenn das Fahrzeug geparkt wird", "Um Ihre Geschwindigkeit bei Bergabfahrt zu halten",
                   "So wenig wie möglich", "Nur während der Kontrollen vor und nach der Fahrt"]},
        13: {
            "q": "Um eine Notbremsung mit Druckluftbremsen unter Verwendung der **'Stab Braking'-Methode** durchzuführen, sollten Sie:",
            "o": ["Das Bremspedal schnell und leicht pumpen",
                  "So stark wie möglich bremsen, von der Bremse gehen, wenn die Räder blockieren, und wieder auf die Bremse gehen, wenn die Räder wieder rollen",
                  "Stark bremsen, bis die Räder blockieren, dann für die gleiche Zeit, die die Räder blockiert waren, von der Bremse gehen",
                  "Fest auf das Bremspedal drücken und das Handventil vollständig betätigen, bis Sie anhalten"]},
        14: {"q": "Feststell- oder Notbremsen von LKWs und Bussen können legal durch ___ gehalten werden.",
             "o": ["Federdruck", "Flüssigkeitsdruck", "Luftdruck", "Atmosphärischer Druck"]},
        15: {
            "q": "Der Fahrer muss eine Warnung sehen können, die gegeben wird, bevor der Luftdruck in den Betriebs-Lufttanks unter ___ fällt.",
            "o": ["20 psi", "40 psi", "60 psi", "80 psi"]},
        16: {"q": "Wenn Ihr Fahrzeug über einen Alkohol-Verdampfer verfügt, ist dieser dazu da, um:",
             "o": ["Den Nassbehälter von Alkohol zu befreien, der kondensiert und sich am Boden absetzt",
                   "Die Notwendigkeit des täglichen Ablassens des Tanks zu eliminieren",
                   "Den Tankdruck auf die gleiche Weise zu erhöhen, wie Turbolader Motoren aufladen",
                   "Das Risiko von Vereisungen in den Druckluftbremsventilen bei kaltem Wetter zu reduzieren"]},
        17: {"q": "Das Bremspedal in einem Druckluftbremssystem:",
             "o": ["Steuert die Geschwindigkeit des Luftkompressors",
                   "Wird im Vergleich zu hydraulischen Systemen selten verwendet",
                   "Steuert den angewendeten Luftdruck, um die Bremsen anzulegen",
                   "Ist über eine Reihe von Stangen und Gestängen mit den Gestängestellern (Slack Adjusters) verbunden"]},
        18: {
            "q": "Wenn Ihr LKW oder Bus über **doppelte Feststellbremsventile (Dual Parking Control Valves)** verfügt, bedeutet dies, dass Sie Druck aus einem separaten Tank verwenden können, um:",
            "o": ["Das Betriebsbremssystem während der Fahrt auszugleichen",
                  "Geparkt zu bleiben, ohne den Betriebsluftdruck zu verbrauchen",
                  "Die Federspeicherbremsen zu lösen, um eine kurze Strecke zu fahren",
                  "Stärker zu bremsen, wenn der Haupttank zur Neige geht"]},
        19: {
            "q": "Um das freie Spiel der **manuellen Gestängesteller (Slack Adjusters) von S-Nocken-Bremsen** zu überprüfen, sollten Sie:",
            "o": ["Auf ebenem Boden anhalten und die Feststellbremsen anziehen",
                  "Auf ebenem Boden parken, die Räder blockieren (chock the wheels) und die Feststellbremsen lösen",
                  "Auf ebenem Boden parken und den Luftdruck ablassen, bevor Sie die Einstellung überprüfen",
                  "Auf einer leichten Steigung parken, die Feststellbremsen lösen, die Betriebsbremsen betätigen und auf Fahrzeugbewegung prüfen"]},
        20: {
            "q": "Von den unten genannten Optionen ist das Erste, was zu tun ist, wenn eine **Warnung für niedrigen Luftdruck** aufleuchtet:",
            "o": ["Hochschalten", "Herunterschalten", "Das Bremspedal für mehr Federweg einstellen",
                  "So schnell wie möglich anhalten und sicher parken"]},
        21: {"q": "Der **Luftkompressor-Regler (Governor)** steuert:",
             "o": ["Die Geschwindigkeit des Luftkompressors", "Den angewendeten Luftdruck auf die Bremsen",
                   "Wann Luft in die Lufttanks gepumpt wird", "Wann die Bremskammern den Druck ablassen"]},
        22: {"q": "Die Bremskraft der Federspeicherbremsen:", "o": ["Erhöht sich, wenn die Betriebsbremsen heiß sind",
                                                                    "Hängt von der Einstellung der Betriebsbremsen ab",
                                                                    "Wird nicht durch den Zustand der Betriebsbremsen beeinflusst",
                                                                    "Kann nur von hochqualifiziertem Bremsservicepersonal getestet werden"]},
        23: {"q": "Mit **Druckluftbremsen ausgestattete Fahrzeuge** müssen haben:",
             "o": ["Ein Luftverbrauchsanzeiger", "Ein Vorratsdruckmanometer (Supply Pressure Gauge)",
                   "Mindestens zwei Bremsheizungen", "Ein hydraulisches Ersatzsystem"]},
        24: {"q": "Wenn Sie eine **Notbremsung** durchführen müssen, sollten Sie so bremsen, dass Sie:",
             "o": ["Zuerst die Handbremse benutzen", "Beim starken Bremsen stark lenken können",
                   "In einer geraden Linie bleiben und lenken können",
                   "Die volle Kraft der Bremsen nutzen und sie blockieren"]}
    }

    # Sicherstellen, dass der Index im gültigen Bereich liegt
    if index >= 0 and index < len(translations):
        return translations[index]
    else:
        return {"q": "Übersetzung nicht verfügbar", "o": ["A", "B", "C", "D"]}


def run_quiz(fragen_liste):
    """
    Führt das interaktive Quiz in der Konsole durch, ohne die Reihenfolge der Fragen zu mischen.
    """
    score = 0
    total_fragen = len(fragen_liste)
    optionen_labels = ['A', 'B', 'C', 'D']

    print("=" * 60)
    print("        Willkommen zum Interaktiven Druckluftbremsen-Quiz! 🚌💨")
    print("      (Fragen in Originalreihenfolge, Antworten verifiziert)")
    print(f"               Es warten {total_fragen} Fragen auf dich.")
    print("=" * 60)
    print("Antworte mit A, B, C oder D.")
    time.sleep(1)

    # Die Fragen werden in der Reihenfolge durchlaufen, in der sie in der Liste stehen
    for i, (frage_en, optionen_en, korrekter_index) in enumerate(fragen_liste, 1):
        # Der Index i-1 ist der direkte Index für die Übersetzung
        original_index = i - 1

        # Deutsche Übersetzung abrufen
        translation = get_german_translation(original_index)
        frage_de = translation['q']
        optionen_de = translation['o']

        korrekte_antwort_label = optionen_labels[korrekter_index]

        print("\n" + "-" * 60)
        print(f"FRAGE {i} von {total_fragen}:")

        # Frage und Optionen in Deutsch und Englisch anzeigen
        print(f"DE: {frage_de}")
        print(f"EN: {frage_en}")
        print("\nOptionen (DE/EN):")

        for label, opt_de, opt_en in zip(optionen_labels, optionen_de, optionen_en):
            print(f"  ({label}) {opt_de} / {opt_en}")

        # Eingabe vom Benutzer anfordern und validieren
        while True:
            user_input = input("\nDeine Antwort (A/B/C/D): ").strip().upper()
            if user_input in optionen_labels:
                break
            else:
                print("Ungültige Eingabe. Bitte antworte nur mit A, B, C oder D.")

        # Antwort prüfen
        if user_input == korrekte_antwort_label:
            score += 1
            print("✅ Korrekt! Gut gemacht.")
        else:
            korrekte_antwort_text_de = optionen_de[korrekter_index]
            print(f"❌ Falsch. Die richtige Antwort ist **{korrekte_antwort_label}**.")
            print(f"    Antwort: {korrekte_antwort_text_de}")

        time.sleep(0.5)

    # Endergebnisse anzeigen
    print("\n" + "=" * 60)
    print("                QUIZ BEENDET - ERGEBNISSE")
    print("=" * 60)
    print(f"Du hast {score} von {total_fragen} Fragen richtig beantwortet.")

    prozent = (score / total_fragen) * 100
    print(f"Deine Punktzahl: **{prozent:.2f}%**")

    if prozent >= 80:
        print("\n🎉 Herzlichen Glückwunsch! Du hast eine sehr gute Punktzahl erreicht!")
    elif prozent >= 60:
        print("\n👍 Nicht schlecht! Du hast die Grundlagen verstanden, aber es gibt noch Verbesserungspotenzial.")
    else:
        print("\n🧐 Weiter üben! Wiederhole die Themen zur Druckluftbremse.")

    print("=" * 60)


# Start des Skripts
if __name__ == "__main__":
    # Startet das Quiz in der definierten Originalreihenfolge
    run_quiz(quiz_fragen)