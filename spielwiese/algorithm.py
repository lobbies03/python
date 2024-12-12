from array import array


def searchInArray():
    nums = [2, 3, 5, 7, 9]
    target = 7

    for i in range(len(nums)):
        if target == nums[i]:
            print("Element found at index", i)
