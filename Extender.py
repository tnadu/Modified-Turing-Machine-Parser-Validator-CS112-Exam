sigma = ["a", "s"]
gamma = ["a", "e", "w", "_"]
states = ["q0", "q1", "q2"]
qA = "q1"
qR = "q2"
q0 = "q0"
transitions = [("q0", "a", "a", "q1", "s", "e", "w"), ("q0", "a", "a", "q2", "s", "e", "w")]
blank="_"
tape1=[]
tape2=[]

# we reached an accept state, thereby we are entitled to ask for other verification using the second tape of the TM
# to do so, we need to extend the delta function in order to verify whether or not the tapes are identical
# if the tapes are, indeed, identical, the given word is accepted
# otherwise, the given word is rejected
def Extended():
    global states, sigma, gamma, transitions, blank, q0, qA, qR, tape1, tape2

    # we begin by extending the delta function
    # in order to do so, we need a few more states such as:

    qBack ="qBack" # this state indicates that the TM is currently returning back to the initial state
    states.append(qBack)
    transitions[qBack] = {}

    qVerify = "qVerif" # this state indicates that the TM is currently verifying whether or not the tapes are equal
    states.append(qVerify)
    transitions[qVerify] = {}

    qAccept = "qAccept" # this is the final accept state
    states.append(qAccept)
    qReject = "qReject" # this is the final reject state
    states.append(qReject)

    blank1 = '( ͡° ͜ʖ ͡°)'

    # the TM's head could either be within the string or at the end of it
    # if the qA state is reached at the end of the string we begin moving backwards to the start of the input
    transitions[qA][tuple([blank, blank])] = {qBack, tuple([blank, blank]), "L"}

    # then, when the blank symbol at the start of the input is reached, we move to qVerify
    transitions[qBack][tuple([blank1, blank1])] = {qVerify, tuple([blank1, blank1]), "R"}

    # if we reach blank symbol, then the tapes are identical, thereby we move to the accept state
    transitions[qVerify][tuple([blank, blank])] = {qAccept, tuple([blank, blank]), "L"}

    for letter in sigma:
        # if the qA state is reached within the string we need to have transitions for each letter of sigma
        # in order to start moving backwards to the start of the input
        transitions[qA][tuple([letter, letter])] = {qBack, tuple([letter, letter]), "L"}

        # next, we iterate through the qBack state until the TM reached the blank symbol at the start of the input
        transitions[qBack][tuple([letter, letter])] = {qBack, tuple([letter, letter]), "L"}

        # now we begin to actually verify whether or not the tapes are equal
        # if the the current symbol is the same on both tapes, we continue the process and move each time to the right
        transitions[qVerify][tuple([letter, letter])] = {qVerify, tuple([letter, letter]), "R"}

        # if the current symbol is not the same on both tapes, we enter the reject state
        # regardless of the current state (qA, qBack, qVerify)
        for different_letter in sigma:
            if different_letter != letter:
                transitions[qA][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}
                transitions[qBack][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}
                transitions[qVerify][tuple([letter, different_letter])] = {qReject, tuple([blank, blank]), "R"}

    # inserting leftmost blank symbol to the beginning of both tapes
    tape1 = tape1.insert(0, blank1)
    tape2 = tape2.insert(0, blank1)

    i+=1    # i-ul trebuie declarat global

    global q, i
    while q!=qReject and q!=qAccept: