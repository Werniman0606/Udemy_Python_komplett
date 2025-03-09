"""In Python kommt es oft zu Fehlermeldungen. Wenn man beispielsweise versucht,folgenden Befehl
print("Hallo"+13)
auszuführen, dann gibt es einen TypeError mit der Begründung 'must be str, not int'
Ein TypeError deutet auf eine Inkompatiblität in Sachen Dateiformate hin. Im Vorliegenden Fall liegt es daran,dass ein Print-Befehl
nicht verschiedene Dateitypen mischen darf und man den Int-Teil (die 13) erst in einen String umwandeln muss. Der korrekte Befehl lautet also

print("Hallo"+str(13))

Bei unbekannten Fehlermeldungen ist es sinnvoll, die Fehlermeldung mal zu googeln und z.B. bei Stackoverflow eine Lösung zu suchen.
"""




