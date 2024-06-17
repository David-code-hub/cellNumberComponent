points = {
    "three1s": 1000, 
    "three2s": 200,
    "three3s":300, 
    "three4s": 400, 
    "three5s":500, 
    "three6s": 600,
    "one1": 100,
    "one5": 50,
}

def score(array):
    score = 0
    threePatternFound = {
        "count":0,
        "number": 0
    }
    for n in array:
        #check if value appears 3 or more in array
        if(array.count(n) >= 3):
            #add points
            if(n != threePatternFound['number']) : score += points[f'three{n}s']
            #store value so that we can reference it
            threePatternFound["count"] += 1
            threePatternFound["number"] = n
            #if the pattern has more that 3 occurances then add the 'one' points
            if(threePatternFound["count"] >= 4): score += points[f'one{n}']
        #if it's normal nums : does not occure 3 or more times
        elif n == 1 or n == 5:
            score += points[f'one{n}']

    print("total",score)
    pass


score([5, 1, 3, 4, 1])
score([1, 1, 1, 3, 1])
score([2, 4, 4, 5, 4])
score([1, 1, 1, 1, 1])