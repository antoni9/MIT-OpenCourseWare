# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time
import csv

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects = {}
    inputFile = open(filename)
    openedFile = csv.reader(inputFile)
    for line in openedFile:
        subjects[line[0]] = (int(line[1]), int(line[2]))
    inputFile.close()
    return subjects

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t=====\t====\n'
    subNames = subjects.keys()
    # subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print(res)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    res = {}
    work = 0
    while work < maxWork:
        temp = {}
        keys = sorted(subjects.keys() - res.keys(), key=float)
        for key in keys:
            if len(temp) < 1:
                temp[key] = subjects[key]
            if comparator(subjects[key], temp[[*temp][0]]):
                if subjects[key][1] + work > maxWork:
                    None
                else:
                    temp.clear()
                    temp[key] = subjects[key]
        work += temp[[*temp][0]][1]
        res.update(temp)
    return printSubjects(res)


def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = list(subjects.keys())
    tupleList = list(subjects.values())
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in list(bestSubset):
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    # TODO...
    start = time.time()
    res = bruteForceAdvisor(subjects, 8)
    timeTaken = time.time() - start
    print(res, timeTaken)

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance

# maxWork = 5, subjectList = subjects, timeTaken = 1.137228012084961
# maxWork = 6, subjectList = subjects, timeTaken = 3.6648690700531006 - too long
# maxWork = 7, subjectList = subjects, timeTaken = 11.948483228683472

#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    memo = {}
    workList = []
    valueList = []
    keyList = list(subjects.keys())
    i = len(keyList)-1
    for item in keyList:
        valueList.append(subjects[item][0])
        workList.append(subjects[item][1])
    res = dpAdvisorHelper(workList, valueList, keyList, i, maxWork, memo)
    print(memo)
    return res


def dpAdvisorHelper(workList, valueList, keyList, i, maxWork, memo):
    try:
        return memo[(i, maxWork)]
    except KeyError:
        if i == 0:
            if workList[i] <= maxWork:
                memo[(i, maxWork)] = valueList[i]
                return valueList[i]
            else:
                memo[(i, maxWork)] = 0
                return 0
        without_i = dpAdvisorHelper(workList, valueList, keyList, i-1, maxWork, memo)
        if workList[i] > maxWork:
            memo[(i, maxWork)] = without_i
            return without_i
        else:
            with_i = valueList[i] + dpAdvisorHelper(workList, valueList, keyList, i-1, maxWork - workList[i], memo)
            res = max(with_i, without_i)
            memo[(i, maxWork)] = res
            return res




#
# Problem 5: Performance Comparison
#
def dpTime():
    start = time.time()
    res = dpAdvisor(subjects, 15)
    timeTaken = time.time() - start
    print(res, timeTaken)

# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.


if __name__ == '__main__':
    subjects = loadSubjects(SUBJECT_FILENAME)
    # printSubjects(subjects)
    # greedyAdvisor(subjects, 15, cmpRatio)
    # bruteForceAdvisor(subjects, 15)
    # bruteForceTime()
    dpTime()