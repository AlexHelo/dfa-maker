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

dfa = {}

currentState = 'q0'
followingState = ''

f = open("test1.txt")

setOfStates = f.readline().split(",")
setOfStates[len(setOfStates)-1] = setOfStates[len(setOfStates)-1].strip()

alphabet = f.readline().split(",")
alphabet[len(alphabet)-1] = alphabet[len(alphabet)-1].strip()

initialState = f.readline()

finalStates = f.readline().split(",")
finalStates[len(finalStates)-1] = finalStates[len(finalStates)-1].strip()

for x in range(len(setOfStates)*2):
    chimp = f.readline()
    if not chimp:
        break
    chimp = chimp.split("=>")
    chimp[len(chimp)-1] = chimp[len(chimp)-1].strip()
    dfa[chimp[0]] = chimp[1]


isValid = 0

toValidate = input("Enter String to Validate: ")
toValidate = list(toValidate)


for x in range(len(toValidate)):
    for y in range(len(alphabet)):
        if alphabet[y] == toValidate[x]:
            isValid += 1
            break
    if isValid != (x+1):
        print("String is not valid since letter " +
              toValidate[x] + " is not in the alphabet")
        break
