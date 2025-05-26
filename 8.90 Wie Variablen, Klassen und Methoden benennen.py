# Namenskonventionen in Python

# Obwohl Python die Funktion eines Codes nicht durch die Namensgebung beeinflusst,
# gibt es **Style Guides**, die dabei helfen, lesbaren und wartbaren Code zu schreiben.
# Der wichtigste ist der **PEP 8 Style Guide**, der Industriestandard für Python-Code.

# Benennungsstile im Überblick:
# 1.  **PascalCase (z.B. 'MeineKlasse' oder 'HttpResponseHandler'):**
#     Jedes Wort beginnt mit einem Großbuchstaben, keine Unterstriche.
# 2.  **camelCase (z.B. 'meinVariablenName' oder 'calculateSum'):**
#     Das erste Wort beginnt mit einem Kleinbuchstaben, nachfolgende Wörter mit Großbuchstaben.
#     **WICHTIG:** camelCase wird in Python **nicht für Standard-Code** verwendet.
# 3.  **snake_case (z.B. 'mein_variablen_name' oder 'berechne_summe'):**
#     Alle Buchstaben sind klein, Wörter werden durch Unterstriche getrennt.

# Wann welcher Stil verwendet wird (gemäß PEP 8):

# **Klassen:**
# Klassennamen werden in **PascalCase** geschrieben.
# Beispiel: `class MeinErstesObjekt:`

# **Variablen und Funktionen:**
# Variablennamen und Funktionsnamen werden in **snake_case** geschrieben.
# Beispiel: `mein_wert = 10`
# Beispiel: `def berechne_ergebnis():`

# **Konstanten:**
# Konstanten (Variablen, deren Wert sich während der Programmlaufzeit nicht ändert)
# werden in **SNAKE_CASE mit Großbuchstaben** geschrieben.
# Beispiel: `MAX_ANZAHL = 100`

# **Zusätzliche Tipps:**
# * Klassen-, Variablen- und Funktionsnamen sollten **aussagekräftig** sein und ihren Zweck klar widerspiegeln.
# * Vermeide übermäßig lange Namen; **1-3 aussagekräftige Wörter** sind oft ideal.
# * Sei **konsistent** in deinem Code. Wenn du dich für einen Stil entscheidest (was PEP 8 dir hier abnimmt), bleibe dabei.