# s-box i odwrocony s-box
# tablica, która służy do podstawienia bajtów w szyfrowaniu i deszyfrowaniu
sbox = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b,
    0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26,
    0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2,
    0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed,
    0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f,
    0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
    0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14,
    0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d,
    0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f,
    0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11,
    0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f,
    0xb0, 0x54, 0xbb, 0x16,
)

odwr_sbox = (
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e,
    0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
    0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32,
    0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49,
    0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50,
    0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05,
    0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
    0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
    0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8,
    0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
    0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b,
    0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59,
    0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
    0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d,
    0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63,
    0x55, 0x21, 0x0c, 0x7d,
)

# ilosc rund w zaleznosci od dlugosci klucza
# rundy to ilosc iteracji przez operacje podstawienia (S-box),
# permutacja (ShiftRows), mieszanie (MixColumns), oraz dodanie klucza (AddRoundKey)
rundyKluczy = {128: 10, 192: 12, 256: 14}

def iloscRund(n):
    # n to ilosc rund podanych przez klucz (np. 10 rund dla 128 bit)
    # stworz liste zer, tyle ile jest rund
    rundy = [0] * n
    for i in range(n):
        if i == 0:
            # pierwszy element jest ustawiany na 0x1
            rundy[i] = 0x1
        else:
            # wez stala z poprzedniej rundy
            prev = rundy[i - 1]
            # podwajamy wartosc poprzedniej stalej rundowej
            rundy[i] = prev * 2

            # jesli wynik przekracza 8 bitów, wykonujemy operację XOR z 0x11b
            if rundy[i] >= 0x100:
                rundy[i] ^= 0x11b

    return rundy

def przesun(word):
    # przesun slowo o 8 bitow w lewo (1 bajt)
    przesunieteLewo = word << 8
    # uzyj maski zeby wynik na pewno miescil sie w 32 bitach
    maskowanePrzesunieteLewo = przesunieteLewo & 0xFFFFFFFF
    # przesuj slowo o 24 bity w prawo (3 bajty)
    przesunietePrawo = word >> 24
    # zlacz wyniki
    wynik = maskowanePrzesunieteLewo | przesunietePrawo
    return wynik


def podstawSlowo(word):
    # zapisuje wartosci bajtow od najbardziej znaczacego
    bajt1 = (word >> 24) & 0xff
    bajt2 = (word >> 16) & 0xff
    bajt3 = (word >> 8) & 0xff
    bajt4 = word & 0xff
    # za pomoca sboxa postawiane sa nowe bajty
    nowyBajt1 = sbox[bajt1]
    nowyBajt2 = sbox[bajt2]
    nowyBajt3 = sbox[bajt3]
    nowyBajt4 = sbox[bajt4]

    # sklejamy zaktualizowane bajty w nowe słowo
    return (nowyBajt1 << 24) | (nowyBajt2 << 16) | (nowyBajt3 << 8) | nowyBajt4


