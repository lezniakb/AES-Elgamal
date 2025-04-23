# pip install customtkinter
# pip install ctkmessagebox

import customtkinter as ct
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

from elgamal import generujKluczeElgamal, elgamalPodpis, elgamalWeryfikuj

# funkcje obslugi plikow

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


def wybierzPodpis():
    filename = filedialog.askopenfilename(defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        odszyfrowanie.delete("0.0", tk.END)
        odszyfrowanie.insert("0.0", content)
        CTkMessagebox(title="success", message="Plik wczytany pomyślnie!", icon="info", icon_size=(61, 61))

def zapiszPlik():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            content = kodowanie.get("0.0", ct.END)
            f.write(content)
        CTkMessagebox(title="success", message="Plik zapisany pomyślnie!", icon="info", icon_size=(61, 61))

def zapiszPodpis():
    """zapisz podpis (z dolnego pola tekstowego) do pliku"""
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            content = odszyfrowanie.get("0.0", ct.END)
            f.write(content)
        CTkMessagebox(title="success", message="Plik zapisany pomyślnie!", icon="info", icon_size=(61, 61))



def wczytajklucz():
    """
    zaladuj klucze elgamal z pliku.
    plik powinien zawierac cztery liczby oddzielone przecinkami: q, a, xa, ya.
    """
    global elgamalklucze
    filename = filedialog.askopenfilename(defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        try:
            parts = content.split(',')
            if len(parts) != 4:
                raise ValueError("Błąd pliku: oczekiwano 4 liczb oddzielonych przecinkami")
            q = int(parts[0].strip())
            a = int(parts[1].strip())
            xa = int(parts[2].strip())
            ya = int(parts[3].strip())
            elgamalklucze = (q, a, xa, ya)
            klucz.delete(0, ct.END)
            klucz.insert(0, content)
            CTkMessagebox(title="success", message="Klucze wczytane!", icon="info", icon_size=(61, 61))
        except Exception as e:
            CTkMessagebox(title="error", message="Błąd przy wczytywaniu kluczy: " + str(e), icon="warning", icon_size=(61, 61))


# operacje podpisu cyfrowego

# globalna zmienna dla kluczow elgamal: (q, a, xa, ya)
elgamalklucze = None

def generujklucze():
    """generuj klucze elgamal do podpisu cyfrowego i wyswietl je"""
    global elgamalklucze
    elgamalklucze = generujKluczeElgamal()
    keysStr = f"{elgamalklucze[0]}, {elgamalklucze[1]}, {elgamalklucze[2]}, {elgamalklucze[3]}"
    klucz.delete(0, ct.END)
    klucz.insert(0, keysStr)
    msg = (
        f"klucze wygenerowane:\n"
        f"q = {elgamalklucze[0]}\n"
        f"a (pierwotny pierwiastek) = {elgamalklucze[1]}\n"
        f"klucz prywatny, xa = {elgamalklucze[2]}\n"
        f"klucz publiczny, ya = {elgamalklucze[3]}"
    )
    CTkMessagebox(title="success", message=msg, icon="info", icon_size=(61, 61))

def podpisz():
    """
    podpisz wiadomosc z gornego pola tekstowego uzywajac podpisu cyfrowego elgamal.
    podpis (s1,s2) jest wyswietlany w dolnym polu tekstowym.
    """
    global elgamalklucze
    if elgamalklucze is None:
        CTkMessagebox(title="error", message="najpierw wygeneruj lub zaladuj klucze!", icon="warning", icon_size=(61, 61))
        return
    message = kodowanie.get("0.0", ct.END).strip()
    if not message:
        CTkMessagebox(title="error", message="brak wiadomosci do podpisania!", icon="warning", icon_size=(61, 61))
        return
    signature = elgamalPodpis(message, elgamalklucze)
    sigStr = f"{signature[0]},{signature[1]}"
    odszyfrowanie.delete("0.0", tk.END)
    odszyfrowanie.insert("0.0", sigStr)
    CTkMessagebox(title="success", message="wiadomosc podpisana pomyslnie!", icon="check", icon_size=(61, 61))

def weryfikuj():
    """
    sprawdz podpis wiadomosci.
    wiadomosc pobierana jest z gornego pola tekstowego, a podpis (w formacie s1,s2)
    z dolnego pola tekstowego.
    """
    global elgamalklucze
    if elgamalklucze is None:
        CTkMessagebox(title="error", message="najpierw wygeneruj lub zaladuj klucze!", icon="warning", icon_size=(61, 61))
        return
    message = kodowanie.get("0.0", ct.END).strip()
    sigText = odszyfrowanie.get("0.0", ct.END).strip()
    if not message or not sigText:
        CTkMessagebox(title="error", message="brak wiadomosci lub podpisu!", icon="warning", icon_size=(61, 61))
        return
    try:
        parts = sigText.split(',')
        if len(parts) != 2:
            raise ValueError("blad formatu podpisu: oczekiwano formatu 's1,s2'.")
        s1 = int(parts[0].strip())
        s2 = int(parts[1].strip())
        signature = (s1, s2)
    except Exception as e:
        CTkMessagebox(title="error", message="blad przy odczycie podpisu: " + str(e), icon="warning", icon_size=(61, 61))
        return
    if elgamalWeryfikuj(message, signature, elgamalklucze):
        CTkMessagebox(title="success", message="podpis jest poprawny!", icon="check", icon_size=(61, 61))
    else:
        CTkMessagebox(title="error", message="podpis jest niepoprawny!", icon="warning", icon_size=(61, 61))


# funkcje pomocnicze gui

def ustawokno():
    tytul = "Podpis cyfrowy ElGamal"
    szerokosc = root.winfo_screenwidth()
    wysokosc = root.winfo_screenheight()
    # zmniejsz okno wzgledem pelnego ekranu
    szerokosc = int(szerokosc / 1.4)
    wysokosc = int(wysokosc / 1.2)
    rozszerzalnosc = [False, False]
    czcionka = ("segoe ui", szerokosc // 70)
    return [tytul, szerokosc, wysokosc, rozszerzalnosc, czcionka]

def oknotekstowe(root, width=100, height=100, palette=None, **kwargs):
    okno = ct.CTkFrame(root, **kwargs)
    wpisane = ct.CTkTextbox(okno, fg_color=palette["podstawowy2"], width=width, height=height)
    wpisane.pack(fill="both", expand=True)

    def get(start, end=None):
        tekst = wpisane.get("0.0", ct.END)
        if tekst == "\n":
            return ""
        if end is not None:
            txt = wpisane.get(start, end)
            return txt[:-1]
        else:
            return tekst[:-1]

    def insert(start, text, tags=None):
        return wpisane.insert(start, text, tags)

    def delete(start, end=None):
        return wpisane.delete(start, end)

    okno.get = get
    okno.insert = insert
    okno.delete = delete
    okno.wpisane = wpisane
    return okno

# inicjalizacja gui

kolory = {
    "podstawowy1": "#1A1A19",
    "podstawowy2": "#123524",
    "tekst": "#FFFFFF",
}

root = ct.CTk()
ustawienia = ustawokno()
root.title(ustawienia[0])
root.geometry(f"{ustawienia[1]}x{ustawienia[2]}")
root.resizable(ustawienia[3][0], ustawienia[3][1])

# glowna ramka
ramka = ct.CTkFrame(root, fg_color=kolory["podstawowy1"])
ramka.pack(padx=40, pady=40, fill="both", expand=True)

# etykieta dla podpisywania
napispodpisywania = ct.CTkLabel(
    ramka, text="Podpis cyfrowy ElGamal",
    fg_color=kolory["podstawowy1"],
    text_color=kolory["tekst"],
    font=ustawienia[4]
)
napispodpisywania.pack(padx=10, pady=0)

# pole tekstowe dla wiadomosci do podpisania
rozmiaryOkna = [int(ustawienia[1] / 1.5), ustawienia[2] // 7]
kodowanie = oknotekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
kodowanie.pack(padx=10, pady=5)

# ramka dla przyciskow i operacji na kluczach
srodek = ct.CTkFrame(ramka, width=(ustawienia[1] // 3), height=(int(ustawienia[2] / 3.5)), corner_radius=0)
srodek.pack(padx=10, pady=10, fill="both", expand=False)

# przyciski w ramce srodek
kodowaniePlik = ct.CTkButton(
    srodek, text="Wczytaj plik", font=ustawienia[4],
    width=(ustawienia[1] // 6), height=(ustawienia[2] // 15),
    command=wybierzPlik
)

zapiszPlikOryginalny = ct.CTkButton(
    srodek, text="Zapisz Plik", font=ustawienia[4],
    width=(ustawienia[1] // 6), height=(ustawienia[2] // 15),
    command=zapiszPlik
)

podpiszBtn = ct.CTkButton(
    srodek, text="Podpisz \u2193", font=ustawienia[4],
    width=(ustawienia[1] // 4), height=(ustawienia[2] // 14),
    command=podpisz
)
weryfikujBtn = ct.CTkButton(
    srodek, text="Zweryfikuj \u2191", font=ustawienia[4],
    width=(ustawienia[1] // 4), height=(ustawienia[2] // 14),
    command=weryfikuj
)

# przyciski do operacji na kluczach
generator = ct.CTkButton(
    srodek, text="Generuj klucze", font=ustawienia[4],
    width=(ustawienia[1] // 6),
    command=generujklucze
)
klucz = ct.CTkEntry(
    srodek, font=ustawienia[4],
    width=(int(ustawienia[1] / 1.5)), height=(ustawienia[2] // 18),
    placeholder_text="Klucze: q, a, xa, ya"
)
wczytywaczKlucza = ct.CTkButton(
    srodek, text="Wczytaj klucze z pliku", font=ustawienia[4],
    width=(ustawienia[1] // 6),
    command=wczytajklucz
)

# umiesc przyciski w ramce srodek
kodowaniePlik.place(relx=0.25, rely=0.25, anchor=tk.CENTER)
zapiszPlikOryginalny.place(relx=0.45, rely=0.25, anchor=tk.CENTER)
podpiszBtn.place(relx=0.70, rely=0.20, anchor=tk.CENTER)
weryfikujBtn.place(relx=0.70, rely=0.50, anchor=tk.CENTER)
generator.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
wczytywaczKlucza.place(relx=0.45, rely=0.55, anchor=tk.CENTER)
klucz.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

# etykieta dla podpisu (wyswietlanego lub wprowadzania przy weryfikacji)
napisweryfikacji = ct.CTkLabel(
    ramka, text="Podpis (S1, S2)",
    fg_color=kolory["podstawowy1"],
    text_color=kolory["tekst"],
    font=ustawienia[4]
)
napisweryfikacji.pack(padx=10, pady=0)

# pole tekstowe dla podpisu (wyswietlanego lub wprowadzania przy weryfikacji)
odszyfrowanie = oknotekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
odszyfrowanie.pack(padx=10, pady=5)

# przyciski do operacji na podpisie
wczytajPlikBtn = ct.CTkButton(
    ramka, text="Wczytaj podpis z pliku", font=ustawienia[4],
    width=(int(ustawienia[1] / 3)), height=(int(ustawienia[2] / 17)),
    command=wybierzPlik
)
wczytajPlikBtn.pack(padx=10, pady=5)

zapiszBtn = ct.CTkButton(
    ramka, text="Zapisz podpis do pliku", font=ustawienia[4],
    width=(int(ustawienia[1] / 3)), height=(int(ustawienia[2] / 17)),
    command=zapiszPodpis
)
zapiszBtn.pack(padx=10, pady=5)

root.mainloop()
