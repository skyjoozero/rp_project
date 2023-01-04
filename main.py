def solution1(n):
    answer = sum([int(x) for x in str(n)] )
    return answer

def solution2(n):
    answer = 0
    x = 1
    while(x <= n):
        if(x % 2 ==0):
            answer += x
        x += 1
    return answer