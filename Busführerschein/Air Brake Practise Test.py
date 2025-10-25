import time

# --- DATENSTRUKTUR: FRAGEN, OPTIONEN UND KORREKTE ANTWORTEN ---
# Format: (Fragentext (EN), [Option A, Option B, Option C, Option D (falls vorhanden)] (EN), Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen_air_brakes_2 = [
    # Frage 1
    ("Modern air brake systems combine three different systems. The systems are the service, parking, and ___ brake systems.",
     ["Emergency", "Foot", "Drum"], 0),
    # Frage 2
    ("The driver must be able to see a warning before air pressure in the service air tanks falls below ___ psi.",
     ["40", "60", "80"], 1),
    # Frage 3
    ("The brake pedal in an air brake system:",
     ["Controls the speed of the air compressor.", "Always needs to be held down halfway during normal driving.",
      "Controls the air pressure applied to the brakes."], 2),
    # Frage 4
    ("Air braking takes more time than hydraulic braking because air:",
     ["Brakes use different brake drums.", "Takes more time to flow through the lines than hydraulic fluid.",
      "Is always leaking through air line fittings."], 1),
    # Frage 5
    ("If your vehicle has an alcohol evaporator, it is there to:",
     ["Rid the wet tank of alcohol that condenses and sits at the bottom.",
      "Eliminate the need for daily tank draining.", "Reduce the risk of ice in air brake valves in cold weather."], 2),
    # Frage 6
    ("If your truck has dual parking control valves, you can use pressure from a separate tank to:",
     ["Release the spring emergency parking brakes to move a short distance.",
      "Apply more brake pressure if the main tank is getting low.",
      "Stay parked twice as long with your service air pressure."], 0),
    # Frage 7
    ("To check the free play of manual slack adjusters on S-cam brakes, you should park on:",
     ["Level ground with the parking brake on, then apply the service brake.",
      "Level ground, chock the wheels, and turn off the parking brakes.",
      "Level ground and drain off air pressure before adjusting."], 1),
    # Frage 8
    ("Of the choices below, the first thing to do when a low air pressure warning comes on is:",
     ["Stop and safely park as soon as possible.", "Shift to the next higher gear.",
      "Open the air supply control valve."], 0),
    # Frage 9
    ("The air compressor governor controls:",
     ["When the brake chambers release pressure.", "Air pressure applied to the brakes.",
      "When air is pumped into the air tanks."], 2),
    # Frage 10
    ("The braking power of the spring brakes:",
     ["Is not affected by the condition of the service brakes.",
      "Can only be tested by highly trained brake service people.",
      "Depends on whether the service brakes are in adjustment."], 2),
    # Frage 11
    ("All vehicles equipped with air brakes have:",
     ["A hydraulic system, in case the air system fails.", "A supply pressure gauge.", "An air use gauge."], 1),
    # Frage 12
    ("If you must make an emergency stop, brake so you:",
     ["Use the full power of the brakes and lock them.", "Can steer and your vehicle stays in a straight line.",
      "Use the hand brake first."], 1),
    # Frage 13
    ("If you do not have automatic tank drains, how often should you drain the oil and water from the bottom of compressed air storage tanks?",
     ["At the end of each day of driving", "Once a week", "Every other week"], 0),
    # Frage 14
    ("The application pressure gauge shows how much air pressure you:",
     ["Have used in this trip.", "Have in the air tanks.", "Are applying to the brakes."], 2),
    # Frage 15
    ("Your brakes are fading when:",
     ["You have to push harder on the brake pedal to control your speed on a downgrade.",
      "The brake pedal feels spongy when you apply pressure.",
      "You release pressure on the brake pedal and speed increases."], 0),
    # Frage 16
    ("If your vehicle has an alcohol evaporator, every day during cold weather you should:",
     ["Check the alcohol level and fill the evaporator if needed.", "Change the alcohol.",
      "Clean the air filter with alcohol."], 0),
    # Frage 17
    ("Why should you drain water from compressed air tanks?",
     ["The low boiling point of water reduces braking power.",
      "Water can freeze in cold weather and cause brake failure.", "Water cools the compressor too much."], 1),
    # Frage 18
    ("Your vehicle has a dual air brake system. If a low air pressure warning comes on for the secondary system, you should:",
     ["Bring the vehicle to a safe stop and continue only when the system is fixed.",
      "Reduce your speed, and test the remaining system while driving.",
      "Reduce your speed, and drive to the nearest garage for repairs."], 0),
    # Frage 19
    ("During normal driving, spring brakes are usually held back by:",
     ["Bolts or clamps.", "Air pressure.", "Spring pressure."], 1),
    # Frage 20
    ("In air brake vehicles, the parking brakes should be used:",
     ["As little as possible.", "Any time the vehicle is parked.", "To hold your speed when going downhill."], 1),
    # Frage 21
    ("Emergency stab braking is when you:",
     ["Press hard on the brake pedal and apply hand valve fully until you stop.",
      "Apply the hand valve for one second, then push hard on the pedal.",
      "Brake as hard as you can, release the brake when the wheels lock, then put on the brakes again when the wheels start rolling."],
     2),
    # Frage 22
    ("A straight truck air brake system should not leak at a rate of more than ___ psi per minute with the engine off and the brakes released.",
     ["6", "4", "2"], 2),
    # Frage 23
    ("The air loss rate for a straight truck with the engine off and the brakes on should not be more than:",
     ["1 psi in 30 seconds.", "2 psi in 45 seconds.", "3 psi in one minute."], 2),
    # Frage 24
    ("The supply pressure gauge shows how much pressure:",
     ["You have used in this trip.", "Is in the air tanks.", "Is going to the brake chambers."], 1),
    # Frage 25
    ("The brake system that applies and releases the brakes when the driver uses the brake pedal is the ___ brake system.",
     ["Service", "Parking", "Drum"], 0),
    # Frage 26
    ("Why should you drain water from compressed air tanks?",
     ["The boiling point reduces braking power.", "Water can freeze in cold weather and cause brake failure.",
      "Water cools the compressor too much."], 1),
    # Frage 27
    ("Total stopping distance for air brakes is longer than that for hydraulic brakes due to ___ distance.",
     ["Perception", "Reaction", "Brake lag"], 2),
    # Frage 28
    ("The most common type of foundation brake found on heavy vehicles is the:",
     ["Disc brake.", "Wedge drum brake.", "S-cam drum brake."], 2),
    # Frage 29
    ("Which of the following makes total stopping distance longer for air brakes than for hydraulic brakes:",
     ["Brake lag", "Perception distance", "Reaction time distance"], 0),
    # Frage 30
    ("If the air compressor develops a leak, what keeps the air in the tanks?",
     ["The one-way check valve", "The emergency relay valve", "The tractor protection valve"], 0)
]


