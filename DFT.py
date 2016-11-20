import finitefield
import truthtable
import primpoly

def DFT(array, dpoly):
    """ Given an array of polynomials, maps it to its discrete fourier transform using as its nth root of unity the root of the primitive polynomial dpoly !!note that order of root must equal size of array!!
    """
    f = []
    uroot = [0,1]
    for i in xrange(len(array)):
        A = [0]
        for j in xrange(len(array)):
            a = finitefield.fieldExp(uroot,j*i,dpoly)
            x = array[j]    
            A = finitefield.fieldAdd(A, finitefield.fieldMult(x,a,dpoly))
        f.append(A)
    return f

def IDFT(array, dpoly):
    """Given an array of polynomials, maps it to its inverse discrete fourier trandform using as its nth root of unity the root of the primitive polynomial dpoly !!note that order of root must equal size of array!!
    """
    f = []
    uroot = [0,1]
    for i in xrange(len(array)):
        A1 = [0]
        for j in xrange(len(array)):
            a = finitefield.fieldExp(uroot,-1*j*i,dpoly)
            x = array[j]    
            A1 = finitefield.fieldAdd(A1, finitefield.fieldMult(x,a,dpoly))
        A2 = finitefield.fieldMult(finitefield.fieldInv([len(array)%2], dpoly), A1, dpoly)
        f.append(A2)
    return f

print IDFT(DFT([[1],[0],[1],[1],[1],[1],[1],[1],[0],[1], [0], [0], [0], [1], [0], [0], [1], [1], [0], [0], [0], [1], [0], [1], [0], [1], [1], [0], [0], [0], [1,0,1]], [1,0,1,0,0,1]),[1,0,1,0,0,1])
print DFT([[1,0,1]]*63,[1,1,0,0,0,0,1])

                       
