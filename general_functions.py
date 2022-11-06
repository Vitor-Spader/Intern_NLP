def less_equals(aux,det,aux0,intent):
    for x in aux:
        for y in det:
            if x == y:
                del det[det.index(y)]
    for x in aux0:
        for y in intent:
            if x == y:
                del intent[intent.index(y)]
    return det,intent

def less(det,intent):
    axu0 = det[0]
    axu1 = intent[0]
    for x in set(det):
        if axu0 > x:
            axu0 = x
    
    for y in set(intent):
        if axu1 > y:
            axu1 = y
    return axu0,axu1

def det_append(question,det,intent,x,y):
    for d,d0 in det:
        if x == d0:
            print(x)
            for r,r0 in intent:
                if y == r0:
                    print(y)
                    question["intent"].append({d:r})    
def test_exist(question,x):
    for y in question["intent"]:
        for i,z in y.items():
            if z == x:
                return True
    return False