# **Passwort-Manager**

## Übersicht

- [Kurzbeschreibung](#Kurzbeschreibung)
- [Sicherheit/Privatsphäre](#SicherheitPrivatsphäre)
- [Vorbereitungen](#Vorbereitungen)
    - [Python installieren](#Python-installieren)
    - [Module installieren](#Module-installieren)
- [Verwendete Technologien](#Verwendete-Technologien)
- [Vorschau](#Vorschau)

---

## Kurzbeschreibung

Dieser Passwort-Manager wurde in Python geschrieben und mithilfe des integrierten Moduls Tkinter in Form einer grafischen Benutzeroberfläche (GUI) entwickelt. Hinzu kommt eine Datenbankanbindung mittels SQLite3 Modul und Verschlüsselung via Fernet. 

---

## Sicherheit/Privatsphäre

Dieses Programm läuft zu 100% offline. An keiner Stelle werden Daten nach außerhalb versendet und alle generierten bzw. gespeicherten Daten verbleiben höchstens auf dem eigenen Rechner. Der generierte Schlüssel ist demnach nur lokal verfügbar, sodass selbst ohne diesen die verschlüsselte Datenbank alleine für einen Angreifer unbrauchbar wäre.

Mit der Implementierung von [Fernet](https://cryptography.io/en/latest/fernet.html) wird die [symmetrische Verschlüsselung](https://de.wikipedia.org/wiki/Symmetrisches_Kryptosystem) gewährleistet, sodass eine damit verschlüsselte Datei nicht gelesen oder verändert werden kann, ohne den zugehörigen Schlüssel ebenfalls im Besitz zu haben.

---

## Vorbereitungen

### Python installieren

- **[python.org](https://www.python.org/downloads/)**

### Module installieren

- **[tkinter](https://docs.python.org/3/library/tkinter.html)**: _Standardmäßig in Python enthalten_
- **[sqlite3](https://docs.python.org/3/library/sqlite3.html)**: _Standardmäßig in Python enthalten_
- **[secrets](https://docs.python.org/3/library/secrets.html)**: _Standardmäßig in Python enthalten_
- **[random](https://docs.python.org/3/library/random.html)**: _Standardmäßig in Python enthalten_
- **[string](https://docs.python.org/3/library/string.html)**: _Standardmäßig in Python enthalten_
- **[pyperclip](https://pypi.org/project/pyperclip/)**: `pip install pyperclip`  
- **[cryptography](https://pypi.org/project/cryptography/)**: `pip install cryptography`
- **[os](https://docs.python.org/3/library/os.html)**: _Standardmäßig in Python enthalten_

---

## Verwendete Technologien

- **Python** 3.8.2
    - **Tkinter** 8.6
    - **SQLite** 2.6.0
    - **Cryptography** 3.4.6

---

## Vorschau

**Hinzufügen eines neuen Eintrags.** 

<img src="https://user-images.githubusercontent.com/80011395/115744095-c835a680-a381-11eb-86b5-8c1f722cb2ac.gif" width="380" height="220"/>

**Generieren eines sicheren Passworts mithilfe des integrierten Passwort-Generators.**

<img src="https://user-images.githubusercontent.com/80011395/115744174-da174980-a381-11eb-8b34-065ce2b1440a.gif" width="400" height="180"/>

**Anzeigen/Verbergen der Kennwörter mit einem Klick.**

<img src="https://user-images.githubusercontent.com/80011395/115744274-f3b89100-a381-11eb-81c5-8860d6d88d48.gif" width="300" height="500"/>

**Löschen und Bearbeiten eines Eintrags.**

<img src="https://user-images.githubusercontent.com/80011395/115744194-ddaad080-a381-11eb-8dfb-6416ab850cd4.gif" width="300" height="500">

---

[Nach oben](#Passwort-Manager)