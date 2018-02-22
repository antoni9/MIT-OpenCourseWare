# Problem 1
#

def percent(percent, whole):
    return (percent * whole) / 100.0


fund = list([0])
def nestEggFixed(salary, save, growthRate, years):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: the annual percent increase in your investment account (an
      integer between 0 and 100).
    - years: the number of years to work.
    - return: a list whose values are the size of your retirement account at
      the end of each year.
    """
    # TODO: Your code here.
    for y in range (0, years):
        value = percent(save, salary) + max(fund) + percent(growthRate, max(fund))
        if fund[0] == 0:
            fund[0] = value
        else:
            fund.append(value)
    return fund

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print(savingsRecord)
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]

    # TODO: Add more test cases here.

def testNestEggFixedMine():
    salary     = 30600
    save       = 5
    growthRate = -10
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print(savingsRecord)

#
# Problem 2
#

def nestEggVariable(salary, save, growthRates):
    # TODO: Your code here.
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: a list of the annual percent increases in your investment
      account (integers between 0 and 100).
    - return: a list of your retirement account value at the end of each year.
    """
    for y in (growthRates):
        value = percent(save, salary) + max(fund) + percent(y, max(fund))
        if fund[0] == 0:
            fund[0] = value
        else:
            fund.append(value)
    return fund


def testNestEggVariable():
    salary      = 10000
    save        = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print(savingsRecord)
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]

    # TODO: Add more test cases here.

def testNestEggVariableMine():
    salary      = 30600
    save        = 5
    growthRates = [1.2, 1.1, 1.1, 0, 0.8]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print(savingsRecord)

#
# Problem 3
#

##def squareRootNR(x, epsilon):
##    assert x >= 0, +str(x)
##    assert epsilon > 0, +str(epsilon)
##    x = float(x)
##    guess = x/2.0
##    diff = guess**2 - x
##    ctr = 1
##    while abs(diff) > epsilon and ctr <= 100:
##        guess = guess - diff/(2.0*guess)
##        diff = guess**2 - x
##        ctr += 1
##    assert ctr<= 100
##    print(ctr, guess)
##    return guess


def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    # TODO: Your code here.
    saved = savings
    for y in (growthRates):
        value = (saved - expenses) + percent(y, (saved - expenses))
        if fund[0] == 0:
            fund[0] = value
        else:
            fund.append(value)
        saved = value
    return fund

def testPostRetirement():
    savings     = 100000
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 30000
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print(savingsRecord)
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]

    # TODO: Add more test cases here.

##def testPostRetirementMine():
##    savings     = 50000
##    growthRates = [1.1, 1.1, 1.1, 1.1, 1.1]
##    expenses    = 14400
##    savingsRecord = postRetirement(savings, growthRates, expenses)
##    print(savingsRecord)

#
# Problem 4
#


##def bsearch(s, e, first, last):
##    print(first, last)
##    if (last - first) < 2: return s[first] == e or s[last] == e
##    mid = int(first + (last - first)/2)
##    if s[mid] == e: return True
##    if s[mid] > e: return bsearch(s, e, first, mid-1)
##    return bsearch(s, e, mid+1, last)
##
##def search1(s, e):
##    return bsearch(s, e, 0, len(s)-1)

def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """
    # TODO: Your code here.

    savedPre = nestEggVariable(salary, save, preRetireGrowthRates)
    print(savedPre)
    
    expenses = range(0, int(max(savedPre)))
    xxx = int(max(savedPre))
    print(xxx)
    e = 5000
    savedPost = postRetirement(xxx, postRetireGrowthRates, e)
    print(savedPost)
    
##    first = 0
##    last = int(max(expenses))
##    mid = int(first + (last - first)/2)
##    ans = 0
##    while ans == 0:
##        if int(max(postRetirement(int(max(savedPre)), postRetireGrowthRates, e))) == .01:
##            ans = e
##            return e
##        if int(max(postRetirement(int(max(savedPre)), postRetireGrowthRates, e))) < .01:
##            e = int(first + (last - first)/2)
##            first = int(first + (last - first)/2)
##        if int(max(postRetirement(int(max(savedPre)), postRetireGrowthRates, e))) > .01:
##            e = int(first + (last - first)/2)
##            last = int(first + (last - first)/2)
##    print(ans)



##int(max(postRetirement(savedPre, postRetireGrowthRates, exp)))

   

def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print(expenses)
    # Output should have a value close to:
    # 1229.95548986

    # TODO: Add more test cases here
