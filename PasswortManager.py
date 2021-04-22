from tkinter import *
import sqlite3, secrets, random, string, pyperclip
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
from os import path

# Einstellungen für das Hauptfenster
root = Tk()
root.title("Passwort-Manager")
root.geometry("410x220")
root.resizable(False, False)

# Farben, die für den Hintergrund, Buttons etc. verwendet werden
hintergrundFarbe = "#282828"
textFarbe = "#FFFFFF"
buttonHGFarbe = "#3a3b3c"
entryHGFarbe = "#e4e6eb"

root.config(bg=hintergrundFarbe)
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='bilder/icons/schloss.png'))
root.option_add( "*font", "Consolas 11" )

# Prüfen, ob dies der erste Durchlauf des Programms ist und demnach ggf. bereits ein Key zum verschlüsseln existiert
with open("ersterDurchlauf.txt", "a+") as ersteFile:
    global fernet
    ersteFile.seek(0)
    if(ersteFile.read() == "1"):
        with open("key.key", "rb") as keyFile:
            keyFile.seek(0)
            key = keyFile.read()
            fernet = Fernet(key)
            
    # Falls nein, wird in der .txt-Datei gekennzeichnet, dass es der erste Durchlauf ist
    # Außerdem wird ein neuer Key generiert und in der .key-Datei abgelegt
    else:
        with open("ersterDurchlauf.txt", "w") as writeFile:
            writeFile.seek(0)
            writeFile.truncate()
            writeFile.write("1")
        with open("key.key", "wb") as keyFile:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            keyFile.seek(0)
            keyFile.write(key)

# Funktioon zum Verschlüsseln der Datenbank
def verschluessleDB():
    with open("pwManager.db", "rb") as file:
        data = file.read()
        data = fernet.encrypt(data)
        with open("pwManager.db", "wb") as file:
            file.write(data)

# Funktion zum Entschlüsseln der Datenbank
def entschluessleDB():
    with open("pwManager.db", "rb") as file:
        data = file.read()
        try:
            data = fernet.decrypt(data)
        except:
            pass
        with open("pwManager.db", "wb") as file:
            file.write(data)

# Prüft, ob diese Datenbank bereits vorhanden ist
# Falls ja, passiert erst einmal nichts und diese Datenbank wird auch weiterhin verwendet
if(path.exists("pwManager.db")):
    pass

