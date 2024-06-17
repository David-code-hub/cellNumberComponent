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
        if(n != threePatternFound["number"] ):
            if(array.count(n) >= 3 ):
                score += points[f'three{n}s']
                threePatternFound["count"] += 1
                threePatternFound["number"] = n
            if n == 1:
                score += points["one1"]
            if n == 5:
                score += points["one5"]

    print("total",score)
    pass



score([5, 1, 3, 4, 1])
score([1, 1, 1, 3, 1])
score([2, 4, 4, 5, 4])