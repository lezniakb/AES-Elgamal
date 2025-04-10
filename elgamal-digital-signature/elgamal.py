import math, hashlib, secrets, random

def odwrotnoscModularna(a, m):
    # funkcja liczaca modularna odwrotnosc a modulo m
    def rozszerzonyNwd(a, b):
        if a == 0:
            return b, 0, 1
        nwd, x, y = rozszerzonyNwd(b % a, a)
        return nwd, y - (b // a) * x, x

    nwd, x, _ = rozszerzonyNwd(a, m)
    if nwd != 1:
        return None
    return x % m

def dzielnikiPierwsze(n):
    # funkcja zwraca liste roznych dzielnikow pierwszych liczby n
    dzielniki = set()
    while n % 2 == 0:
        dzielniki.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            dzielniki.add(i)
            n //= i
        i += 2
    if n > 1:
        dzielniki.add(n)
    return list(dzielniki)

def znajdzPierwotnyPierwiastek(liczbaQ):
    # funkcja szuka pierwotnego pierwiastka modulo liczbaQ
    phi = liczbaQ - 1
    dzielniki = dzielnikiPierwsze(phi)
    for pierwiastek in range(2, liczbaQ):
        flaga = True
        for dzielnik in dzielniki:
            if pow(pierwiastek, phi // dzielnik, liczbaQ) == 1:
                flaga = False
                break
        if flaga:
            return pierwiastek
    return None

def generujKluczeElgamal():
    """
    funkcja generujaca pare kluczy elgamal.
    do przykladu wybieramy mala liczbe pierwsza z ustalonej listy.
    klucz prywatny (kluczPrywatny) jest losowa liczba z przedzialu [1, liczbaQ - 1],
    a klucz publiczny (kluczPubliczny) to wynik: generator^kluczPrywatny mod liczbaQ.
    zwracane sa: (liczbaQ, generator, kluczPrywatny, kluczPubliczny).
    """
    liczbaQ = secrets.choice([71993, 100999, 152093, 202409, 272329, 336163, 396061, 410233, 470201, 499879])
    generator = znajdzPierwotnyPierwiastek(liczbaQ)
    kluczPrywatny = random.randint(1, liczbaQ - 2)
    kluczPubliczny = pow(generator, kluczPrywatny, liczbaQ)
    return (liczbaQ, generator, kluczPrywatny, kluczPubliczny)


def elgamalPodpis(wiadomosc, klucze):
    """
    optymalizowana funkcja do podpisywania elgamal.
    zwraca krotke (podpisCzesc1, podpisCzesc2) reprezentujaca podpis.
    """
    liczbaQ, generator, kluczPrywatny, kluczPubliczny = klucze
    modWartosc = liczbaQ - 1  # obliczamy raz
    # oblicz hash wiadomosci i zredukuj modulo (liczbaQ - 1)
    hashWiadomosci = int(hashlib.sha256(wiadomosc.encode('utf-8')).hexdigest(), 16) % modWartosc

    # uzywamy modulu secrets dla bezpiecznego wyboru losowej liczby
    while True:
        losowaLiczba = secrets.randbelow(modWartosc) + 1  # losowa liczba z przedzialu [1, liczbaQ - 1]
        if math.gcd(losowaLiczba, modWartosc) == 1:
            break

    # oblicz podpis czesc 1: s1 = generator^losowaLiczba mod liczbaQ
    podpisCzesc1 = pow(generator, losowaLiczba, liczbaQ)
    # oblicz modularna odwrotnosc losowej liczby modulo modWartosc
    odwrotnoscLiczby = odwrotnoscModularna(losowaLiczba, modWartosc)
    # oblicz podpis czesc 2: s2 = odwrotnoscLiczby * (hashWiadomosci - kluczPrywatny * podpisCzesc1) mod modWartosc
    podpisCzesc2 = (odwrotnoscLiczby * (hashWiadomosci - kluczPrywatny * podpisCzesc1)) % modWartosc

    # opcjonalnie: sprawdzenie zakresu podpisCzesc1 i podpisCzesc2
    if not (1 <= podpisCzesc1 < liczbaQ):
        raise ValueError("podpisCzesc1 nie mieści się w oczekiwanym zakresie (1 <= s1 < liczbaQ).")
    if not (0 <= podpisCzesc2 < modWartosc):
        raise ValueError("podpisCzesc2 nie mieści się w oczekiwanym zakresie (0 <= s2 < liczbaQ-1).")

    return (podpisCzesc1, podpisCzesc2)


def elgamalWeryfikuj(wiadomosc, podpis, klucze):
    """
    funkcja sprawdzajaca podpis cyfrowy elgamal.
    kroki:
      1. oblicz hash wiadomosci modulo (liczbaQ - 1).
      2. oblicz wartosc1 = generator^hashWiadomosci mod liczbaQ.
      3. oblicz wartosc2 = (kluczPubliczny^(podpisCzesc1) * podpisCzesc1^(podpisCzesc2)) mod liczbaQ.
    zwraca true, jesli podpis jest poprawny (wartosc1 rowna wartosc2), inaczej false.
    """
    liczbaQ, generator, kluczPrywatny, kluczPubliczny = klucze
    podpisCzesc1, podpisCzesc2 = podpis
    hashWiadomosci = int(hashlib.sha256(wiadomosc.encode('utf-8')).hexdigest(), 16) % (liczbaQ - 1)
    wartosc1 = pow(generator, hashWiadomosci, liczbaQ)
    wartosc2 = (pow(kluczPubliczny, podpisCzesc1, liczbaQ) * pow(podpisCzesc1, podpisCzesc2, liczbaQ)) % liczbaQ
    zwracam = wartosc1 == wartosc2
    return zwracam
