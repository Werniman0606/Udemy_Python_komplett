"""<!-- Dies ist das Grundgerüst eines HTML5-Dokuments. -->
<html>
    <head>
        <!-- Der Titel der Webseite, der im Browser-Tab angezeigt wird. -->
        <title>Ich bin der Seitentitel</title>

        <!-- CSS-Stile für die Webseite. Diese definieren das Aussehen der Elemente. -->
        <style type="text/css">
            /* Die Klasse "important" färbt den Text rot. */
            .important {
                color: red;
            }
            /* Die ID "test123" färbt den Text orange. IDs sollten nur einmal pro Seite verwendet werden. */
            #test123 {
                color: orange;
            }
            /* Alle <span>-Elemente werden grün gefärbt. */
            span {
                color: green;
            }

            /* Absätze innerhalb des Elements mit der Klasse "absatz1" werden fett dargestellt. D.h. es wird nach
            Elementen der Klasse "absatz1" gesucht, in denen ein Absatz p enthalten ist. Diese werden in fetter
            Schrift geschrieben. */
            .absatz1 p {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <!-- Ein Div-Container mit der Klasse "absatz1". -->
        <div class="absatz1">
            <!-- Ein Absatz innerhalb von "absatz1". Dieser wird aufgrund des CSS fett dargestellt. -->
            <p>ABSATZ1: Ich bin ein Absatz</p>
        </div>
        <!-- Ein Div-Container mit der Klasse "absatz2". -->
        <div class="absatz2">
            <!-- Ein Absatz innerhalb von "absatz2". -->
            <p>ABSATZ2: Ich bin ein Absatz</p>
        </div>

        <!-- Ein Absatz mit der Klasse "important", der rot gefärbt wird. -->
        <p class="important">Ich bin ein Absatz!</p>
        <!-- Ein weiterer Absatz mit der Klasse "important", der ebenfalls rot gefärbt wird. -->
        <p class="important">Ich bin ein Absatz!</p>
        <!-- Ein Absatz mit der ID "test123", der orange gefärbt wird. -->
        <p id="test123">Ich bin ein Absatz!</p>
        <!-- Ein weiterer Absatz mit der Klasse "important", der rot gefärbt wird. -->
        <p class="important">Ich bin ein Absatz!</p>
        <!-- Standard-Absätze ohne spezielle Stile. -->
        <p>Ich bin ein Absatz!</p>
        <p>Ich bin ein Absatz!</p>

        <!-- Ein <span>-Element, das aufgrund des CSS grün gefärbt wird. -->
        <span>Ich bin ein anderer Text!</span>

    </body>
</html>
"""
"""
Wie wir sehen, gibts in Zeile 10 einen punkt,der den Browser anweist, alle Objekte der Klasse "Important" in Rot zu 
schreiben. Dieses "Preset" erkennt man an dem vorangestellten Punkt. Sprich: alle Zeilen,wo der Style mit <p 
class="important"> beginnt, werden in Rot geschrieben, alle Zeilen,wo der Style mit  <div class="absatz1"> beginnt, 
werden fett geschrieben usw.


"""