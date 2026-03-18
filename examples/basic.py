"""Basic usage example for raga."""
from src.core import Raga

def main():
    instance = Raga(config={"verbose": True})

    print("=== raga Example ===\n")

    # Run primary operation
    result = instance.generate(input="example data", mode="demo")
    print(f"Result: {result}")

    # Run multiple operations
    ops = ["generate", "create", "validate]
    for op in ops:
        r = getattr(instance, op)(source="example")
        print(f"  {op}: {"✓" if r.get("ok") else "✗"}")

    # Check stats
    print(f"\nStats: {instance.get_stats()}")

if __name__ == "__main__":
    main()
