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

    # Passing score for Passenger Transport is often 80% (33/41)
    required_to_pass = int(gesamt_fragen * 0.80)
    print(f"Ergebnis: {richtige_antworten} von {gesamt_fragen} Fragen richtig beantwortet.")
    if richtige_antworten / gesamt_fragen >= 0.8:
        print(f"🎉 **PASS!** (You needed {required_to_pass}/{gesamt_fragen} correct answers) / **BESTANDEN!**")
    else:
        print(
            f"😢 **FAIL.** You need {required_to_pass}/{gesamt_fragen} to pass. Keep practicing. / **NICHT BESTANDEN.**")


# --- Passenger Transport Test Fragen (41 Fragen) ---
# Format: (Fragentext EN, Fragentext DE, [Optionen EN], [Optionen DE], Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen_passenger_transport = [
    ("If your bus has an emergency exit door, it must:",
     "Wenn Ihr Bus eine Notausgangstür hat, muss diese:",
     ["Be closed when operating the bus.", "Always have a red door light on.", "Be free to open for fresh air."],
     ["Beim Betrieb des Busses geschlossen sein.", "Immer ein rotes Türlicht eingeschaltet haben.",
      "Zum Frischlüften geöffnet werden dürfen."],
     0),
    ("Many buses have curved (convex or \"spot\") mirrors. These mirrors:",
     "Viele Busse haben gekrümmte (konvexe oder Spot-) Spiegel. Diese Spiegel:",
     ["Are against the law in some states.", "Make things seem smaller and farther away than they really are.",
      "Do not need to be checked often because they show a larger area."],
     ["Sind in einigen Staaten gesetzeswidrig.",
      "Lassen Dinge kleiner und weiter entfernt erscheinen, als sie tatsächlich sind.",
      "Müssen nicht oft überprüft werden, da sie einen größeren Bereich zeigen."],
     1),
    ("To stop for railroad tracks, a bus driver must stop ___ feet before the nearest track.",
     "Um an Bahngleisen anzuhalten, muss ein Busfahrer ___ Fuß vor dem nächsten Gleis anhalten.",
     ["10 to 25", "15 to 50", "20 to 75"],
     ["10 bis 25", "15 bis 50", "20 bis 75"],
     1),
    ("When you inspect your bus, make sure that:",
     "Wenn Sie Ihren Bus inspizieren, stellen Sie sicher, dass:",
     ["Emergency exit handles have been removed.", "Every other handhold and railing is secure.",
      "Rider signaling devices are working."],
     ["Notausgangsgriffe entfernt wurden.", "Jede zweite Haltestange und jedes zweite Geländer gesichert ist.",
      "Fahrgastsignaleinrichtungen funktionieren."],
     2),
    ("If a rider wants to bring a car battery or a can of gasoline aboard your bus, you should:",
     "Wenn ein Fahrgast eine Autobatterie oder einen Kanister Benzin in Ihren Bus mitbringen möchte, sollten Sie:",
     ["Not allow the rider to do it.", "Collect an extra fare for this type of cargo.",
      "Put the battery or gasoline in the cargo compartment."],
     ["Dem Fahrgast dies nicht erlauben.", "Einen zusätzlichen Fahrpreis für diese Art von Ladung verlangen.",
      "Die Batterie oder das Benzin in das Gepäckfach legen."],
     0),
    ("If there is no traffic light or attendant, stop for a drawbridge about ___ feet away.",
     "Wenn es keine Ampel oder Aufsichtsperson gibt, halten Sie vor einer Zugbrücke etwa ___ Fuß entfernt an.",
     ["25", "50", "100"],
     ["25", "50", "100"],
     1),
    ("A bus must never carry riders:",
     "Ein Bus darf niemals Fahrgäste befördern:",
     ["In the aisle.", "Behind the standee line.", "In front of the standee line."],
     ["Im Gang.", "Hinter der Standelinie.", "Vor der Standelinie."],
     2),
    ("In a bus, you should check to see that the maximum number of riders is displayed:",
     "In einem Bus sollten Sie überprüfen, ob die maximale Anzahl der Fahrgäste angezeigt wird:",
     ["In the back of the bus.", "In the center of the bus.", "On the door frame of the driver's seat."],
     ["Im hinteren Teil des Busses.", "In der Mitte des Busses.", "Am Türrahmen des Fahrersitzes."],
     2),
    ("The maximum weight of a carton or package on a bus is:",
     "Das Höchstgewicht eines Kartons oder Pakets in einem Bus beträgt:",
     ["100 pounds.", "150 pounds.", "200 pounds."],
     ["100 Pfund.", "150 Pfund.", "200 Pfund."],
     0),
    ("Passengers must stand only behind the:",
     "Fahrgäste dürfen nur hinter der/dem ___ stehen:",
     ["Standee line.", "Driver's seat.", "First passenger seat."],
     ["Standelinie.", "Fahrersitz.", "Ersten Fahrgastsitz."],
     0),
    ("You must stop at an open railroad crossing:",
     "Sie müssen an einem offenen Bahnübergang anhalten:",
     ["Only if the tracks are clearly visible.", "Only if passengers signal you to.",
      "If getting off the bus sooner would be unsafe."],
     ["Nur wenn die Gleise klar sichtbar sind.", "Nur wenn Fahrgäste Sie dazu auffordern.",
      "Wenn ein früheres Aussteigen aus dem Bus unsicher wäre."],
     2),
    ("The federally-mandated minimum tread depth for front tires is 4/32 inch. For all other tires, the minimum is 2/32 inch. You should inspect the tread depth:",
     "Die bundesweit vorgeschriebene Mindestprofiltiefe für Vorderreifen beträgt 4/32 Zoll. Für alle anderen Reifen beträgt das Minimum 2/32 Zoll. Sie sollten die Profiltiefe überprüfen:",
     ["Only on the front tires.", "Anywhere except the front wheels.", "Only on the drive axle tires."],
     ["Nur an den Vorderreifen.", "Überall außer an den Vorderrädern.", "Nur an den Antriebsachsreifen."],
     1),
    ("The three required emergency items on a bus are:",
     "Die drei vorgeschriebenen Notfallgegenstände in einem Bus sind:",
     ["Fire extinguisher, spare electric fuses unless equipped with circuit breakers, reflectors",
      "Fire extinguisher, first-aid kit, spare tire", "Spare electric fuses, first-aid kit, reflectors"],
     ["Feuerlöscher, elektrische Ersatzsicherungen, sofern nicht mit Schutzschaltern ausgestattet, Reflektoren",
      "Feuerlöscher, Erste-Hilfe-Kasten, Ersatzreifen",
      "Elektrische Ersatzsicherungen, Erste-Hilfe-Kasten, Reflektoren"],
     0),
    ("You are driving a bus on a two-lane road. You are required to use your four-way flashers or warning lights when the speed limit is ___ mph or less.",
     "Sie fahren einen Bus auf einer zweispurigen Straße. Sie müssen Ihre Warnblinkanlage oder Warnleuchten verwenden, wenn die Geschwindigkeitsbegrenzung ___ mph oder weniger beträgt.",
     ["45", "50", "55"],
     ["45", "50", "55"],
     1),
    ("Buses may not carry:",
     "Busse dürfen Folgendes nicht befördern:",
     ["Small-arms ammunition.", "Irritating materials or tear gas.", "Ammunition in a closed container."],
     ["Kleinwaffenmunition.", "Reizstoffe oder Tränengas.", "Munition in einem geschlossenen Behälter."],
     1),
    ("You are NOT allowed to fuel a bus:",
     "Es ist Ihnen NICHT gestattet, einen Bus zu betanken:",
     ["In a closed building.", "While the bus is running.", "While passengers are loading."],
     ["In einem geschlossenen Gebäude.", "Während der Bus läuft.", "Während Fahrgäste einsteigen."],
     0),
    ("When driving a bus, you should be able to see the air pressure gauge and the:",
     "Beim Fahren eines Busses sollten Sie in der Lage sein, die Luftdruckanzeige und den/die ___ zu sehen:",
     ["Tachometer.", "Odometer.", "Speedometer."],
     ["Drehzahlmesser (Tachometer).", "Wegstreckenzähler (Odometer).", "Geschwindigkeitsmesser (Speedometer)."],
     2),
    ("When loading baggage, be sure to load it:",
     "Beim Verladen von Gepäck sollten Sie darauf achten, es zu verladen:",
     ["By distributing the weight to the rear axle.", "As safe as possible.", "As high as possible."],
     ["Durch Gewichtsverteilung auf die Hinterachse.", "So sicher wie möglich.", "So hoch wie möglich."],
     1),
    ("When driving a bus through a curve, you should:",
     "Beim Fahren eines Busses durch eine Kurve sollten Sie:",
     ["Slow to a safe speed before entering curves, then accelerate slightly through them.",
      "Start applying the brakes in the curve.", "Avoid accelerating through curves."],
     ["Vor dem Einfahren in die Kurven auf eine sichere Geschwindigkeit reduzieren, dann leicht durch sie hindurch beschleunigen.",
      "Beginnen, in der Kurve zu bremsen.", "Vermeiden, durch Kurven zu beschleunigen."],
     0),
    ("The maximum number of times you should pump the brake pedal when doing a stop:",
     "Die maximale Anzahl von Malen, die Sie das Bremspedal beim Anhalten pumpen sollten:",
     ["0 (zero)", "1", "2"],
     ["0 (null)", "1", "2"],
     0),
    ("What is the maximum number of times you should shift gears when doing a stop:",
     "Wie oft sollten Sie maximal schalten, wenn Sie anhalten:",
     ["0 (zero)", "1", "2"],
     ["0 (null)", "1", "2"],
     0),
    ("Which of the following is correct regarding speed and stopping distance:",
     "Welche der folgenden Aussagen ist richtig in Bezug auf Geschwindigkeit und Anhalteweg:",
     ["You need about twice as much stopping distance at 40 mph as at 20 mph.",
      "You need about three times as much stopping distance at 40 mph as at 20 mph.",
      "You need about four times as much stopping distance at 40 mph as at 20 mph."],
     ["Sie benötigen etwa doppelt so viel Anhalteweg bei 40 mph wie bei 20 mph.",
      "Sie benötigen etwa dreimal so viel Anhalteweg bei 40 mph wie bei 20 mph.",
      "Sie benötigen etwa viermal so viel Anhalteweg bei 40 mph wie bei 20 mph."],
     2),
    ("The maximum height of a package on the rack is:",
     "Die maximale Höhe eines Pakets auf der Gepäckablage beträgt:",
     ["15 inches.", "18 inches.", "24 inches."],
     ["15 Zoll.", "18 Zoll.", "24 Zoll."],
     1),
    ("You must stop at all railroad crossings. You must not drive again until you can see clearly in both directions, and the bus:",
     "Sie müssen an allen Bahnübergängen anhalten. Sie dürfen erst wieder fahren, wenn Sie in beide Richtungen klar sehen können und der Bus:",
     ["Has all doors closed.", "Has shifted to a higher gear.", "Is running at high idle."],
     ["Alle Türen geschlossen hat.", "In einen höheren Gang geschaltet hat.", "Im hohen Leerlauf läuft."],
     0),
    ("Most brake systems are designed to operate at ___ psi.",
     "Die meisten Bremssysteme sind darauf ausgelegt, bei ___ psi zu arbeiten.",
     ["80", "90", "100"],
     ["80", "90", "100"],
     2),
    ("If a bus is equipped with a lift, it must be inspected:",
     "Wenn ein Bus mit einem Lift ausgestattet ist, muss dieser inspiziert werden:",
     ["Daily.", "Weekly.", "Monthly."],
     ["Täglich.", "Wöchentlich.", "Monatlich."],
     0),
    ("If you have a brake failure on a bus, you should:",
     "Wenn Sie einen Bremsausfall an einem Bus haben, sollten Sie:",
     ["Pump the brakes repeatedly to build air pressure.", "Shift to a lower gear.", "Accelerate to maintain speed."],
     ["Die Bremsen wiederholt pumpen, um Luftdruck aufzubauen.", "In einen niedrigeren Gang schalten.",
      "Beschleunigen, um die Geschwindigkeit aufrechtzuerhalten."],
     1),
    ("The purpose of the brake interlock is to:",
     "Der Zweck der Bremsverriegelung (Brake Interlock) ist es:",
     ["Prevent the bus from moving when the lift is in use.",
      "Ensure the parking brake is set before the lift is used.", "Both of the above."],
     ["Zu verhindern, dass sich der Bus bewegt, wenn der Lift in Gebrauch ist.",
      "Sicherzustellen, dass die Feststellbremse angezogen ist, bevor der Lift benutzt wird.", "Beides ist richtig."],
     2),
    ("How often should you check the air pressure in your tires:",
     "Wie oft sollten Sie den Luftdruck in Ihren Reifen überprüfen:",
     ["Every day.", "Every week.", "Before every trip."],
     ["Jeden Tag.", "Jede Woche.", "Vor jeder Fahrt."],
     2),
    ("When driving a bus, you should look ahead at least ___ seconds.",
     "Beim Fahren eines Busses sollten Sie mindestens ___ Sekunden vorausschauen.",
     ["5 to 10", "12 to 15", "15 to 20"],
     ["5 bis 10", "12 bis 15", "15 bis 20"],
     1),
    ("When should you check the fluid levels under the hood:",
     "Wann sollten Sie die Flüssigkeitsstände unter der Motorhaube überprüfen:",
     ["Every day.", "Before every trip.", "Every 100 miles."],
     ["Jeden Tag.", "Vor jeder Fahrt.", "Alle 100 Meilen."],
     1),
    ("If you are driving a bus and another vehicle is tailgating you, what should you do:",
     "Wenn Sie einen Bus fahren und ein anderes Fahrzeug fährt Ihnen dicht auf, was sollten Sie tun:",
     ["Increase your speed and try to pull away from them.", "Slow down to encourage them to pass.",
      "Increase your following distance."],
     ["Ihre Geschwindigkeit erhöhen und versuchen, sich von ihnen zu entfernen.",
      "Langsamer werden, um sie zum Überholen zu ermutigen.", "Ihren Sicherheitsabstand vergrößern."],
     2),
    ("What is the maximum number of times you should check the vehicle's engine oil level:",
     "Wie oft sollten Sie maximal den Motorölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's brake fluid level:",
     "Wie oft sollten Sie maximal den Bremsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     2),
    ("What is the maximum number of times you should check the vehicle's power steering fluid level:",
     "Wie oft sollten Sie maximal den Servolenkungsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's windshield washer fluid level:",
     "Wie oft sollten Sie maximal den Scheibenwischerflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's clutch fluid level:",
     "Wie oft sollten Sie maximal den Kupplungsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's transmission fluid level:",
     "Wie oft sollten Sie maximal den Getriebeölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's differential fluid level:",
     "Wie oft sollten Sie maximal den Differentialölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's engine oil:",
     "Wie oft sollten Sie maximal das Motoröl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    ("What is the maximum number of times you should check the vehicle's brake fluid:",
     "Wie oft sollten Sie maximal die Bremsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0)
]

# Start des zweisprachigen Passenger Transport Quiz
if __name__ == "__main__":
    run_bilingual_quiz(quiz_fragen_passenger_transport, "Passenger Transport Test (Extended)",
                       "Personenbeförderung Test (Erweitert)")