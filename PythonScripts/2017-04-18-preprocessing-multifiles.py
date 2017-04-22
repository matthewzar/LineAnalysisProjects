def calculateRTP(lineValue):
    '''
    Convert line values to payout percentages.
    For example: 
        lineValue -150 has a return rate of 150%
        lineValue 200 has a return rate of 50%        
    '''
    if(float(lineValue) < 0):
        return 100.0/(-float(lineValue))
    return float(lineValue)/100.0

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
    Accepts a dictionary where the values (somewhere) are team names, the indexes
    of those team names are given by teamNameIndexes.
    The given dictionary IS NOT changed, only read
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
            
#############################################
#############################################
#############################################
#############################################
    

def getFileAsDictionaryOfLists(address):
    """
    iterates over file taking single column as key, and then populates a list of
    lists for each key/game.
    """        
    gameDict = {}    
    for line in fileWholeRowIterator(address):
        #Exlude all non-game type lines
        if(line[1] != 'game'):
            if(line[0] == "d7296281-7ffe-4b95-930f-0c35210dbf55"):
                print("BALITMORE")
            continue
        
        key = line[0]
    
        if(key not in gameDict):
            gameDict[key] = []
        gameDict[key].append(line[1:])
        
    return gameDict
    
def getFileAsDictionaryOfLists_WithCustomProcessor(address, dataProcessor):
    """
    iterates over file taking single column as key, and then populates a list of
    lists for each key/game.
    """        
    gameDict = {}    
    for line in fileWholeRowIterator(address):
        #Exlude all non-game type lines
        if(line[1] != 'game'):
            if(line[0] == "d7296281-7ffe-4b95-930f-0c35210dbf55"):
                print("BALITMORE")
            continue
        key = line[0]
    
        if(key not in gameDict):
            gameDict[key] = []

        toSave = dataProcessor(line)
        gameDict[key].append(toSave)
        
    return gameDict
    
def extractAndNormaliseRTP(line):
    ret = line[4:6]
    for i in range(len(ret)):
        ret[i] = calculateRTP(ret[i])
    return ret

def tokeniseAndMarkWinners_WithLineData(outcomeData):
    for key in list(outcomeData.keys()):
        ##tokenise the dictionaries values
        outcomeData[key][0] = team_to_token[outcomeData[key][0]]
        outcomeData[key][1] = team_to_token[outcomeData[key][1]]
        
        ##decide on winning lines - IMPORTANT: we don't care which team won or by how much, the only thing that matters is the outcome for the gambler
        awayScore = int(outcomeData[key][2])
        homeScore = int(outcomeData[key][3])
        outcomeData[key][2] = 1 if awayScore > homeScore else 0
        outcomeData[key][3] = 1 if homeScore > awayScore else 0
        
        #check for missing line-data and remove assocaited entries
        if(key not in lineData):
            outcomeData.pop(key)
            continue
        
        #take the lienData for a given game and make it a data point.
        lineMovement = lineData[key]
        outcomeData[key].append(lineMovement)
        
    return outcomeData

def convertTimeDataToString(singleLineEntry):
    """
    Accepts a single list of line data such as:
    [0.8, 1.05] -> "0.8,1.05"
    """
    ret = ""
    for i in range(len(singleLineEntry)-1):
        ret = ret + str(singleLineEntry[i]) + "," 
    
    return ret + str(singleLineEntry[-1])
    
def createFilesForDataDictioanry(data, directory):
    """
    Create one new file for each game id, first line will contain
    team tokens, followed by winning/losing lines
    all subsequent lines are line movement data
    """
    for key in data:
        with open(directory + key+".csv", 'w') as file:
            entry = data[key]
            toWrite = "{0},{1},{2},{3}\n".format(entry[0],entry[1],entry[2],entry[3])
            file.write(toWrite)
            for timeline in entry[4]:
                toWrite = convertTimeDataToString(timeline)
                file.write(toWrite+"\n")
    
##Extract 5 columns from the fiven file into a dictionary
outcomeData = { row[0]: row[1:] for row in fileRowIterator_ColumnExclusion("./data/mlb.csv", [0, 2, 3, 5, 6]) }

lineData = getFileAsDictionaryOfLists_WithCustomProcessor('./data/mlb3csv.csv', extractAndNormaliseRTP)
                              
##using the dictioanry, puplate out tokenization maps
tokeniseTeamFromDict(outcomeData, [0,1])

outcomeData = tokeniseAndMarkWinners_WithLineData(outcomeData)

createFilesForDataDictioanry(outcomeData, "./formattedData/")



