def get_german_translation(index):
    """
    Manuell erstellte deutsche Übersetzungen für Fragen und Optionen (entsprechend dem Index).
    """
    translations = [
        {
            "q": "Moderne Druckluftbremssysteme kombinieren drei verschiedene Systeme. Die Systeme sind die Betriebs-, Feststell- und ___ Bremssysteme.",
            "o": ["Notfall- (Emergency)", "Fuß- (Foot)", "Trommel- (Drum)"]},
        {
            "q": "Der Fahrer muss eine Warnung sehen können, bevor der Luftdruck in den Betriebs-Lufttanks unter ___ psi fällt.",
            "o": ["40", "60", "80"]},
        {"q": "Das Bremspedal in einem Druckluftbremssystem:", "o": ["Steuert die Geschwindigkeit des Luftkompressors.",
                                                                     "Muss während der normalen Fahrt immer auf halber Strecke gehalten werden.",
                                                                     "Steuert den auf die Bremsen angewendeten Luftdruck."]},
        {"q": "Druckluftbremsen benötigen mehr Zeit als hydraulische Bremsen, weil Luft:",
         "o": ["Andere Bremstrommeln verwendet.",
               "Mehr Zeit benötigt, um durch die Leitungen zu fließen als Hydraulikflüssigkeit.",
               "Immer durch die Luftleitungsanschlüsse entweicht."]},
        {"q": "Wenn Ihr Fahrzeug einen Alkohol-Verdampfer (Alcohol Evaporator) besitzt, dient er dazu, um:",
         "o": ["Den Nassbehälter von kondensiertem Alkohol zu befreien, der sich am Boden absetzt.",
               "Die Notwendigkeit des täglichen Ablassens des Tanks zu eliminieren.",
               "Das Risiko von Vereisungen in den Druckluftbremsventilen bei kaltem Wetter zu reduzieren."]},
        {
            "q": "Wenn Ihr LKW doppelte Feststellbremsventile hat, können Sie Druck aus einem separaten Tank verwenden, um:",
            "o": ["Die Federspeicher-Notbremsen zu lösen, um eine kurze Strecke zu fahren.",
                  "Mehr Bremsdruck anzuwenden, wenn der Haupttank zur Neige geht.",
                  "Doppelt so lange mit Ihrem Betriebs-Luftdruck geparkt zu bleiben."]},
        {
            "q": "Um das freie Spiel der manuellen Gestängesteller (Slack Adjusters) an S-Nocken-Bremsen zu überprüfen, sollten Sie parken auf:",
            "o": ["Ebener Fläche mit angezogener Feststellbremse, dann die Betriebsbremse betätigen.",
                  "Ebener Fläche, die Räder blockieren (chock the wheels) und die Feststellbremsen lösen.",
                  "Ebener Fläche und den Luftdruck ablassen, bevor Sie einstellen."]},
        {
            "q": "Von den unten genannten Optionen ist das Erste, was zu tun ist, wenn eine Warnung für niedrigen Luftdruck aufleuchtet:",
            "o": ["So schnell wie möglich anhalten und sicher parken.", "In den nächsthöheren Gang schalten.",
                  "Das Luftversorgungs-Steuerventil öffnen."]},
        {"q": "Der Luftkompressor-Regler (Governor) steuert:",
         "o": ["Wann die Bremskammern den Druck ablassen.", "Den auf die Bremsen angewendeten Luftdruck.",
               "Wann Luft in die Lufttanks gepumpt wird."]},
        {"q": "Die Bremskraft der Federspeicherbremsen:",
         "o": ["Wird nicht durch den Zustand der Betriebsbremsen beeinflusst.",
               "Kann nur von hochqualifiziertem Bremsservicepersonal getestet werden.",
               "Hängt davon ab, ob die Betriebsbremsen richtig eingestellt sind."]},
        {"q": "Alle Fahrzeuge, die mit Druckluftbremsen ausgestattet sind, haben:",
         "o": ["Ein hydraulisches System, falls das Luftsystem ausfällt.",
               "Ein Vorratsdruckmanometer (Supply Pressure Gauge).", "Einen Luftverbrauchsanzeiger."]},
        {"q": "Wenn Sie eine Notbremsung durchführen müssen, bremsen Sie so, dass Sie:",
         "o": ["Die volle Kraft der Bremsen nutzen und sie blockieren.",
               "Lenken können und Ihr Fahrzeug in einer geraden Linie bleibt.", "Zuerst die Handbremse benutzen."]},
        {
            "q": "Wenn Sie keine automatischen Tankablässe haben, wie oft sollten Sie das Öl und Wasser vom Boden der Druckluftspeicherbehälter ablassen?",
            "o": ["Am Ende jedes Fahrtages", "Einmal pro Woche", "Jede zweite Woche"]},
        {"q": "Das Bremsdruckmanometer (Application Pressure Gauge) zeigt an, wie viel Luftdruck Sie:",
         "o": ["Auf dieser Fahrt verbraucht haben.", "In den Lufttanks haben.", "Auf die Bremsen anwenden."]},
        {"q": "Ihre Bremsen lassen nach (fading), wenn:",
         "o": ["Sie das Bremspedal stärker drücken müssen, um Ihre Geschwindigkeit bei einem Gefälle zu kontrollieren.",
               "Das Bremspedal sich schwammig anfühlt, wenn Sie Druck ausüben.",
               "Sie den Druck auf das Bremspedal lösen und die Geschwindigkeit zunimmt."]},
        {"q": "Wenn Ihr Fahrzeug einen Alkohol-Verdampfer hat, sollten Sie jeden Tag bei kaltem Wetter:",
         "o": ["Den Alkoholspiegel prüfen und den Verdampfer bei Bedarf auffüllen.", "Den Alkohol wechseln.",
               "Den Luftfilter mit Alkohol reinigen."]},
        {"q": "Warum sollten Sie Wasser aus Druckluftbehältern ablassen?",
         "o": ["Der niedrige Siedepunkt von Wasser reduziert die Bremskraft.",
               "Wasser kann bei kaltem Wetter gefrieren und zu Bremsversagen führen.",
               "Wasser kühlt den Kompressor zu stark ab."]},
        {
            "q": "Ihr Fahrzeug hat ein Zweikreis-Druckluftbremssystem. Wenn eine Warnung für niedrigen Luftdruck für das sekundäre System aufleuchtet, sollten Sie:",
            "o": ["Das Fahrzeug sicher anhalten und erst weiterfahren, wenn das System repariert ist.",
                  "Ihre Geschwindigkeit reduzieren und das verbleibende System während der Fahrt testen.",
                  "Ihre Geschwindigkeit reduzieren und zur nächsten Werkstatt fahren."]},
        {
            "q": "Während der normalen Fahrt werden Federspeicherbremsen (Spring Brakes) normalerweise zurückgehalten durch:",
            "o": ["Bolzen oder Klemmen.", "Luftdruck.", "Federdruck."]},
        {"q": "Bei Fahrzeugen mit Druckluftbremsen sollte die Feststellbremse verwendet werden:",
         "o": ["So wenig wie möglich.", "Jederzeit, wenn das Fahrzeug geparkt wird.",
               "Um Ihre Geschwindigkeit bei Bergabfahrt zu halten."]},
        {"q": "Not-Stoßbremsen (Emergency stab braking) ist, wenn Sie:",
         "o": ["Fest auf das Bremspedal drücken und das Handventil vollständig betätigen, bis Sie anhalten.",
               "Das Handventil für eine Sekunde betätigen und dann fest auf das Pedal drücken.",
               "So stark wie möglich bremsen, die Bremse lösen, wenn die Räder blockieren, und dann die Bremsen wieder betätigen, wenn die Räder wieder rollen."]},
        {
            "q": "Ein Druckluftbremssystem eines geraden LKWs sollte mit ausgeschaltetem Motor und gelösten Bremsen nicht mehr als ___ psi pro Minute verlieren.",
            "o": ["6", "4", "2"]},
        {
            "q": "Die Luftverlustrate für einen geraden LKW mit ausgeschaltetem Motor und angezogenen Bremsen sollte nicht mehr als:",
            "o": ["1 psi in 30 Sekunden.", "2 psi in 45 Sekunden.", "3 psi in einer Minute."]},
        {"q": "Das Vorratsdruckmanometer (Supply Pressure Gauge) zeigt an, wie viel Druck:",
         "o": ["Sie auf dieser Fahrt verbraucht haben.", "In den Lufttanks ist.",
               "An die Bremskammern gesendet wird."]},
        {
            "q": "Das Bremssystem, das die Bremsen anlegt und löst, wenn der Fahrer das Bremspedal betätigt, ist das ___ Bremssystem.",
            "o": ["Betriebs- (Service)", "Feststell- (Parking)", "Trommel- (Drum)"]},
        {"q": "Warum sollten Sie Wasser aus Druckluftbehältern ablassen?",
         "o": ["Der Siedepunkt reduziert die Bremskraft.",
               "Wasser kann bei kaltem Wetter gefrieren und zu Bremsversagen führen.",
               "Wasser kühlt den Kompressor zu stark ab."]},
        {
            "q": "Der gesamte Bremsweg bei Druckluftbremsen ist länger als bei hydraulischen Bremsen aufgrund der ___ Distanz.",
            "o": ["Wahrnehmungs-", "Reaktions-", "Bremsverzögerungs- (Brake Lag)"]},
        {"q": "Der am häufigsten bei schweren Fahrzeugen verwendete Typ der Betriebsbremse ist die:",
         "o": ["Scheibenbremse.", "Keil-Trommelbremse.", "S-Nocken-Trommelbremse (S-cam drum)."]},
        {
            "q": "Was von den folgenden Faktoren führt dazu, dass der gesamte Bremsweg bei Druckluftbremsen länger ist als bei hydraulischen Bremsen:",
            "o": ["Bremsverzögerung (Brake Lag)", "Wahrnehmungsdistanz", "Reaktionszeit-Distanz"]},
        {"q": "Wenn der Luftkompressor ein Leck entwickelt, was hält die Luft in den Tanks?",
         "o": ["Das Einweg-Rückschlagventil (One-way check valve)", "Das Notfall-Relaisventil",
               "Das Sattelzug-Schutzventil"]}
    ]

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
    antwort_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    print("=" * 60)
    print("      Willkommen zum Interaktiven Druckluftbremsen-Quiz (Teil 2)! 🚌💨")
    print(f"               Es warten {total_fragen} Fragen auf dich.")
    print("=" * 60)
    print("Antworte mit A, B, C oder D.")
    time.sleep(1)

    for i, (frage_en, optionen_en, korrekter_index) in enumerate(fragen_liste, 1):
        original_index = i - 1

        # Deutsche Übersetzung abrufen
        translation = get_german_translation(original_index)
        frage_de = translation['q']
        optionen_de = translation['o']

        # Labels für diese Frage bestimmen (z.B. A, B, C oder A, B, C, D)
        aktuelle_labels = optionen_labels[:len(optionen_en)]
        korrekte_antwort_label = aktuelle_labels[korrekter_index]

        print("\n" + "-" * 60)
        print(f"FRAGE {i} von {total_fragen}:")

        # Frage und Optionen in Deutsch und Englisch anzeigen
        print(f"DE: {frage_de}")
        print(f"EN: {frage_en}")
        print("\nOptionen (DE / EN):")

        # Optionen anzeigen
        for label, opt_de, opt_en in zip(aktuelle_labels, optionen_de, optionen_en):
            print(f"  ({label}) {opt_de} / {opt_en}")

        # Eingabe vom Benutzer anfordern und validieren
        while True:
            user_input = input("\nDeine Antwort (A/B/C/D): ").strip().upper()
            if user_input in aktuelle_labels:
                benutzer_index = antwort_mapping[user_input]
                break
            else:
                print(f"Ungültige Eingabe. Bitte antworte nur mit {', '.join(aktuelle_labels)}.")

        # Antwort prüfen
        if benutzer_index == korrekter_index:
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
        print("\n🎉 Herzlichen Glückwunsch! Du bist sehr gut vorbereitet!")
    elif prozent >= 60:
        print("\n👍 Solide Leistung! Ein bisschen Übung noch, dann passt es.")
    else:
        print("\n🧐 Weiter üben! Wiederhole die Grundlagen der Druckluftbremse.")

    print("=" * 60)


# Start des Skripts
if __name__ == "__main__":
    run_quiz(quiz_fragen_air_brakes_2)