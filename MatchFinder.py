# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 10:54:03 2019

@author: Luis Villa Perez
"""

# =============================================================================
# Libraries required for this to work
# =============================================================================
#For diference between strings
import difflib 
#For using regular expresions
import re
# # Functions to get complete word diference instead of partial word diference

# =============================================================================
# Global Variables
# =============================================================================
#Variable determines the similarity ratio, by default 70%
similarityRatio = 0.7 
#Variable determines if we fix the indexes of compared strings
fixCompResult = True
#Variable sets the minimum number of letters to determines string for fixing
minLettersDifferent = 2
#Variable defines the maximum number of lines a string can be found in
maxLines = 4


# =============================================================================
# Splits string by simbols (non words)
# =============================================================================
def splitBySymbols(in_str):
    if not isinstance(in_str, str):
        raise TypeError('Must be \'str\'not \'%s\''%type(in_str))        
    else:
        return re.split('(\W)', in_str)
# =============================================================================
# Simplifies Lines removing accents, special characters, spaces, etc
# =============================================================================
def simplifyLine(in_str):    
    if not isinstance(in_str, str):
        raise TypeError('Must be \'str\'not \'%s\''%type(in_str))
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    simpleLine = str(in_str).lower()
    for accent in accents:
        simpleLine = simpleLine.replace(accent, accents[accent])
    simpleLine = re.sub('(\W)', '', simpleLine)
    simpleLine = re.sub('[ñÑ]', '', simpleLine)
# =============================================================================
#     simpleLine = simpleLine.replace(' ', '')
#     simpleLine = simpleLine.replace('.','')
#     simpleLine = simpleLine.replace(',','')    
#     simpleLine = simpleLine.replace('/','') 
#     simpleLine = simpleLine.replace('\\','') 
#     simpleLine = simpleLine.replace('\"','') 
#     simpleLine = simpleLine.replace('\'','') 
#     simpleLine = simpleLine.replace('(','') 
#     simpleLine = simpleLine.replace(')','') 
# =============================================================================
    return simpleLine

# =============================================================================
# Removes just accents and makes lower    
# =============================================================================
def simpleLine(in_str):    
    if not isinstance(in_str, str):
        raise TypeError('Must be \'str\'not \'%s\''%type(in_str))
    # Remove accents and lower all line
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    simpleStr = str(in_str).lower()    
    for accent in accents:
        simpleStr = simpleStr.replace(accent, accents[accent])    
    return simpleStr   

# =============================================================================
# Sets similarityRatio value, by default its 70%
# =============================================================================
def setSimilarityRatio(ratio):
    global similarityRatio
    if isinstance(ratio, (int, float)):
        similarityRatio = ratio
    else:
        raise TypeError('Must be \'int\' or \'float\' not \'%s\''%type(ratio))
        
# =============================================================================
# Function returns if two string are similar and returns the similarity ratio
# 
# Improve line for comparison removing elements such as Cpitals or simbols that 
# may affect comparison    
# =============================================================================
def areSimilar(in_str1, in_str2):
    global similarityRatio
    if not isinstance(in_str1, str) or not isinstance(in_str2, str):
        raise TypeError('Input arguments must be (\'str\', \'str\') not' 
                        + '(\'%s\', \'%s\')'%(type(in_str1),type(in_str2)))
    #Diference ratio
    simRatio = difflib.SequenceMatcher(None, simplifyLine(in_str1), 
                                simplifyLine(in_str2)).ratio()       
    #If the similarity is enought return true else false, and return the ratio 
    if simRatio >= similarityRatio:
        return True, simRatio
    else:
        return False, simRatio

# =============================================================================
# Function returns if two string are similar and returns the similarity ratio
# 
# No line modification, absolute comparison  
# =============================================================================
def areSimilarAbsolute(in_str1, in_str2):
    global similarityRatio
    if not isinstance(in_str1, str) or not isinstance(in_str2, str):
        raise TypeError('Input arguments must be (\'str\', \'str\') not' 
                        + '(\'%s\', \'%s\')'%(type(in_str1),type(in_str2)))
    #Diference ratio
    simRatio = difflib.SequenceMatcher(None, in_str1, in_str2).ratio()       
    #If the similarity is enought return true else false, and return the ratio 
    if simRatio >= similarityRatio:
        return True, simRatio
    else:
        return False, simRatio
    
#Sets the variables value
def setFixCompResult(in_bool):
    global fixCompResult
    if not isinstance(in_bool, bool):
        raise TypeError('Must be \'bool\'not \'%s\''%type(in_bool))
    fixCompResult = in_bool


# =============================================================================
# Sets the value for minLettersDifferent
# =============================================================================
def setMinLettersDiferent(in_num):
    global minLettersDifferent
    if isinstance(in_num, (int, float)):
        raise TypeError('Must be \'bool\'not \'%s\''%type(in_num))
    else:
        minLettersDifferent = int(in_num)
        
# =============================================================================
# If Word has been found to be diferent, and there are more than X diferent elements
# we return true fix the indexes to refer the whole word
# =============================================================================
def wordFound(strIdxs, idxs):
    global minLettersDifferent
    count = 0
    for x in strIdxs:
        if x in idxs:
            count += 1
        if count >= minLettersDifferent:
            return True
    return False

# =============================================================================
# Return the indexes for every word in input string
# =============================================================================
def getStringIdxs(in_str):    
    strIdxs = []
    aux = splitBySymbols(in_str)
    aux = list(filter(lambda x: x != '' and x != ' ', aux))
    a = 0
    i = 0
    while i < len(in_str) or a < len(aux):
        word = aux[a]
        if in_str[i:i+len(word)] == word:
            strIdxs.append([aux[a], [x + i for x in list(range(len(aux[a])))]])
            a += 1
            i += len(word)
            if a >= len(aux):
                break
        else:
            i += 1
    return strIdxs

# =============================================================================
# Function fix results indexes if fixCompResult and for every word there are 
# minLettersDifferent letters wrong
# =============================================================================
def fixComparisonResultIdx(doc, idxs):
    global fixCompResult
    newIdxs = []
    for word in getStringIdxs(doc):
        if wordFound(word[1], idxs):
            newIdxs.extend(word[1])
    idxs.extend(newIdxs)
    idxs = list(dict.fromkeys(idxs))
    idxs.sort()
    return idxs

# =============================================================================
# Function compares and returns diference betweent two elements    
# =============================================================================
def compare(in_str1, in_str2):    
    global fixCompResult
    if not isinstance(in_str1, str) or not isinstance(in_str2, str):
        raise TypeError('Input arguments must be (\'str\', \'str\') not' 
                        + '(\'%s\', \'%s\')'%(type(in_str1),type(in_str2)))        
    compared = []    
        
    #Calcular diferencia
    matches = difflib.ndiff(in_str1, in_str2)
    matches = (list(matches))
    
    #Ubicacion en el string de las diferencias
    str_Idx_1 = []
    str_Idx_2 = []
    str_Result_1 = []
    str_Result_2 = []
    
    for match in matches:
        if match[0] == '-':
            str_Idx_1.append(len(str_Result_1))
            str_Result_1.append(match[1:])
        elif match[0] == '+':
            str_Idx_2.append(len(str_Result_2))
            str_Result_2.append(match[1:])        
        elif match[0] == '?':
            continue
        else:#saving results of comparison
            str_Result_1.append(match)
            str_Result_2.append(match)            
        
        if fixCompResult:
            str_Idx_1 = fixComparisonResultIdx(in_str1, str_Idx_1)
            str_Idx_2 = fixComparisonResultIdx(in_str2, str_Idx_2)
            
    compared = [in_str1, str_Idx_1, in_str2, str_Idx_2]
    return compared


# =============================================================================
# Compare every element from input string list to input strin
# =============================================================================
def compareListToString(in_list, in_str):  
    if not isinstance(in_list, list) or not isinstance(in_str, str):
        raise TypeError('Input arguments must be (\'list\', \'str\') not' 
                        + '(\'%s\', \'%s\')'%(type(in_list),type(in_str)))    
        
    compared = []    
    for string in in_list:
        compared.append(compare(string, in_str))
    return compared

# =============================================================================
# Function returns index of lines that match given regular expresion
# =============================================================================
def getIdxStringByRegex(regex, in_target):
    found = []
    if isinstance(in_target, str):
        in_target = [in_target]
    elif not(isinstance(in_target, list) and 
             all(isinstance(element, str) for element in in_target)):
        raise TypeError('Must be \'list\'or \'str\' not \'%s\''%type(in_target))    
    
    found = [i for i in range(len(in_target)) if re.search(regex,in_target[i])]
    return found


# =============================================================================
# Finds Best match contained in a string
# =============================================================================
def getBestMatchInStringSimple(goal, target):        
    bestMatch = None
    bestRatio = 0.0               
    #Split words by spaces to group them later
    subStrings = target.split(' ')   

    # Joining points that may be afte a space
    for x in reversed(range(1, len(subStrings))):
        if re.search('[\.,]',subStrings[x]) and re.search('[a-zA-z]', subStrings[x-1][-1]):
            subStrings[x-1] = subStrings[x-1] + ' ' + subStrings[x]
            subStrings = subStrings[:x] + subStrings[x+1:]        
    
    #Crea agrupaciones de j = (1,2,...,len(lineWords)) h  
    for j in range(1, len(subStrings)+1):
        for st in range(len(subStrings)):
            end = st + j            
            if end < len(subStrings)+1:                    
                partial = ' '.join(subStrings[st:end])
                sim, r = areSimilar(partial, goal)
                if sim and r > bestRatio:
                    if r == 1.0:
                        return (partial, r)
                    else:
                        bestMatch = partial
                        bestRatio = r
            else:                    
                break              
    return (bestMatch, bestRatio)

# =============================================================================
# Sets maxLines value
# =============================================================================
def setMaxLinesLookup(maximum):
    global maxLines 
    maxLines = maximum
    
# =============================================================================
# Finds the best match, may be in line and contained between multiple lines, 
# can choose the number of line
# =============================================================================
def getBestMatchInString(goal, target):
    global maxLines
    
    bestMatch = None
    bestRatio = 0.0    
    positions = []
    extendedLines = []
    bestPosicion = []    
    
    for i in range(len(target)):
        if target[i] == '':
            continue
        line = target[i]
        (bm, r) = getBestMatchInStringSimple(goal, line)
        if r == 1 and bm == goal:                
            return (bm, r, [i])
        elif r > bestRatio:
            bestRatio = r
            bestMatch = bm             
            bestPosicion = [i]
    
    for i in range(len(target)):                        
        #Generate Extended lines
        if target[i] == '':
            continue
        line = target[i]
        positions.append(i)
        extendedLines.append(line)        
        for a in range(1,maxLines):            
            if len(target) > i+a:
                if target[i+a] == '':
                    break
                line  += ' ' + target[i+a]
                extendedLines.append(line)
                positions.append(list(range(i, i+a+1)))    
        #Calculate Similarities
    for j in range(len(extendedLines)):
        line = extendedLines[j]
        (bm, r) = getBestMatchInStringSimple(goal, line)
        if r == 1 and bm == goal:         
            return (bm, r, positions[j])
        elif r > bestRatio:
            bestRatio = r
            bestMatch = bm             
            bestPosicion = positions[j]                               
    return (bestMatch, bestRatio, bestPosicion)


# =============================================================================
# Finds the best maches of the given string
# =============================================================================
def getBestMatchesInString(goal, target):
    target = list(target)
    bestMatches = []      
    while(True):   
        bestMatch = getBestMatchInString(goal, target)
        if bestMatch[0] == None:
            break    
        else:
#            print('BM: \"%s\" - %s\n%s-%s\n'%(bestMatch[0], goal, str(areSimilar(bestMatch[0], goal)), str(bestMatch[2])))
            bestMatches.append(bestMatch)
            linesFound = bestMatch[2]  
            for i in linesFound:
                target[i] = ''            
    return bestMatches

