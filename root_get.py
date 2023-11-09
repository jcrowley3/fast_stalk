import requests
import timeit
import statistics
import numpy as np

times = []
differences = []

def get_request():
    requests.get('http://localhost:8000')

def get_root():
    try:
        while True:
            current_time = timeit.timeit(get_request, number=1)
            times.append(current_time)

            rolling_avg = statistics.mean(times)
            difference = current_time - rolling_avg
            differences.append(difference)

            print(f'Current time: {round(current_time, 5)}s, Rolling average: {round(rolling_avg, 5)}s, Difference: {round(difference, 5)}s')
    except KeyboardInterrupt:
        total_avg = statistics.mean(times)
        total_avg_diff = statistics.mean(differences)
        final_rolling_diff = differences[-1]
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times)
        percentile_95 = np.percentile(times, 95)
        print(f'\nFinal statistics:')
        print(f'Total average: {round(total_avg, 5)}s\nCurrent rolling average: {round(rolling_avg, 5)}s')
        print(f'Total average difference: {round(total_avg_diff, 5)}s\nFinal rolling difference: {round(final_rolling_diff, 5)}s')
        print(f'Min time: {round(min_time, 5)}s\nMax time: {round(max_time, 5)}s')
        print(f'Standard deviation: {round(std_dev, 5)}s')
        print(f'95th percentile time: {round(percentile_95, 5)}s')

if __name__ == "__main__":
    get_root()
