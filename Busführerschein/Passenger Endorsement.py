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

    # Passing score for Passenger Endorsement is often 80% (18/22)
    required_to_pass = int(gesamt_fragen * 0.80)
    print(f"Ergebnis: {richtige_antworten} von {gesamt_fragen} Fragen richtig beantwortet.")
    if richtige_antworten / gesamt_fragen >= 0.8:
        print(f"🎉 **PASS!** (You needed {required_to_pass}/{gesamt_fragen} correct answers) / **BESTANDEN!**")
    else:
        print(
            f"😢 **FAIL.** You need {required_to_pass}/{gesamt_fragen} to pass. Keep practicing. / **NICHT BESTANDEN.**")


# --- Passenger Endorsement Test Fragen (22 Fragen) ---
# Format: (Fragentext EN, Fragentext DE, [Optionen EN], [Optionen DE], Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen_passenger_endorsement = [
    ("Which of the following lists the three types of emergency equipment that you must have on your bus?",
     "Welche der folgenden Listen führt die drei Arten von Notfallausrüstung auf, die Sie in Ihrem Bus mitführen müssen?",
     ["Fire extinguisher, spare electrical fuses unless equipped with circuit breakers and reflectors.",
      "Hydraulic jack, fire extinguisher, signal flares.",
      "Reflectors, fire extinguisher, tire repair kit.",
      "First aid kit, spare electrical fuses unless equipped with circuit breakers, fire extinguisher."],
     ["Feuerlöscher, elektrische Ersatzsicherungen, sofern nicht mit Schutzschaltern ausgestattet, und Reflektoren.",
      "Hydraulischer Wagenheber, Feuerlöscher, Signalflammen.",
      "Reflektoren, Feuerlöscher, Reifenreparaturset.",
      "Erste-Hilfe-Kasten, elektrische Ersatzsicherungen, sofern nicht mit Schutzschaltern ausgestattet, Feuerlöscher."],
     0),
    ("Which of these statements about hazards is true?",
     "Welche dieser Aussagen über Gefahren ist wahr?",
     ["A car with out of state plates is a hazard.",
      "Movement inside a parked car could mean someone is about to step out.",
      "If you can see any part of another vehicle, assume the driver sees you.",
      "All of the above are true."],
     ["Ein Auto mit auswärtigen Kennzeichen ist eine Gefahr.",
      "Bewegung in einem geparkten Auto könnte bedeuten, dass jemand im Begriff ist auszusteigen.",
      "Wenn Sie irgendeinen Teil eines anderen Fahrzeugs sehen können, nehmen Sie an, dass der Fahrer Sie sieht.",
      "Alle der oben genannten sind wahr."],
     1),
    ("During your pre-trip inspection which are some of the items you should be checking for?",
     "Auf welche Punkte sollten Sie bei Ihrer Inspektion vor der Fahrt achten?",
     ["Lights and reflectors.", "Parking brake.", "Service brakes and parking brake.", "All of the above."],
     ["Lichter und Reflektoren.", "Feststellbremse.", "Betriebsbremsen und Feststellbremse.",
      "Alle der oben genannten."],
     3),
    ("If you have riders aboard, you should never fuel your bus:",
     "Wenn Sie Fahrgäste an Bord haben, sollten Sie Ihren Bus niemals tanken:",
     ["In a closed building.", "Without a static chain.", "Without a fire bottle handy.", "With windows open."],
     ["In einem geschlossenen Gebäude.", "Ohne Erdungskette.", "Ohne einen griffbereiten Feuerlöscher.",
      "Bei geöffneten Fenstern."],
     0),
    ("When you inspect your bus, make sure that:",
     "Wenn Sie Ihren Bus inspizieren, stellen Sie sicher, dass:",
     ["Every other handhold and railing is secure.",
      "Rider signaling devices are working.",
      "Emergency exit handles have been removed.",
      "All of the above."],
     ["Jede zweite Haltestange und jedes zweite Geländer gesichert ist.",
      "Fahrgastsignaleinrichtungen funktionieren.",
      "Notausgangsgriffe entfernt wurden.",
      "Alle der oben genannten."],
     1),
    ("When checking the outside of your bus:",
     "Beim Überprüfen der Außenseite Ihres Busses:",
     ["Remember to check frame alignment.",
      "Open storage compartments to allow smells to escape.",
      "Have a rider stand behind to check backup lights.",
      "None of the above."],
     ["Denken Sie daran, die Rahmenausrichtung zu überprüfen.",
      "Öffnen Sie Staufächer, damit Gerüche entweichen können.",
      "Lassen Sie einen Fahrgast dahinter stehen, um die Rückfahrlichter zu überprüfen.",
      "Keines der oben genannten."],
     3),
    ("When should you check your mirrors for a lane change?",
     "Wann sollten Sie Ihre Spiegel für einen Spurwechsel überprüfen?",
     ["After signaling the change.", "Right after starting the lane change.",
      "After completing the lane change.", "At each of the times stated above."],
     ["Nach dem Signalisieren des Wechsels.", "Direkt nach Beginn des Spurwechsels.",
      "Nach Abschluss des Spurwechsels.", "Zu jedem der oben genannten Zeitpunkte."],
     3),
    ("Which of these statements about seeing ahead is true?",
     "Welche dieser Aussagen über das Vorausschauen ist wahr?",
     ["At highway speed, you should look no more than 1/8 mile ahead.",
      "Many drivers do not look far enough ahead.",
      "Good drivers keep attention on one place for 12 to 15 seconds.",
      "All of the above are true."],
     ["Bei Autobahngeschwindigkeit sollten Sie nicht mehr als 1/8 Meile vorausschauen.",
      "Viele Fahrer schauen nicht weit genug voraus.",
      "Gute Fahrer halten die Aufmerksamkeit 12 bis 15 Sekunden lang an einem Ort.",
      "Alle der oben genannten sind wahr."],
     1),
    ("You are driving at night and must dim your headlights from high to low. What should you do with your speed?",
     "Sie fahren nachts und müssen Ihre Scheinwerfer von Fernlicht auf Abblendlicht dimmen. Was sollten Sie mit Ihrer Geschwindigkeit tun?",
     ["Speed up.", "Drop 5 mph until your eyes adjust.", "Slow down.", "Nothing."],
     ["Beschleunigen Sie.", "Reduzieren Sie die Geschwindigkeit um 5 mph, bis sich Ihre Augen angepasst haben.",
      "Verlangsamen Sie.", "Nichts."],
     2),
    ("A bus may carry baggage and freight only if secured so that:",
     "Ein Bus darf Gepäck und Fracht nur dann befördern, wenn es so gesichert ist, dass:",
     ["The driver can move freely.",
      "Any rider can use any door or window in an emergency.",
      "Riders are protected from falling or shifting packages.",
      "All of the above are true."],
     ["Der Fahrer sich frei bewegen kann.",
      "Jeder Fahrgast im Notfall jede Tür oder jedes Fenster benutzen kann.",
      "Fahrgäste vor herabfallenden oder verrutschenden Paketen geschützt sind.",
      "Alle der oben genannten sind wahr."],
     3),
    ("Normally, how many seats that are not securely fastened to the bus are allowed?",
     "Wie viele Sitze, die nicht sicher am Bus befestigt sind, sind normalerweise erlaubt?",
     ["0", "1", "2", "3"],
     ["0", "1", "2", "3"],
     0),
    ("When stopping for a drawbridge, you should stop at least:",
     "Beim Anhalten vor einer Zugbrücke sollten Sie mindestens anhalten:",
     ["50 feet", "25 feet", "30 feet", "At bridge and stop, look and listen."],
     ["50 Fuß", "25 Fuß", "30 Fuß", "An der Brücke anhalten, schauen und zuhören."],
     0),
    ("Why should you double check the crossing before crossing the tracks, even after the train has passed?",
     "Warum sollten Sie den Bahnübergang vor dem Überqueren der Gleise doppelt überprüfen, auch nachdem der Zug vorbeigefahren ist?",
     ["To make sure there is not another train coming.",
      "To look for everyone walking on the tracks.",
      "To look for any loose rails.",
      "All of the above."],
     ["Um sicherzustellen, dass kein weiterer Zug kommt.",
      "Um nach allen Personen zu suchen, die auf den Gleisen gehen.",
      "Um nach lockeren Schienen zu suchen.",
      "Alle der oben genannten."],
     0),
    ("Your bus is disabled. The bus, with riders aboard, may be towed or pushed to a safe spot to discharge passengers only:",
     "Ihr Bus ist fahruntüchtig. Der Bus darf mit Fahrgästen an Bord nur dann zu einem sicheren Ort zum Aussteigen abgeschleppt oder geschoben werden:",
     ["If the distance is less than 1 mile.",
      "By a 27,000 GVWR or larger tow truck.",
      "By another bus with its 4-way flashers on.",
      "If getting off the bus sooner would be unsafe."],
     ["Wenn die Entfernung weniger als 1 Meile beträgt.",
      "Von einem Abschleppwagen mit 27.000 GVWR oder mehr.",
      "Von einem anderen Bus mit eingeschalteter Warnblinkanlage.",
      "Wenn ein früheres Aussteigen aus dem Bus unsicher wäre."],
     3),
    ("You should not let riders stand:",
     "Sie sollten Fahrgäste nicht stehen lassen:",
     ["In front of the standee line.",
      "Between the wheel wells.",
      "Within two feet of an emergency exit.",
      "In front of any open luggage space."],
     ["Vor der Standelinie.",
      "Zwischen den Radkästen.",
      "Innerhalb von zwei Fuß von einem Notausgang.",
      "Vor einem offenen Gepäckraum."],
     0),
    ("Which of these will result in the best control on curves?",
     "Was führt zu der besten Kontrolle in Kurven?",
     ["Slow to a safe speed before entering, then accelerate slightly through.",
      "Maintain constant speed through curves.",
      "Speed up before curves, then brake through.",
      "None of the above."],
     ["Vor dem Einfahren auf eine sichere Geschwindigkeit reduzieren, dann leicht durch die Kurve beschleunigen.",
      "Durch die Kurven eine konstante Geschwindigkeit beibehalten.",
      "Vor den Kurven beschleunigen, dann durch sie hindurch bremsen.",
      "Keines der oben genannten."],
     0),
    ("When you discharge an unruly rider, you should choose a place that is:",
     "Wenn Sie einen widerspenstigen Fahrgast entlassen, sollten Sie einen Ort wählen, der:",
     ["Convenient for you.", "As safe as possible.", "Isolated.", "Near a hospital."],
     ["Für Sie bequem ist.", "So sicher wie möglich ist.", "Isoliert ist.", "In der Nähe eines Krankenhauses ist."],
     1),
    ("Buses may have recapped or regrooved tires:",
     "Busse dürfen runderneuerte oder nachgeschnittene Reifen haben:",
     ["Only when speed < 40 mph.", "Only on the outside of duals.", "Anywhere except the front wheels.",
      "On any or all wheels."],
     ["Nur wenn die Geschwindigkeit < 40 mph ist.", "Nur an der Außenseite der Zwillingsreifen.",
      "Überall außer an den Vorderrädern.", "An allen oder einzelnen Rädern."],
     2),
    ("You may sometimes haul small arms ammunition or emergency hospital supplies on your bus. The total weight of all such hazardous materials must not be more than:",
     "Sie dürfen manchmal Kleinwaffenmunition oder Notfall-Krankenhausbedarf in Ihrem Bus transportieren. Das Gesamtgewicht aller dieser Gefahrstoffe darf nicht mehr als ___ betragen:",
     ["5", "50", "500", "5000"],
     ["5", "50", "500", "5000"],
     2),
    ("If a rider wants to bring a car battery or a can of gasoline aboard your bus, you should:",
     "Wenn ein Fahrgast eine Autobatterie oder einen Kanister Benzin in Ihren Bus mitbringen möchte, sollten Sie:",
     ["Not allow the rider to do it.", "Tell them to sit in the rear.", "Collect an extra fare.",
      "Put it in the cargo compartment."],
     ["Dem Fahrgast dies nicht erlauben.", "Ihm sagen, er solle im hinteren Teil sitzen.",
      "Einen zusätzlichen Fahrpreis verlangen.", "Es in das Gepäckfach legen."],
     0),
    ("Many buses have curved (convex or spot) mirrors. These mirrors:",
     "Viele Busse haben gekrümmte (konvexe oder Spot-) Spiegel. Diese Spiegel:",
     ["Are against the law in some states.",
      "Make things seem smaller and farther away than they really are.",
      "Do not need to be checked often.",
      "All of the above."],
     ["Sind in einigen Staaten gesetzeswidrig.",
      "Lassen Dinge kleiner und weiter entfernt erscheinen, als sie tatsächlich sind.",
      "Müssen nicht oft überprüft werden.",
      "Alle der oben genannten."],
     1),
    ("You are stopped on a divided highway. How many feet apart should you place the triangles to the rear of the bus?",
     "Sie stehen auf einer geteilten Autobahn. Wie viele Fuß voneinander entfernt sollten Sie die Warndreiecke hinter dem Bus platzieren?",
     ["10, 20, & 100", "50, 100, & 200", "10, 100, & 200", "100, 200, & 500"],
     ["10, 20, & 100", "50, 100, & 200", "10, 100, & 200", "100, 200, & 500"],
     2)
]

# Start des zweisprachigen Passenger Endorsement Quiz
if __name__ == "__main__":
    run_bilingual_quiz(quiz_fragen_passenger_endorsement, "Passenger Endorsement Test", "Fahrgastbeförderung Test")