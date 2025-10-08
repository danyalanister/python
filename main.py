import time
import random
import sys

# Увеличиваем глубину рекурсии для больших массивов
sys.setrecursionlimit(1000000)


class SortingAnalyzer:
    def __init__(self):
        self.swap_count = 0
        self.comparison_count = 0

    def reset_counters(self):
        self.swap_count = 0
        self.comparison_count = 0

    # 1. Пузырьковая сортировка
    def bubble_sort(self, arr):
        self.reset_counters()
        n = len(arr)
        arr = arr.copy()

        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparison_count += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swap_count += 1
        return arr

    # 2. Сортировка выбором
    def selection_sort(self, arr):
        self.reset_counters()
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.comparison_count += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.swap_count += 1
        return arr

    # 3. Сортировка вставками
    def insertion_sort(self, arr):
        self.reset_counters()
        arr = arr.copy()

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            while j >= 0:
                self.comparison_count += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    self.swap_count += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
        return arr

    # 4. Быстрая сортировка
    def quick_sort(self, arr):
        self.reset_counters()
        arr = arr.copy()
        return self._quick_sort_helper(arr, 0, len(arr) - 1)

    def _quick_sort_helper(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort_helper(arr, low, pi - 1)
            self._quick_sort_helper(arr, pi + 1, high)
        return arr

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self.comparison_count += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swap_count += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swap_count += 1
        return i + 1

    # 5. Сортировка слиянием
    def merge_sort(self, arr):
        self.reset_counters()
        arr = arr.copy()
        return self._merge_sort_helper(arr)

    def _merge_sort_helper(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._merge_sort_helper(arr[:mid])
        right = self._merge_sort_helper(arr[mid:])

        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            self.comparison_count += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            self.swap_count += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # 6. Шейкерная сортировка
    def shaker_sort(self, arr):
        self.reset_counters()
        arr = arr.copy()
        n = len(arr)
        swapped = True
        start = 0
        end = n - 1

        while swapped:
            swapped = False

            # Проход слева направо
            for i in range(start, end):
                self.comparison_count += 1
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    self.swap_count += 1
                    swapped = True

            if not swapped:
                break

            end -= 1
            swapped = False

            # Проход справа налево
            for i in range(end - 1, start - 1, -1):
                self.comparison_count += 1
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    self.swap_count += 1
                    swapped = True

            start += 1

        return arr


def generate_array(size):
    """Генерация массива случайных чисел"""
    return [random.randint(1, 100000) for _ in range(size)]


def run_experiment():
    """Проведение эксперимента"""
    analyzer = SortingAnalyzer()
    sizes = [1000, 10000, 100000]
    algorithms = {
        'Bubble sort': analyzer.bubble_sort,
        'Selection sort': analyzer.selection_sort,
        'Insertion sort': analyzer.insertion_sort,
        'Quick sort': analyzer.quick_sort,
        'Merge sort': analyzer.merge_sort,
        'Shaker sort': analyzer.shaker_sort
    }

    results = {algo: {} for algo in algorithms.keys()}

    print("Начало эксперимента...")
    print("=" * 80)

    for size in sizes:
        print(f"\nРазмер массива: {size:,} элементов")
        print("-" * 50)

        # Генерируем один массив для всех алгоритмов
        test_array = generate_array(size)

        for algo_name, algo_func in algorithms.items():
            best_time = float('inf')
            best_swaps = 0

            # 5 запусков для каждого алгоритма
            for run in range(5):
                arr_copy = test_array.copy()

                start_time = time.time()
                sorted_arr = algo_func(arr_copy)
                end_time = time.time()

                execution_time = (end_time - start_time) * 1000  # в миллисекундах

                # Проверяем корректность сортировки
                assert sorted_arr == sorted(test_array), f"Ошибка сортировки в {algo_name}"

                if execution_time < best_time:
                    best_time = execution_time
                    best_swaps = analyzer.swap_count

            results[algo_name][size] = {
                'time': round(best_time, 2),
                'swaps': best_swaps
            }

            print(f"{algo_name:<15} | Лучшее время: {best_time:>8.2f} мс | Перестановок: {best_swaps:>8,}")

    return results


def print_results_table(results):
    """Вывод результатов в виде таблицы"""
    sizes = [1000, 10000, 100000]

    print("\n" + "=" * 100)
    print("ТАБЛИЦА 1. РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА")
    print("=" * 100)
    print(f"{'Вид сортировки':<20} | {'1000':<25} | {'10000':<25} | {'100000':<25}")
    print(
        f"{'':<20} | {'Время':<10} {'Перестановки':<12} | {'Время':<10} {'Перестановки':<12} | {'Время':<10} {'Перестановки':<12}")
    print("-" * 100)

    for algo in results:
        row = f"{algo:<20} | "
        for size in sizes:
            time_val = results[algo][size]['time']
            swaps_val = results[algo][size]['swaps']
            row += f"{time_val:>8.2f} мс {swaps_val:>12,} | "
        print(row)


def analyze_complexity():
    """Анализ теоретической сложности алгоритмов"""
    print("\n" + "=" * 80)
    print("ТАБЛИЦА 2. СРАВНЕНИЕ ВРЕМЕННОЙ СЛОЖНОСТИ АЛГОРИТМОВ")
    print("=" * 80)
    print(f"{'Алгоритм':<20} | {'Лучший':<12} | {'Средний':<12} | {'Худший':<12} | {'Память':<10}")
    print("-" * 80)

    complexities = [
        ('Bubble sort', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)'),
        ('Selection sort', 'O(n²)', 'O(n²)', 'O(n²)', 'O(1)'),
        ('Insertion sort', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)'),
        ('Quick sort', 'O(n log n)', 'O(n log n)', 'O(n²)', 'O(log n)'),
        ('Merge sort', 'O(n log n)', 'O(n log n)', 'O(n log n)', 'O(n)'),
        ('Shaker sort', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)')
    ]

    for algo, best, avg, worst, memory in complexities:
        print(f"{algo:<20} | {best:<12} | {avg:<12} | {worst:<12} | {memory:<10}")


def main():
    """Основная функция"""
    print("ПРАКТИЧЕСКАЯ РАБОТА №1: ОЦЕНКА СЛОЖНОСТИ АЛГОРТМОВ СОРТИРОВКИ")
    print("Выполняется эксперимент... Это может занять несколько минут.")

    # Запускаем эксперимент
    results = run_experiment()

    # Выводим таблицу результатов
    print_results_table(results)

    # Выводим таблицу сложности
    analyze_complexity()

    # Выводы
    print("\n" + "=" * 80)
    print("ВЫВОДЫ:")
    print("=" * 80)
    print("1. Для малых массивов (1000 элементов): простые алгоритмы могут работать")
    print("   достаточно быстро, но уже заметно преимущество O(n log n) алгоритмов.")
    print("2. Для средних массивов (10000 элементов): квадратичные алгоритмы")
    print("   начинают значительно отставать.")
    print("3. Для больших массивов (100000 элементов): только O(n log n) алгоритмы")
    print("   (Quick Sort, Merge Sort) остаются практичными.")
    print("4. Quick Sort обычно показывает лучшие результаты на случайных данных.")
    print("5. Merge Sort стабилен, но требует дополнительной памяти.")


if __name__ == "__main__":
    main()