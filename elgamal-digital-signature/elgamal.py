import random, math, hashlib

def modinv(a, m):
    """Compute the modular inverse using the extended Euclidean algorithm."""

    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % m


def prime_factors(n):
    """Return the distinct prime factors of n."""
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 1:
        factors.add(n)
    return list(factors)


def find_primitive_root(q):
    """
    Finds a primitive root modulo the prime q.
    For each candidate g from 2 to q-1, we check that for every prime factor f of (q-1):
         g^((q-1)/f) mod q != 1.
    """
    phi = q - 1
    factors = prime_factors(phi)
    for g in range(2, q):
        flag = True
        for factor in factors:
            if pow(g, phi // factor, q) == 1:
                flag = False
                break
        if flag:
            return g
    return None


# =========================================
# ElGamal Digital Signature Functions
# =========================================

def generate_elgamal_keys():
    """
    Generates an ElGamal digital signature key pair.
    For demonstration we choose a small prime q from a preset list.
    The private key is XA (1 <= XA < q-1) and the public key is YA = a^XA mod q.
    The global parameters are q and a (a primitive root of q).
    """
    q = random.choice([19, 467, 7919])  # For demo; in production, use large primes.
    a = find_primitive_root(q)
    XA = random.randint(1, q - 2)
    YA = pow(a, XA, q)
    return (q, a, XA, YA)


def elgamal_sign(message, keys):
    """
    Signs a message using the ElGamal digital signature scheme.

    Steps:
      1. Compute m = H(M) mod (q-1), where H is SHA256.
      2. Choose a random integer K ∈ [1, q-1] with gcd(K, q-1) = 1.
      3. Compute S1 = a^K mod q.
      4. Compute K⁻¹ mod (q-1).
      5. Compute S2 = K⁻¹ * (m - XA * S1) mod (q-1).

    Returns a tuple (S1, S2) as the signature.
    """
    q, a, XA, YA = keys
    # Compute hash value m. (Reduce the SHA256 digest modulo (q-1) so 0 <= m <= q-1.)
    m = int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16) % (q - 1)
    # Choose K with gcd(K, q-1) = 1.
    K = random.randint(1, q - 1)
    while math.gcd(K, q - 1) != 1:
        K = random.randint(1, q - 1)
    S1 = pow(a, K, q)
    invK = modinv(K, q - 1)
    S2 = (invK * (m - XA * S1)) % (q - 1)
    return (S1, S2)


def elgamal_verify(message, signature, keys):
    """
    Verifies the ElGamal digital signature.

    Steps:
      1. Compute m = H(M) mod (q-1).
      2. Compute V1 = a^m mod q.
      3. Compute V2 = (YA^(S1) * S1^(S2)) mod q.

    Returns True if the signature is valid (V1 equals V2), otherwise False.
    """
    q, a, XA, YA = keys
    S1, S2 = signature
    m = int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16) % (q - 1)
    V1 = pow(a, m, q)
    V2 = (pow(YA, S1, q) * pow(S1, S2, q)) % q
    return V1 == V2

