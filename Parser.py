'''
The file format should be:

Sigma:
    string lipit (fiecare caracter e un element al lui sigma)
    #->linie care incepe cu un # inseamna ca e comentariu, nu il bagam in seama
End

Gamma:
    _$
End

States:
    q0 (cuvinte formate din litere si cifre, fara spatii) S #(start)
    q1
    qA A #(accept)
    qR R #(reject)
End

Transitions:
    q0 a b qA c d R/r (right/left) (tuplu)
End

'''
'''
sigma = lista de caractere
gamma = lista de caractere
states = lista de caractere
qA = string, accept state
qR = string, reject state
q0 = string, start state
transitions = lista de 7-tupluri de string-uri
'''

import string

sigma = []  # lista de caractere
blankSymbol = ""  # _B
gamma = []  # lista de caractere
states = []  # lista de caractere
qA = ""  # string, accept state
qR = ""  # string, reject state
q0 = ""  # string, start state
transitions = []  # lista de 7-tupluri de string-uri

configFile = open("config.txt", "r")

lines = configFile.readlines()

'''
Edi:
- sigma: stringul sa contina doar 0-9a-zA-Z; sa nu fie gol
- gamma: stringul sa contina doar 0-9a-zA-Z; sa nu fie gol; contine doar ce are in plus fata de sigma
'''
i = 0
while i < len(lines):
    line = lines[i]
    # tripping spaces and newlines
    line.rstrip(" \n")
    # verify that the line is not a comment,newline, or end of a block description
    if line[0] != "#" and line[0] != "\n" and line != "End":
        if line == "Sigma:":
            while (line != "End"):
                i += 1
                # checking if sigma was defined earlier and there is a valid input
                if len(sigma) != 0 and line != "#" and line != "\n":
                    line.rstrip(" \n")
                    for char in line:
                        if char in string.ascii_letters or char in string.digits:
                            sigma.append(char)
                        else:
                            raise Exception("sigma must have only letters or digit symboles")
            # checking if sigma has any inputs
            if len(sigma) == 0:
                raise Exception("sigma must have at least one symbole")

        if line == "Gamma:":
            while (line != "End"):
                i += 1
                line = lines[i]
                # checking if gamma was definer earlier
                if len(gamma) != 0:
                    line = lines[i]
                    line.rstrip(" \n")
                    for char in line:
                        if char in sigma:
                            raise Exception("gamma input must differ from sigma")
                        elif char in string.ascii_letters or char in string.digits:
                            gamma.append(char)
                        else:
                            raise Exception("gamma must have only letters or digit symboles")

            else:
                if blankSymbole != None:
                    line = line.strip()
                    if len(line == 2) and line[1] in 'Bb':
                        blankSymbole = line
        if len(gamma) == 0:
            raise Exception("gamma must have at least one symbole")

    if line == "States":
        while (line != "End"):
            i += 1
            line = lines[i].rstrip(" \n")
            # checking if states was defined earlier
            for char in line[0]:
                if char not in string.ascii_letters or char not in string.digits:
                    raise Exception("state must contain only digits and letters")
                if char in " ":
                    raise Exception("state must not contain spaces")
            if len(states) != 0:
                line = line.strip()
                if len(line) > 1:
                    if line[1] == 'S' or line[1] == 's':
                        if len(q0) != 0:
                            raise Exception("Turing Machine must have only one initial state instance")
                        q0 = line[0]
                    elif line[1] == 'A' or line[1] == 'a':
                        if len(qA) != 0:
                            raise Exception("Turing Machine must have only one acceptance state instance")
                        qA = line[0]
                    elif line[1] == 'R' or line[1] == 'r':
                        if len(q0) != 0:
                            raise Exception("Turing Machine must have only one reject state instance")
                        qR = line[0]
                    else:
                        raise Exception("state must have associated symbol")

    '''- transitions: 7 tuplu (split cu spatiu),
    ultimul caracter este R/r/L/l
    '''
    if line == "Transitions":
        if len(states) != 0:
            while (line != "End"):
                i += 1
                line = lines[i].rstrip(" \n")
                # checking if transitions was definer earlier
                trans = ()
                line = line.strip()
                if len(line) != 7:
                    raise Exception("transitions must have 7 parameters")
                if line[6] not in "RrLl":
                    raise Exception("last parameter of transition must be the direction R/r/L/l")
                for char in line:
                    trans.append(char)
                transitions.append(trans)
i += 1
