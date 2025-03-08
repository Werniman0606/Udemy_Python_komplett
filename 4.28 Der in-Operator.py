students = ["Max", "Monika", "Erik", "Franziska"]  # Eine Liste mit namen wird angelegt
print("Monika" in students)  # True, da es den Namen Monika in der Liste gibt
print("Moritz" in students)  # False, da es den Namen Moritz in der Liste nicht gibt
# D.h. der In-Operator prüft,ob der Wert in einer Liste drin ist

if "Monika" in students:
    print(
        "Ja, die Monika studiert hier!")  # Text wird ausgegeben,da die Abfrage ein True zurückgibt, ergo wird der Kommanoblock ausgeführt.
if "Moritz" in students:
    print("Ja, der Moritz studiert hier!")  # Text wird nicht ausgegeben, da Moritz nicht in der Liste drin ist, die Abfrage ergibt False

# Dieser String-Operator funktioniert auch in Sätzen:
sentence = "Ja, die Monika studiert hier!"  # Satz wird erstellt
if "!" in sentence:  # wenn es im Satz ein Ausrufezeichen gibt,wird der folgende Befehl ausgegeben.
    print("Ja, dieses Zeichen existiert hier!")
else:  # ansonsten dieser hier
    print("Nein, dieses Zeichen gibts in diesem Satz nicht!")
