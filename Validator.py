sigma = ["a", "s"]
gamma = ["a", "e", "w", "_"]
states = ["q0", "q1", "q2"]
qA = "q1"
qR = "q2"
q0 = "q0"
transitions = [("q0", "a", "a", "q1", "s", "e", "w"), ("q0", "a", "a", "q2", "s", "e", "w")]
blank="_"

def validate():
    global states, sigma, gamma, transitions, blank, q0, qA, qR
    print("Beginning validation...")
    print()

    # beginning logic verification of the given list of states
    print("Verifying the TM given states:")
    # a functional TM must have an initial state
    if q0 == "":
        print("Error: the initial state must not be null")
        return False

    # a functional TM must have an accept state in order to be considered decidable
    elif qA == "":
        print("Error: the accept state must not be null")
        return False

    # a functional TM must have a reject state in order to be considered decidable
    elif qR == "":
        print("Error: the reject state must not be null")
        return False

    # each state within the given list of states must be one-of-a-kind in order to have a functional TM
    if len(states) != len(set(states)):
        print("Error: Each state within the list must be unique")
        return False
    print("States status: OK!")

    print()
    # beginning verification of the given transitions list
    print("Verifying the TM transition function:")

    # next, we verify the existence of all three important states (Start, Accept, Reject) within the list containing
    # 7-tuples we also need to check whether or not each transition has the correct syntax: which is:
    # ( state, sigma-letter, gamma-letter, state, sigma-letter, gamma-letter, next-move(left/right) )
    Start = False
    Accept = False
    Reject = False

    # index => variable that holds the index of the current tuple within the list
    index = 1
    for transition in transitions:
        # verification of the first implied condition => existence of Start, Accept, Reject states
        if transition[0] == q0:  # if so, then the list contains a start state
            Start = True
        if transition[3] == qA:  # if so, then the list contains an accept state
            Accept = True
        if transition[3] == qR:  # if so, then the list contains a reject state
            Reject = True

        # verification of the second implied condition => correct syntax
        # we check whether or not the first element of the current tuple is a state from states
        if transition[0] not in states:
            print(f"Error tuple #{index}: first element of each transition must be a member of states")
            return False
        # we check whether or not the first position within the transition contains the accept state, which is incorrect
        # because accept state is final
        elif transition[0] == qA:
            print(f"Error: tuple #{index}: accept state is final")
            return False
        # we check whether or not the first position within the transition contains the reject state, which is incorrect
        # because accept state is final
        elif transition[0] == qR:
            print(f"Error: tuple #{index}: reject state is final")
            return False

        # we check whether or not the second element of the current tuple is a letter from sigma
        elif transition[1] not in sigma and transition[1] not in gamma:
            print(f"Error tuple #{index}: second element of each transition must be a member of gamma")
            return False

        # we check whether or not the third element of the current tuple is a letter from gamma
        elif transition[2] not in sigma and transition[2] not in gamma:
            print(f"Error tuple #{index}: third element of each transition must be a member of gamma")
            return False

        # we check whether or not the fourth element of the current tuple is a state from states
        elif transition[3] not in states:
            print(f"Error tuple #{index}: fourth element of each transitions must be a member of states")
            return False

        # we check whether or not the fifth element of the current tuple is a letter from sigma
        elif transition[4] not in sigma and transition[4] not in gamma:
            print(f"Error tuple #{index}: fifth element of each transition must be a member of sigma")
            return False

        # we check whether or not the sixth element of the current tuple is a letter from gamma
        elif transition[5] not in sigma and transition[5] not in gamma:
            print(f"Error tuple #{index}: sixth element of each transition must be a member of gamma")
            return False
        index += 1

    # verification of the first implied condition => existence of Start, Accept, Reject states
    # TM does not have initial state
    if not Start:
        print("Error: this TM does not have a starting point within the given transitions")
        return False
    # TM does no have accept state
    elif not Accept:
        print("Error: this TM does not reach any accept state")
        return False
    # TM does not have reject state
    elif not Reject:
        print("Error: this TM does not reach ant reject state")
        return False
    print("Transitions status: OK!")

    print()
    # beginning verification of the given sigma list
    print("Verifying the TM sigma alphabet...")

    # we check whether or not there are any letters from gamma,
    # different form the intersection of the two sets, within sigma
    # because sigma alphabet must not contain any letters from gamma
    if set(sigma).intersection(set(gamma)):
        print("Error: sigma alphabet must not contain elements from gamma")
        return False
    print("Sigma status: OK!")

    print()
    # beginning verification of the given gamma list
    print("Verifying the TM gamma alphabet...")

    # we check whether or not the blank symbol is in gamma
    if blank not in gamma:
        print("Error: gamma does not contain the blank symbol")
        return False
    print("Gamma status: OK!")

    print()
    print("This Turing Machine is valid!")
    return True

# validate()
