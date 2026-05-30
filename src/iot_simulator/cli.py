import asyncio
import argparse
import sys

from .main import run


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Base Python Project CLI")
    return parser.parse_args(args)


async def async_main() -> None:
    _ = parse_args(sys.argv[1:])
    await run()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
