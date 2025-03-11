def two_highest(arr):
    sorted_arr = sorted(arr)
    return sorted_arr[-1], sorted_arr[-2]

def two_lowest(arr):
    sorted_arr = sorted(arr)
    return sorted_arr[0], sorted_arr[1]


T = int(input())

for _ in range(T):
    N = int(input())
    arr = list(map(int,input().split()))
    if len(arr) >= 4:
        max1, max2 = two_highest(arr)
        min1, min2 = two_lowest(arr)
        print(max1 + max2 - min1 - min2)
    if len(arr) <= 3:
        sorted_arr = sorted(arr)
        print(sorted_arr[-1] - sorted_arr[0])