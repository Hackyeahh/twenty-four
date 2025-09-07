# twenty-four

My friend Caleb is really good at [this](https://en.wikipedia.org/wiki/24_(puzzle)) game. I've consistently lost to his speed and sheer ability to calculate.

No more.

## What is the 24 Game?

The 24 puzzle is a mathematical game where you must manipulate four given integers to create the number 24, using only basic arithmetic operations (+, -, ×, ÷) and parentheses. Each number must be used exactly once.

**Example:** With `4, 7, 8, 8`:
- ✅ `(7 - (8 ÷ 8)) × 4 = 24`  
- ❌ `4 × 7 - 8 = 20` (doesn't equal 24)

Some combinations like `3, 3, 8, 8` have no solution - this solver will tell you definitively.


## Installation

```bash
pip install twenty-four
```

## Usage

```bash
# Solve directly from command line
twenty-four 2 2 3 6
> INFO     | took 25.76ms to search 1368 nodes.
> INFO     | 11.2% = (153/1368) were cache hits!
> SUCCESS  | solution: [2÷2=1.0] [3+1.0=4.0] [6×4.0=24.0] 
> INFO     | (6 more solutions available with --all)

# Interactive mode (no arguments)
twenty-four
> INFO     | enter 4 numbers for the 24 game:
> number 1: 3
> number 2: 3
> number 3: 8
> number 4: 8
> INFO     | took 8.31ms to search 1035 nodes.
> INFO     | 6.6% = (68/1035) were cache hits!
> ERROR    | no solution found

# Show all possible solutions
twenty-four --all 1 5 7 13
> INFO     | took 38.41ms to search 2803 nodes.
> INFO     | 7.0% = (195/2803) were cache hits!
> SUCCESS  | found 47 solutions:
> INFO     |   1. [1-5=-4] [7+13=20] [20--4=24] 
> INFO     |   2. [1-5=-4] [7-13=-6] [-4×-6=24]

# Quiet mode (clean output)
twenty-four --quiet 6 6 6 6  
> solution: [6+6=12] [6+6=12] [12+12=24]

# Quick alias
s24 2 2 3 6
> INFO     | took 19.67ms to search 1368 nodes.
> INFO     | 11.2% = (153/1368) were cache hits!
> SUCCESS  | solution: [2÷2=1.0] [3+1.0=4.0] [6×4.0=24.0] 
> INFO     | (6 more solutions available with --all)
```
