from collections import defaultdict

import numpy as np
import polars as pl

#   We create an array for each horizonal, vertical, and diagonal (both left to right,
#   and right to left) of the matrix. Then we can simply count XMAS and SAMX occurences
#   on all of those arrays.

with open("/Users/crussell/AoC/advent-of-code-24/data/inputs/04.txt", "r") as file:
    df = pl.DataFrame(list(list(line.strip("\n")) for line in file)).select(
        pl.all().replace_strict(
            {"X": 1, "M": 2, "A": 4, "S": 8}, default=0, return_dtype=pl.Int8
        )
    )
XMAS = np.array([1, 2, 4, 8], dtype="int8")
SAMX = np.array([8, 4, 2, 1], dtype="int8")

df_T = df.transpose()
diagonals1_map = defaultdict(list)
diagonals2_map = defaultdict(list)
diagonals1_coords = defaultdict(list)
diagonals2_coords = defaultdict(list)

n_rows, n_cols = df.shape
arr = df.to_numpy()
arr_T = arr.T
horizontals = [arr[:, i] for i in range(n_cols)]
verticals = [arr_T[:, j] for j in range(n_rows)]


for i in range(n_rows):
    for j in range(n_cols):
        diagonals1_map[i - j].append(arr[i, j])
        diagonals2_map[n_cols - i - j - 1].append(arr[i, j])
        diagonals1_coords[i - j].append((i, j))
        diagonals2_coords[n_cols - i - j - 1].append((i, j))

diagonals1_map = {k: np.array(v, dtype="int8") for k, v in diagonals1_map.items()}
diagonals2_map = {k: np.array(v, dtype="int8") for k, v in diagonals2_map.items()}
for k, v in diagonals1_coords.items():
    diagonals1_coords[k] = min(v, key=lambda x: x[1])
for k, v in diagonals2_coords.items():
    diagonals2_coords[k] = max(v, key=lambda x: x[1])


count = 0
for name, direction in {
    "horizontals": horizontals,
    "vert": verticals,
    "diag1": list(diagonals1_map.values()),
    "diag2": list(diagonals2_map.values()),
}.items():
    _count_forward = 0
    _count_backward = 0
    for series in direction:
        for i in range(len(series) - 3):
            _count_forward += np.all(series[i : i + 4] == XMAS)
            _count_backward += np.all(series[i : i + 4] == SAMX)
    count += _count_forward + _count_backward
print(f"answer1: {count}")


# Pt2
#   We find the co-ordinates of all the A's in diagonals going from left to right,
#   and in diagonals going from right to left. Then, the number of X-mas is the
#   size of the intersection of these two sets of co-ordinates.

MAS = np.array([2, 4, 8], dtype="int8")
SAM = np.array([8, 4, 2], dtype="int8")


def get_a_coords_1(diagonals, start_coords) -> list[tuple[int, int]]:
    """Get the (x,y) co-ordinates of A in MAS in left-to-right diagonals"""
    mas_a_coords = []
    for offset, series in diagonals.items():
        start_x, start_y = start_coords[offset]
        for i in range(len(series) - 2):
            x = start_x + i
            y = start_y + i
            if np.all(series[i : i + 3] == MAS):
                mas_a_coords.append((x + 1, y + 1))
            if np.all(series[i : i + 3] == SAM):
                mas_a_coords.append((x + 1, y + 1))
    return mas_a_coords


def get_a_coords_2(diagonals, start_coords) -> list[tuple[int, int]]:
    """Get the (x,y) co-ordinates of A in MAS in right-to-left diagonals"""
    # Note: almost the same as above function, except y decreases as x increases
    mas_a_coords = []
    for offset, series in diagonals.items():
        start_x, start_y = start_coords[offset]
        for i in range(len(series) - 2):
            x = start_x + i
            y = start_y - i  # only part different from above function
            if np.all(series[i : i + 3] == MAS):
                mas_a_coords.append((x + 1, y - 1))
            if np.all(series[i : i + 3] == SAM):
                mas_a_coords.append((x + 1, y - 1))
    return mas_a_coords


mas_a_coords_1 = get_a_coords_1(diagonals1_map, diagonals1_coords)
mas_a_coords_2 = get_a_coords_2(diagonals2_map, diagonals2_coords)

x_mas_a_coords = (
    pl.Series(mas_a_coords_1)
    .list.to_struct()
    .struct.unnest()
    .join(
        pl.Series(mas_a_coords_2).list.to_struct().struct.unnest(),
        on=["field_0", "field_1"],
        how="inner",
    )
)
answer2 = x_mas_a_coords.height
print(f"answer2: {answer2}")
