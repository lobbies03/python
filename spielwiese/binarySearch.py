

arr = [3, 6, 8, 12, 14, 17, 25, 29, 31, 36, 42, 47, 53, 55, 62]
lo = 1
hi = len(arr)
mid = (lo+hi)/2

print(lo, hi, mid)


def binarySearch(arr, arrLength, key):
    l = 0
    h = arrLength
