import primpoly
import truthtable

def fieldGen(size):
    """ Given a particular size n, generates the set of binary polynomials ie. the set on which the field is defined to produce the field of degree n over GF(2)
    """
    field  = []
    for i in range(0, 2**(size)):
        a = truthtable.binary(i,size)
        field.append(a)
    return field

def polyMult(array1,array2):
    """Given two polynomials in array form (leading term last) multiplies them together and returns the answer in array form
    """
    ndegree = len(array1)+len(array2)-1
    expanded = []
    for i in range(0,len(array1)):
        newpoly = 0
        if array1[i]== 1:
            for j in range(0,len(array2)):
                if array2[j]== 1:
                    newpoly += 2**(j+i)
            expanded.append(truthtable.binary(newpoly,ndegree))
    final = truthtable.binary(0,ndegree)
    for polynomial in expanded:
        final =  [(a + b)%2 for a,b in zip(final,polynomial)]       
    return final[::-1]
    
def fieldMult(array1,array2, dpoly):
    """Given two field elements, defines the multiplicative operation of them with respect to a pariticular definition of the field
    """
    prod = polyMult(array1,array2)
    ans = primpoly.divAlg(prod,dpoly)[1]
    return ans[:primpoly.polyDeg(ans)+1]
    

def fieldInv(array, dpoly):
    """Given a field element, finds its inverse in the field defined by dpoly
    """
    if truthtable.fromBinary(array)==0:
        raise Exception("No inverse for zero element")
    field = fieldGen(len(dpoly)-1)
    for element in field:
        if fieldMult(element, array, dpoly) == [1]:
            return element[:primpoly.polyDeg(element)+1]
            break

def fieldExp(array1, exponent, dpoly):
    """Given a field element, raises it to the power defined by exponent over the field defined by the irreducible polynomial dpoly
    """
    if exponent < 0:
        array1 = fieldInv(array1,dpoly)
        exponent = -1*exponent
    a = [1]
    for i in xrange(exponent):
        a = fieldMult(a,array1,dpoly)
    return a
    
def fieldAdd(array1,array2):
    """Given two field elements, defines the additive operation between them over GF(2), since we are working over GF(2), this is the same as subtraction
    """
    a = truthtable.fromBinary(array1[::-1])
    b = truthtable.fromBinary(array2[::-1])
    added = a^b
    ans = truthtable.binary(added, max(len(array1),len(array2)))[::-1]
    return ans[:primpoly.polyDeg(ans)+1]
    

def bigFPolyDeg(array):
    """Given a polynomial in F_{2^{n}}[x], returns its degree
    """
    for i in range(len(array)-1,-1,-1):
        if truthtable.fromBinary(array[i]) > 0:
            return i
    return 0

def bigFPolyAdd(array1,array2):
    """Given two polynomials in F_{2^{n}}[x], returns their sum
    """
    d1 = bigFPolyDeg(array1)
    d2 = bigFPolyDeg(array2)
    if d2 < d1:
       array1,array2 = array2, array1
       d1, d2 = d2, d1 
    added = [[0] for i in range(d2+1)]
    for i in xrange(d2+1):
        if i < d1+1:
            added[i] = fieldAdd(array1[i], array2[i])
        else:
            added[i] = array2[i]
    return added
    
def bigFPolyMult(array1, array2, dpoly):
    """Given two polynomials in F_{2^n}[x], returns their product"""
    d1 = bigFPolyDeg(array1)
    d2 = bigFPolyDeg(array2)
    prod = [[0] for i in range(d1+d2+1)]
    for i in xrange(len(array1)):
        for j in xrange(len(array2)):
            p = fieldMult(array1[i], array2[j], dpoly)
            prod[i+j] = fieldAdd(prod[i+j], p)
    return prod   

def bigFDivAlg(array1, array2, dpoly):
    """Given two polynomials in F_{2^{n}}[x], performs the division algorithm to divide the first by the second and returns their quotient and remainder
    """
    d1 = bigFPolyDeg(array1)
    d2 = bigFPolyDeg(array2)
    if d1 < d2:
        return [[[0]], array1]
    q = [[0] for i in range(d1 - d2)]
    q.append(fieldMult(array1[d1], fieldInv(array2[d2],dpoly), dpoly))
    m = bigFPolyMult(q,array2, dpoly)
    r = bigFPolyAdd(m,array1)
    newQ,newR = bigFDivAlg(r,array2,dpoly)
    return [bigFPolyAdd(newQ, q), newR]


def trace(array1, order, dpoly):
    """Given and element of a field of the same degree over GF(2) as dpoly, calculates the trace of a particular order for the field element array1
    """
    trace = [0]
    for i in xrange(order):
        alpha = fieldExp(array1,2**i,dpoly)
        trace = fieldAdd(alpha,trace)
    return trace


if __name__=="__main__":
    print fieldExp([0,0,0,0,1], -2, [1,0,1,0,0,1]) # Should return [1,0,1,1]
    print fieldAdd([1,0,1,1], [1,0,1,1])
    print fieldInv([0,0,0,0,1],[1,0,1,0,0,1])
    print "sum",bigFPolyAdd([[0,1,1,1], [0,0,1]], [[0],[0,0,1]])
    q,r = bigFDivAlg([ [0], [0], [1], [0], [0], [0], [0,0,0,0,1] ], [ [0], [1,0,1], [0], [0,1] ], [1,0,1,0,0,1] ) # should return [[[0], [0,0,1,0,1], [0], [0,0,0,1]], [[0], [0], [1,1,1,1]]]
    print q
    print r
    
    