#Falls nein, wird eine neue Datenbank angelegt und anschließend direkt verschlüsselt
else:
    conn = sqlite3.connect("pwManager.db")
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS pwManager (
                            appName text,
                            username text,
                            url text,
                            password text
                            )""")

    # Speichern der Änderungen und Schließen der Datenbankverbindung
    conn.commit()
    conn.close()
    # Verschlüsseln der Datenbank
    verschluessleDB()

# Fenster für den Passwortgenerator
def passwortGeneratorFenster():
    passGen = Toplevel()
    passGen.attributes("-topmost", True)
    passGen.focus()
    passGen.resizable(width=False, height=False)
    passGen.title("Passwort-Generator")
    passGen.config(bg=hintergrundFarbe)
    passGen.tk.call('wm', 'iconphoto', passGen._w, PhotoImage(file='bilder/icons/schloss.png'))
    
    # Prüft, welche der vier Optionen der Benutzer ausgewählt hat
    def pruefeObAngekreuzt():
        global pruefeKlein
        global pruefeGross
        global pruefeZahlen
        global pruefeZeichen
        pruefeKlein = varKlein.get()
        pruefeGross = varGross.get()
        pruefeZahlen = varZahlen.get()
        pruefeZeichen = varZeichen.get()
        
    # Übergibt die ausgewählte Länge des Passworts in eine globale Variable
    def gebeLaengeAn(laenge):
        global passwortLaenge
        passwortLaenge = laenge
        
    # Generiert das Passwort gemäß den Parametern der Eingabe des Benutzers
    def generierePasswort():
        passwortFeldPG.delete(0, END)
        zaehler = 0
        auswahlListe = []
        passwort = ""
        global passwortLaenge

        # Prüft, welche Option angekreuzt wurde und hält dies in einem Array fest
        try:
            if pruefeKlein == 1:
                zaehler += 1
                auswahlListe.append("klein")
        except:
            pass
        try:
            if pruefeGross == 1:
                zaehler += 1
                auswahlListe.append("gross")
        except:
            pass
        try:
            if pruefeZahlen == 1:
                zaehler += 1
                auswahlListe.append("zahlen")
        except:
            pass
        try:
            if pruefeZeichen == 1:
                zaehler += 1
                auswahlListe.append("zeichen")
        except:
            pass

        # Falls mindestens eine Option angekreuzt wurde, wird ein Passwort generiert
        if zaehler !=0:
            try:
                durchlauf = int(passwortLaenge)
            except:
                durchlauf = 8
            while durchlauf > 0:
                # Je nachdem, welche Option angekreuzt wurde, wird das Passwort aus zufälligen Werten zusammengesetzt
                if "klein" in auswahlListe:
                    passwort += secrets.choice(vorratKlein)
                    durchlauf -= 1
                if "gross" in auswahlListe:
                    passwort += secrets.choice(vorratGross)
                    durchlauf -= 1
                if "zahlen" in auswahlListe:
                    passwort += secrets.choice(vorratZahlen)
                    durchlauf -= 1
                if "zeichen" in auswahlListe:
                    passwort += secrets.choice(vorratZeichen)
                    durchlauf -= 1

        # Falls keine der vier Optionen angekreuzt wurde, wird eine Fehlermeldung ausgegeben
        else:
            messagebox.showerror("Fehler", "Es muss mind. eine Option angekreut sein!")
            passGen.lift()
            passGen.focus()
            
        # Reiht die einzelnen Werte des Arrays in einer zufälligen Reihenfolge an
        passwortArray = list(passwort)
        random.shuffle(passwortArray)
        passwort = ''.join(passwortArray)
        passwortFeldPG.config(state=NORMAL)
        passwortFeldPG.delete(0, END)
        passwortFeldPG.insert(END, passwort)
        passwortFeldPG.config(state=DISABLED)
        
    # Fügt das erstellte Passwort in die Zwischenablage des Benutzers ein
    def kopiereEingabe():
        passwortKopie = passwortFeldPG.get()
        pyperclip.copy(passwortKopie)
        
    # Schließt das Passwortgeneratorfenster nach Abbruch
    def brecheVorgangAb():
        passGen.destroy()
        
    # Schließt das Passwortgeneratorfenster nach erfolgreichem Erstellen des Passworts
    def bestaetigePasswort():
        if(passwortFeldPG.get()!=""):
            passwortEingabeEntry.config(state=NORMAL)
            passwortEingabeEntry.delete(0, END)
            passwortEingabeEntry.insert(END, passwortFeldPG.get())
            passwortEingabeEntry.config(state=DISABLED)
            passGen.destroy()
            
        else:
            messagebox.showerror("Fehler", "Es ist kein Passwort ausgewählt!")
            passGen.lift()
            passGen.focus()

    # Variablen mit den zur Verfügung stehenden Zeichen
    vorratKlein = list(string.ascii_lowercase)
    vorratGross = list(string.ascii_uppercase)
    vorratZahlen = list(string.digits)
    vorratZeichen = list(string.punctuation)

    # Schaltfläche für das Anzeigen von "Passwort"
    passwortLabelPG = Label(passGen, text="Passwort: ", fg=textFarbe, bg=hintergrundFarbe)
    passwortLabelPG.grid(row=0, padx=10)
    passwortFeldPG = Entry(passGen, state=DISABLED, bg=entryHGFarbe)
    passwortFeldPG.grid(row=0, column=1)
    
    varKlein = IntVar()
    varGross = IntVar()
    varZahlen = IntVar()
    varZeichen = IntVar()

    # Anzukreuzende Kästchen, die der Benutzer auswählen kann
    Checkbutton(passGen, text="Kleinbuchstaben", variable=varKlein, command=pruefeObAngekreuzt, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe).grid(row=2, column=0)
    Checkbutton(passGen, text="Großbuchstaben", variable=varGross, command=pruefeObAngekreuzt, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe).grid(row=3, column=0)
    Checkbutton(passGen, text="Zahlen", variable=varZahlen, command=pruefeObAngekreuzt, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe).grid(row=2, column=1)
    Checkbutton(passGen, text="Sonderzeichen", variable=varZeichen, command=pruefeObAngekreuzt, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe).grid(row=3, column=1)

    # Schaltfläche für das Anzeigen von "Länge"
    laengePWLabel = Label(passGen, text="Länge des Passworts:", fg=textFarbe, bg=hintergrundFarbe)
    laengePWLabel.grid(row=1, column=0, sticky="w", padx=10)
        
    # Regler, den der Benutzer verschieben kann, um die Passwortlänge festzulegen
    laengePWRegler = Scale(passGen, from_=8, to=30, orient=HORIZONTAL, command=gebeLaengeAn, fg=textFarbe, bg=hintergrundFarbe, activebackground=hintergrundFarbe, highlightbackground=hintergrundFarbe)
    laengePWRegler.grid(row=1, column=1)

    # Erzeugt einen eingerahmten Text
    tippFrame = Frame(passGen, bg="#efebdc", bd=2)
    tippFrame.grid(row=1, column=2, rowspan=3)
    tipp = Label(tippFrame, text="Tipp: \nKombiniere ein \nlanges Passwort \n mit verschiedenen \nSymbolen!", fg=textFarbe, bg=hintergrundFarbe)
    tipp.grid(row=0, column=0, rowspan=3)

    # Erzeugt den Button für die Funktion zum Kopieren des Passworts
    kopierenButton = Button(passGen, text="PW kopieren", command=kopiereEingabe, fg=textFarbe, bg=hintergrundFarbe)
    kopierenButton.grid(row=0, column=2, padx=10, pady=10)

    # Erzeugt den Button für die Funktion zum Generieren des Passworts
    pwGenerierenButton = Button(passGen, text="PW generieren", command=generierePasswort, fg=textFarbe, bg=hintergrundFarbe)
    pwGenerierenButton.grid(row=6, column=0)

    # Erzeugt den Button zum Abbrechen des Vorgangs
    abbrechenButton = Button(passGen, text="Abbrechen", command=brecheVorgangAb, fg=textFarbe, bg=hintergrundFarbe)
    abbrechenButton.grid(row=6, column=2)

    # Erzeugt einen Button zum Bestätigen des Passworts
    pwBestaetigenButton = Button(passGen, text="PW bestätigen", command=bestaetigePasswort, fg=textFarbe, bg=hintergrundFarbe)
    pwBestaetigenButton.grid(row=6, column=1, pady=10)

# Prüft, ob die manuelle oder automatische Option ausgewählt ist
def autoOderManuell():
    if wahlRadio.get() == "A":
        passwortEingabeEntry.delete(0, END)
        passwortEingabeEntry.config(state=DISABLED)
        zumPWGeneratorButton.config(state=NORMAL)
        
    else:
        passwortEingabeEntry.config(state=NORMAL)
        passwortEingabeEntry.delete(0, END)
        zumPWGeneratorButton.config(state=DISABLED)

# Fügt den Eintrag der Datenbank hinzu
def fuegeEintragHinzu():
    # Entschlüsseln der Datenbank
    entschluessleDB()
    # Aufbauen der Datenbankverbindung und Generieren des Cursors
    conn = sqlite3.connect("pwManager.db")
    cursor = conn.cursor()

    # Wenn alle Pflichtfelder ausgefüllt wurden, wird der Eintrag der Datenbank hinzugefügt
    if nameEingabeEntry.get()!= "" and nutzerNameEingabeEntry.get()!= "" and passwortEingabeEntry.get()!= "":
        cursor.execute("INSERT INTO pwManager VALUES(:nameEingabeEntry, :nutzerNameEingabeEntry, :urlNameEingabeEntry, :passwortEingabeEntry)",

        {
        'nameEingabeEntry': nameEingabeEntry.get(),
        'nutzerNameEingabeEntry': nutzerNameEingabeEntry.get(),
        'urlNameEingabeEntry': urlEingabeEntry.get(),
        'passwortEingabeEntry': passwortEingabeEntry.get()
        })

        # Speichern der Änderungen und Schließen der Datenbankverbindung
        conn.commit()
        conn.close()
        # Verschlüsseln der Datenbank
        verschluessleDB()

        messagebox.showinfo("Information", " Eintrag hinzugefügt!")
        manuellRadio.select()
        zumPWGeneratorButton.config(state="disabled")
        nameEingabeEntry.delete(0, END)
        urlEingabeEntry.delete(0, END)
        nutzerNameEingabeEntry.delete(0, END)
        passwortEingabeEntry.config(state=NORMAL)
        passwortEingabeEntry.delete(0, END)
        showRecords(3)

    # Falls nicht alle Pflichtfelder angegeben wurden, wird eine Fehlermeldung ausgegeben
    else:
        messagebox.showerror("Fehler", "Unvollständige Eingaben!")
        # Schließen der Datenbankverbindung
        conn.close()
        # Verschlüsseln der Datenbank
        verschluessleDB()

# Löscht den Eintrag aus der Datenbank 
def deleteRecord():
    loescheID = loescheEintragEntry.get()
    # Prüft, ob eine ID eingegeben wurde
    if(loescheID!=""):
        # Prüft, ob die eingegebene ID einen Treffer in der Datenbank erzielt
        try:
            # Entschlüsseln der Datenbank
            entschluessleDB()
            # Aufbauen der Datenbankverbindung und Generieren des Cursors
            conn = sqlite3.connect("pwManager.db")
            cursor = conn.cursor()
            cursor.execute("Select appName from pwManager where oid = " +loescheID)
            pruefeObZeileExistiert = cursor.fetchall()
            nameEingabeEntry.insert(END, pruefeObZeileExistiert)
        
            # Falls kein Treffer gefunden wird, wird ein Fehler ausgegeben und die Datenbankverbindung geschlossen
            if(nameEingabeEntry.get()==""):
                messagebox.showerror("Fehler", "ID nicht gefunden!")
                loescheEintragEntry.config(state=NORMAL)
                bearbeiteEintragEntry.config(state=NORMAL)
                # Speichern der Änderungen und Schließen der Datenbankverbindung
                conn.commit()
                conn.close()
                # Verschlüsseln der Datenbank
                verschluessleDB()
                
            # Falls ein Treffer gefunden wird, wird der Eintrag gelöscht
            else:
                nameEingabeEntry.delete(0, END)
                cursor.execute("DELETE FROM pwManager where oid = " + loescheID)
                messagebox.showinfo("Information", "Eintrag %s gelöscht!" %loescheID)
                manuellRadio.select()
                zumPWGeneratorButton.config(state="disabled")
                loescheEintragEntry.delete(0, END)
                dbFrame.destroy()
                # Speichern der Änderungen und Schließen der Datenbankverbindung
                conn.commit()
                conn.close()
                # Verschlüsseln der Datenbank
                verschluessleDB()
                showRecords(4)
                
        except:
            messagebox.showerror("Fehler", "ID nicht gefunden!")
            
    else:
        messagebox.showerror("Fehler", "Es muss eine ID angegeben werden!")

# Schließt die Ansicht der Einträge  
def verbergeEintraege():
    dbFrame.destroy()
    root.minsize(410,220)
    root.maxsize(410,220)
    zeigeEintraegeButton.config(text="Einträge anzeigen", command= lambda: showRecords(3))

# Aktualisiert den ausgewählten Eintrag
def aktualisiereEintrag():
    # Entschlüsseln der Datenbank
    entschluessleDB()
    # Aufbauen der Datenbankverbindung und Generieren des Cursors
    conn = sqlite3.connect("pwManager.db")
    cursor = conn.cursor()  

    # Falls eins der vier Felder nicht leer ist (der Benutzer hat etwas eingegeben), wird der jeweilige Eintrag in der Datenbank aktualsiert
    if nameEingabeEntry.get()!="" or urlEingabeEntry.get()!="" or nutzerNameEingabeEntry.get()!="" or passwortEingabeEntry.get()!="":
        pruefzahl = 0
        if nameEingabeEntry.get()!="":
            cursor.execute("""UPDATE pwManager SET
                        appName = :appName
                            
                        WHERE oid = :oid""",
                        {
                        'appName': nameEingabeEntry.get(),
                        'oid': bearbeiteEintragEntry.get()
                        }
            )
            pruefzahl += 1
            
        if nutzerNameEingabeEntry.get()!="":
            cursor.execute("""UPDATE pwManager SET
                        username = :username
                            
                        WHERE oid = :oid""",
                        {
                        'username': nutzerNameEingabeEntry.get(),
                        'oid': bearbeiteEintragEntry.get()
                        }
            )
            pruefzahl += 1
            
        if urlEingabeEntry.get()!="":
            cursor.execute("""UPDATE pwManager SET
                        url = :url
                            
                        WHERE oid = :oid""",
                        {
                        'url': urlEingabeEntry.get(),
                        'oid': bearbeiteEintragEntry.get()
                        }
            )
            pruefzahl += 1
                
        if passwortEingabeEntry.get()!="":
            cursor.execute("""UPDATE pwManager SET
                        password = :password
                            
                        WHERE oid = :oid""",
                        {
                        'password': passwortEingabeEntry.get(),
                        'oid': bearbeiteEintragEntry.get()
                        }
            )
            pruefzahl += 1
            
        # Speichern der Änderungen und Schließen der Datenbankverbinden
        conn.commit()
        conn.close()
        # Verschlüsseln der Datenbank
        verschluessleDB()
        
        # Wenn mindestens eine Angabe geändert wurde, wird eine Benachrichtigung ausgegeben, die Felder werden geleert und die aktualisierten Einträge werden ausgegeben
        if(pruefzahl!=0):
            messagebox.showinfo("Information", "Eintrag aktualisiert!")
            passwortEingabeEntry.config(state=NORMAL)
            manuellRadio.select()
            passwortEingabeEntry.delete(0, END)
            urlEingabeEntry.delete(0, END)
            nutzerNameEingabeEntry.delete(0, END)
            nameEingabeEntry.delete(0, END)
            dbFrame.destroy()
            showRecords(3)
            fuegeEintragHinzuButton.config(text="Eintrag hinzufügen", command=fuegeEintragHinzu)
            zeigeEintraegeButton.config(text="Einträge verbergen", command=verbergeEintraege)
            loescheEintragEntry.config(state=NORMAL)
            bearbeiteEintragEntry.config(state=NORMAL)
            bearbeiteEintragEntry.delete(0, END)
            bearbeiteEintragEntry.insert(END, "Bitte ID angeben")
        
    else:
        messagebox.showerror("Fehler", "Gueltige ID eingeben!")

# Prüft, ob der angegebene Eintrag aktualisiert werden kann
def aktualisiereVorbereitung():
    bearbeiteID = bearbeiteEintragEntry.get()
    # Prüft, ob eine ID angegeben wurde. Falls ja, wird die Datenbankverbindung aufgebaut und ein Cursor generiert
    if(bearbeiteID!=""):
        # Entschlüsseln der Datenbank
        entschluessleDB()
        # Aufbauen der Datenbankverbindung und Generieren des Cursors
        conn = sqlite3.connect("pwManager.db")
        cursor = conn.cursor()
        # Prüft, ob es zu der eingegebenen ID einen Eintrag in der Datenbank gibt
        try:
            cursor.execute("Select appName from pwManager where oid = " +bearbeiteID)
            pruefeObZeileExistiert = cursor.fetchall()
            nameEingabeEntry.insert(END, pruefeObZeileExistiert)
            
            # Falls nein, wird ein Fehler ausgegeben
            if(nameEingabeEntry.get()==""):
                messagebox.showerror("Fehler", "ID nicht gefunden!")
                loescheEintragEntry.config(state=NORMAL)
                bearbeiteEintragEntry.config(state=NORMAL)

            # Falls ja, werden die entsprechenden gespeicherten Werte des Eintrags in die jeweiligen Felder eingefügt
            else:
                fuegeEintragHinzuButton.config(text="Eintrag aktualisie", command=aktualisiereEintrag)
                zeigeEintraegeButton.config(text="Abbrechen", command=aktuAbbrechen)
                loescheEintragEntry.config(state=DISABLED)
                bearbeiteEintragEntry.config(state=DISABLED)
                
                # Da bereits geprüft wurde, ob etwas für das "Name"-Feld eingetragen wurde, wird es jetzt nicht erneut hineinkopiert
                
                cursor.execute("Select url from pwManager where oid = " +bearbeiteID)
                zeile = cursor.fetchall()
                urlEingabeEntry.insert(END, zeile)
                
                # Falls keine optionale URL angegeben wurde, wird der Platzhalter entfernt
                urlTest = urlEingabeEntry.get()
                if(urlTest=="{{}}"):
                    urlEingabeEntry.delete(0, END)
                
                cursor.execute("Select username from pwManager where oid = " +bearbeiteID)
                zeile = cursor.fetchall()
                nutzerNameEingabeEntry.insert(END, zeile)
                
                cursor.execute("Select password from pwManager where oid = " +bearbeiteID)
                zeile = cursor.fetchall()
                passwortEingabeEntry.config(state=NORMAL)
                passwortEingabeEntry.delete(0, END)
                passwortEingabeEntry.insert(END, zeile)
                manuellRadio.select()
                
                # Da bei manchen Zeichen im Passwort oder Namen Klammern um diese gemacht werden, werden sie entfernt
                # Bspw. bei einer Raute wird fälschlicherweise {{#}} draus
                entferneKlammernPW = passwortEingabeEntry.get()
                entferneKlammernName = nameEingabeEntry.get()
                if("{{" in entferneKlammernPW):
                    passwortEingabeEntry.delete(0, END)
                    entferneKlammernPW = entferneKlammernPW.replace("{{", "")
                    entferneKlammernPW = entferneKlammernPW.replace("}}", "")
                    passwortEingabeEntry.insert(END, entferneKlammernPW)
                if("{{" in entferneKlammernName):
                    nameEingabeEntry.delete(0, END)
                    entferneKlammernName = entferneKlammernName.replace("{{", "")
                    entferneKlammernName = entferneKlammernName.replace("}}", "")
                    nameEingabeEntry.insert(END, entferneKlammernName)
        # Falls die eingegebene ID keinen Treffer erhält, wird ein Fehler ausgegeben
        except:
            messagebox.showerror("Fehler", "ID nicht gefunden!")
           
        # Speichern der Änderungen und Schließen der Datenbankverbindung 
        conn.commit()
        conn.close()
        # Verschlüsseln der Datenbank
        verschluessleDB()
    
    else:
        messagebox.showerror("Fehler", "Keine ID angegeben!")

# Bricht den Vorgang des Aktualisierens ab
def aktuAbbrechen():
    fuegeEintragHinzuButton.config(text="Eintrag hinzufügen", command=fuegeEintragHinzu)
    zeigeEintraegeButton.config(text="Einträge verbergen", command=verbergeEintraege)
    loescheEintragEntry.config(state=NORMAL)
    bearbeiteEintragEntry.config(state=NORMAL)
    # Löschen der Angaben 
    bearbeiteEintragEntry.delete(0, END)
    nameEingabeEntry.delete(0, END)
    urlEingabeEntry.delete(0, END)
    nutzerNameEingabeEntry.delete(0, END)
    passwortEingabeEntry.delete(0, END)

# Erstellt den Button zum Anzeigen / Verstecken der Passwörter in der Datenbank
def augenButton():
    global showHidePWsButton
    global photo
    photo = PhotoImage(file="bilder/icons/eye_crossed.png")
    showHidePWsButton = Button(root, image=photo, command=zeigePWsAn, bg=hintergrundFarbe)
    showHidePWsButton.grid(row=8, column=1, sticky="e", padx= (1,20))
    global neuPhoto
    neuPhoto = PhotoImage(file="bilder/icons/eye.png")

# Versteckt die Passwörter der Einträge in der Datenbank
def hidePWs():
    dbFrame.destroy()
    showRecords(1)
    showHidePWsButton.config(image=photo, command=zeigePWsAn)

# Zeigt die Passwörter der Einträge in der Datenbank an
def zeigePWsAn():
    dbFrame.destroy()
    showRecords(2)
    showHidePWsButton.config(image=neuPhoto, command=hidePWs)

# Zeigt die Einträge der Datenbank an
def showRecords(x):
    # Erzeugen des Rahmens für die Auflistung der Einträge
    global dbFrame
    try:
        dbFrame.destroy()
    except:
        pass
    dbFrame = Frame(root, highlightbackground="#3a3b3c", highlightthickness=4)
    dbFrame.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.5, anchor = "n")
    # Erzeugen der horizontalen Scrollbar
    horiScrollbar = Scrollbar(dbFrame, orient = 'horizontal')
    horiScrollbar.pack(side = BOTTOM, fill = X)
    # Erzeugen der vertikalen Scrollbar
    vertiScrollbar = Scrollbar(dbFrame, orient= 'vertical')
    vertiScrollbar.pack(side = RIGHT, fill = Y)
    # Erzeugt das Textfenster, in dem die Einträge aufgelistet werden
    global textFensterEinträge
    textFensterEinträge = Text(dbFrame, width = 67, height = 16.8, wrap = NONE, xscrollcommand = horiScrollbar.set,  
                 yscrollcommand = vertiScrollbar.set, fg=textFarbe, bg="#212121")
    textFensterEinträge.pack()
    horiScrollbar.config(command=textFensterEinträge.xview)
    vertiScrollbar.config(command=textFensterEinträge.yview)
    
    # Entschlüsseln der Datenbank
    entschluessleDB()
    # Aufbauen der Datenbankverbindung und Generieren des Cursors
    conn = sqlite3.connect("pwManager.db")
    cursor = conn.cursor()
    
    if(x==1):
        augenButton()
        passwortEingabeEntry.config(show="*")
        # Listet alle Einträge der Datenbank in Klartext auf, wobei das Passwort jedoch als generische Sternenfolge ausgegeben wird
        cursor.execute("SELECT *, oid FROM pwManager")
        eintraege = cursor.fetchall()
        angezeigteEintraege = ""
        for record in eintraege:
            angezeigteEintraege += "ID:" + "\t\t" + str(record[4])+ "\n" + "Name:" + "\t\t" + str(record[0])+ "\n" + "Nutzername:" + "\t\t" + str(record[1])+ "\n" + "URL:" + "\t\t" + str(record[2]) + "\n" + "Passwort:" + "\t\t" + "**************"+ "\n----------------------------------------------\n"

        textFensterEinträge.insert(END, angezeigteEintraege)
        textFensterEinträge.config(state=DISABLED)
    elif (x==2):
        augenButton()
        # Zeigt das oben stehende Passwort in Klartext an
        passwortEingabeEntry.config(show="")
        # Listet alle Einträge der Datenbank in Klartext auf
        cursor.execute("SELECT *, oid FROM pwManager")
        eintraege = cursor.fetchall()
        angezeigteEintraege = ""
        for record in eintraege:
            angezeigteEintraege += "ID:" + "\t\t" + str(record[4])+ "\n" + "Name:" + "\t\t" + str(record[0])+ "\n" + "Nutzername:" + "\t\t" + str(record[1])+ "\n" + "URL:" + "\t\t" + str(record[2]) + "\n" + "Passwort:" + "\t\t" + str(record[3])+ "\n----------------------------------------------\n"

        textFensterEinträge.insert(END, angezeigteEintraege)
        textFensterEinträge.config(state=DISABLED)
    
    elif(x==3):
        # Setzt die Größe des Fensters fest
        root.minsize(410, 600)
        root.maxsize(410, 600)
        
        # Erzeugt den Button und das Eingabefeld zum Löschen eines Eintrags
        loescheEintragButton = Button(root, text="Eintrag löschen", command=deleteRecord, fg=textFarbe, bg=hintergrundFarbe)
        loescheEintragButton.grid(row=7, column=0)
        global loescheEintragEntry
        loescheEintragEntry = Entry(root, bg=entryHGFarbe)
        loescheEintragEntry.grid(row=7, column=1, sticky="w", padx=25)
        loescheEintragEntry.insert(END, "Bitte ID angeben")
        loescheEintragEntry.config(font="Consolas 11 italic")
        # Erzeugt den Button und das Eingabefeld zum Bearbeiten eines Eintrags
        bearbeiteEintragButton = Button(root, text="Eintrag bearbeiten", command=aktualisiereVorbereitung, fg=textFarbe, bg=hintergrundFarbe)
        bearbeiteEintragButton.grid(row=8, column=0)
        global bearbeiteEintragEntry
        bearbeiteEintragEntry = Entry(root, bg=entryHGFarbe)
        bearbeiteEintragEntry.grid(row=8, column=1, sticky="w", padx=25)
        bearbeiteEintragEntry.insert(END, "Bitte ID angeben")
        bearbeiteEintragEntry.config(font="Consolas 11 italic")
        zeigeEintraegeButton.config(text="Einträge verbergen", command=verbergeEintraege)
        
        # Funktion zum Löschen des Platzhalters des Feldes zur Eingabe der ID, dessen Eintrag gelöscht werden soll
        def loeschePlatzhalterDelete(event):
            loescheEintragEntry.delete(0, END)
            loescheEintragEntry.unbind('<Button-1>', loeschePHdeleteBind)
        loeschePHdeleteBind = loescheEintragEntry.bind('<Button-1>', loeschePlatzhalterDelete)
        
        # Funktion zum Löschen des Platzhalters des Feldes zur Eingabe der ID, dessen Eintrag bearbeitet werden soll
        def loeschePlatzhalterEdit(event):
            bearbeiteEintragEntry.delete(0, END)
            bearbeiteEintragEntry.unbind('<Button-1>', loeschePHeditBind)
        loeschePHeditBind = bearbeiteEintragEntry.bind('<Button-1>', loeschePlatzhalterEdit)
        
        augenButton()
        
        # Listet alle Einträge der Datenbank auf
        cursor.execute("SELECT *, oid FROM pwManager")
        eintraege = cursor.fetchall()
        angezeigteEintraege = ""
        for record in eintraege:
            angezeigteEintraege += "ID:" + "\t\t" + str(record[4])+ "\n" + "Name:" + "\t\t" + str(record[0])+ "\n" + "Nutzername:" + "\t\t" + str(record[1])+ "\n" + "URL:" + "\t\t" + str(record[2]) + "\n" + "Passwort:" "\t\t" + "**************" + "\n----------------------------------------------\n"
        textFensterEinträge.insert(END, angezeigteEintraege)
        textFensterEinträge.config(state=DISABLED)
        
    elif(x==4):
        # Listet alle Einträge der Datenbank auf
        cursor.execute("SELECT *, oid FROM pwManager")
        eintraege = cursor.fetchall()
        angezeigteEintraege = ""
        for record in eintraege:
            angezeigteEintraege += "ID:" + "\t\t" + str(record[4])+ "\n" + "Name:" + "\t\t" + str(record[0])+ "\n" + "Nutzername:" + "\t\t" + str(record[1])+ "\n" + "URL:" + "\t\t" + str(record[2]) + "\n" + "Passwort:" "\t\t" + "**************" + "\n----------------------------------------------\n"
        textFensterEinträge.insert(END, angezeigteEintraege)
        textFensterEinträge.config(state=DISABLED)
        
    # Speichern der Änderungen und Schließen der Datenbankverbindung
    conn.commit()
    conn.close()
    # Verschlüsseln der Datenbank
    verschluessleDB()

# Global variables
global nameEingabeEntry, nutzerNameEingabeEntry, urlEingabeEntry, passwortEingabeEntry

# Create Text Boxes
nameEingabeEntry = Entry(root, width=25, bg=entryHGFarbe)
nameEingabeEntry.grid(row=0, column=1, padx=25, pady=5)
nutzerNameEingabeEntry = Entry(root, width=25, bg=entryHGFarbe)
nutzerNameEingabeEntry.grid(row=1, column=1, padx=20, pady=5)
urlEingabeEntry = Entry(root, width=25, bg=entryHGFarbe)
urlEingabeEntry.grid(row=2, column=1, padx=20, pady=5)
passwortEingabeEntry = Entry(root, width=25, show="*", bg=entryHGFarbe)
passwortEingabeEntry.grid(row=4, column=1, padx=20, pady=5)

# Erzeugt die Labels für die Passwortkriterien
nameEingabeLabel = Label(root, text="Name:", fg=textFarbe, bg=hintergrundFarbe)
nameEingabeLabel.grid(row=0, column=0)
nutzerNameEingabeLabel = Label(root, text="Nutzername:", fg=textFarbe, bg=hintergrundFarbe)
nutzerNameEingabeLabel.grid(row=1, column=0)
urlEingabeLabel = Label(root, text="URL (optional):", fg=textFarbe, bg=hintergrundFarbe)
urlEingabeLabel.grid(row=2, column=0)
passwortEingabeLabel = Label(root, text="Passwort:", fg=textFarbe, bg=hintergrundFarbe)
passwortEingabeLabel.grid(row=4, column=0)

# Erzeugt die Radiobuttons
wahlRadio = StringVar()
manuellRadio = Radiobutton(root, text="Manuell", variable=wahlRadio, value="M", command=autoOderManuell, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe)
manuellRadio.grid(row=3, column=1, sticky="w", padx=18)
autoRadio = Radiobutton(root, text="Automatisch", variable=wahlRadio, value="A", command=autoOderManuell, fg=textFarbe, bg=hintergrundFarbe, selectcolor=buttonHGFarbe)
autoRadio.grid(row=3, column=1, sticky="e", padx=25)
# Standardmäßig wird manuell ausgewählt
manuellRadio.select()

# Erzeugt den Button, der zum Passwortgenerator führt
zumPWGeneratorButton = Button(root, text="PW generieren", command=passwortGeneratorFenster, state=DISABLED, fg=textFarbe, bg=hintergrundFarbe)
zumPWGeneratorButton.grid(row=3, column=0)

# Erzeugt den Button, mit dem man den Eintrag der Datenbank hinzufügen kann
fuegeEintragHinzuButton = Button(root, text="Eintrag hinzufügen", command=fuegeEintragHinzu, fg=textFarbe, bg=hintergrundFarbe)
fuegeEintragHinzuButton.grid(row=5, column=0, padx=10, pady=20)

# Erzeugt den Button, mit dem man die Einträge der Datenbank anzeigen lassen kann
zeigeEintraegeButton = Button(root, text="Einträge anzeigen", command= lambda: showRecords(3), fg=textFarbe, bg=hintergrundFarbe)
zeigeEintraegeButton.grid(row=5, column=1, pady=20)






root.mainloop()