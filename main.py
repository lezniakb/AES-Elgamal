# pip install customtkinter
# https://customtkinter.tomschimansky.com/
# koniecznie trzeba potem zrobic z pythona .exe !

# gui
import customtkinter as ct

def ustawOkno():
    tytul = "Zaszyfruj i odszyfruj AES"
    szerokosc = root.winfo_screenwidth()
    wysokosc = root.winfo_screenheight()

    # wez dane z monitora uzytkownika i zmniejsz
    szerokosc = int(szerokosc / 1.7)
    wysokosc = int(wysokosc / 1.7)

    return [tytul, szerokosc, wysokosc]

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

# def wygenerujKlucz():

# -------------------------
# main
# paleta barw
kolory = {"podstawowy1":"#18230F",
          "podstawowy2":"#27391C",
          "podstawowy3":"#255F38",
          "podstawowy4":"#1F7D53",
          "tekst":"#FFFFFF",
          "tekstWylaczony":"#808080"}


# otworz okno dla tkintera (custom)
root = ct.CTk()

# ustawienia = tytul, szerokosc, wysokosc
ustawienia = ustawOkno()

root.title(ustawienia[0])
root.geometry(f"{ustawienia[1]}x{ustawienia[2]}")

# wstaw ramke do programu
ramka = ct.CTkFrame(root, fg_color=kolory["podstawowy1"])
ramka.pack(padx=40, pady=40, fill="both", expand=True)

napisKodowania = ct.CTkLabel(ramka, text="Szyfrowanie AES", fg_color=kolory["podstawowy1"],
                             text_color=(kolory["tekst"]),
                             font=("Segoe UI", 26))
napisKodowania.pack(padx=10, pady=10)

# wstaw okno do zakodowania tekstu
kodowanie = oknoTekstowe(ramka, width=700, height=200, palette=kolory)
kodowanie.pack(padx=10, pady=10)

root.mainloop()

"""
TODO:
1. reszta GUI
2. zmienić kolory w słowniku "kolory" (to jest główne miejsce z którego zaciągane są kolorki
"""