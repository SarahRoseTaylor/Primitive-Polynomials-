def binary(x, size):
    """ Takes a number and outputs it in a binary array
    """
    A = []
    for i in range(size):
        if (2**i)&x == 2**i:
            A.append(1)
        else:
            A.append(0)
    return A[::-1] 
    

def bitsequenceGen(size):
    """ Generates the rows of the truth table of size n
    """
    table = []
    for i in range(2**size):
        table.append(binary(i,size))
    return table


def fromBinary(array):
    """ Takes a binary number and outputs a number
    """
    x = 0
    for i in range(len(array)):
        if array[i] == 1:
            x += 2**(len(array) -1 -i)
    return x        

def ANF(table,size):
    """ Prints a function to the console which is the algebraic normal form of the function defined by the truthtable
    """
    s = ""
    for i in table:
        if table[i]== 1:
            B = binary(i,size)
            for j in range(len(B)):
                if B[j] == 0:
                    s += "(x_"+str(j) + "+1)"
                else:
                    s+= "x_" + str(j)    
            s += "\\\\\n +"
    print s        
            
def singleRow(array):
    """ Takes a row of the truth table of a Boolean function and returns its relevant terms in the ANF of the function
    """
    terms = []
    term = [0 for j in range(len(array))]
    terms.append(term)
    for k in range(len(array)):
        if array[k] == 1:
            for sequences in terms:
                sequences[k] = 1
        else:
            keepterms = [i[:] for i in terms]
            for sequences in terms:
                sequences[k]=1
            terms += keepterms
    return terms

def reducedANF(table,size):
    """ Takes a truth table and goes through all the rows and adds them to a dictionary which counts individual terms. If the count of a particular term is zero mod 2 it does not add it to the function. Returns the reduced ANF of the function
    """
    termcount = {}
    function = ""
    for row in table:
        if table[row]==1:
            array = binary(row,size)
            terms = singleRow(array)
            for i in range(len(terms)):
                terms[i] = fromBinary(terms[i])   
            for term in terms:
                if term in termcount:
                    termcount[term] += 1
                else:
                    termcount[term] = 1
    print termcount                
    for key in termcount:
        if (termcount[key]%2)== 1:
            B = binary(key, size)
            s = ""
            for j in range(len(B)):     
                if B[j] == 1:
                    s += "x_" + str(j)
            function+= "\\\\\n+" + s
            if key == 0:
                function = function + 1
    return function    
            
    
if __name__ == '__main__':
    print reducedANF({0: 0, 1: 0, 2: 0, 3: 0, 4: 0,  5: 1, 6: 0, 7: 1, 8: 0, 9: 0, 10: 1, 11: 1, 12: 0, 13: 1, 14: 1, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 1, 22: 0, 23: 1, 24: 0, 25: 0, 26: 1, 27: 1, 28: 0, 29: 1, 30: 1, 31: 1, 32: 0, 33: 1, 34: 0, 35: 1, 36: 0, 37: 0, 38:0, 39: 0, 40: 0, 41: 1, 42: 1, 43: 0, 44: 0, 45: 0, 46: 1, 47: 1, 48: 0, 49: 1, 50: 1, 51: 0, 52: 0, 53: 0, 54: 1, 55: 1, 56: 0, 57: 1, 58: 0, 59: 1, 60: 0, 61: 0, 62: 0, 63: 1},6)   


