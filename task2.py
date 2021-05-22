import sys
import random
import time
import copy

#Domains (All possible words)
wordList = ['ADD', 'ADO', 'AGE', 'AGO', 'AID', 'AIL', 'AIM', 'AIR', 'AND',
            'ANY', 'APE', 'APT', 'ARC', 'ARE', 'ARK', 'ARM', 'ART', 'ASH',
            'ASK', 'AUK', 'AWE', 'AWL', 'AYE', 'BAD', 'BAG', 'BAN', 'BAT',
            'BEE', 'BOA', 'EAR', 'EEL', 'EFT', 'FAR', 'FAT', 'FIT', 'LEE',
            'OAF', 'RAT', 'TAR', 'TIE']

#Variables (Cells in the crossword)
class variables:
    def __init__(self, name):
        self.name = name    #Variable name i.e A1 A2....
        self.word = ""  #Current word in the variable
        self.domains = copy.deepcopy(wordList) #Major problem here. First we had domains = wordList. Now it works with deepcopy
        self.neighbours = []    #Neighbour variables

#Create variables
A1 = variables("A1")
A2 = variables("A2")
A3 = variables("A3")

D1 = variables("D1")
D2 = variables("D2")
D3 = variables("D3")

#Adding neighbours (All variables except target variable)
A1.neighbours = [D1, D2, D3, A2, A3]
A2.neighbours = [D1, D2, D3, A1, A3]
A3.neighbours = [D1, D2, D3, A1, A2]

D1.neighbours = [A1, A2, A3, D2, D3]
D2.neighbours = [A1, A2, A3, D1, D3]
D3.neighbours = [A1, A2, A3, D1, D2]

#Add variables to a list
variableList = [A1, A2, A3, D1, D2, D3]

#Add variables to list (OLD IMPLEMENTATION BEFORE C TASK)
#variableList = [variables("A1"), variables("A2"), variables("A3"), variables("D1"), variables("D2"), variables("D3")]

def testingArcCon(xI, x, xJ, y):    #CSP for arc consistency
    if xI.name[0] == xJ.name[0]:    #if same var letter i.e A1 == A2
        if x != y:  #Check if same word
            return True
        else:   #if not same word
            return False
    if x == y:  #If same word but different variable letter i.e A2!=D2
        return False

    posXI = (int(xI.name[1]) - 1)   #word position for cross check
    posXJ = (int(xJ.name[1]) - 1)   #word2 position for cross check
    if y == "": #if empty word
        return True

    if x[posXJ] == y[posXI]:    #if same letter in word
        return True
    else:
        return False

#function for arc consistency
def removeInconsistentValues(xI, xJ):
    removed = False #Bool to see if we remove any domain

    for x in xI.domains:    #Loop all domains for variable xI
        signal = False  #Bool value to see if y in xJ allows (x,y)
        for y in xJ.domains:    #Loop domains for variable xJ
            if testingArcCon(xI, x, xJ, y): #If the domain is ok in both variables
                signal = True   #Making it true = not removing and domain
        if signal == False: #If any y is impossible for x
            xI.domains.remove(x)    #Remove x from xI domainlist
            removed = True  #We removed something
    return removed

#Arc consistency (AC3)
def arcConsistency(varList, queue = None):  #Start with empty queue

    if queue == None:   #First step
        queue = [(xI, xK) for xI in varList for xK in xI.neighbours]    #add var to queue and neighbour var

    while queue:    #While queue not empty
        (xI, xJ) = queue.pop()  #pop variables
        if removeInconsistentValues(xI, xJ):    #Check if inconsistent
            for xK in xI.neighbours: #Loop neighbour vars for xI
                queue.append((xK, xI))  #Push variables
    return varList  #returns a list with less domains

#Top level for task C and D
def backtrackingSearchWithArcCon(varList):
    topLevelRecursiveBacktrackingSearch(arcConsistency(varList))#First we do AC3 then rBTS

#CSP testing
def testingCon(word, var, varList):

    posVar = (int(varList[var].name[1])) - 1 #Take the value in name and minus 1 i.e A2 = 1

    for next in varList:#Loop all variables
        posNext = (int(next.name[1])) - 1 #Take value in name minus 1 of next variable i.e D1 = 0
        if next.name != varList[var].name:  #If not the same variable
            if next.name[0] != varList[var].name[0]:    #if not the same letter i.e A1 != D2
                if next.word != "": #Check if variable has word or not
                    if word[posNext] != next.word[posVar]:  #Check if same letter at respective position
                        return False    #If not same letter return false
            else:   #if the same letter i.e A1 = A2
                if next.word == word:   #Only check if word already exists
                    return False
    return True #If everything passes, return True


#Check all constrains
def checkAll(varList):
    for next in varList:    #Loop all variables
        if next.word == "": #If unused variable
            return False
        if (not testingCon(next.word, varList.index(next), varList)):   #If CSP
            return False
    return True #if no problems, DONE


def selectUnassignedVar(varList):
    for next in varList:    #Loop all variables
        if next.word == "": #If unused variable
            return varList.index(next)  #Return index of variable

#Useless function that was in pseudo code
def backtrackingSearch(varList):
    return recursiveBacktrackingSearch(varList) #Very useless....

#Main recursive backtracking search function
def recursiveBacktrackingSearch(varList):
    if checkAll(varList):   #Check if complete
        return varList  #Return list with words

    var = selectUnassignedVar(varList)  #Take a unused variable

    for next in varList[var].domains:   #Loop through all domains (words)
        if testingCon(next, var, varList):  #CSP for given domain and variable
            varList[var].word = next    #Assign the word if no CSP
            arcConsistency(varList) #Arc consistency for task D
            result = recursiveBacktrackingSearch(varList) #The "recursiveness"

            if result != None:  #If variable got a domain that is OK
                return result


            varList[var].word = ""  #Else remove the domain from the variable

    return None #If CSP



#Just top level function for the wholeness
def topLevelRecursiveBacktrackingSearch(varList):
    print('Loading....')    #Because it takes time...
    print() #Newline

    start = time.time()
    result = recursiveBacktrackingSearch(variableList)   #Function calling
    #Making a matrix with variables and domains
    print(result[0].word[0] + result[3].word[0], result[0].word[1] + result[4].word[0],
          result[0].word[2] + result[5].word[0])
    print(result[1].word[0] + result[3].word[1], result[1].word[1] + result[4].word[1],
          result[1].word[2] + result[5].word[1])
    print(result[2].word[0] + result[3].word[2], result[2].word[1] + result[4].word[2],
          result[2].word[2] + result[5].word[2])
    print()

    print('Execution time: ',(time.time()-start))
    print('Done!')#Becuase it's done

#Call top level function
topLevelRecursiveBacktrackingSearch(variableList)
test = arcConsistency(variableList)
for x in test:
    print(x.name, x.domains)

backtrackingSearchWithArcCon(variableList)