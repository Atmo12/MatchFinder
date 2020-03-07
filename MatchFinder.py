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

# =============================================================================
# Splits string by simbols (non words)
# =============================================================================
def splitBySymbols(string):
    return re.split('(\W)', string)

# =============================================================================
# Simplifies Lines removing accents, special characters, spaces, etc
# =============================================================================
def simplifyLine(line):    
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    simpleLine = str(line)
    simpleLine = simpleLine.lower()
    for letter in accents:
        simpleLine = simpleLine.replace(letter, accents[letter])
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
def simpleLine(line):    
    # Remove accents and lower all line
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    simpleLine = str(line)
    simpleLine = simpleLine.lower()
    for letter in accents:
        simpleLine = simpleLine.replace(letter, accents[letter])    
    return simpleLine   

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
def areSimilar(line1, line2):
    global similarityRatio
    #Diference ratio
    diffRatio = difflib.SequenceMatcher(None, simplifyLine(line1), 
                                simplifyLine(line2)).ratio()       
    if diffRatio >= similarityRatio: # If is the best similarity so far, it is saved
        return True, diffRatio
    else:
        return False, diffRatio
    
  