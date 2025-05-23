"""Wir stellen uns vor,wir möchten einen Supermarkt modellieren
Alles was uns wichtig ist, ist dass wir im Supermarkt einkaufen können. Damit der Supermarkt aber funktioniert,
werden viele andere Dinge benötigt. So müssen zum Beispiel kassierer beschäftigt werden. Es muss Strom bezahlt
werden, es müssen neue Produkte bestellt werden usw. Davon soll der Kunde aber nichts mitkriegen, er soll einfach nur
einkaufen können.

Der Kunde soll also im Supermarkt nur einkaufen können, er soll aber nicht die ganzen Dinge tun können,
die zum Betrieb des Supermarktes nötig sind (z.B. Waren nachbestellen). Überträgt man das nach Python,sieht das so aus:

-Tool,welches eine Seite herunterlädt
-Wie genau die Datenpakete übers Internet verschickt werden, geht mich als Nutzer nichts an. Für den User ist also
nur relevant, dass die Webseite heruntergeladen wird, die Prozesse im Hintergrund sind für ihn irrelevant.
Die idee ist also,dass wir all das,was den Nutzer nicht interessiert, verstecken, so dass man von außen nicht drauf
zugreifen können.
Was heißt das ? Das heißt, dass wir die Sichtbarkeit von Methoden und Variablen verstecken

"""