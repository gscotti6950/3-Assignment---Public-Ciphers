from Crypto.Util.number import GCD

#primeRoots function courtesy of MazDak
#https://stackoverflow.com/questions/40190849/efficient-finding-primitive-roots-modulo-n-using-python
def primRoots(modulo):
    coprime_set = {num for num in range(1, modulo) if GCD(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]

n = 37
print(primRoots(n))


