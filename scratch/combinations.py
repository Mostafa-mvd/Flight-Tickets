from itertools import combinations, product


def all_combinations(items_list):
    return combinations(items_list, 2)


def all_combinations2(item_list):
    def check_equal_constraint(letters):
        if (letters[0], letters[1]) != ("a", "b"):
            return letters
    return list(filter(check_equal_constraint, combinations(item_list, 2)))


items_list = ['a', 'b', 'c']
#result = all_combinations(items_list)
result = all_combinations2(items_list)

print(result)
print(list(all_combinations(items_list)))

#for combo in result:
    #print(combo)
