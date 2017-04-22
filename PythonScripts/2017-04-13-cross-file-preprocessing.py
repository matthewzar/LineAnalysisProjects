def calculateRTP(lineValue):
    '''
    Convert line values to payout percentages.
    For example: 
        lineValue -150 has a return rate of 150%
        lineValue 200 has a return rate of 50%        
    '''
    if(lineValue < 0):
        return 100.0/(-lineValue)
    return lineValue/100.0

def getSingleRawFileInfo(address, linesToIgnore=1):
    '''
    Parse 2 column line data csv file, return a 2d list of line change prices, and times of changes.
    Expected per-line format --> "Thu Apr 06 2017 00:15:00 GMT+0000 (UTC), 186, -208"
    '''
    ret = []
    lineCount = 0
    for line in open(address):
        lineCount += 1
        if(linesToIgnore >= lineCount):
            continue

        splitResult = line.split(",")
        splitResult[1] = splitResult[1].strip()
        splitResult[1] = calculateRTP(int(splitResult[1]))
        splitResult[2] = splitResult[2].strip()
        splitResult[2] = calculateRTP(int(splitResult[2]))

        ret.append(splitResult)

    return ret

team_to_token = {}
token_to_team = {}

def tokeniseTeam(teamName, knownToken = None):
    """
    Team woll be added to the 2 token dictionaries
    """    
    if(teamName in team_to_token):
        #raise Exception("Duplicate team")
        return;
    
    if(knownToken == None):       
        tokenValue = len(team_to_token)
    elif(int(knownToken) >= 0):
        tokenValue = int(knownToken)
    else:
        raise Exception("negative tokens not allowed")
        
    token_to_team[tokenValue] = teamName
    team_to_token[teamName] = tokenValue
    
    
def tokeniseTeamFromDict(dictionary, teamNameIndexes):
    """
     >> mydict = { row[0]: row[1:] for row in fileRowIterator_ColumnExclusion("mlb.csv", [0, 2, 3]) }
    """
    global team_to_token, token_to_team
    team_to_token = {}
    token_to_team = {}
    for key in dictionary:
        for i in teamNameIndexes:
            tokeniseTeam(dictionary[key][i])      
            
def saveTokens(address):
    '''
    Save tokenised values to the given file. You should use this ONCE near
    the completion of preprocessing.
    '''
    with open(address, 'w') as file:
        for team in team_to_token:    
            file.write(str(team)+","+str(team_to_token[team])+"\n")


def loadTokens(address):
    '''
    Load tokens from a file, after preprocessing has been done this should be 
    your only source of tokens (i.e. no more calling tokeniseTeamFromDict)
    '''
    for line in open(address, 'r'):
        splitVars = line.split(",") 
        tokeniseTeam(splitVars[0], splitVars[1])
    
            
            
def fileSingleElementRowIterator(address, columnNum, linesToIgnore=1):
    """
    This iterator return each value in a single column one at a time.
    Useful for handling a large data file, without reloading it.
    
    Example use in list comprehension:
        [ ident for ident in fileSingleElementRowIterator("mlb.csv", 0) ]
    """
    lineCount = 0
    for line in open(address, 'r'):
        lineCount += 1
        if(linesToIgnore >= lineCount):
            continue
        
        #yield str(line.split(",")[columnNum]) # 'str' is implied due to file IO
        yield line.split(",")[columnNum]
    

def fileWholeRowIterator(address, linesToIgnore=1):
    """
    Pull entire row as a split list of strings.
    
    To create dictionary of ID-data pairs, use this dictionary comprehension:
        mydict = { row[0]: row[1:] for row in fileWholeRowIterator("mlb.csv") }
    """
    lineCount = 0
    for line in open(address, 'r'):
        lineCount += 1
        if(linesToIgnore >= lineCount):
            continue
        
        yield line.split(",")
        
        
def fileRowIterator_ColumnExclusion(address, indexesToStore,  linesToIgnore=1):
    """
    Get rows from the given file with only values from the provided list of 
    indexes. 
    
    To create a custom ordered list of row data use this:
    mylist = [ data for data in fileRowIterator_ColumnExclusion("mlb.csv", [3, 2, 0]) ]
    
    mydict = { row[0]: row[1:] for row in fileRowIterator_ColumnExclusion("mlb.csv", [0, 3, 2]) }
    """
    lineCount = 0
    for line in open(address, 'r'):
        currentList = []
        lineCount += 1
        if(linesToIgnore >= lineCount):
            continue
        
        values = line.split(",")    
        for i in indexesToStore:
            currentList.append(values[i])
        
        yield currentList
        
def convertLinesToRTP(dictionary, lineIndexes):
    """
    take a dictionary of event data, where key is the ID, and lineIndexes refer
    to locations in the list value where line-data is stored.
    
    example usage:
        >> mydict = {'fff72753-691c-4bf7-91dc-bdfcc48820cb': [101, -1.1]}
        >> convertLinesToRTP(mydict, [0,1])
        >> mydict
        [1.01, 0.01]
    """
    for key in dictionary:
        for i in lineIndexes:
            dictionary[key][i] = calculateRTP(int(dictionary[key][i]))
        

    
    
    
    
    
    
    
    
    
    
    
    
    