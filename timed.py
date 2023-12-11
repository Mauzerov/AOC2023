from timeit import timeit
import termplotlib as tpl
import re


if __name__ == '__main__':
    with open("main.py") as f:
        lines = f.read().splitlines()
        times = []
        for line in lines:
            time = timeit(line, number=1)
            day_label = "Day #" + re.findall(r'\d+', line)[0]
            times.append((day_label, time))
            print(f"Time taken: {time:.4f} seconds for: {day_label!r}")

    # Analyze results
    print("\nAnalyzing results...")
    slowest = max(times, key=lambda x: x[1])
    fastest = min(times, key=lambda x: x[1])
    print(f"Slowest day took: {slowest[1]:.4f} seconds for: {slowest[0]!r}")
    print(f"Fastest day took: {fastest[1]:.4f} seconds for: {fastest[0]!r}")
    # Plot results
    fig = tpl.figure()
    fig.barh(
        labels=list(map(lambda x: x[0], times)),
        vals=list(map(lambda x: round(x[1], 5), times)),
        val_format="{:.5f}s",
    )
    fig.show()
