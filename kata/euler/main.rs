//
// Project Euler
//


// Problem 1
// Multiples of 3 and 5
fn problem_0001() -> u32 {
    let mut sum = 0;
    for i in 1..1000 {
        if i % 3 == 0 || i % 5 == 0 {
            sum += i;
        }
    }
    sum
}

// Problem 2
// Even Fibonacci numbers
fn problem_0002() -> u32 {
    let mut sum = 0;
    let mut a = 1;
    let mut b = 2;
    while b < 4000000 {
        if b % 2 == 0 {
            sum += b;
        }
        let c = a + b;
        a = b;
        b = c;
    }
    sum
}

// Problem 3
// Largest prime factor
fn problem_0003() -> u64 {
    let mut n = 600851475143;
    let mut i = 2;
    while i * i <= n {
        if n % i == 0 {
            n /= i;
        } else {
            i += 1;
        }
    }
    n
}

fn main() {
   println!("Problem 1: {}", problem_0001());
   println!("Problem 2: {}", problem_0002());
   println!("Problem 3: {}", problem_0003());
}
