
def getFiloMetrics(listOfLengths, TIME_STEP):
    # Constants
    MIN_MAX_LEN = 1
    # Instantiate variables to store the output
    maxLengthList = []
    averageExtendingTimeList = []
    timePerExtensionList = []
    timeAtMaxList = []
    averageRetractingTimeList = []
    timePerRetractionList = []

    """FOR EACH LIST OF LENGTHS"""
    listCtr = 0 # TODO remove
    for lengthsList in listOfLengths: 
        # Each list might contain the recorded lengths of multiple filopodia, so we need to further split this list of lengths into separate lists for each filopodium
        individualFilopodia = []
        for i in range(len(lengthsList)):
            # Start a new list of lengths if we are on the first index or the previous length is 0
            if i==0 or (lengthsList[i] > 0 and lengthsList[i-1]==0):
                individualFilopodia.append([])
            individualFilopodia[-1].append(lengthsList[i])

        # TODO debugging remove
        # if len(individualFilopodia) > 1 and individualFilopodia[-1][-1]!=0:
            # print(individualFilopodia)
            # print(listCtr)

        # TODO remove
        filoctr = 0
        """FOR EACH FILOPODIUM"""
        for lengths in individualFilopodia:
            # Only parse this filo's lengths if it has retracted fully, i.e. last length is 0
            if lengths[-1] != 0:
                continue
            # Get the maximum length reached
            maxLen = max(lengths)
            # If the max length reached is too small, then do not record this filopodium
            if maxLen < MIN_MAX_LEN:
                continue
            maxLengthList.append(maxLen)
            # Instantiate values for this filopodium
            timeTilMax = timeAtMax = timeTilZero = extDuration = extendedLength = retDuration = retractedLength = 0
            maxLenReached = retracting = False

            """FOR EACH RECORDED LENGTH"""
            prev = 0
            for length in lengths:
                # Filo has not reached its max length 
                if length < maxLen and not maxLenReached:
                    timeTilMax += TIME_STEP
                # Filo is at its max length for the first time
                elif length == maxLen and not maxLenReached:
                    timeTilMax += TIME_STEP
                    averageExtendingTimeList.append(timeTilMax/maxLen)
                    # # DEBUGGING TODO REMOVE
                    # if timeTilMax/maxLen > 400:
                    #     print("avgExt =" + str(timeTilMax/maxLen) + ",  list "+ str(listCtr) + " filoCtr " + str(filoctr))
                    maxLenReached = True
                # Filo has previously reached max length and is still on it
                elif length == maxLen and maxLenReached:
                    timeAtMax += TIME_STEP
                # Filo has just started to retract
                elif length < maxLen and prev == maxLen:
                    timeAtMaxList.append(timeAtMax)
                    
                # Filo has not fully retracted
                if length < maxLen and length > 0 and maxLenReached:
                    timeTilZero += TIME_STEP
                # Filo has just completely retracted
                elif length == 0 and prev > 0:
                    timeTilZero += TIME_STEP
                    averageRetractingTimeList.append(timeTilZero/maxLen)

                # Increment the duration and length of actual extension/retraction
                diff = length - prev
                if diff > 0: # Extension 
                    extDuration += TIME_STEP
                    extendedLength += diff
                elif diff < 0: # Retraction
                    retDuration += TIME_STEP
                    retractedLength += abs(diff)

                prev = length

            # For this filo, add seconds taken to extend each micron. Do the same for retraction.
            timePerExtensionList.append(extDuration / extendedLength)
            if retractedLength > 0:
                timePerRetractionList.append(retDuration / retractedLength)
            
            filoctr += 1

        listCtr += 1

    output = {
        "maxLen": maxLengthList,
        "averageExtendingTime": averageExtendingTimeList,
        "averageRetractingTime": averageRetractingTimeList,
        "timeAtMax": timeAtMaxList,
        "timePerExtension": timePerExtensionList,
        "timePerRetraction": timePerRetractionList
    } 
    return output