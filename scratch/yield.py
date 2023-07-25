def infinite_sequence():
    num = 0
    while num != 10:
        yield num
        num += 1
        yield num
        num += 1


generator = infinite_sequence()
#print(list(generator))

for i in generator:
    print(i)