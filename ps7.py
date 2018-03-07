# 1) What is the computational complexity of fact0? Explain your answer.
def fact0(i: object) -> object:
    assert type(i) == int and i >= 0
    if i == 0 or i == 1:
       return 1
    return i * fact0(i-1)
# Answer: When i increases, the number of times that fact0() is called increases proportionally.
# O() = O(i) + O(assert and if checks: 2*1)
# O(i) + O(2) = linear


# 2) What is the computational complexity of fact1? Explain your answer.
def fact1(i):
    assert type(i) == int and i >= 0
    res = 1
    while i > 1:
        res = res * i
        i -= 1
    return res
# Answer: When i increases, the number of times the while loop runs increases proportionally,
# however there's 2 commands the while loop is executing, complexity *= 2
# O() = O(i*2) + O(assert: 1) = linear


# 3) What is the computational complexity of makeSet? Explain your answer.
def makeSet(s):
    assert type(s) == str
    res = ''
    for c in s:
        if not c in res:
            res = res + c
    return res
# Answer: for each element of s python searches through res for s, due to the way lists are created each iteration of
# .find() = O(1)
# O() = O(s*1) = linear


# 4) What is the computational complexity of intersect? Explain your answer.
def intersect(s1, s2):
    assert type(s1) == str and type(s2) == str
    s1 = makeSet(s1)
    s2 = makeSet(s2)
    res = ''
    for e in s1:
        if e in s2:
            res = res + e
    return res
# Answer: for each element of s1 python searches through s2 for e, due to the way lists are created each iteration of
# .find() = O(1)
# However makeSet() calls = O(len(s1)) + O(ken(s2))
# O() = O(s*1) + O(len(s1)) + O(ken(s2))
# The overhead of makeSet() increases the overall O()


#5) Present a hand simulation of the code below. Describe the value to which each
#identifier is bound after each step of the computation. Note that “s1” and “s2” exist
#in more than one scope.
def swap0(s1, s2):
    assert type(s1) == list and type(s2) == list
    tmp = s1[:]
    s1 = s2[:]
    s2 = tmp
    return
s1 = [1]
s2 = [2]
swap0(s1, s2)
print(s1, s2)
# Answer: for each element of s1 python searches through s2 for e, due to the way lists are created each iteration of
# .find() = O(1)
# However makeSet() calls = O(len(s1)) + O(ken(s2))
# O() = O(s*1) + O(len(s1)) + O(ken(s2))
# The overhead of makeSet() increases the overall O()


#6) Present a hand simulation of the following code:
def swap1(s1, s2):
    assert type(s1) == list and type(s2) == list
    return s2, s1
s1 = [1]
s2 = [2]
s1, s2 = swap1(s1, s2)
print(s1, s2)
# This function doesn't do anything, but prints s1 and s2 in reverse order, no elements from lists were moved


#7) Present a hand simulation of the following code:
def rev(s):
    assert type(s) == list
    for i in range(int(len(s)/2))
        tmp = s[i]
        s[i] = s[-(i+1)]
        s[-(i+1)] = tmp
s = [1,2,3]
rev(s)
print(s)
# Answer: the list which is printed is not the final output of the function rev()