def tworzenieKluczyRund(key, lenKlucz):
    # tworzy klucze rundowe, dzieli klucz glowny na kawalki
    rund = iloscRund(rundyKluczy[lenKlucz] + 1)
    # N to ilosc liczb wewnatrz listy. Tj jesli mamy 128 bit, to lista ma -> 4 elementy po 32 bity
    # jesli klucz jest 192 to lista na -> 6 elementow 32 bit itd.
    if lenKlucz == 128:
        N = 4
    elif lenKlucz == 192:
        N = 6
    elif lenKlucz == 256:
        N = 8
    else:
        print("DEBUG: wystapil blad przy tworzeniu kluczy rundowych. Ustawiono domyslnie N=4 (128 bit)")
        N = 4
    mask = 0xffffffff

    # lista K będzie przechowywać poszczególne 32-bitowe fragmenty klucza
    K = []
    # przechodzimy po kazdym kluczu w zakresie N (czyli ilosci "kawalkow")
    for i in range(N):
        # przesuniecie bitow klucza w prawo o 32*i miejsc - wydzielenie 32bit fragmetnu
        przesuniecie = key >> (32 * i)
        # aby wyciagnac tylko 32 bity dodajemy mastke 0xffffffff
        kawalek = przesuniecie & mask
        # dodajemy oddzielony kawalek klucza do listy K
        K.append(kawalek)

    # R - ilosc rund, ktora trzeba lacznie wykonac na podstawie dlugosci klucza. Dodajemy 1, bo numeracja jest od 0
    R = rundyKluczy[lenKlucz] + 1

    # lista W przechowuje wszystkie klucze rundowe
    # N - liczba slow w kluczu
    # R - liczba rund
    # uzupelniamy zerami na poczatku
    W = [0] * (N * R)

    for i in range(N * R):
        if i < N:
            # pierwsze N elementow z listy W jest kopia pierwszych N slow klucza K
            W[i] = K[i]
        elif i % N == 0:
            # dla indeksu, ktory jest wielokrotnoscia N, generowany jest nowy klucz rundowy
            # bierzemy poprzedni klucz, robimy przesuniecie wzgledem poprzedniego klucza
            # wstawiamy operacje podstawienia i nakladamy operacje XOR
            W[i] = W[i - N] ^ podstawSlowo(przesun(W[i - 1])) ^ rund[i // N]
        else:
            # przy reszcie dajemy XOR na wczesniejszych kluczach rundowych
            W[i] = W[i - N] ^ W[i - 1]

    # W - lista wsyzstkich kluczy rundowych
    return W


def podzielKlucz(W, lenKlucz):
    # funkcja dzieli klucz rozszerzeony (liste 32-bit slow) na kilka kluczy rundowych
    # kazdy klucz rund sklada sie z 128 bitow (4 * 32 bity)
    # kazdy klucz rund jest wykorzystywany w AddRoundKey
    # lenKlucz to np. 128, 256, zaleznie od wybranego klucza
    kluczeRundowe = []
    # iloscRund = 10 lub 12 lub 14 (128bit:10)
    iloscRund = rundyKluczy[lenKlucz] + 1
    # iterujemy przez wszystkie rundy
    for i in range(rundyKluczy[lenKlucz] + 1):
        klucz = 0
        # polacz 4 nastepne 32-bit slowa aby dostac 128bit klucz rundowy
        for j in range(4):
            klucz = (klucz << 32) + W[i * 4 + j]
        kluczeRundowe.append(klucz)
    return kluczeRundowe


def podstawSbox(macierz):
    # podstawia kazdy bajt z macierzy przez wartosc z sbox
    # z macierzy 4x4 kazdy element jest zamieniany na 4x4 z macierzy sbox
    for i in range(4):
        for j in range(4):
            macierz[i][j] = sbox[macierz[i][j]]

def odwrPodstawSbox(macierz):
    # operacja odwrotna do podstawSbox
    for i in range(4):
        for j in range(4):
            macierz[i][j] = odwr_sbox[macierz[i][j]]

def przesunRzedy(macierz):
    # przesuwa wiersze macierzy
    for i in range(4):
        macierz[i] = macierz[i][i:] + macierz[i][:i]

def odwrPrzesunRzedy(macierz):
    # przesuwa wiersze w odwrotnej kolejnosci
    for i in range(4):
        macierz[i] = macierz[i][-i:] + macierz[i][:-i]

def xtime(a):
    # mnozy przez x w ciele GF(2^8). Uzywana w mixColumns
    # sprawdzenie czy najbardziej znaczacy bit jest ustawiony
    if (a & 0x80):
        # jesli tak, to przesuwamy w lewo i robimy xor
        przesuniete = a << 1
        wynik = przesuniete ^ 0x1b
        # zwracamy wynk po redukcji (xor), ograniczamy do 8 bitow dzieki masce
        return wynik & 0xff
    else:
        # jesli najstarszy bit nie jest ustawiony, przesuwamy bity liczby "a" w lewo o 1
        return a << 1  # Zwracamy wynik przesunięcia w lewo

# nizej do zrobienia
def pomieszajKol(macierz):
    # operacja "MixColumns"
    # dla kazdej kolumny (jest ich 4)
    for i in range(4):
        # t - suma XOR wszystkich elementow kolumny i
        t = macierz[0][i] ^ macierz[1][i] ^ macierz[2][i] ^ macierz[3][i]
        # u - przechowuje oryginalna wartosc pierwszego elementu kolumny
        u = macierz[0][i]
        # dalej aktualizujemy nastepne czesci kolumny
        # kazdy bajt jest xor'orwany z wartoscia t i xor'owany z wynikiem funkcji xtime sasiadujacych elementow
        macierz[0][i] ^= t ^ xtime(macierz[0][i] ^ macierz[1][i])
        macierz[1][i] ^= t ^ xtime(macierz[1][i] ^ macierz[2][i])
        macierz[2][i] ^= t ^ xtime(macierz[2][i] ^ macierz[3][i])
        macierz[3][i] ^= t ^ xtime(macierz[3][i] ^ u)


def odwrPomieszajKol(macierz):
    # odwrotne mieszanie kolumn
    for i in range(4):
        u = xtime(xtime(macierz[0][i] ^ macierz[2][i]))
        v = xtime(xtime(macierz[1][i] ^ macierz[3][i]))
        macierz[0][i] ^= u
        macierz[1][i] ^= v
        macierz[2][i] ^= u
        macierz[3][i] ^= v
    pomieszajKol(macierz)

def add_round_key(macierz, round_key):
    # laczy macierz z kluczem rundy
    key_bytes = []
    hex_str = f"{round_key:032x}"
    for i in range(0, 32, 2):
        key_bytes.append(int(hex_str[i:i+2], 16))
    for i in range(4):
        for j in range(4):
            macierz[i][j] ^= key_bytes[i * 4 + j]

def zaszyfrujMacierz(macierz, key, lenKlucz):
    # szyfrowanie macierzy (blok 16 bajtow)
    W = tworzenieKluczyRund(key, lenKlucz)
    subKeys = podzielKlucz(W, lenKlucz)
    add_round_key(macierz, subKeys[0])
    for i in range(1, rundyKluczy[lenKlucz]):
        podstawSbox(macierz)
        przesunRzedy(macierz)
        pomieszajKol(macierz)
        add_round_key(macierz, subKeys[i])
    podstawSbox(macierz)
    przesunRzedy(macierz)
    add_round_key(macierz, subKeys[rundyKluczy[lenKlucz]])
    return macierz

def odszyfrujMacierz(macierz, key, lenKlucz):
    # odszyfrowanie macierzy
    W = tworzenieKluczyRund(key, lenKlucz)
    subKeys = podzielKlucz(W, lenKlucz)
    add_round_key(macierz, subKeys[rundyKluczy[lenKlucz]])
    odwrPrzesunRzedy(macierz)
    odwrPodstawSbox(macierz)
    for i in range(rundyKluczy[lenKlucz] - 1, 0, -1):
        add_round_key(macierz, subKeys[i])
        odwrPomieszajKol(macierz)
        odwrPrzesunRzedy(macierz)
        odwrPrzesunRzedy(macierz)
        odwrPodstawSbox(macierz)
    add_round_key(macierz, subKeys[0])
    return macierz

def text_to_macierz(text):
    # Convert text to bytes using UTF-8 and build a 4x4 macierz (16-byte block).
    data = text.encode('utf-8')
    if len(data) < 16:
        data += b'\x00' * (16 - len(data))
    else:
        data = data[:16]
    return [list(data[i*4:(i+1)*4]) for i in range(4)]

def macierz_to_text(macierz):
    # laczy macierz do tekstu, ignorujac zera
    bytes_arr = []
    for row in macierz:
        bytes_arr.extend(row)
    return ''.join(chr(b) for b in bytes_arr if b != 0)

def encrypt_text(plaintext, key_text, lenKlucz):
    key_int = int.from_bytes(key_text.encode('utf-8'), 'big')
    encrypted_result = []
    # Work with the full plaintext as bytes and process it in 16-byte blocks.
    data = plaintext.encode('utf-8')
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        if len(block) < 16:
            block += b'\x00' * (16 - len(block))
        # Create the 4x4 macierz from this block.
        macierz = [list(block[j*4:(j+1)*4]) for j in range(4)]
        encrypted_macierz = zaszyfrujMacierz(macierz, key_int, lenKlucz)
        encrypted_block = ''.join(f"{val:02x}" for row in encrypted_macierz for val in row)
        encrypted_result.append(encrypted_block)
    return ''.join(encrypted_result)

def decrypt_text(ciphertext, key_text, lenKlucz):
    key_int = int.from_bytes(key_text.encode('utf-8'), 'big')
    decrypted_bytes = bytearray()
    # Each block is 16 bytes (represented by 32 hex characters)
    for i in range(0, len(ciphertext), 32):
        block_hex = ciphertext[i:i+32]
        block = bytes(int(block_hex[j:j+2], 16) for j in range(0, 32, 2))
        # Build the 4x4 macierz from this block.
        macierz = [list(block[j*4:(j+1)*4]) for j in range(4)]
        decrypted_macierz = odszyfrujMacierz(macierz, key_int, lenKlucz)
        decrypted_bytes.extend(bytes(val for row in decrypted_macierz for val in row))
    return decrypted_bytes.rstrip(b'\x00').decode('utf-8', errors='ignore')
