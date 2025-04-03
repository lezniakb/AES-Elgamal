# pip install customtkinter
# pip install CTkMessagebox

import customtkinter as ct
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

from elgamal import modinv, prime_factors, find_primitive_root, generate_elgamal_keys, elgamal_sign, elgamal_verify

# =========================================
# File Handling Functions
# =========================================

def wybierzPlik():
    """Load message from a text file into the input field."""
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        kodowanie.delete("0.0", tk.END)
        kodowanie.insert("0.0", content)


def wczytajKlucz():
    """
    Load ElGamal keys from a file.
    The file should contain four comma‐separated numbers: q, a, XA, YA.
    """
    global elgamal_keys
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        try:
            parts = content.split(',')
            if len(parts) != 4:
                raise ValueError("Key file format error: expected 4 numbers separated by commas.")
            q = int(parts[0].strip())
            a = int(parts[1].strip())
            XA = int(parts[2].strip())
            YA = int(parts[3].strip())
            elgamal_keys = (q, a, XA, YA)
            klucz.delete(0, ct.END)
            klucz.insert(0, content)
            CTkMessagebox(title="Success", message="Keys loaded successfully!", icon="info", icon_size=(61, 61))
        except Exception as e:
            CTkMessagebox(title="Error", message="Error loading keys: " + str(e), icon="warning", icon_size=(61, 61))


def zapiszPlik():
    """Save the signature (from the lower text box) to a file."""
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            content = odszyfrowanie.get("0.0", ct.END)
            f.write(content)
        CTkMessagebox(title="Success", message="File saved successfully!", icon="info", icon_size=(61, 61))


# =========================================
# Digital Signature Operations
# =========================================

# Global variable for ElGamal keys: (q, a, XA, YA)
elgamal_keys = None


def generujKlucze():
    """Generate ElGamal keys for the digital signature and display them."""
    global elgamal_keys
    elgamal_keys = generate_elgamal_keys()
    keys_str = f"{elgamal_keys[0]}, {elgamal_keys[1]}, {elgamal_keys[2]}, {elgamal_keys[3]}"
    klucz.delete(0, ct.END)
    klucz.insert(0, keys_str)
    msg = (
        f"Keys generated:\n"
        f"q = {elgamal_keys[0]}\n"
        f"a (primitive root) = {elgamal_keys[1]}\n"
        f"Private key, XA = {elgamal_keys[2]}\n"
        f"Public key, YA = {elgamal_keys[3]}"
    )
    CTkMessagebox(title="Success", message=msg, icon="info", icon_size=(61, 61))


def podpisz():
    """
    Sign the message from the top text box using ElGamal digital signature.
    The signature (S1,S2) is displayed in the lower text box.
    """
    global elgamal_keys
    if elgamal_keys is None:
        CTkMessagebox(title="Error", message="Generate or load keys first!", icon="warning", icon_size=(61, 61))
        return
    message = kodowanie.get("0.0", ct.END).strip()
    if not message:
        CTkMessagebox(title="Error", message="No message to sign!", icon="warning", icon_size=(61, 61))
        return
    signature = elgamal_sign(message, elgamal_keys)
    sig_str = f"{signature[0]},{signature[1]}"
    odszyfrowanie.delete("0.0", tk.END)
    odszyfrowanie.insert("0.0", sig_str)
    CTkMessagebox(title="Success", message="Message signed successfully!", icon="check", icon_size=(61, 61))


def weryfikuj():
    """
    Verify the signature for the message.
    The message is taken from the top text box and the signature (in the format S1,S2)
    from the lower text box.
    """
    global elgamal_keys
    if elgamal_keys is None:
        CTkMessagebox(title="Error", message="Generate or load keys first!", icon="warning", icon_size=(61, 61))
        return
    message = kodowanie.get("0.0", ct.END).strip()
    sig_text = odszyfrowanie.get("0.0", ct.END).strip()
    if not message or not sig_text:
        CTkMessagebox(title="Error", message="Message or signature missing!", icon="warning", icon_size=(61, 61))
        return
    try:
        parts = sig_text.split(',')
        if len(parts) != 2:
            raise ValueError("Signature format error: expected format 'S1,S2'.")
        S1 = int(parts[0].strip())
        S2 = int(parts[1].strip())
        signature = (S1, S2)
    except Exception as e:
        CTkMessagebox(title="Error", message="Error parsing signature: " + str(e), icon="warning", icon_size=(61, 61))
        return
    if elgamal_verify(message, signature, elgamal_keys):
        CTkMessagebox(title="Success", message="Signature is valid!", icon="check", icon_size=(61, 61))
    else:
        CTkMessagebox(title="Error", message="Signature is invalid!", icon="warning", icon_size=(61, 61))


# =========================================
# GUI Helper Functions
# =========================================

