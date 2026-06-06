import argparse
import asyncio
import sys
from typing import Any

from .main import run


def parse_distribution(value: str) -> dict[str, Any]:
    try:
        # Expected format:
        # create_distribution, delay_distribution,
        # event_value_distribution, client_count
        # Example: normal,10
        (
            create_distribution,
            delay_distribution,
            event_value_distribution,
            clients,
        ) = value.split(",")
        return {
            "create_distribution": create_distribution,
            "delay_distribution": delay_distribution,
            "event_value_distribution": event_value_distribution,
            "clients": int(clients),
        }
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            "Distributions must be formatted as 'type,clients' (e.g., normal,10)"
        ) from err


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discrete Event Simulator")
    parser.add_argument(
        "--dist",
        type=parse_distribution,
        action="append",
        required=True,
        help=(
            "Specify distribution and clients as 'type,clients'. "
            "Example: --dist normal,10 --dist poisson,5"
        ),
    )

    parsed_args = parser.parse_args()

    # Iterate through your configured client groups
    for config in parsed_args.dist:
        print(
            f"Spawning {config['clients']} clients with "
            f"{config['create_distribution']} event creation distribution, "
            f"{config['delay_distribution']} delay distribution, "
            f"{config['event_value_distribution']} event value distribution."
        )

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
