import socket


def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
    Das erste Argument (socket.AF_INET) gibt die IP-Adressfamilie fuer IPv4 an (weitere Optionen sind: AF_INET6 fuer die
    IPv6-Familie und AF_UNIX fuer Unix-Sockets).
    Das zweite Argument (socket.SOCK_STREAM)gibt an, dass wir einen TCP-Socket verwenden. Bei Verwendung von TCP
    erstellt das Betriebssystem eine zuverlaessige Verbindung mit geordneter Datenuebertragung, Fehlererkennung und
    erneuter Uebertragung sowie Flusskontrolle. Sie muessen sich keine Gedanken ueber die Implementierung all dieser
    Details machen. Es besteht auch die Moeglichkeit, einen UDP-Socket anzugeben: socket.SOCK_DGRAM. Dadurch wird ein
    Socket erstellt, der alle Funktionen von UDP im Hintergrund implementiert. Falls Sie tiefer gehen und Ihr eigenes
    Transportschichtprotokoll auf dem von Sockets verwendeten TCP/IP-Netzwerkschichtprotokoll aufbauen moechten, koennen
    Sie als zweites Argument den Wert verwenden. In diesem Fall uebernimmt das Betriebssystem keine hoeherstufigen
    Protokollfunktionen fuer Sie und Sie muessen alle Header, Verbindungsbestaetigungen und Neuuebertragungsfunktionen
    selbst implementieren, falls Sie diese benoetigen. Es gibt auch andere Werte, ueber die Sie in der Dokumentation
    socket.RAW_SOCKET lesen koennen.
    """

    '''
    Server-Socket an IP-Adresse und Port binden
    Definieren Sie den Hostnamen oder die Server-IP und den Port, um die Adresse anzugeben, von der aus der Server 
    erreichbar ist und wo er auf eingehende Verbindungen wartet. In diesem Beispiel wartet der Server auf dem lokalen 
    Computer – dies wird durch die server_ip Variable definiert, die auf gesetzt ist 127.0.0.1(auch localhost genannt).
    Die port Variable ist auf gesetzt 8000. Dies ist die Portnummer, anhand derer die Serveranwendung vom Betriebssystem 
    identifiziert wird. (Es wird empfohlen, fuer Ihre Portnummern Werte ueber 1023 zu verwenden, um Kollisionen mit von 
    Systemprozessen verwendeten Ports zu vermeiden.)
    '''
    server_ip = "127.0.0.1"
    port = 8000

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    '''
    Richten Sie mithilfe der Funktion einen Abhoerzustand im Server-Socket ein, listenum eingehende Client-Verbindungen 
    empfangen zu koennen. Diese Funktion akzeptiert ein Argument namens , backlogdas die maximale Anzahl in die 
    Warteschlange gestellter, nicht akzeptierter Verbindungen angibt. In diesem Beispiel verwenden wir den Wert 0 fuer 
    dieses Argument. Dies bedeutet, dass nur ein einziger Client mit dem Server interagieren kann. Ein Verbindungs-
    versuch eines beliebigen Clients, der durchgefuehrt wird, waehrend der Server mit einem anderen Client arbeitet, 
    wird abgelehnt. Wenn Sie einen Wert angeben, der groesser ist als 0beispielsweise 1, teilt er dem Betriebssystem 
    mit, wie viele Clients in die Warteschlange gestellt werden koennen, bevor die acceptMethode fuer sie aufgerufen 
    wird. Sobald accept aufgerufen wird, wird ein Client aus der Warteschlange entfernt und nicht mehr auf dieses Limit
    angerechnet. 
    Dies wird vielleicht klarer, wenn Sie sich weitere Teile des Codes ansehen, aber was dieser Parameter im 
    Wesentlichen tut, laesst sich wie folgt veranschaulichen: Sobald Ihr abhoerender Server die Verbindungsanforderung 
    erhaelt, wird er diesen Client zur Warteschlange hinzufuegen und mit der Annahme seiner Anforderung fortfahren. Wenn 
    der Server, bevor er acceptden ersten Client intern aufrufen konnte, eine Verbindungsanforderung von einem zweiten 
    Client erhaelt, wird er diesen zweiten Client in dieselbe Warteschlange verschieben, sofern darin genuegend Platz ist. 
    Die Groesse dieser Warteschlange wird genau durch das Backlog-Argument gesteuert. Sobald der Server den ersten Client 
    akzeptiert, wird dieser Client aus der Warteschlange entfernt und der Server beginnt mit ihm zu kommunizieren. Der 
    zweite Client bleibt weiterhin in der Warteschlange und wartet darauf, dass der Server frei wird und die Verbindung 
    annimmt. Wenn Sie das Backlog-Argument weglassen, wird es auf den Standard Ihres Systems gesetzt (unter Unix koennen 
    Sie diesen Standard normalerweise in der /proc/sys/net/core/somaxconnDatei sehen).
    '''
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accept incoming connections
    '''
    Die acceptMethode haelt den Ausfuehrungsthread an, bis ein Client eine Verbindung herstellt. Anschliessend gibt sie ein 
    Tupelpaar von zurueck (conn, address), wobei Adresse ein Tupel aus der IP-Adresse und dem Port des Clients ist und 
    conn ein neues Socket-Objekt darstellt, das eine Verbindung mit dem Client teilt und zur Kommunikation mit ihm 
    verwendet werden kann. accept erstellt einen neuen Socket zur Kommunikation mit dem Client, anstatt den Listening-
    Socket ( server in unserem Beispiel aufgerufen) an die Adresse des Clients zu binden und fuer die Kommunikation zu 
    verwenden, da der Listening-Socket auf weitere Verbindungen anderer Clients warten muss, da er sonst blockiert waere. 
    Natuerlich behandeln wir in unserem Fall immer nur einen einzigen Client und lehnen dabei alle anderen Verbindungen 
    ab, aber das wird relevanter, sobald wir zum Beispiel mit dem Multithread-Server kommunizieren.
    '''
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    '''
    Erstellen einer Kommunikationsschleife. Sobald eine Verbindung zum Client hergestellt wurde (nach Aufruf der accept
    Methode), initiieren wir eine Endlosschleife zur Kommunikation. In dieser Schleife fuehren wir einen Aufruf der recv
    Methode des client_socket Objekts durch. Diese Methode erhaelt vom Client die angegebene Anzahl an Bytes – in unserem 
    Fall 1024. 1024 Bytes ist nur eine gaengige Konvention fuer die Groesse der Nutzlast, da es sich um eine Zweierpotenz 
    handelt, die fuer Optimierungszwecke moeglicherweise besser ist als ein beliebiger anderer Wert. Sie koennen diesen 
    Wert jedoch beliebig aendern. Da die vom Client in der request Variable empfangenen Daten im Rohbinaerformat 
    vorliegen, haben wir sie mithilfe der decode Funktion von einer Bytefolge in einen String umgewandelt. Dann haben 
    wir eine if-Anweisung, die aus der Kommunikationsschleife ausbricht, wenn wir eine ”close” Nachricht erhalten. Das 
    bedeutet, dass unser Server, sobald er eine ”close” Zeichenfolge als Anfrage erhaelt, die Bestaetigung an den Client 
    zuruecksendet und seine Verbindung mit ihm beendet. Andernfalls drucken wir die empfangene Nachricht auf der Konsole 
    aus. Die Bestaetigung ist in unserem Fall einfach das Senden einer ”closed” Zeichenfolge an den Client. Beachten Sie, 
    dass die lower Methode, die wir in der if-Anweisung auf die Zeichenfolge anwenden request, diese einfach in 
    Kleinbuchstaben umwandelt. Auf diese Weise ist es uns egal, ob die close Zeichenfolge urspruenglich mit Gross- oder 
    Kleinbuchstaben geschrieben wurde.
    '''
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")  # convert bytes to string

        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        '''
        Antwort zurueck an den Client senden. Jetzt sollten wir die normale Antwort des Servers an den Client verarbeiten
        (also wenn der Client die Verbindung nicht schliessen moechte). Fuegen Sie innerhalb der while-Schleife direkt nach 
        print(f"Received: {request}") die folgenden Zeilen hinzu, die eine Antwortzeichenfolge (in unserem Fall) in 
        Bytes umwandeln und an den Client senden. Auf diese Weise sendet ”accepted”der Server jedes Mal, wenn er eine 
        Nachricht vom Client empfaengt, die nicht ist , die Zeichenfolge als Antwort:”close” ”accepted”
        '''
        response = "accepted".encode("utf-8")  # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)

    # close connection socket with the client
    '''
    Sobald wir aus der unendlichen while-Schleife ausbrechen, ist die Kommunikation mit dem Client abgeschlossen. Wir 
    schliessen also den Client-Socket mit der close Methode, um Systemressourcen freizugeben. Mit derselben Methode 
    schliessen wir auch den Server-Socket, wodurch unser Server effektiv heruntergefahren wird. In einem realen Szenario 
    wuerden wir natuerlich wahrscheinlich wollen, dass unser Server weiterhin auf andere Clients hoert und nicht nach der 
    Kommunikation mit nur einem einzigen herunterfaehrt, aber keine Sorge, wir werden weiter unten auf ein weiteres 
    Beispiel zurueckkommen.
    '''
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

if __name__ == '__main__':
    run_server()


