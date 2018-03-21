from string import *

target1 = 'atgacatgcacaagtatgcat'
target2 = 'atgaatgcatggatgtaaatgcag'

key10 = 'a'
key11 = 'atg'
key12 = 'atgc'
key13 = 'atgca'

def countSubStringRecursive(target, key):
    occurances = 0
    a = 0
    while a > -1:
        a = target.find(key)
        target = target[a+1: len(target)]
        if a > -1:
            occurances += 1
    return(occurances)

def subStringMatchExact(target, key):
    occurances = ()
    a = 0
    n = 0
    if not key:
        for n in range(0, len(target)):
            tup =(a,)
            occurances = occurances + tup
            a += 1
    else: 
        while a > -1:
            a = target.find(key, n)
            n += 1
            if a > -1 and a not in occurances:
                tup = (a,)
                occurances = occurances + tup
    return(occurances)


def constrainedMatchPair(firstMatch,secondMatch,length):
    result = ()
    for k in secondMatch:
        for n in firstMatch:
            if n + length + 1 == k:
                result = result + (n,)
    return(result)


### the following procedure you will use in Problem 3


def subStringMatchOneSub(key,target):
    """search for all locations of key in target, with one substitution"""
    allAnswers = ()
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        print ('breaking key',key,'into',key1,key2)
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
        print ('match1',match1)
        print ('match2',match2)
        print ('possible matches for',key1,key2,'start at',filtered)
        print ('----------------------------------------------------')
    return allAnswers

def subStringMatchExactlyOneSub(target1,key13):
    noSubs = subStringMatchExact(target, key)
    withSubs = subStringMatchOneSub(key, target)
    finalResult = ()
    for x in withSubs:
        if x not in noSubs:
            finalResult = finalResult + (x,)
    print('------------------------------------')
    print(noSubs)
    print(withSubs)
    return(finalResult)
