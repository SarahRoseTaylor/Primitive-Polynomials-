import truthtable

def polyGen(size):
    """ Generates an array all binary polynomials of a particular degree with an odd number of terms and a constant term and stores them as binary strings
    """
    polynomials = []
    for i in range(1,2**(size-1)+1):
        a = truthtable.binary(i,size-1)
        checksum = 0
        for j in a:
            checksum += j
        if (checksum%2) == 1:
            poly = [1] + a
            poly.append(1)
            polynomials.append(poly)
    return polynomials

def polyDeg(array):
    """ For a particular polynomial, returns the degree
    """
    for i in range(len(array)-1,-1,-1):
        if array[i] == 1:
            return i
    return 0

def divAlg(array1,array2):
    """ Given two polynomials, performs the division algorithm to find the quotient and remainder of the polynomial of first the polynomial divided by the second over the field GF(2)
    """
    dif= polyDeg(array1) -polyDeg(array2)
    if dif < 0:
        return [0], array1
    a = [0 for i in range(dif)]
    q = truthtable.binary(2**(dif),len(array1))[::-1]
    m = a + array2
    r = truthtable.binary((truthtable.fromBinary(m[::-1]))^(truthtable.fromBinary(array1[::-1])), len(array1))[::-1]
    newQ,newR = divAlg(r,array2)
    return [truthtable.binary((truthtable.fromBinary(newQ[::-1]))^(truthtable.fromBinary(q[::-1])), len(q))[::-1],newR]

def irrChecker(array):
    """ Given a particular polynomial, prints true if it is irreducible false if it is not
    """
    d = polyDeg(array)
    for i in range(2,2**(d)+1):
        j = truthtable.binary(i,len(array))[::-1]
        a = divAlg(array,j)[1]
        b = truthtable.fromBinary(a[::-1])
        if b == 0:
            return False
    return True

def divChecker(array1, array2):
    """ Given two polynomials, determines whether one divides the other
    """
    if polyDeg(array1) == polyDeg(array2):
        return False
    a = divAlg(array1, array2)[1]
    j = truthtable.fromBinary(a[::-1])
    if j == 0:
        return True
    else:
        return False

def polyOrder(array):
    """ Given a polynomial, returns its order to the console
    """
    for T in range(len(array)-1, 2**(len(array)-1)):
        poly = truthtable.binary(2**(T)+1, T+1)[::-1]
        a = divChecker(poly, array)
        if a == True:
            return T

def primPoly(size):
    """Finds all the primitive polynomials of a particular degree
    """
    candidates = polyGen(size)
    primitives = []
    for poly in candidates:
        if irrChecker(poly)== True:
            if polyOrder(poly) == (2**(size) -1):
                primitives.append(poly)
    return primitives

#print primPoly(6)         
        
            
        
        
