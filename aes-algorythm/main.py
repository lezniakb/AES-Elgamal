# pip install customtkinter
# https://customtkinter.tomschimansky.com/
# koniecznie trzeba potem zrobic z pythona .exe !

# gui
import customtkinter as ct
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

from crypto.Random import get_random_bytes
from random import choice
import string
from AES import zakodujTekst, odszyfrujTekst

def ustawOkno():
    tytul = "Zaszyfruj i odszyfruj AES"
    szerokosc = root.winfo_screenwidth()
    wysokosc = root.winfo_screenheight()
    print(f"[INFO] pierwotnie: szerokość={szerokosc}, wysokość={wysokosc}")

    # wez dane z monitora uzytkownika i zmniejsz
    szerokosc = int(szerokosc / 1.4)
    wysokosc = int(wysokosc / 1.2)

    rozszerzalnosc = [False, False]

    czcionka = ("Segoe UI", szerokosc//70)

    print(f"[INFO] szerokość={szerokosc}, wysokość={wysokosc}, czcionka={czcionka}")
    return [tytul, szerokosc, wysokosc, rozszerzalnosc, czcionka]

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

def sprawdzKlucz():
    kluczTekstowy = klucz.get().strip()

    # jesli nic nie podano w polu z kluczem to wyrzuc blad
    if not kluczTekstowy:
        CTkMessagebox(title="Wystąpił błąd!!", message="Podaj klucz", icon="warning", icon_size=(61,61))
        return None

    if wyborKluczaTxt.get().strip() not in ("128 bit", "192 bit", "256 bit"):
        CTkMessagebox(title="Wystąpił błąd!!", message="Wybierz odpowiedni rozmiar klucza", icon="warning", icon_size=(61,61))
        return None

    bitow = wyborKluczaTxt.get()
    bitow = bitow.split()[0]
    bitow = int(bitow)

    if bitow == 128:
        spodziewanaDlugosc = 16
    elif bitow == 192:
        spodziewanaDlugosc = 24
    else:
        spodziewanaDlugosc = 32

    if len(kluczTekstowy) != spodziewanaDlugosc:
        CTkMessagebox(title="Wystąpił błąd!!",
                      message=f"Podany klucz musi mieć {spodziewanaDlugosc} znaków (dla klucza {bitow} bit)",
                      icon="warning", icon_size=(61, 61))
        return None
    return kluczTekstowy, bitow

def szyfruj():
    # funkcja wykonujaca szyfrowanie lub odszyfrowanie
    sprawdzenie = sprawdzKlucz()
    if sprawdzenie == None:
        return
    else:
        kluczTekstowy, bitow = sprawdzenie
    kluczTekstowy = kluczTekstowy.encode("ascii").hex()
    # jezeli pole do szyfrowania zawiera tekst, szyfruj go
    tekst_jawny = kodowanie.get("0.0", ct.END).strip()
    if tekst_jawny:
        zaszyfrowany = zakodujTekst(tekst_jawny, kluczTekstowy, bitow)
        odszyfrowanie.delete("0.0", tk.END)
        odszyfrowanie.insert("0.0", zaszyfrowany)
        CTkMessagebox(title="Udało się!!", message="Tekst został pomyślnie zaszyfrowany!", icon="check", icon_size=(61,61))


def odszyfruj():
    sprawdzenie = sprawdzKlucz()
    if sprawdzenie == None:
        return
    else:
        kluczTekstowy, bitow = sprawdzenie
    kluczTekstowy = kluczTekstowy.encode("ascii").hex()
    zaszyfrowany = odszyfrowanie.get("0.0", ct.END).strip()
    if not zaszyfrowany:
        CTkMessagebox(title="Wystąpił błąd", message="Brak danych do odszyfrowania", icon="warning", icon_size=(61, 61))
        return

    jawny = odszyfrujTekst(zaszyfrowany, kluczTekstowy, bitow)

    kodowanie.delete("0.0", tk.END)
    kodowanie.insert("0.0", jawny)

    CTkMessagebox(title="Sukces", message="Tekst został odszyfrowany!", icon="check", icon_size=(61, 61))

def generujKlucz():
    # pobierz wybrany rozmiar klucza
    rozmiar_klucza = wyborKluczaTxt.get()
    rozmiar_map = {"128 bit": 16, "192 bit": 24, "256 bit": 32}
    if rozmiar_klucza not in rozmiar_map:
        CTkMessagebox(title="Wystąpił błąd!!", message="Proszę wybrać poprawny klucz (np. 256 bit)", icon="warning", icon_size=(61,61))
        return
    kluczTekstowy = ""
    for i in range(rozmiar_map[rozmiar_klucza]):
        litera = choice(string.ascii_letters + string.digits)
        kluczTekstowy += litera
    klucz.delete(0, ct.END)
    klucz.insert(0, kluczTekstowy)
    CTkMessagebox(title="Udało się", message="Wygenerowano klucz", icon="info", icon_size=(61,61))

def wczytajKlucz():
    # funkcja do wczytywania klucza z pliku, uzywamy istniejacego okna
    sciezka_pliku = filedialog.askopenfilename(
        title="Wybierz plik z kluczem",
        filetypes=[("pliki tekstowe", "*.txt"), ("wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        CTkMessagebox(title="Uwaga!", message="Nie wybrano pliku z kluczem", icon="info", icon_size=(61,61))
        return
    with open(sciezka_pliku, "rb") as plik:
        klucz_odczytany = plik.read()
    klucz.delete(0, tk.END)
    klucz.insert(0, klucz_odczytany.decode("utf-8"))
    CTkMessagebox(title="Udało się!", message="Klucz został wczytany pomyślnie!", icon="check", icon_size=(61,61))

def zapiszOdkodowany():
    sciezka_pliku = filedialog.asksaveasfilename(
        title="Zapisz odszyfrowany plik",
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        CTkMessagebox(title="Uwaga", message="Nie wybrano miejsca do zapisu", icon="warning", icon_size=(61, 61))
        return
    tekst = kodowanie.get("0.0", tk.END)
    bajty = tekst.encode("utf-8", errors="surrogateescape")
    try:
        with open(sciezka_pliku, "wb") as plik:
            plik.write(bajty)
        CTkMessagebox(title="Sukces", message="Zapisano odszyfrowany plik!", icon="check", icon_size=(61, 61))
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie udało się zapisać pliku:\n{e}", icon="warning", icon_size=(61, 61))

def zapiszPlik():
    sciezka_pliku = filedialog.asksaveasfilename(
        title="Zapisz zaszyfrowany plik",
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        CTkMessagebox(title="Uwaga", message="Nie wybrano miejsca do zapisu", icon="warning", icon_size=(61,61))
        return
    tekst = odszyfrowanie.get("0.0", tk.END)
    try:
        with open(sciezka_pliku, "w", encoding="utf-8") as plik:
            plik.write(tekst)
        CTkMessagebox(title="Sukces", message="Zapisano zaszyfrowany plik!", icon="check", icon_size=(61,61))
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie udało się zapisać pliku:\n{e}", icon="warning", icon_size=(61,61))

def wczytajZaszyfrowany():
    sciezka_pliku = filedialog.askopenfilename(
        title="Wybierz plik zaszyfrowany",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        CTkMessagebox(title="Uwaga!", message="Nie wybrano pliku", icon="info", icon_size=(61,61))
        return
    with open(sciezka_pliku, "rb") as plik:
        zawartosc_pliku = plik.read()
    odszyfrowanie.delete("0.0", tk.END)
    odszyfrowanie.insert("0.0", zawartosc_pliku.decode("utf-8"))
    CTkMessagebox(title="Sukces", message="Plik został wczytany", icon="check", icon_size=(61,61))

def wybierzPlik():
    # funkcja do wyboru pliku do szyfrowania, uzywamy istniejacego okna
    sciezka_pliku = filedialog.askopenfilename(
        title="Wybierz plik do zaszyfrowania",
        filetypes=[("wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        CTkMessagebox(title="info", message="Nie wybrano pliku", icon="info", icon_size=(61,61))
        return
    with open(sciezka_pliku, "rb") as plik:
        zawartosc = plik.read()

    kodowanie.delete("0.0", tk.END)
    tekst = zawartosc.decode("utf-8", errors="surrogateescape")
    kodowanie.insert("0.0", tekst)
    CTkMessagebox(title="Udało się", message="Plik został wczytany", icon="check", icon_size=(61,61))


# -------------------------
# main
# paleta barw
kolory = {"podstawowy1":"#1A1A19",
          "podstawowy2":"#123524",
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

# label z napisem zachecajacym do wprowadzenia tekstu
napisKodowania = ct.CTkLabel(ramka, text="Szyfrowanie AES", fg_color=kolory["podstawowy1"],
                             text_color=(kolory["tekst"]),
                             font=ustawienia[4])
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
kodowaniePlik = ct.CTkButton(srodek, text="Wczytaj plik", font=ustawienia[4], width=(ustawienia[1]//6), height=(ustawienia[2]//12), command=wybierzPlik)
zapisaniePlik = ct.CTkButton(srodek, text="Zapisz plik", font=ustawienia[4], width=(ustawienia[1]//6), height=(ustawienia[2]//12), command=zapiszOdkodowany)

# szyfruj i odszyfruj (przycisk)
szyfruj = ct.CTkButton(srodek, text="Zaszyfruj \u2193", font=ustawienia[4], width=(ustawienia[1]//4), height=(ustawienia[2]//14), command=szyfruj)
odszyfruj = ct.CTkButton(srodek, text="Odszyfruj \u2191", font=ustawienia[4], width=(ustawienia[1]//4), height=(ustawienia[2]//14), command=odszyfruj)

# wybor klucza
wyborKluczaTxt = ct.StringVar(value="Rozmiar klucza")
listaKluczy = ct.CTkComboBox(srodek, values=klucze, font=ustawienia[4], width=(ustawienia[1]//8), variable=wyborKluczaTxt)
generator = ct.CTkButton(srodek, text="Wygeneruj klucz!", font=ustawienia[4], command=generujKlucz)
klucz = ct.CTkEntry(srodek, font=ustawienia[4], width=(int(ustawienia[1]/1.5)), height=(ustawienia[2]//18), placeholder_text="Klucz")
wczytywaczKlucza = ct.CTkButton(srodek, text="Wczytaj klucz z pliku", font=ustawienia[4], command=wczytajKlucz)

# wstaw przyciski
kodowaniePlik.place(relx=0.20, rely=0.25, anchor=tk.CENTER)
zapisaniePlik.place(relx=0.42, rely=0.25, anchor=tk.CENTER)
szyfruj.place(relx=0.70, rely=0.20, anchor=tk.CENTER)
odszyfruj.place(relx=0.70, rely=0.50, anchor=tk.CENTER)

# wstaw pole do generowania kluczy
listaKluczy.place(relx=0.15, rely=0.55, anchor=tk.CENTER)
generator.place(relx=0.315, rely=0.55, anchor=tk.CENTER)
wczytywaczKlucza.place(relx=0.47, rely=0.55, anchor=tk.CENTER)
klucz.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

napisOdszyfrowania = ct.CTkLabel(ramka, text="Deszfyrowanie AES", fg_color=kolory["podstawowy1"],
                             text_color=(kolory["tekst"]),
                             font=ustawienia[4])
napisOdszyfrowania.pack(padx=10, pady=0)

# wstaw okno do  tekstu
odszyfrowanie = oknoTekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
odszyfrowanie.pack(padx=10, pady=5)

wczytajPlikBtn = ct.CTkButton(ramka, text="Wczytaj zaszyfrowany plik", font=ustawienia[4],
                              width=(int(ustawienia[1]/3)), height=(int(ustawienia[2]/17)), command=wczytajZaszyfrowany)
wczytajPlikBtn.pack(padx=10, pady=5)

zapiszBtn = ct.CTkButton(ramka, text="Zapisz zaszyfrowany plik", font=ustawienia[4],
                          width=(int(ustawienia[1]/3)), height=(int(ustawienia[2]/17)), command=zapiszPlik)
zapiszBtn.pack(padx=10, pady=5)

root.mainloop()