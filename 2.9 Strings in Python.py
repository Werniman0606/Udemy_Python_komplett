age = 22
# print ("Ich bin " + age + "Jahrae alt.")  # Diese Zeile würde fehlschlagen,weil man bei der String-Ausgabe nicht mehrere Formate mischen
# darf, sondern den Zahlenwert der Variable in einen String umwandeln muss. Stattdessen nutzt man dies hier
print("Ich bin " + str(age) + " Jahre alt.")

# Man kann aber auch eine moderne Darstellungsvariante nutzen, die sogenannten F-Strings. Diese benötigen keine Umwandlung in einen String.

print(f"Ich bin {age} Jahre alt.")