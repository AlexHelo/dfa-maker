#  .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. |
# | |  ________    | || |  _________   | || |      __      | |
# | | |_   ___ `.  | || | |_   ___  |  | || |     /  \     | |
# | |   | |   `. \ | || |   | |_  \_|  | || |    / /\ \    | |
# | |   | |    | | | || |   |  _|      | || |   / ____ \   | |
# | |  _| |___.' / | || |  _| |_       | || | _/ /    \ \_ | |
# | | |________.'  | || | |_____|      | || ||____|  |____|| |
# | |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'

import sys

def stringBuilder(state, letter):
    global currentString
    currentString = (state + "," + letter)

#boolean that checks if the dfa can be minimized
canItBeDone = True
dfa1 = {}
#Where we create the new dictionary where the dfa is minimized
dfa2={}
#Dumb way to give letters to the minimized states
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','X','Y','Z']
#Keep track of which letter comes after every minimization
globalIndex=0

currentState = 'q0'

test = input("Wich test do you want to open, test1(1) or test2(2)?")

if test == '1':
    f = open("test1.txt")
elif test == '2':
    f = open("test2.txt")

#split the set of states by their ',' and put them in an array
setOfStates = f.readline().split(",")
setOfStates[len(setOfStates)-1] = setOfStates[len(setOfStates)-1].strip()
#split the alphabet by their ',' and put them in an array
alphabet = f.readline().split(",")
alphabet[len(alphabet)-1] = alphabet[len(alphabet)-1].strip()
#we get the initial state
initialState = f.readline().rstrip()
#split the final states by their ',' and put them in an array
finalStates = f.readline().split(",")
finalStates[len(finalStates)-1] = finalStates[len(finalStates)-1].strip()

#create the dictionary with the transitions
for x in range(len(setOfStates)*2):
    chimp = f.readline()
    if not chimp:
        break
    chimp = chimp.split("=>")
    chimp[len(chimp)-1] = chimp[len(chimp)-1].strip()
    dfa1[chimp[0]] = chimp[1]
    dfa2[chimp[0]] = chimp[1]

#Here we filled the missing transitions. For example in test1, q3 when you process a it doesn't exist, so in this method we create that missing transition and put a lambda character
def completeDictionary():
    for state in setOfStates:
        #Here we check if all states have the alphabet
        for value in alphabet:
            key = state + ',' + value
            #In case they don't, we add the missing alphabet that leads to a lambda
            if key not in dfa2.keys():
                dfa2[key] = 'λ'

#In this method will check for matches so that we can minimize
def checkMatch(canItBeDone):
    global initialState,globalIndex
    #We create a table that will containt the transitions
    transitionTable = []
    for state in setOfStates:
        #We save the row of the table and add it to a temporary array that will later be used to put the row in the transition table
        line = []
        line.append(state)
        line.append([])
        for value in alphabet:
            key = state + ',' + value
            line[1].append(dfa2[key])
        #We save the value of the key and put it on our transition table
        transitionTable.append(line)
    #In this array will save the transitions that are the same but that don't repeat. For example, q1 is equivalent with q2 and vice versa, so we have to have only one.
    differentSame=[]
    for line in transitionTable:
        #We save the processed line so we can compare it later
        processed = line[1]
        same=[]
        #We check if the line is the same, in case they are, we save it on the first array where we save the same lines
        for line2 in transitionTable:
            if line2[1] == processed:
                same.append(line2[0])
        if len(same) > 1:
            #We then save the lines that are not duplicated as explained before (q1 equals q2 and vice versa)
            if same not in differentSame:
                differentSame.append(same)
     #We check if there were states that matched, if not, we stop looping the code
    if not differentSame:
        canItBeDone=False
    #Create a temporary dictionary so that we can get the minimized one because in this dictionary we save only the old state and relate it to the new state (q1 = qA)
    tempDic={}
    
    #Where we give the new names to the minimized states, so instead of being q1 and q2, they are going to be qA
    if(globalIndex==0):    
        for index in range(0, len(differentSame)):
            newName = "q" + letters[index]
            for things in differentSame[index]:
                tempDic[things] = newName
    #Where in case the global index for the letter list, we make the index be in 1 instead of 0 plus what we have in the index for the letters
    elif globalIndex!=0:
        for index in range(0, len(differentSame)):
            newName = "q" + letters[index+globalIndex+1]
            for things in differentSame[index]:
                tempDic[things] = newName
    globalIndex=globalIndex+1
    minimized = {}
    for key in dfa2.keys():
        #We get the value of the key of the old dictionary
        state = key[:-2]
        if state in tempDic.keys():
            #Save the new key remplacing the old state with the new state
            newKey = tempDic[state] + ',' +key[len(key) - 1]
        else: newKey = state + ',' +key[len(key) - 1]
        minimized[newKey] = dfa2[key]
        #Here we change the value of the key
    for key in minimized.keys():
        if minimized.get(key) in tempDic.keys():
            minimized[key] = tempDic[minimized[key]]

    #We update the dictionary so that our future loops are updated and are not using an old version of the dictionary
    for key in tempDic.keys():
        #We check if the key belongs in the set of states, if they do, we take it from the list
        if key in setOfStates:
            setOfStates.remove(key)
        #Same as before, check the final states and if the match we remove it, but we also update the final states
        if key in finalStates:
            finalStates.remove(key)
            if tempDic[key] not in finalStates:
                finalStates.append(tempDic[key])
        #We update the new initial state
        if key == initialState:
            initialState=tempDic[key]
        #if the temporary keys (qA, qB, etc) is not in the set of states, we add it
        if tempDic[key] not in setOfStates:
            setOfStates.append(tempDic[key])

    return canItBeDone,minimized

option = input("Do you want to validate(1) or minimize(2)?: ")

if option == '1':

    isValid = 0
    toValidate = input("Enter String to Validate: ")
    toValidate = list(toValidate)


    for x in range(len(toValidate)):
        for y in range(len(alphabet)):
            if alphabet[y] == toValidate[x]:
                isValid += 1
                break
        if isValid != (x+1):
            sys.exit("String is not valid since letter " +
                    toValidate[x] + " is not in the alphabet")

    isValid = 0

    for x in range(len(toValidate)):
        for key, value in dfa1.items():
            stringBuilder(currentState, toValidate[x])
            print("Trying " + currentString + " with " + key)
            if currentString == key:
                print("Match! " + currentState + " will be replaced with " + value)
                currentState = value
                isValid += 1
                break
        if isValid != (x+1):
            sys.exit("String is not valid since " + currentState +
                    " never points to " + toValidate[x])

    for x in range(len(finalStates)):
        if finalStates[x] == currentState:
            sys.exit("String is valid!")

    print("String is not valid since " + currentState + " is not a final state")
elif option == '2':
    completeDictionary()
    #keep looping the code until we can't minimize
    while canItBeDone:
        canItBeDone,dfa2 = checkMatch(canItBeDone) 

    print("Normal:")
    print(dfa1)
    print("Minimized:")
    print(dfa2)  