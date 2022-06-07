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
import sys

sigma = []
blank = ""  # blank symbol
gamma = []
states = []
qA = ""  # accept state
qR = ""  # reject state
q0 = ""  # start state
transitions = []


if len(sys.argv) == 1:  # 1st case: only python file name passed as argument in CLI
    print("Error: no arguments given\nUse the keyword 'help' as an argument for usage instructions")
    quit()
elif len(sys.argv) == 2 and sys.argv[1] == 'help':  # 2nd case: help menu
    print()
    # help CLI function
    quit()
elif len(sys.argv) == 2:  # 3rd case: only config file name passed as argument in CLI, no word passed for validation
    print('No word received for validation\nChecking validity of config file...')
elif len(sys.argv) == 3:  # 4th case: both config file name and word passed as arguments in CLI
    print('Checking validity of config file...')
    word = sys.argv[2]
else:  # 5th case: too many arguments passed in CLI
    print('Error: Too many arguments')
    quit()

configFileName = sys.argv[1]
try:
    configFile = open(configFileName)
except:
    print(f"Error: Invalid config file: '{configFileName}'")
    quit()

lines = configFile.readlines()  # the lines of the file will be traversed iteratively
i = 0

# ignore 'comment' lines
while(line.strip()[0] == '#'):
    if i == len(lines) - 1:     # end of file reached before complete data extraction
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]

if line == "Sigma:":
    while (line != "End"):
        if i == len(lines) - 1:     # end of file reached before complete data extraction
            print('Format error: end of file reached before sigma section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":   # line is not a 'comment' line
            # verifying each character is alphanumerical
            for char in line.strip():
                if char in string.ascii_letters or char in string.digits:
                    sigma.append(char)
                else:
                    raise Exception(f"Format error: '{char}' is not alphanumerical")

    if len(sigma) == 0:
        raise Exception("Format error: sigma cannot be empty")
else:   # sigma section expected immediately after comment lines
    print(f"Format error: sigma section expected before:\n'{line}'")


# ignore 'comment' lines
while(line.strip()[0] == '#'):
    if i == len(lines) - 1:     # end of file reached before complete data extraction
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]


if line == "Gamma:":
    while (line != "End"):
        if i == len(lines) - 1:     # end of file reached before complete data extraction
            print('Format error: end of file reached before gamma section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":  # line is not a 'comment' line
            line = line.split(' ')
            if len(line) == 1:  # a single string found
                if len(line[0])!=1:     # gamma letter consists of multiple characters
                    raise Exception(f"Format error: gamma letters must consist of a single character")
                else:
                    # verifying character is alphanumerical
                    if line[0] in string.ascii_letters or line[0] in string.digits:
                        gamma.append(line[0])
                    else:
                        raise Exception(f"Format error: '{line[0]}' is not alphanumerical")

            elif len(line) == 2:    # two strings found, separated by a space
                if len(line[0]) != 1 or line[1].lower() != 'b':     # gamma letter consists of multiple characters or marking string is not B/b
                    raise Exception(f"Format error: '{' '.join(line)}' is not valid gamma section syntax")
                elif blank:         # blank symbol was already stored
                    raise Exception(f"Error: blank symbol must be unique")
                else:
                    # verifying character is alphanumerical
                    if line[0] in string.ascii_letters or line[0] in string.digits:
                        blank = line[0]
                        gamma.append(line[0])
                    else:
                        raise Exception(f"Format error: '{line[0]}' is not alphanumerical")

            else:   # bad syntax
                raise Exception(f"Format error: '{' '.join(line)}' is not valid gamma section syntax")

    if len(gamma) == 0:
        raise Exception("Error: gamma cannot be empty")
else:   # gamma section expected immediately after comment lines
    print(f"Format error: gamma section expected before:\n'{line}'")


# ignore 'comment' lines
while(line.strip()[0] == '#'):
    if i == len(lines) - 1:
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]


if line == "States:":
    while (line != "End"):
        if i == len(lines) - 1:     # end of file reached before complete data extraction
            print('Format error: end of file reached before states section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":
            line = line.split(' ')
            if len(line) == 1:
                for char in line[0]:
                    if char not in string.ascii_letters and char not in string.digits:
                        raise Exception(f"Format error: '{char}' is not alphanumerical")

                states.append(line[0])

            elif len(line) == 2:
                if line[1].lower() == 's':
                    if q0:
                        raise Exception(f"Error: start state must be unique")
                    else:
                        q0 = line[0]
                        states.append(line[0])

                if line[1].lower() == 'a':
                    if qA:
                        raise Exception(f"Error: accept state must be unique")
                    else:
                        qA=line[0]
                        states.append(line[0])

                if line[1].lower() == 'r':
                    if qR:
                        raise Exception(f"Error: reject state must be unique")
                    else:
                        qR = line[0]
                        states.append(line[0])

                else:
                    raise Exception(f"Format error: '{' '.join(line)}' is not valid states section syntax")

    if len(states)==0:
        raise Exception(f'Error: states cannot be empty')

else:
    print(f"Format error: states section expected before:\n'{line}'")


# ignore 'comment' lines
while(line.strip()[0] == '#'):
    if i == len(lines) - 1:
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]


if line == "Transitions:":
    while (line != "End"):
        if i == len(lines) - 1:
            print('Format error: end of file reached before sigma section')
            quit()
        i += 1
        line = lines[i]

        transition = tuple(line.split(' '))
        if len(transition) != 7:
            raise Exception("Error: transitions section entry must consist of 7 parameters")
        elif transition[6].lower() not in "rl":
            raise Exception("Format error: direction parameter must be either L(eft) or R(right)")
        else:
            transitions.append(transition)
else:
    print(f"Format error: transitions section expected before:\n'{line}'")

# ignore 'comment' lines
while(line.strip()[0] == '#'):
    if i == len(lines) - 1:
        break
    i += 1
    line = lines[i]

if i != len(lines) - 1:
    print('Format error: end of file already reached')
    quit()