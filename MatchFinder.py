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
