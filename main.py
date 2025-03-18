# pip install customtkinter
# https://customtkinter.tomschimansky.com/
# koniecznie trzeba potem zrobic z pythona .exe !

# gui
import customtkinter as ct
import tkinter as tk

def ustawOkno():
    tytul = "Zaszyfruj i odszyfruj AES"
    szerokosc = root.winfo_screenwidth()
    wysokosc = root.winfo_screenheight()

    # wez dane z monitora uzytkownika i zmniejsz
    szerokosc = int(szerokosc / 1.4)
    wysokosc = int(wysokosc / 1.2)

    rozszerzalnosc = [False, False]

    return [tytul, szerokosc, wysokosc, rozszerzalnosc]

def oknoTekstowe(root, width=100, height=100, palette=None, **kwargs):
    # utworz ramke (okno) jako tlo oraz pole tekstowe
    okno = ct.CTkFrame(root, **kwargs)
    wpisane = ct.CTkTextbox(okno, fg_color=palette["podstawowy2"], width=width, height=height)
    wpisane.pack(fill="both", expand=True)

    # funkcja ktora bierze tekst (od znaku index1 do index2)
    def get(poczatek, koniec=None):
        # wez tekst z calego pola
        tekst = wpisane.get("0.0", ct.END)

        # jesli tekst jest pustym znakiem nowej linii no to zwroc pusty string
        if tekst == "\n":
            return ""

        # jesli koniec (pozycja konca tekstu) zostal ustawiony
        if koniec is not None:
            # to wez tekst miedzy tymi indeksami
            tekst = wpisane.get(poczatek, koniec)
            # i usun ostatni znak nowej linii
            tekst = tekst[:-1]
            return tekst

        # w przeciwnym wypadku wez tekst od poczatku do konca pola tekstowego
        else:
            # to wez tekst miedzy tymi indeksami
            tekst = wpisane.get(poczatek, ct.END)
            # i usun ostatni znak nowej linii
            tekst = tekst[:-1]
            return tekst

    # wpisuje podany tekst do okna (automatyczne wpisywanie np. z pliku); tags jest do ewentualnych wyjatkow
    def insert(poczatek, txt, tags=None):
        return wpisane.insert(poczatek, txt, tags)

    # usuwa tekst z okna w podanym przedziale. bez wpisania konca usuwa wszystko
    def delete(poczatek, koniec=None):
        return wpisane.delete(poczatek, koniec)

    okno.get = get
    okno.insert = insert
    okno.delete = delete
    okno.wpisane = wpisane

    return okno

def wykonaj():
    return True

def generujKlucz():
    return True

def wczytajKlucz():
    return True

# -------------------------
# main
# paleta barw
kolory = {"podstawowy1":"#18230F",
          "podstawowy2":"#27391C",
          "podstawowy3":"#255F38",
          "podstawowy4":"#1F7D53",
          "tekst":"#FFFFFF",
          "tekstWylaczony":"#808080"}

klucze = ["128 bit",
          "192 bit",
          "256 bit"]
# otworz okno dla tkintera (custom)
root = ct.CTk()

# ustawienia = tytul, szerokosc, wysokosc
ustawienia = ustawOkno()

root.title(ustawienia[0])
root.geometry(f"{ustawienia[1]}x{ustawienia[2]}")
root.resizable(ustawienia[3][0], ustawienia[3][1])
# wstaw ramke do programu
ramka = ct.CTkFrame(root, fg_color=kolory["podstawowy1"])
ramka.pack(padx=40, pady=40, fill="both", expand=True)

napisKodowania = ct.CTkLabel(ramka, text="Szyfrowanie AES", fg_color=kolory["podstawowy1"],
                             text_color=(kolory["tekst"]),
                             font=("Segoe UI", 26))
napisKodowania.pack(padx=10, pady=0)

# rozmiar okna szerokosc, wysokosc
rozmiaryOkna = [int(ustawienia[1]/1.5),ustawienia[2] //7]

# wstaw okno do zakodowania tekstu
kodowanie = oknoTekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
kodowanie.pack(padx=10, pady=5)

# wstaw plansze na srodku z opcjami
srodek = ct.CTkFrame(ramka, width=(ustawienia[1] //3), height=(int(ustawienia[2] /3.5)), corner_radius=0)
srodek.pack(padx=10, pady=10, fill="both", expand=False)

# przyciski w srodku
# wczytywanie z pliku
kodowaniePlik = ct.CTkButton(srodek, text="Wczytaj plik", width=(ustawienia[1]//4), height=(ustawienia[2]//10), command=lambda: choose_file(False))

# szyfruj / odszyfruj
szyfrOdszyfr = ct.CTkButton(srodek, text="Zaszyfruj / Odszyfruj",  width=(ustawienia[1]//4), height=(ustawienia[2]//10), command=wykonaj)

# wybor klucza
wyborKluczaTxt = ct.StringVar(value="Rozmiar klucza")
listaKluczy = ct.CTkComboBox(srodek, values=klucze, variable=wyborKluczaTxt)
generator = ct.CTkButton(srodek, text="Wygeneruj klucz!", command=generujKlucz)
klucz = ct.CTkEntry(srodek, width=(int(ustawienia[1]/1.5)), placeholder_text="Klucz")
wczytywaczKlucza = ct.CTkButton(srodek, text="Wczytaj klucz z pliku", command=wczytajKlucz)

# wstaw przyciski
kodowaniePlik.place(relx=0.30, rely=0.20, anchor=tk.CENTER)
szyfrOdszyfr.place(relx=0.70, rely=0.20, anchor=tk.CENTER)

# wstaw pole do generowania kluczy
listaKluczy.place(relx=0.213, rely=0.55, anchor=tk.CENTER)
generator.place(relx=0.40, rely=0.55, anchor=tk.CENTER)
klucz.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
wczytywaczKlucza.place(relx=0.788, rely=0.55, anchor=tk.CENTER)

napisOdszyfrowania = ct.CTkLabel(ramka, text="Deszfyrowanie AES", fg_color=kolory["podstawowy1"],
                             text_color=(kolory["tekst"]),
                             font=("Segoe UI", 26))
napisOdszyfrowania.pack(padx=10, pady=0)

# wstaw okno do  tekstu
odszyfrowanie = oknoTekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
odszyfrowanie.pack(padx=10, pady=5)

# odszyfr z pliku
odszyfrPliku = ct.CTkButton(ramka, text="Odszyfruj plik", width=(int(ustawienia[1]/3)), command=lambda: choose_file(True))
odszyfrPliku.pack(padx=10, pady=10)
root.mainloop()

"""
TODO:
1. reszta GUI
2. zmienić kolory w słowniku "kolory" (to jest główne miejsce z którego zaciągane są kolorki
"""