import asyncio
import argparse
import sys

from .main import run


def parse_distribution(value):
    try:
        # Expected format: distribution_name,client_count
        # Example: normal,10
        dist_type, clients = value.split(",")
        return {"type": dist_type, "clients": int(clients)}
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Distributions must be formatted as 'type,clients' (e.g., normal,10)"
        )


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discrete Event Simulator")
    parser.add_argument(
        "--dist",
        type=parse_distribution,
        action="append",
        required=True,
        help="Specify distribution and clients as 'type,clients'. Example: --dist normal,10 --dist poisson,5",
    )

    parsed_args = parser.parse_args()

    # Iterate through your configured client groups
    for config in parsed_args.dist:
        print(
            f"Spawning {config['clients']} clients with {config['type']} distribution."
        )

    return parsed_args


async def async_main() -> None:
    args = parse_args(sys.argv[1:])
    await run(args)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
