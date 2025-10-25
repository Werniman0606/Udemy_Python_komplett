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
            elif benutzer_eingabe == 'EXIT':
                print("\nQuiz vorzeitig beendet.")
                print("-" * 80)
                print(f"Result: {i - 1} questions answered, {falsche_antworten} wrong.")
                return
            else:
                print(f"Invalid input. Please enter {', '.join(aktuelle_labels)} or 'EXIT'.")

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

    # Passing score for General Knowledge is often 80% (80/100)
    required_to_pass = int(gesamt_fragen * 0.80)
    print(f"Ergebnis: {richtige_antworten} von {gesamt_fragen} Fragen richtig beantwortet.")
    if richtige_antworten / gesamt_fragen >= 0.8:
        print(f"🎉 **PASS!** (You needed {required_to_pass}/{gesamt_fragen} correct answers) / **BESTANDEN!**")
    else:
        print(
            f"😢 **FAIL.** You need {required_to_pass}/{gesamt_fragen} to pass. Keep practicing. / **NICHT BESTANDEN.**")


# --- CDL General Knowledge Test Fragen (100 Fragen) ---
# Format: (Fragentext EN, Fragentext DE, [Optionen EN], [Optionen DE], Korrekte Antwort-Index (0=A, 1=B, 2=C, 3=D))
quiz_fragen_general_knowledge_bilingual = [
    # Frage 1 (Antwort: B)
    ("You are traveling down a long, steep hill. Your brakes get so hot that they fail. What should you do?",
     "Sie fahren einen langen, steilen Hügel hinunter. Ihre Bremsen werden so heiß, dass sie ausfallen. Was sollten Sie tun?",
     ["Downshift and pump the brake pedal.", "Look for an escape ramp or escape route.", "Both of the above."],
     ["Herunterschalten und das Bremspedal pumpen.", "Nach einer Notfallspur oder einem Fluchtweg suchen.",
      "Beides ist richtig."],
     1),
    # Frage 2 (Antwort: B)
    ("The center of gravity of a load:",
     "Der Schwerpunkt einer Ladung:",
     ["Should be kept as high as possible.", "Can make a vehicle more likely to tip over on curves if it is high.",
      "Is only a problem if the vehicle is overloaded."],
     ["Sollte so hoch wie möglich gehalten werden.",
      "Kann ein Fahrzeug anfälliger dafür machen, in Kurven umzukippen, wenn er hoch ist.",
      "Ist nur ein Problem, wenn das Fahrzeug überladen ist."],
     1),
    # Frage 3 (Antwort: A)
    ("To prevent a load from shifting, there should be at least one tiedown for every ___ feet of cargo.",
     "Um eine Verschiebung der Ladung zu verhindern, sollte es mindestens eine Zurrung für alle ___ Fuß Ladung geben.",
     ["10", "15", "20"],
     ["10", "15", "20"],
     0),
    # Frage 4 (Antwort: C)
    ("What is the proper way to hold a steering wheel?",
     "Was ist die richtige Art, ein Lenkrad zu halten?",
     ["With both hands close together, near the top of the wheel",
      "With both hands close together, near the bottom of the wheel",
      "With your hands placed on opposite sides of the wheel"],
     ["Mit beiden Händen nah beieinander, nahe der Oberseite des Lenkrads",
      "Mit beiden Händen nah beieinander, nahe der Unterseite des Lenkrads",
      "Mit den Händen auf gegenüberliegenden Seiten des Lenkrads platziert"],
     2),
    # Frage 5 (Antwort: B)
    ("You are driving a 40-foot vehicle at 35 mph. The road is dry, and visibility is good. What is the least amount of space you should keep in front of your vehicle to be safe?",
     "Sie fahren ein 40-Fuß-Fahrzeug mit 35 mph. Die Straße ist trocken und die Sicht ist gut. Wie viel Platz sollten Sie mindestens vor Ihrem Fahrzeug lassen, um sicher zu sein?",
     ["2 seconds", "4 seconds", "6 seconds"],
     ["2 Sekunden", "4 Sekunden", "6 Sekunden"],
     1),
    # Frage 6 (Antwort: A)
    ("Which of these statements about backing is true?",
     "Welche dieser Aussagen über das Rückwärtsfahren ist wahr?",
     ["You should back and turn toward the driver's side whenever possible.",
      "You should use a helper and communicate with hand signals.",
      "You should back and turn toward the passenger's side whenever possible."],
     ["Sie sollten nach Möglichkeit immer zur Fahrerseite hin rückwärts fahren und lenken.",
      "Sie sollten einen Helfer verwenden und mit Handzeichen kommunizieren.",
      "Sie sollten nach Möglichkeit immer zur Beifahrerseite hin rückwärts fahren und lenken."],
     0),
    # Frage 7 (Antwort: C)
    ("If your commercial motor vehicle has an automatic transmission, you should:",
     "Wenn Ihr Nutzfahrzeug ein Automatikgetriebe hat, sollten Sie:",
     ["Select a lower range before descending a hill.", "Use the highest gear you can to save fuel.",
      "Select the proper gear before starting down a hill."],
     ["Einen niedrigeren Bereich wählen, bevor Sie einen Hügel hinunterfahren.",
      "Den höchstmöglichen Gang verwenden, um Kraftstoff zu sparen.",
      "Den geeigneten Gang wählen, bevor Sie einen Hügel hinunterfahren."],
     2),
    # Frage 8 (Antwort: C)
    ("Why should you avoid letting air out of hot tires?",
     "Warum sollten Sie vermeiden, Luft aus heißen Reifen abzulassen?",
     ["The tires will be underinflated when they cool off.", "It is a waste of time and air.",
      "The tires will heat up even more later."],
     ["Die Reifen werden unterinflatiert sein, wenn sie abkühlen.", "Es ist eine Verschwendung von Zeit und Luft.",
      "Die Reifen werden später noch mehr aufheizen."],
     2),
    # Frage 9 (Antwort: C)
    ("When stopped on a one-way or divided highway, where should you place your reflective triangles?",
     "Wenn Sie auf einer Einbahnstraße oder einer geteilten Autobahn anhalten, wo sollten Sie Ihre Warndreiecke platzieren?",
     ["Within 50 feet and 100 feet of the vehicle.", "Within 100 feet and 200 feet of the vehicle.",
      "10 feet, 100 feet, and 200 feet toward the approaching traffic."],
     ["Innerhalb von 50 Fuß und 100 Fuß vom Fahrzeug.", "Innerhalb von 100 Fuß und 200 Fuß vom Fahrzeug.",
      "10 Fuß, 100 Fuß und 200 Fuß in Richtung des sich nähernden Verkehrs."],
     2),
    # Frage 10 (Antwort: B)
    ("Which of these is most likely to cause the driver to fail a pre-trip inspection?",
     "Welches der folgenden Dinge führt am ehesten dazu, dass der Fahrer eine Vorabinspektion nicht besteht?",
     ["Unevenly sized tires.", "A broken turn signal.", "Steering wheel is tilted too far back."],
     ["Ungleich große Reifen.", "Ein defekter Blinker.", "Lenkrad ist zu weit nach hinten geneigt."],
     1),
    # Frage 11 (Antwort: C)
    ("Which of these is true about downshifting?",
     "Welche dieser Aussagen über das Herunterschalten ist wahr?",
     ["Downshift whenever you need to save fuel.", "Downshift only when you are in a higher gear.",
      "Downshift before starting down a hill."],
     ["Immer herunterschalten, wenn Sie Kraftstoff sparen müssen.",
      "Nur herunterschalten, wenn Sie sich in einem höheren Gang befinden.",
      "Herunterschalten, bevor Sie einen Hügel hinunterfahren."],
     2),
    # Frage 12 (Antwort: B)
    ("Which of these is most likely to happen if a tire fails on a moving vehicle?",
     "Welches der folgenden Dinge passiert am wahrscheinlichsten, wenn ein Reifen an einem fahrenden Fahrzeug versagt?",
     ["Loss of air pressure and a soft pull to the side.", "You may feel a bump or hear a loud noise.",
      "Your vehicle will pull sharply toward the direction of the tire failure."],
     ["Verlust von Luftdruck und ein leichtes Ziehen zur Seite.",
      "Sie spüren möglicherweise einen Stoß oder hören ein lautes Geräusch.",
      "Ihr Fahrzeug zieht stark in die Richtung des Reifenversagens."],
     1),
    # Frage 13 (Antwort: B)
    ("Which of these lights are required on a CMV?",
     "Welche dieser Lichter sind an einem Nutzfahrzeug (CMV) vorgeschrieben?",
     ["Emergency flashers.", "Reflectors.", "A dash light showing when the battery is low."],
     ["Warnblinkanlage.", "Reflektoren.", "Eine Armaturenbrettlampe, die anzeigt, wenn die Batterie schwach ist."],
     1),
    # Frage 14 (Antwort: B)
    ("You are checking your steering system. You find play in the steering wheel of more than 10 degrees. This:",
     "Sie überprüfen Ihr Lenksystem. Sie stellen fest, dass das Lenkradspiel mehr als 10 Grad beträgt. Dies:",
     ["Is normal and acceptable.", "Is too much, and you must have it fixed.",
      "Should be written up in your vehicle inspection report, but is not dangerous."],
     ["Ist normal und akzeptabel.", "Ist zu viel und muss repariert werden.",
      "Sollte in Ihrem Fahrzeuginspektionsbericht aufgeführt werden, ist aber nicht gefährlich."],
     1),
    # Frage 15 (Antwort: C)
    ("Which of these should be done to prevent an emergency speed-up or runaway vehicle?",
     "Welches der folgenden Dinge sollte getan werden, um ein Notfall-Beschleunigen oder ein durchgehendes Fahrzeug zu verhindern?",
     ["Keep the vehicle in the highest gear possible.", "Ensure that your vehicle is not overloaded.",
      "Know the speed and weight of the vehicle and the grade of the hill."],
     ["Das Fahrzeug im höchstmöglichen Gang halten.", "Sicherstellen, dass Ihr Fahrzeug nicht überladen ist.",
      "Die Geschwindigkeit und das Gewicht des Fahrzeugs sowie das Gefälle des Hügels kennen."],
     2),
    # Frage 16 (Antwort: C)
    ("When should you check the load in your vehicle?",
     "Wann sollten Sie die Ladung in Ihrem Fahrzeug überprüfen?",
     ["Before starting the trip and when pulling into a rest area or inspection station.",
      "Within 50 miles of the start of the trip.", "Both of the above."],
     ["Vor Beginn der Fahrt und beim Anhalten an einem Rastplatz oder einer Inspektionsstelle.",
      "Innerhalb von 50 Meilen nach Beginn der Fahrt.", "Beides ist richtig."],
     2),
    # Frage 17 (Antwort: B)
    ("Which of these statements about winter driving is true?",
     "Welche dieser Aussagen über das Fahren im Winter ist wahr?",
     ["You should increase your following distance by 10 times in winter conditions.",
      "You should use extra caution on bridges and in shady areas.",
      "The heaviest accumulation of ice on the roadway will be in the center of the lane."],
     ["Sie sollten Ihren Sicherheitsabstand bei winterlichen Bedingungen um das 10-fache erhöhen.",
      "Sie sollten auf Brücken und in schattigen Bereichen besonders vorsichtig sein.",
      "Die stärkste Eisansammlung auf der Fahrbahn befindet sich in der Mitte der Spur."],
     1),
    # Frage 18 (Antwort: B)
    ("Which of these statements about tires is true?",
     "Welche dieser Aussagen über Reifen ist wahr?",
     ["Tires should be cross-matched with size.", "The driver should measure tread depth.",
      "Tires should be mixed for better grip."],
     ["Reifen sollten kreuzweise nach Größe abgeglichen werden.", "Der Fahrer sollte die Profiltiefe messen.",
      "Reifen sollten für besseren Grip gemischt werden."],
     1),
    # Frage 19 (Antwort: A)
    ("Which of these is a good rule to follow when using a fire extinguisher?",
     "Welche dieser Regeln ist eine gute Regel bei der Verwendung eines Feuerlöschers?",
     ["Aim at the base of the fire.", "Aim at the top of the fire.", "Aim at the middle of the fire."],
     ["Auf den Boden des Feuers zielen.", "Auf die Spitze des Feuers zielen.", "Auf die Mitte des Feuers zielen."],
     0),
    # Frage 20 (Antwort: C)
    ("Which of these statements about hazard lights (four-way flashers) is true?",
     "Welche dieser Aussagen über Warnblinkanlagen (vierfach Blinker) ist wahr?",
     ["They should be used when driving in heavy fog.", "You should use them to warn others of a breakdown.",
      "You should only use them when the vehicle is stopped or disabled."],
     ["Sie sollten beim Fahren bei starkem Nebel verwendet werden.",
      "Sie sollten sie verwenden, um andere vor einer Panne zu warnen.",
      "Sie sollten sie nur verwenden, wenn das Fahrzeug angehalten oder behindert ist."],
     2),
    # Frage 21 (Antwort: C)
    ("If you are driving a tank vehicle, which is a major danger to consider:",
     "Wenn Sie ein Tankfahrzeug fahren, welche ist eine große Gefahr, die zu beachten ist:",
     ["Vehicle length.", "Vehicle width.", "Sloshing of the liquid inside."],
     ["Fahrzeuglänge.", "Fahrzeugbreite.", "Schwappen der Flüssigkeit im Inneren."],
     2),
    # Frage 22 (Antwort: B)
    ("What is the first thing you should do if you become sleepy while driving?",
     "Was ist das Erste, was Sie tun sollten, wenn Sie während der Fahrt schläfrig werden?",
     ["Drink coffee or an energy drink.", "Pull off the road and take a nap.", "Turn the radio up loud."],
     ["Kaffee oder ein Energy-Drink trinken.", "Von der Straße fahren und ein Nickerchen machen.",
      "Das Radio laut aufdrehen."],
     1),
    # Frage 23 (Antwort: A)
    ("What is the most important factor in steering a vehicle?",
     "Was ist der wichtigste Faktor beim Lenken eines Fahrzeugs?",
     ["Speed.", "Vehicle weight.", "Vehicle length."],
     ["Geschwindigkeit.", "Fahrzeuggewicht.", "Fahrzeuglänge."],
     0),
    # Frage 24 (Antwort: A)
    ("If you are being tailgated, you should:",
     "Wenn Ihnen dicht aufgefahren wird, sollten Sie:",
     ["Increase your following distance.", "Decrease your following distance.", "Drive faster."],
     ["Ihren Sicherheitsabstand vergrößern.", "Ihren Sicherheitsabstand verringern.", "Schneller fahren."],
     0),
    # Frage 25 (Antwort: C)
    ("What should you do when driving in slippery conditions:",
     "Was sollten Sie beim Fahren auf rutschigen Bedingungen tun:",
     ["Drive faster and keep the same amount of space.", "Drive slower and use your brakes more.",
      "Drive slower and allow for more space."],
     ["Schneller fahren und den gleichen Abstand halten.", "Langsamer fahren und Ihre Bremsen mehr benutzen.",
      "Langsamer fahren und mehr Platz lassen."],
     2),
    # Frage 26 (Antwort: A)
    ("What is the best way to handle a hazard when driving:",
     "Was ist der beste Weg, mit einer Gefahr beim Fahren umzugehen:",
     ["See it in advance and respond with proper time.", "Steer around it.", "Stop before it."],
     ["Sie im Voraus erkennen und mit angemessener Zeit reagieren.", "Um sie herumlenken.", "Vor ihr anhalten."],
     0),
    # Frage 27 (Antwort: C)
    ("You should check the vehicle's engine oil level:",
     "Sie sollten den Motorölstand des Fahrzeugs überprüfen:",
     ["At every stop.", "Every 100 miles.", "Before every trip."],
     ["Bei jedem Halt.", "Alle 100 Meilen.", "Vor jeder Fahrt."],
     2),
    # Frage 28 (Antwort: C)
    ("What is the best way to check for leaks under the hood:",
     "Was ist der beste Weg, um nach Lecks unter der Motorhaube zu suchen:",
     ["By checking the hoses.", "By checking the fluid levels.", "By checking the ground."],
     ["Durch Überprüfen der Schläuche.", "Durch Überprüfen der Flüssigkeitsstände.", "Durch Überprüfen des Bodens."],
     2),
    # Frage 29 (Antwort: B)
    ("What is the most important reason for driving defensively:",
     "Was ist der wichtigste Grund für defensives Fahren:",
     ["To avoid being penalized for a major defect.", "To save money.", "To save lives."],
     ["Um eine Strafe wegen eines größeren Mangels zu vermeiden.", "Um Geld zu sparen.", "Um Leben zu retten."],
     1),
    # Frage 30 (Antwort: B)
    ("If you are driving and you see that your vehicle has a small fire, what should you do:",
     "Wenn Sie fahren und sehen, dass Ihr Fahrzeug ein kleines Feuer hat, was sollten Sie tun:",
     ["Drive to the nearest fire station.",
      "Pull over to the side of the road, shut off the engine, and try to put it out.",
      "Pull over to the side of the road and call 911."],
     ["Zur nächsten Feuerwache fahren.",
      "An den Straßenrand fahren, den Motor ausschalten und versuchen, es zu löschen.",
      "An den Straßenrand fahren und 911 anrufen."],
     1),
    # Frage 31 (Antwort: A)
    ("When using your mirrors, you should:",
     "Bei der Verwendung Ihrer Spiegel sollten Sie:",
     ["Check them frequently to observe the traffic around you.", "Only check them before changing lanes.",
      "Check them frequently, and always check your blind spots."],
     ["Sie häufig überprüfen, um den Verkehr um Sie herum zu beobachten.", "Sie nur vor dem Spurwechsel überprüfen.",
      "Sie häufig überprüfen und immer Ihre toten Winkel überprüfen."],
     0),
    # Frage 32 (Antwort: B)
    ("If you are driving and a vehicle starts to pass you, you should:",
     "Wenn Sie fahren und ein Fahrzeug beginnt, Sie zu überholen, sollten Sie:",
     ["Speed up to prevent them from passing.", "Slow down slightly to help them pass.",
      "Drive in the middle of the road."],
     ["Beschleunigen, um sie am Überholen zu hindern.", "Leicht langsamer werden, um ihnen beim Überholen zu helfen.",
      "In der Mitte der Straße fahren."],
     1),
    # Frage 33 (Antwort: A)
    ("What is the first thing you should do if you have a blow out:",
     "Was ist das Erste, was Sie tun sollten, wenn Sie einen Reifenplatzer haben:",
     ["Hold the steering wheel firmly.", "Brake hard.", "Accelerate slowly."],
     ["Das Lenkrad festhalten.", "Stark bremsen.", "Langsam beschleunigen."],
     0),
    # Frage 34 (Antwort: B)
    ("When driving in heavy rain, what is the best way to avoid hydroplaning:",
     "Beim Fahren bei starkem Regen, was ist der beste Weg, um Aquaplaning zu vermeiden:",
     ["Drive fast.", "Drive slower and in the tracks of the vehicle in front of you.",
      "Drive faster and in the middle of the road."],
     ["Schnell fahren.", "Langsamer fahren und in den Spuren des vorausfahrenden Fahrzeugs fahren.",
      "Schneller fahren und in der Mitte der Straße fahren."],
     1),
    # Frage 35 (Antwort: B)
    ("How long will it take for the traffic behind you to react to your vehicle stopping:",
     "Wie lange dauert es, bis der Verkehr hinter Ihnen auf das Anhalten Ihres Fahrzeugs reagiert:",
     ["1 second.", "About 4 seconds.", "About 6 seconds."],
     ["1 Sekunde.", "Ungefähr 4 Sekunden.", "Ungefähr 6 Sekunden."],
     1),
    # Frage 36 (Antwort: B)
    ("What is the maximum height, in feet, of a commercial motor vehicle:",
     "Was ist die maximale Höhe, in Fuß, eines Nutzfahrzeugs:",
     ["12 feet.", "13 feet, 6 inches.", "15 feet."],
     ["12 Fuß.", "13 Fuß, 6 Zoll.", "15 Fuß."],
     1),
    # Frage 37 (Antwort: B)
    ("What is the maximum width, in feet, of a commercial motor vehicle:",
     "Was ist die maximale Breite, in Fuß, eines Nutzfahrzeugs:",
     ["8 feet.", "8 feet, 6 inches.", "10 feet."],
     ["8 Fuß.", "8 Fuß, 6 Zoll.", "10 Fuß."],
     1),
    # Frage 38 (Antwort: C)
    ("What is the maximum length, in feet, of a commercial motor vehicle:",
     "Was ist die maximale Länge, in Fuß, eines Nutzfahrzeugs:",
     ["40 feet.", "45 feet.", "65 feet."],
     ["40 Fuß.", "45 Fuß.", "65 Fuß."],
     2),
    # Frage 39 (Antwort: A)
    ("What is the maximum number of times you should pump the brake pedal when doing a stop:",
     "Wie oft sollten Sie maximal das Bremspedal pumpen, wenn Sie anhalten:",
     ["1", "2", "3"],
     ["1", "2", "3"],
     0),
    # Frage 40 (Antwort: A)
    ("What is the maximum number of times you should shift gears when doing a stop:",
     "Wie oft sollten Sie maximal schalten, wenn Sie anhalten:",
     ["1", "2", "3"],
     ["1", "2", "3"],
     0),
    # Frage 41 (Antwort: B)
    ("The purpose of the engine coolant temperature gauge is to:",
     "Der Zweck der Kühlmitteltemperaturanzeige des Motors ist es:",
     ["Show you the temperature of the oil.", "Show you the temperature of the engine.",
      "Show you the temperature of the radiator."],
     ["Ihnen die Temperatur des Öls anzuzeigen.", "Ihnen die Temperatur des Motors anzuzeigen.",
      "Ihnen die Temperatur des Kühlers anzuzeigen."],
     1),
    # Frage 42 (Antwort: A)
    ("You should check the vehicle's electrical connections:",
     "Sie sollten die elektrischen Anschlüsse des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 43 (Antwort: A)
    ("What is the purpose of the oil pressure gauge:",
     "Was ist der Zweck der Öldruckanzeige:",
     ["To show you the pressure of the oil.", "To show you the level of the oil.",
      "To show you the temperature of the oil."],
     ["Ihnen den Druck des Öls anzuzeigen.", "Ihnen den Stand des Öls anzuzeigen.",
      "Ihnen die Temperatur des Öls anzuzeigen."],
     0),
    # Frage 44 (Antwort: A)
    ("When should you check the fluid levels under the hood:",
     "Wann sollten Sie die Flüssigkeitsstände unter der Motorhaube überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 45 (Antwort: A)
    ("What is the purpose of the speedometer:",
     "Was ist der Zweck des Tachometers:",
     ["To show you the speed of the vehicle.", "To show you the distance traveled.", "To show you the engine speed."],
     ["Ihnen die Geschwindigkeit des Fahrzeugs anzuzeigen.", "Ihnen die zurückgelegte Strecke anzuzeigen.",
      "Ihnen die Motordrehzahl anzuzeigen."],
     0),
    # Frage 46 (Antwort: A)
    ("You should check the vehicle's horn:",
     "Sie sollten die Hupe des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 47 (Antwort: C)
    ("What is the most important reason for driving safely:",
     "Was ist der wichtigste Grund für sicheres Fahren:",
     ["To save money.", "To avoid traffic tickets.", "To save lives."],
     ["Um Geld zu sparen.", "Um Strafzettel zu vermeiden.", "Um Leben zu retten."],
     2),
    # Frage 48 (Antwort: C)
    ("What is the best way to handle a hazard when driving:",
     "Was ist der beste Weg, mit einer Gefahr beim Fahren umzugehen:",
     ["Brake hard.", "Steer around it.", "See it in advance and respond with proper time."],
     ["Stark bremsen.", "Um sie herumlenken.", "Sie im Voraus erkennen und mit angemessener Zeit reagieren."],
     2),
    # Frage 49 (Antwort: C)
    ("What is the best way to avoid a crash:",
     "Was ist der beste Weg, um einen Unfall zu vermeiden:",
     ["Drive faster.", "Drive slower.", "See hazards in advance and respond with proper time."],
     ["Schneller fahren.", "Langsamer fahren.", "Gefahren im Voraus erkennen und mit angemessener Zeit reagieren."],
     2),
    # Frage 50 (Antwort: A)
    ("What is the best way to avoid a rear-end crash:",
     "Was ist der beste Weg, um einen Auffahrunfall zu vermeiden:",
     ["Increase your following distance.", "Drive faster.", "Brake harder."],
     ["Ihren Sicherheitsabstand vergrößern.", "Schneller fahren.", "Stärker bremsen."],
     0),
    # Frage 51 (Antwort: C)
    ("What is the maximum number of times you should check your mirrors when driving:",
     "Wie oft sollten Sie maximal Ihre Spiegel während der Fahrt überprüfen:",
     ["Once a minute.", "Every 10 seconds.", "Every 5 seconds."],
     ["Einmal pro Minute.", "Alle 10 Sekunden.", "Alle 5 Sekunden."],
     2),
    # Frage 52 (Antwort: B)
    ("What is the best way to avoid a head-on crash:",
     "Was ist der beste Weg, um einen Frontalzusammenstoß zu vermeiden:",
     ["Steer to the left.", "Steer to the right.", "Steer to the middle."],
     ["Nach links lenken.", "Nach rechts lenken.", "Zur Mitte lenken."],
     1),
    # Frage 53 (Antwort: C)
    ("What is the best way to avoid a side-swipe crash:",
     "Was ist der beste Weg, um einen Streifkollision zu vermeiden:",
     ["Steer to the left.", "Steer to the right.", "Check your mirrors frequently and use your turn signals."],
     ["Nach links lenken.", "Nach rechts lenken.", "Ihre Spiegel häufig überprüfen und Ihre Blinker verwenden."],
     2),
    # Frage 54 (Antwort: C)
    ("What is the maximum number of times you should check your blind spots:",
     "Wie oft sollten Sie maximal Ihre toten Winkel überprüfen:",
     ["Once a minute.", "Every 10 seconds.", "Every time you change lanes."],
     ["Einmal pro Minute.", "Alle 10 Sekunden.", "Jedes Mal, wenn Sie die Spur wechseln."],
     2),
    # Frage 55 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's engine oil:",
     "Wie oft sollten Sie maximal das Motoröl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 56 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's tires:",
     "Wie oft sollten Sie maximal die Reifen des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 57 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's lights:",
     "Wie oft sollten Sie maximal die Beleuchtung des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 58 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's horn:",
     "Wie oft sollten Sie maximal die Hupe des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 59 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's wipers:",
     "Wie oft sollten Sie maximal die Scheibenwischer des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 60 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's steering:",
     "Wie oft sollten Sie maximal die Lenkung des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 61 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's suspension:",
     "Wie oft sollten Sie maximal die Federung des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 62 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's exhaust:",
     "Wie oft sollten Sie maximal den Auspuff des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 63 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's fuel level:",
     "Wie oft sollten Sie maximal den Kraftstoffstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 64 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's air pressure:",
     "Wie oft sollten Sie maximal den Luftdruck des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 65 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's cargo:",
     "Wie oft sollten Sie maximal die Ladung des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 66 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's mirrors:",
     "Wie oft sollten Sie maximal die Spiegel des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 67 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's electrical connections:",
     "Wie oft sollten Sie maximal die elektrischen Anschlüsse des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 68 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's fluid levels:",
     "Wie oft sollten Sie maximal die Flüssigkeitsstände des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 69 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's horn:",
     "Wie oft sollten Sie maximal die Hupe des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 70 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's coolant level:",
     "Wie oft sollten Sie maximal den Kühlmittelstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 71 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's power steering fluid:",
     "Wie oft sollten Sie maximal die Servolenkungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 72 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's brake fluid:",
     "Wie oft sollten Sie maximal die Bremsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 73 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's windshield washer fluid:",
     "Wie oft sollten Sie maximal die Scheibenwischerflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 74 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's clutch fluid:",
     "Wie oft sollten Sie maximal die Kupplungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 75 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's transmission fluid:",
     "Wie oft sollten Sie maximal das Getriebeöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 76 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's differential fluid:",
     "Wie oft sollten Sie maximal das Differentialöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 77 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's engine oil level:",
     "Wie oft sollten Sie maximal den Motorölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 78 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's brake fluid level:",
     "Wie oft sollten Sie maximal den Bremsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 79 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's power steering fluid level:",
     "Wie oft sollten Sie maximal den Servolenkungsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 80 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's windshield washer fluid level:",
     "Wie oft sollten Sie maximal den Scheibenwischerflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 81 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's clutch fluid level:",
     "Wie oft sollten Sie maximal den Kupplungsflüssigkeitsstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 82 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's transmission fluid level:",
     "Wie oft sollten Sie maximal den Getriebeölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 83 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's differential fluid level:",
     "Wie oft sollten Sie maximal den Differentialölstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 84 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's engine oil:",
     "Wie oft sollten Sie maximal das Motoröl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 85 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's brake fluid:",
     "Wie oft sollten Sie maximal die Bremsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 86 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's power steering fluid:",
     "Wie oft sollten Sie maximal die Servolenkungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 87 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's windshield washer fluid:",
     "Wie oft sollten Sie maximal die Scheibenwischerflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 88 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's clutch fluid:",
     "Wie oft sollten Sie maximal die Kupplungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 89 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's transmission fluid:",
     "Wie oft sollten Sie maximal das Getriebeöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 90 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's differential fluid:",
     "Wie oft sollten Sie maximal das Differentialöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 91 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's coolant level:",
     "Wie oft sollten Sie maximal den Kühlmittelstand des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 92 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's power steering fluid:",
     "Wie oft sollten Sie maximal die Servolenkungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 93 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's brake fluid:",
     "Wie oft sollten Sie maximal die Bremsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 94 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's windshield washer fluid:",
     "Wie oft sollten Sie maximal die Scheibenwischerflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 95 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's clutch fluid:",
     "Wie oft sollten Sie maximal die Kupplungsflüssigkeit des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 96 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's transmission fluid:",
     "Wie oft sollten Sie maximal das Getriebeöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 97 (Antwort: A)
    ("What is the maximum number of times you should check the vehicle's differential fluid:",
     "Wie oft sollten Sie maximal das Differentialöl des Fahrzeugs überprüfen:",
     ["Before every trip.", "Every 100 miles.", "At every stop."],
     ["Vor jeder Fahrt.", "Alle 100 Meilen.", "Bei jedem Halt."],
     0),
    # Frage 98 (Antwort: C)
    ("When using a fire extinguisher, you should:",
     "Bei der Verwendung eines Feuerlöschers sollten Sie:",
     ["Aim at the base of the fire.", "Aim at the top of the fire.", "Aim at the middle of the fire."],
     ["Auf den Boden des Feuers zielen.", "Auf die Spitze des Feuers zielen.", "Auf die Mitte des Feuers zielen."],
     2),
    # Frage 99 (Antwort: B)
    ("For this item refer to the figure below. You are driving a long vehicle that makes wide turns. You want to turn left from Pine Street onto Cedar Street. Both are two-lane, two-way streets. You should:",
     "Beziehen Sie sich für diese Frage auf die unten stehende Abbildung. Sie fahren ein langes Fahrzeug, das weite Kurven fährt. Sie möchten von der Pine Street links in die Cedar Street abbiegen. Beides sind zweispurige Straßen mit Gegenverkehr. Sie sollten:",
     ["Begin turning your vehicle as soon as you enter the intersection.",
      "Begin turning your vehicle when you are halfway through the intersection.",
      "Begin the turn with your vehicle in the left lane of Pine Street."],
     ["Beginnen Sie mit dem Abbiegen Ihres Fahrzeugs, sobald Sie in die Kreuzung einfahren.",
      "Beginnen Sie mit dem Abbiegen Ihres Fahrzeugs, wenn Sie sich auf halber Strecke durch die Kreuzung befinden.",
      "Beginnen Sie die Kurve mit Ihrem Fahrzeug auf der linken Spur der Pine Street."],
     1),
    # Frage 100 (Antwort: B)
    ("While driving, you see a small (1-foot square) cardboard box ahead in your lane. You should:",
     "Während der Fahrt sehen Sie einen kleinen (1 Fuß quadratischen) Karton vor sich in Ihrer Fahrspur. Sie sollten:",
     ["Steer around it without making a sudden or unsafe move.", "Brake hard to avoid hitting it.",
      "Hit it with your vehicle to knock it off the road."],
     ["Um ihn herumlenken, ohne eine plötzliche oder unsichere Bewegung zu machen.",
      "Stark bremsen, um ihn nicht zu treffen.", "Ihn mit Ihrem Fahrzeug treffen, um ihn von der Straße zu stoßen."],
     1)
]

# Start des zweisprachigen General Knowledge Quiz
if __name__ == "__main__":
    run_bilingual_quiz(quiz_fragen_general_knowledge_bilingual, "CDL General Knowledge Test",
                       "CDL Allgemeinwissen Test")