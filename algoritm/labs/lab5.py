n, k = map(int, input().split())
sort_array = list(map(int, input().split()))
numbers = list(map(int, input().split()))

for num in numbers:
    left, right=0, n-1
    found=0

    while left<=right:
        mid=(right+left)//2
        if sort_array[mid]==num:
            found=1
            break
        elif sort_array[mid]<num:
            left=mid+1
        else:
            right=mid-1

    if found == 1:
        print("YES")
    else:
        print("NO")
