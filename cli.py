from loguru import logger
from main import solve_24, State, Counter

values = [int(input(f"provide number {i + 1}: ")) for i in range(4)]


paths = solve_24(values)

if paths:
    logger.success(f"{len(paths)} solutions found!")
    logger.success(paths[0])
else:
    logger.info("no solution found :(")
