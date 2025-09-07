import sys
from loguru import logger
import typer
from typing import List, Optional
from twenty_four.engine import solve_24

# remove default handler
logger.remove()

app = typer.Typer(
    help="solve the 24 game: make 24 from 4 numbers using +, -, ×, ÷",
    epilog="example: twenty-four 2 2 3 6",
)


@app.command()
def solve(
    numbers: Optional[List[int]] = typer.Argument(
        None, help="Four numbers to solve (if not provided, uses interactive mode)"
    ),
    all_solutions: bool = typer.Option(
        False, "--all", "-a", help="show all solutions, not just the first one"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="only show solutions, no performance info"
    ),
):
    """Solve the 24 game puzzle"""

    if quiet:
        # Only SUCCESS, WARNING, ERROR, CRITICAL
        logger.add(sys.stderr, format="{message}", level="SUCCESS")
    else:
        # All levels (INFO and above)
        logger.add(
            sys.stderr,
            format="<level>{level: <8}</level> | <level>{message}</level>",
        )

    # Get numbers
    if not numbers:
        numbers = get_numbers_interactive()
        if not numbers:
            return

    if len(numbers) < 4:
        logger.warning(
            "you gave less than 4 numbers. thats fine, but just letting you know :)"
        )

    if len(numbers) > 4:
        logger.warning(
            "things may slow down if you have more than 4 numbers. if things are too slow, feel free to make a PR to make things faster."
        )

    paths = solve_24(numbers)

    if paths:
        if all_solutions:
            logger.success(f"found {len(paths)} solutions:")
            for i, path in enumerate(paths, 1):
                logger.info(f"  {i}. {path}")
        else:
            logger.success(f"solution: {paths[0]}")
            if len(paths) > 1:
                logger.info(f"({len(paths) - 1} more solutions available with --all)")
    else:
        logger.error("no solution found")
        raise typer.Exit(1)


def get_numbers_interactive() -> Optional[List[int]]:
    """get 4 numbers interactively"""
    logger.info("enter 4 numbers for the 24 game:")
    numbers = []

    for i in range(4):
        try:
            num = typer.prompt(f"number {i + 1}", type=int)
            numbers.append(num)
        except typer.Abort:
            logger.info("Cancelled")
            return None

    return numbers


def main():
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
