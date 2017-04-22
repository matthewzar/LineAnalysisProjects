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
        #splitResult = ["Thu Apr 06 2017 00:15:00 GMT+0000 (UTC)", "186", "-208" ]
        splitResult[1] = splitResult[1].strip()
        splitResult[1] = calculateRTP(int(splitResult[1]))
        splitResult[2] = splitResult[2].strip()
        splitResult[2] = calculateRTP(int(splitResult[2]))
        #splitResult = ["Thu Apr 06 2017 00:15:00 GMT+0000 (UTC)", 1.86, 0.48]

#       splitResult[0] = calculateRTP(timeParser(splitResult[0]))
        #splitResult = [currentTime, 1.86, 0.48]

        ret.append(splitResult)

    return ret

savedValue = getSingleRawFileInfo("testcsv.csv", 1)
print(savedValue)