def ustawOkno():
    tytul = "ElGamal Digital Signature"
    szerokosc = root.winfo_screenwidth()
    wysokosc = root.winfo_screenheight()
    # Scale the window down relative to full screen dimensions
    szerokosc = int(szerokosc / 1.4)
    wysokosc = int(wysokosc / 1.2)
    rozszerzalnosc = [False, False]
    czcionka = ("Segoe UI", szerokosc // 70)
    return [tytul, szerokosc, wysokosc, rozszerzalnosc, czcionka]


def oknoTekstowe(root, width=100, height=100, palette=None, **kwargs):
    """
    Creates a text area inside a CTkFrame.
    Returns the frame with helper methods: get, insert, and delete.
    """
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


# =========================================
# Initialize the GUI
# =========================================

kolory = {
    "podstawowy1": "#1A1A19",
    "podstawowy2": "#123524",
    "podstawowy3": "#255F38",
    "podstawowy4": "#1F7D53",
    "tekst": "#FFFFFF",
    "tekstWylaczony": "#808080"
}

root = ct.CTk()
ustawienia = ustawOkno()
root.title(ustawienia[0])
root.geometry(f"{ustawienia[1]}x{ustawienia[2]}")
root.resizable(ustawienia[3][0], ustawienia[3][1])

# Main frame
ramka = ct.CTkFrame(root, fg_color=kolory["podstawowy1"])
ramka.pack(padx=40, pady=40, fill="both", expand=True)

# Label for signing
napisPodpisywania = ct.CTkLabel(
    ramka, text="ElGamal Digital Signature",
    fg_color=kolory["podstawowy1"],
    text_color=kolory["tekst"],
    font=ustawienia[4]
)
napisPodpisywania.pack(padx=10, pady=0)

# Text area for message input (to be signed)
rozmiaryOkna = [int(ustawienia[1] / 1.5), ustawienia[2] // 7]
kodowanie = oknoTekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
kodowanie.pack(padx=10, pady=5)

# Frame for buttons and key operations
srodek = ct.CTkFrame(ramka, width=(ustawienia[1] // 3), height=(int(ustawienia[2] / 3.5)), corner_radius=0)
srodek.pack(padx=10, pady=10, fill="both", expand=False)

# Buttons in the srodek frame
kodowaniePlik = ct.CTkButton(
    srodek, text="Load File", font=ustawienia[4],
    width=(ustawienia[1] // 4), height=(ustawienia[2] // 15),
    command=wybierzPlik
)
podpiszBtn = ct.CTkButton(
    srodek, text="Sign ↓", font=ustawienia[4],
    width=(ustawienia[1] // 4), height=(ustawienia[2] // 14),
    command=podpisz
)
weryfikujBtn = ct.CTkButton(
    srodek, text="Verify ↑", font=ustawienia[4],
    width=(ustawienia[1] // 4), height=(ustawienia[2] // 14),
    command=weryfikuj
)

# Buttons for key operations
generator = ct.CTkButton(
    srodek, text="Generate Keys", font=ustawienia[4],
    command=generujKlucze
)
klucz = ct.CTkEntry(
    srodek, font=ustawienia[4],
    width=(int(ustawienia[1] / 1.5)), height=(ustawienia[2] // 18),
    placeholder_text="Keys: q, a, XA, YA"
)
wczytywaczKlucza = ct.CTkButton(
    srodek, text="Load Keys from File", font=ustawienia[4],
    command=wczytajKlucz
)

# Place the buttons in the srodek frame.
kodowaniePlik.place(relx=0.30, rely=0.25, anchor=tk.CENTER)
podpiszBtn.place(relx=0.70, rely=0.20, anchor=tk.CENTER)
weryfikujBtn.place(relx=0.70, rely=0.50, anchor=tk.CENTER)
generator.place(relx=0.15, rely=0.55, anchor=tk.CENTER)
wczytywaczKlucza.place(relx=0.47, rely=0.55, anchor=tk.CENTER)
klucz.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

# Label for signature (displayed or to be entered for verification)
napisWeryfikacji = ct.CTkLabel(
    ramka, text="Signature (S1,S2)",
    fg_color=kolory["podstawowy1"],
    text_color=kolory["tekst"],
    font=ustawienia[4]
)
napisWeryfikacji.pack(padx=10, pady=0)

# Text area for signature output (or manual input for verification)
odszyfrowanie = oknoTekstowe(ramka, width=rozmiaryOkna[0], height=rozmiaryOkna[1], palette=kolory)
odszyfrowanie.pack(padx=10, pady=5)

# Buttons for file operations on the signature
wczytajPlikBtn = ct.CTkButton(
    ramka, text="Load Signature from File", font=ustawienia[4],
    width=(int(ustawienia[1] / 3)), height=(int(ustawienia[2] / 17)),
    command=lambda: None  # Optional: you can add a similar function if desired
)
wczytajPlikBtn.pack(padx=10, pady=5)

zapiszBtn = ct.CTkButton(
    ramka, text="Save Signature to File", font=ustawienia[4],
    width=(int(ustawienia[1] / 3)), height=(int(ustawienia[2] / 17)),
    command=zapiszPlik
)
zapiszBtn.pack(padx=10, pady=5)

root.mainloop()
