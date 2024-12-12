def IsNumberInList(number, list):
    l = 0
    h = len(list)-1
    lastMid = 0
    loops = 0

    while True:
        loops += 1
        mid = round((l+h)/2)
        # print(mid)

        if number == list[mid]:
            print("loops:", loops)
            return True
        if lastMid == mid:
            break
        elif number > list[mid]:
            l = mid
        else:
            h = mid
        lastMid = mid

    print("loops:", loops)
    return False


a = [1, 3, 5, 30, 42, 43, 500]
number = 41

if IsNumberInList(number, a):
    print(f"{number} is in list.")
else:
    print(f"{number} is not in list")
