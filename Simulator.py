word=''
if not set(word).issubset(sigma):
    print(f"Error: '{word}' must contain only characters of the input alphabet!")

sigma = []
gamma = []
states = []
qA = ''; qR = ''; q0 = ''
blank = ''
transitions = []

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

def extended():
    return True

# simulation function
def simulate(i, q):    # i - current head position; q - current state
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

    if q == qA:     # TM entered the accept state
        return True, i
    return False, i    # TM entered the reject state

i = 0
accepted = False
accepted, i = simulate(0, q0)

if accepted:
    print(f"The word '{word}' was accepted by the turing machine!")
    if extended(i)[0]:
        print(f"No storage errors detected!")
    else:
        print(f"Storage errors detected!")
else:
    print(f"The word '{word}' was not accepted by the turing machine!")
