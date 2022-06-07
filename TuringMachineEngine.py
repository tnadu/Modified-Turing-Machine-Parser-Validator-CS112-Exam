# Team members:
#   1. Constantinescu Ioana
#   2. Nadu Toma
#   3. Marin Eduard
#   GROUP 141

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
    print(f'Usage: {sys.argv[0]} [<config file> / "help"] [<word> - optional]')
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

# PARSING

# ignore 'comment' lines
while (line.strip()[0] == '#'):
    if i == len(lines) - 1:  # end of file reached before complete data extraction
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]

if line == "Sigma:":
    while (line != "End"):
        if i == len(lines) - 1:  # end of file reached before complete data extraction
            print('Format error: end of file reached before sigma section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":  # line is not a 'comment' line
            # verifying each character is alphanumerical
            for char in line.strip():
                if char in string.ascii_letters or char in string.digits:
                    sigma.append(char)
                else:
                    raise Exception(f"Format error: '{char}' is not alphanumerical")

    if len(sigma) == 0:
        raise Exception("Format error: sigma cannot be empty")
else:  # sigma section expected immediately after comment lines
    print(f"Format error: sigma section expected before:\n'{line}'")

# ignore 'comment' lines
while (line.strip()[0] == '#'):
    if i == len(lines) - 1:  # end of file reached before complete data extraction
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]

if line == "Gamma:":
    while (line != "End"):
        if i == len(lines) - 1:  # end of file reached before complete data extraction
            print('Format error: end of file reached before gamma section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":  # line is not a 'comment' line
            line = line.split(' ')
            if len(line) == 1:  # a single string found
                if len(line[0]) != 1:  # gamma letter consists of multiple characters
                    raise Exception(f"Format error: gamma letters must consist of a single character")
                else:
                    # verifying character is alphanumerical
                    if line[0] in string.ascii_letters or line[0] in string.digits:
                        gamma.append(line[0])
                    else:
                        raise Exception(f"Format error: '{line[0]}' is not alphanumerical")

            elif len(line) == 2:  # two strings found, separated by a space
                if len(line[0]) != 1 or line[1].lower() != 'b':  # gamma letter consists of multiple characters or marking string is not B/b
                    raise Exception(f"Format error: '{' '.join(line)}' is not valid gamma section syntax")
                elif blank:  # blank symbol was already stored
                    raise Exception(f"Error: blank symbol must be unique")
                else:
                    # verifying character is alphanumerical
                    if line[0] in string.ascii_letters or line[0] in string.digits:
                        blank = line[0]
                        gamma.append(line[0])
                    else:
                        raise Exception(f"Format error: '{line[0]}' is not alphanumerical")

            else:  # bad syntax
                raise Exception(f"Format error: '{' '.join(line)}' is not valid gamma section syntax")

    if len(gamma) == 0:
        raise Exception("Error: gamma cannot be empty")
else:  # gamma section expected immediately after comment lines
    print(f"Format error: gamma section expected before:\n'{line}'")

# ignore 'comment' lines
while (line.strip()[0] == '#'):
    if i == len(lines) - 1:
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]

if line == "States:":
    while (line != "End"):
        if i == len(lines) - 1:  # end of file reached before complete data extraction
            print('Format error: end of file reached before states section ending')
            quit()
        i += 1
        line = lines[i]

        if line.strip()[0] != "#":  # line is not a 'comment' line
            line = line.split(' ')  # splitting into array of strings, by the space character
            if len(line) == 1:  # only a state is found
                # verifying each character is alphanumerical
                for char in line[0]:
                    if char not in string.ascii_letters and char not in string.digits:
                        raise Exception(f"Format error: '{char}' is not alphanumerical")

                states.append(line[0])

            elif len(line) == 2:  # both a state and its special type are found
                if line[1].lower() == 's':  # state type is start
                    if q0:  # a state has been stored in q0 before
                        raise Exception(f"Error: start state must be unique")
                    else:
                        q0 = line[0]
                        states.append(line[0])

                if line[1].lower() == 'a':  # state type is accept
                    if qA:  # a state has been stored in qA before
                        raise Exception(f"Error: accept state must be unique")
                    else:
                        qA = line[0]
                        states.append(line[0])

                if line[1].lower() == 'r':  # state type is reject
                    if qR:  # a state has been stored in qR before
                        raise Exception(f"Error: reject state must be unique")
                    else:
                        qR = line[0]
                        states.append(line[0])

                else:
                    raise Exception(f"Format error: '{' '.join(line)}' is not valid states section syntax")
            else:  # more than 3 strings found on current line
                raise Exception(f"Format error: '{' '.join(line)}' is not valid states section syntax")

    if len(states) == 0:
        raise Exception(f'Error: states cannot be empty')
else:  # states section expected immediately after comment lines or after gamma section ending
    print(f"Format error: states section expected before:\n'{line}'")

# ignore 'comment' lines
while (line.strip()[0] == '#'):
    if i == len(lines) - 1:  # end of file reached before complete data extraction
        print('Format error: end of file reached before sigma section')
        quit()
    i += 1
    line = lines[i]

if line == "Transitions:":
    while (line != "End"):
        if i == len(lines) - 1:  # end of file reached before complete data extraction
            print('Format error: end of file reached before sigma section')
            quit()
        i += 1
        line = lines[i]

        transition = tuple(line.split(' '))  # transition becomes a tuple of the split line by the space character
        if len(transition) != 7:
            raise Exception("Error: transitions section entry must consist of 7 parameters")
        elif transition[6].lower() not in "rl":  # last element of tuple must be R/r/L/l
            raise Exception("Format error: direction parameter must be either L(eft) or R(right)")
        else:
            transitions.append(transition)
else:  # gamma section expected immediately after comment lines or after states section ending
    print(f"Format error: transitions section expected before:\n'{line}'")

commented = False  # store if last line of file was commented
# ignore 'comment' lines
while (line.strip()[0] == '#'):
    if i == len(lines) - 1:  # end of file reached before complete data extraction
        commented = True
        break
    i += 1
    line = lines[i]

if commented:  # a line after the transitions section ending was not commented
    print('Format error: end of file already reached')
    quit()


# VALIDATION

def validate():
    global states, sigma, gamma, transitions, blank, q0, qA, qR
    print("Beginning validation...")

    # beginning logic verification of the given list of states
    print("Verifying the TM given states:")
    # a functional TM must have an initial state
    if q0 == "":
        print("Error: the initial state must not be null")
        return False

    # a functional TM must have an accept state 
    elif qA == "":
        print("Error: the accept state must not be null")
        return False

    # a functional TM must have a reject state 
    elif qR == "":
        print("Error: the reject state must not be null")
        return False

    # each state within the given list of states must be one-of-a-kind in order to have a functional TM
    if len(states) != len(set(states)):
        print("Error: each state within the list must be unique")
        return False
    print("States status: OK!")

    # beginning verification of the given sigma list
    print("Verifying the TM sigma alphabet...")

    # sigma alphabet must not contain any letters from gamma - sigma
    if set(sigma).intersection(set(gamma)):
        print("Error: sigma alphabet must not contain elements from gamma - sigma")
        return False
    print("Sigma status: OK!")

    # beginning verification of the given gamma list
    print("Verifying the TM gamma alphabet...")

    # we check whether or not the blank symbol was marked
    if blank not in gamma:
        print("Error: blank symbol not marked")
        return False
    print("Gamma status: OK!")

    # beginning verification of the given transitions list
    print("Verifying the TM transition function:")

    # next, we verify the existence of all three important states (Start, Accept, Reject) within the list containing
    # 7-tuples. we also need to check whether or not each transition has the correct syntax, which is:
    # ( state, gamma-letter, gamma-letter, state, gamma-letter, gamma-letter, next-move(left/right) )
    Start = False
    Accept = False
    Reject = False

    # index => variable that holds the index of the current tuple within the list
    index = 1
    for transition in transitions:
        # verification of the first implied condition => existence of Start, Accept, Reject states
        if transition[0] == q0:  # if so, then the list contains a start configuration
            Start = True
        if transition[3] == qA:  # if so, then the list contains an accept configuration
            Accept = True
        if transition[3] == qR:  # if so, then the list contains a reject configuration
            Reject = True

        # verification of the second implied condition => correct syntax
        # we check whether or not the first element of the current tuple is a state from states
        if transition[0] not in states:
            print(f"Error: at tuple #{index} of transitions - not a member of states")
            return False
        # we check whether or not the first position within the transition contains the accept state, which is incorrect
        # because the accept state is final
        elif transition[0] == qA:
            print(f"Error: at tuple #{index} of transitions - accept state is halting")
            return False
        # we check whether or not the first position within the transition contains the reject state, which is incorrect
        # because the reject state is final
        elif transition[0] == qR:
            print(f"Error: at tuple #{index} of transitions - reject state is final")
            return False

        # we check whether or not the second element of the current tuple is a letter from gamma
        elif transition[1] not in sigma and transition[1] not in gamma:
            print(f"Error: at tuple #{index} of transitions - second element of each transition must be a member of gamma")
            return False

        # we check whether or not the third element of the current tuple is a letter from gamma
        elif transition[2] not in sigma and transition[2] not in gamma:
            print(f"Error: at tuple #{index} of transitions - third element of each transition must be a member of gamma")
            return False

        # we check whether or not the fourth element of the current tuple is a state from states
        elif transition[3] not in states:
            print(f"Error: at tuple #{index} of transitions - fourth element of each transitions must be a member of states")
            return False

        # we check whether or not the fifth element of the current tuple is a letter from gamma
        elif transition[4] not in sigma and transition[4] not in gamma:
            print(f"Error: at tuple #{index} of transitions - fifth element of each transition must be a member of gamma")
            return False

        # we check whether or not the sixth element of the current tuple is a letter from gamma
        elif transition[5] not in sigma and transition[5] not in gamma:
            print(f"Error: at tuple #{index} of transitions - sixth element of each transition must be a member of gamma")
            return False
        index += 1

    # verification of the first implied condition => existence of Start, Accept, Reject states
    if not Start:  # TM does not have an initial state
        print("Error: this TM does not have a starting point within the given transitions")
        return False
    elif not Accept:  # TM does not have an accept state
        print("Error: this TM does not reach any accept state")
        return False
    elif not Reject:  # TM does not have a reject state
        print("Error: this TM does not reach ant reject state")
        return False
    print("Transitions status: OK!")

    print("This Turing Machine is valid!")
    return True


