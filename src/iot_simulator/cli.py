import argparse
import asyncio
import sys
from typing import Any

from .main import run


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discrete Event Simulator")
    
    parser.add_argument(
        "--num_clients",
        required=True,
        type=int,
        help=(
            "The number of clients to generate"
        ),
    )
    
    parser.add_argument(
        "--max_workers",
        required=True,
        help=(
            "The number of workers to generate"
        ),
        type = int
    )

    parsed_args = parser.parse_args()

    # Iterate through your configured client groups
    print(f"Spawning {parsed_args.num_clients} clients with ")

    return parsed_args


async def async_main() -> None:
    args = parse_args(sys.argv[1:])
    await run(args)


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n[!] IoT Simulator stopped by user. Exiting gracefully...")


if __name__ == "__main__":
    main()
