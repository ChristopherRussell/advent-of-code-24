//! Bit rusty on rust, didn't worry about optimizing anything or making the code pretty.
use std::collections::HashMap;

advent_of_code::solution!(1);

pub fn part_one(input: &str) -> Option<u32> {
    let mut list1 = vec![];
    let mut list2 = vec![];
    for line in input.lines() {
        let mut ints = line
            .split("   ")
            .map(|s| s.parse::<i64>().expect("Could not parse input as integer"));
        list1.push(ints.next().expect("Didn't find any ints on line"));
        list2.push(ints.next().expect("Didn't find a second int on line"));
        if ints.next().is_some() {
            panic!("Found more than two integers in line")
        }
    }
    list1.sort();
    list2.sort();
    Some(
        list1
            .into_iter()
            .zip(list2)
            .map(|(x, y)| (x - y).abs())
            .sum::<i64>()
            .try_into()
            .expect("Failed to cast i64 result of sum to u32"),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut map1 = HashMap::new();
    let mut map2 = HashMap::new();
    for line in input.lines() {
        let mut ints = line
            .split("   ")
            .map(|s| s.parse::<u32>().expect("Could not parse input as u32"));
        let int1 = ints.next().expect("Didn't find any ints on line");
        let int2 = ints.next().expect("Didn't find a second int on line");
        map1.entry(int1).and_modify(|e| *e += 1).or_insert(1);
        map2.entry(int2).and_modify(|e| *e += 1).or_insert(1);
        if ints.next().is_some() {
            panic!("Found more than two integers in line")
        }
    }
    let mut result = 0;
    for (key, value1) in map1 {
        let value2 = map2.get(&key);
        if let Some(x) = value2 {
            result += key * value1 * x;
        }
    }
    Some(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(11));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(31));
    }
}