if validate() and len(sys.argv) == 3:  # validation successful and word received for validation, so the program may proceed
    if not set(word).issubset(sigma):  # word received for validation contains letters which aren't in sigma
        print(f"Error: '{word}' must contain only characters of the input alphabet!")

    # since the way we designed the simulation process is dependent on a specific nested dictionary structure
    # the 7-tuple structure used to store the transitions must be converted to our designated data structure format
    oldTransitions = transitions
    transitions = {}
    for oldTransition in oldTransitions:
        # the state our TM transitions into, the characters written on both tapes and the direction the head will move (the codomain)
        # are dependent on the current state and the contents of the tapes at the current head position (the domain), so it makes sense
        # to store them as tuples at the final level of our nested dictionaries, for convenient access
        # ----------------->       Q           x         Γ         x         Γ          x         {R/L}
        currentTransition = tuple([oldTransition[3], tuple([oldTransition[4], oldTransition[5]]), oldTransition[6]])

        if oldTransition[0] not in transitions:  # the current state stored in oldTransition[0] hasn't been associated with a transition yet
            #  δ:              Q          x           Γ          x          Γ     ----->
            transitions[oldTransition[0]] = {tuple([oldTransition[1], oldTransition[2]]): currentTransition}
        else:  # the current state stored in oldTransition[0] has already been associated with a transition
            #  δ:              Q          x           Γ          x          Γ     ----->
            transitions[oldTransition[0]][tuple([oldTransition[1], oldTransition[2]])] = currentTransition

    # initializing two identical tapes, consisting of the input string and the blank symbol
    tape1 = word.split('').append(blank)
    tape2 = word.split('').append(blank)


    # SIMULATION

    def simulate(i, q):  # i - current head position; q - current state
        global states, sigma, gamma, transitions, blank, q0, qA, qR

        while q != qA and q != qR:  # TM halts only if it enters a final state (accept/reject)
            # check if current state transitions into another state
            # if it does, check if there is a transition corresponding to the current contents of the tapes at the current position
            # if the search fails, the current state transitions into the reject state, thus halting
            if q not in transitions or tuple([tape1[i], tape2[i]]) not in transitions[q]:
                q = qR
            else:
                # for q and the tuple consisting of the characters at position i on the tapes, the next state is stored on the 0th position of the tuple
                q = transitions[q][tuple([tape1[i], tape2[i]])][0]
                # for q and the tuple consisting of the characters at position i on the tapes, the tapes' contents to be copied
                # are stored on the 1st position of the tuple; there, a 2-tuple is stored, consisting of the new tapes' contents
                tape1[i], tape2[i] = transitions[q][tuple([tape1[i], tape2[i]])][1][0], transitions[q][tuple([tape1[i], tape2[i]])][1][1]
                # for q and the tuple consisting of the characters at position i on the tapes,
                # the direction the head moves next is stored on the 2nd position of the tuple
                if (transitions[q][tuple([tape1[i], tape2[i]])][2].lower() == 'r'):  # moving to the right
                    i += 1
                    if (i == len(tape1)):
                        tape1.append(blank)
                        tape2.append(blank)
                elif i != 0:  # moving to the left; i is decremented only if it is currently non-null (on the leftmost position of the tapes)
                    i -= 1

        if q == qA:  # TM entered the accept state
            return True, i
        return False, i  # TM entered the reject state


    # EXTENDED FUNCTIONALITY

    # we reached an accept state, thereby we can attempt to perform the last validation step (storage errors),
    # using the second tape of the TM; to do so, we need to extend the delta function in order to verify
    # whether or not the tapes are identical; if the tapes are, indeed, identical, the given word is accepted
    # otherwise, the given word is rejected
    def extended(i):
        global states, sigma, gamma, transitions, blank, q0, qA, qR, tape1, tape2

        # we begin by extending the delta function
        # in order to do so, we need a few more states such as:

        qBack = "qBack"  # this state is used to move the head back to the leftmost tapes' squares
        states.append(qBack)
        transitions[qBack] = {}

        qVerify = "qVerify"  # this state is used to verify whether or not the tapes are identical
        states.append(qVerify)
        transitions[qVerify] = {}

        qAccept = "qAccept"  # this is the final accept state
        states.append(qAccept)
        qReject = "qReject"  # this is the final reject state
        states.append(qReject)

        q = qA  # storing the old accept state
        qA = qAccept
        qR = qReject

        blank1 = '( ͡° ͜ʖ ͡°)'  # second blank symbol used to differentiate between the ends of the input
        # inserting leftmost blank symbol at the beginning of both tapes
        tape1 = tape1.insert(0, blank1)
        tape2 = tape2.insert(0, blank1)

        # the TM's head could either be within the string or at the end of it
        # if the qA state is reached at the end of the string we begin moving backwards to the start of the input
        transitions[qA][tuple([blank, blank])] = {qBack, tuple([blank, blank]), "L"}

        # then, when the leftmost blank symbol at the start of the input is reached, we move to qVerify
        transitions[qBack][tuple([blank1, blank1])] = {qVerify, tuple([blank1, blank1]), "R"}

        # if we reach rightmost blank symbol, then the tapes are identical, thereby we move to the accept state
        transitions[qVerify][tuple([blank, blank])] = {qA, tuple([blank, blank]), "L"}

        for letter in sigma:
            # if qA is reached within the string we need to have transitions for each letter of sigma
            # in order to start moving backwards to the start of the input
            transitions[qA][tuple([letter, letter])] = {qBack, tuple([letter, letter]), "L"}

            # next, we iterate through the tapes' contents, using qBack until the TM reached the leftmost blank symbol at the start of the input
            transitions[qBack][tuple([letter, letter])] = {qBack, tuple([letter, letter]), "L"}

            # now we begin to actually verify whether or not the tapes are identical
            # if the current symbol is the same on both tapes, we continue the process and move each time to the right
            transitions[qVerify][tuple([letter, letter])] = {qVerify, tuple([letter, letter]), "R"}

            # if the current symbol is not the same on both tapes, we enter the new reject state
            # regardless of the current state (qA, qBack, qVerify)
            for different_letter in sigma:
                if different_letter != letter:
                    transitions[qA][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}
                    transitions[qBack][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}
                    transitions[qVerify][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}

        i += 1  # compensating the insertion of the leftmost blank space
        # once the TM was modified, a second simulation begins from the
        # old accept state, at the head position at which it initially stalled
        if simulate(i, q)[0]:
            return True
        return False


    i = 0  # stores the position at which the TM stalled
    accepted = False  # stores whether the word was accepted or rejected
    accepted, i = simulate(0, q0)

    if accepted:  # additional storage error checking performed only if the word was accepted
        print(f"The word '{word}' was accepted by the turing machine!")
        if extended(i):
            print(f"No storage errors detected!")
        else:
            print(f"Storage errors detected!")
    else:
        print(f"The word '{word}' was not accepted by the turing machine!")
