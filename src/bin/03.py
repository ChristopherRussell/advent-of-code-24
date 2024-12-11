import re

mult_pattern = re.compile(r"mul\((\d+),(\d+)\)")
answer1 = 0


def get_answer_for_line(line):
    answer = 0
    mult_pairs = re.findall(mult_pattern, line)
    for x, y in mult_pairs:
        answer += int(x) * int(y)
    return answer


with open("/Users/crussell/AoC/advent-of-code-24/data/inputs/03.txt", "r") as file:
    for line in file:
        answer1 += get_answer_for_line(line)

print(f"answer1: {answer1}")

do_pattern = re.compile(r"do\(\)")

answer2 = 0
with open("/Users/crussell/AoC/advent-of-code-24/data/inputs/03.txt", "r") as file:
    # We cant read line-by-line as do and don't effects persist across lines.
    line = "".join(file)
    # apart from the first one, every split starts in don't mode
    splits = line.split("don't()")
    answer2 += get_answer_for_line(splits[0])
    for split in splits[1:]:
        # Once we see a do(), we can count all multiplies after that in the split.
        first_do = re.search(do_pattern, split)
        if first_do:
            first_do_end_idx = first_do.end()
            answer = get_answer_for_line(split[first_do_end_idx:])
            # print(answer)
            answer2 += answer

print(f"answer2: {answer2}")
