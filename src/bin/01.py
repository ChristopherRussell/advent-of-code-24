from collections import defaultdict

list1, list2 = [], []
map1, map2 = defaultdict(lambda: 0), defaultdict(lambda: 0)
with open("/Users/crussell/AoC/advent-of-code-24/data/inputs/01.txt", "r") as file:
    for line in file:
        x, y = map(int, line.split("   "))
        list1.append(x)
        list2.append(y)
        map1[x] += 1
        map2[y] += 1
list1.sort()
list2.sort()
answer1 = sum(map(lambda t: abs(t[0] - t[1]), zip(list1, list2)))
answer2 = sum(map(lambda t: t[0] * map2[t[0]] * t[1], map1.items()))
print(f"answer1: {answer1}")
print(f"answer2: {answer2}")
