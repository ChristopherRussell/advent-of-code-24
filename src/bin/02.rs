use itertools::Itertools;
use tracing::{debug, info};
advent_of_code::solution!(2);

fn iter_is_increasing<'a, I>(iter: I, max_step: i32) -> bool
where
    I: Iterator<Item = &'a i32>,
{
    iter.tuple_windows().all(|(x, y)| is_safe(x, y, max_step))
}

fn is_safe(x: &i32, y: &i32, max_step: i32) -> bool {
    let safe = (x - y <= max_step) & (x - y > 0);
    if safe {
        debug!(x = x, y = y, "safe pair");
    } else {
        debug!(x = x, y = y, "unsafe pair");
    }
    safe
}

fn line_is_safe(line: &str, max_step: i32) -> bool {
    let vec = line_to_vec(line);
    if iter_is_increasing(vec.iter(), max_step) {
        info!(vec = ?vec, "safe vector (forward)");
        return true;
    }
    if iter_is_increasing(vec.iter().rev(), max_step) {
        info!(vec = ?vec, "safe vector (backward)");
        return true;
    }
    info!(vec = ?vec, "unsafe in both directions");
    false
}

fn line_to_vec(line: &str) -> Vec<i32> {
    line.split(' ')
        .map(|s| s.parse::<i32>().unwrap())
        .collect::<Vec<i32>>()
}

pub fn part_one(input: &str) -> Option<u32> {
    // Initialize tracing subscriber
    Some(input.lines().map(|line| line_is_safe(line, 3) as u32).sum())
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut safe_count = 0;
    for mut vec in input.lines().map(line_to_vec) {
        debug!(vec = ?vec, "checking vector");
        if check_safe_v2(&vec) {
            info!("safe vector (forward)");
            safe_count += 1;
            continue;
        }
        vec.reverse();
        if check_safe_v2(&vec) {
            info!("safe vector (backward)");
            safe_count += 1;
        } else {
            info!("unsafe vector");
        }
    }
    Some(safe_count)
}

fn check_safe_v2(slice: &[i32]) -> bool {
    for (first_idx, (x, y)) in slice.iter().tuple_windows().enumerate() {
        if !is_safe(x, y, 3) {
            debug!(index = first_idx, "trying without x or y");
            return iter_is_increasing(
                slice[..first_idx]
                    .iter()
                    .chain(slice[first_idx + 1..].iter()),
                3,
            ) | iter_is_increasing(
                slice[..first_idx + 1]
                    .iter()
                    .chain(slice[first_idx + 2..].iter()),
                3,
            );
        }
    }
    true
}
#[cfg(test)]
mod tests {
    use super::*;

    fn init_tracing() {
        // Don't initialize twice if running both tests at once.
        let _ = tracing_subscriber::fmt::try_init();
    }

    #[test]
    fn test_part_one() {
        init_tracing();
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(2));
        let result = part_one(&advent_of_code::template::read_file_part(
            "examples", DAY, 1,
        ));
        assert_eq!(result, Some(2));
    }

    #[test]
    fn test_part_two() {
        init_tracing();
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4));

        let result = part_two(&advent_of_code::template::read_file_part(
            "examples", DAY, 2,
        ));
        assert_eq!(result, Some(6));
    }
}
