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
            times.append((time, day_label))
            print(f"Time taken: {{:.5f}} seconds for: {{!r}}".format(*times[-1]))

    # Analyze results
    print("\nAnalyzing results...")
    slowest = max(times, key=lambda x: x[0])
    fastest = min(times, key=lambda x: x[0])
    print(f"Slowest day took: {{:.5f}} seconds for: {{!r}}".format(*slowest))
    print(f"Fastest day took: {{:.5f}} seconds for: {{!r}}".format(*fastest))
    # Plot results
    fig = tpl.figure()
    fig.barh(
        *zip(*times),
        val_format=f"{{:.5f}}s",
    )
    fig.show()
    sum_times = sum(map(lambda x: x[0], times))
    print(f"Total   time: {{:.5f}} seconds".format(sum_times))
    print(f"Average time: {{:.5f}} seconds".format(sum_times / len(times)))
