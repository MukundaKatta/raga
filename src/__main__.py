"""CLI for raga."""
import sys, json, argparse
from .core import Raga

def main():
    parser = argparse.ArgumentParser(description="Raga — AI Indian Music Composer. Generates Indian classical music compositions with raga and tala awareness.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Raga()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.generate(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"raga v0.1.0 — Raga — AI Indian Music Composer. Generates Indian classical music compositions with raga and tala awareness.")

if __name__ == "__main__":
    main()
