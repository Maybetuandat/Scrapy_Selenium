a = ['o', 'a', 2]
index = 0
while true:
    try:
        print(1/a[index])
    except Exception as e:
        index += 1
        continue