
from collections import deque
from dataclasses import dataclass
import sys


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def read_processes(filename):
    processes = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Пропускаем пустые строки и комментарии
            if not line or line.startswith("#"):
                continue

            pid, arrival, burst, priority = line.split()

            processes.append(
                Process(
                    pid=pid,
                    arrival=int(arrival),
                    burst=int(burst),
                    priority=int(priority),
                )
            )

    return processes


def fcfs(processes):
    """First Come, First Served — порядок прибытия."""
    time = 0
    intervals = []

    for p in sorted(processes, key=lambda p: p.arrival):
        start = max(time, p.arrival)
        end = start + p.burst

        intervals.append((p.pid, start, end))
        time = end

    return intervals


def sjf(processes):
    """Shortest Job First — невытесняющий алгоритм."""
    time = 0
    remaining = list(enumerate(processes))
    intervals = []

    while remaining:
        available = [
            (index, p)
            for index, p in remaining
            if p.arrival <= time
        ]

        # Если нет доступных процессов, переходим ко времени
        # прибытия ближайшего процесса.
        if not available:
            time = min(p.arrival for _, p in remaining)
            available = [
                (index, p)
                for index, p in remaining
                if p.arrival <= time
            ]

        index, p = min(
            available,
            key=lambda item: (item[1].burst, item[0])
        )

        start = time
        end = start + p.burst

        intervals.append((p.pid, start, end))
        time = end

        remaining = [
            item for item in remaining
            if item[0] != index
        ]

    return intervals


def rr(processes, quantum):
    """Round Robin — планирование с квантованием времени."""
    if quantum <= 0:
        raise ValueError("Квант времени должен быть больше нуля")

    ordered = sorted(
        enumerate(processes),
        key=lambda item: item[1].arrival
    )

    remaining = {
        index: p.burst
        for index, p in ordered
    }

    queue = deque()
    intervals = []
    time = 0
    next_index = 0

    while next_index < len(ordered) or queue:

        # Если очередь пуста, ждём ближайший процесс.
        if not queue and next_index < len(ordered):
            time = max(time, ordered[next_index][1].arrival)

        # Добавляем все процессы, прибывшие к текущему времени.
        while (
            next_index < len(ordered)
            and ordered[next_index][1].arrival <= time
        ):
            queue.append(ordered[next_index][0])
            next_index += 1

        if not queue:
            continue

        index = queue.popleft()
        p = processes[index]

        start = time
        duration = min(quantum, remaining[index])
        time += duration
        remaining[index] -= duration

        intervals.append((p.pid, start, time))

        # Сначала добавляем новые прибывшие процессы.
        while (
            next_index < len(ordered)
            and ordered[next_index][1].arrival <= time
        ):
            queue.append(ordered[next_index][0])
            next_index += 1

        # Незавершённый процесс возвращается в конец очереди.
        if remaining[index] > 0:
            queue.append(index)

    return intervals


def calculate_metrics(processes, intervals):
    """Среднее время ожидания и turnaround."""
    completion = {}

    for pid, start, end in intervals:
        completion[pid] = end

    waiting_times = []
    turnaround_times = []

    for p in processes:
        turnaround = completion[p.pid] - p.arrival
        waiting = turnaround - p.burst

        turnaround_times.append(turnaround)
        waiting_times.append(waiting)

    average_waiting = sum(waiting_times) / len(processes)
    average_turnaround = sum(turnaround_times) / len(processes)

    return average_waiting, average_turnaround


def show_gantt(intervals):
    print("Диаграмма Ганта:")

    if not intervals:
        print("(нет процессов)")
        return

    print(" -> ".join(
        f"{pid}[{start}-{end}]"
        for pid, start, end in intervals
    ))


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 scheduler.py set1.txt [quantum]")
        sys.exit(1)

    filename = sys.argv[1]
    quantum = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    try:
        processes = read_processes(filename)

        if not processes:
            print("Ошибка: файл не содержит процессов.")
            sys.exit(1)

        algorithms = [
            ("FCFS", fcfs),
            ("SJF", sjf),
            ("RR", lambda ps: rr(ps, quantum)),
        ]

        print(f"Файл: {filename}")
        print(f"Квант RR: {quantum}")

        for name, algorithm in algorithms:
            intervals = algorithm(processes)
            avg_waiting, avg_turnaround = calculate_metrics(
                processes, intervals
            )

            print(f"\n=== {name} ===")
            show_gantt(intervals)
            print(f"Среднее время ожидания: {avg_waiting:.2f}")
            print(f"Среднее время turnaround: {avg_turnaround:.2f}")

    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        sys.exit(1)
    except ValueError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()

