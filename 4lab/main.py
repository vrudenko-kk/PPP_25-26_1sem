"""Система классов для работы с временными интервалами в разных форматах."""

from abc import ABC, abstractmethod


class TimeInterval(ABC):
    """Абстрактный базовый класс для временных интервалов."""
    
    @abstractmethod
    def get_seconds(self):
        """Возвращает длительность интервала в секундах."""
        pass

    @abstractmethod
    def format(self):
        """Возвращает человекочитаемое представление интервала."""
        pass

    @abstractmethod
    def format_hms(self):
        """Возвращает представление в формате ЧЧ:ММ:СС."""
        pass

    def get_components(self, secs):
        """
        Вспомогательный метод для получения часов, 
        минут и секунд из общего кол-ва секунд.   
        """
        total_secs = int(secs)
        hours = total_secs // 3600
        mins = (total_secs % 3600) // 60
        secs = total_secs % 60
        return hours, mins, secs


class HmsInterval(TimeInterval):
    """Интервал в формате чч:мм:сс."""
    def __init__(self, hours, mins, secs):
        self.hours = int(hours)
        self.mins = int(mins)
        self.secs = int(secs)

    def get_seconds(self):
        return self.hours * 3600 + self.mins * 60 + self.secs

    def format(self):
        parts = []
        if self.hours > 0:
            parts.append(f"{self.hours} h")
        if self.mins > 0:
            parts.append(f"{self.mins} min")
        if self.secs > 0 or not parts:
            parts.append(f"{self.secs} s")
        return " ".join(parts)

    def format_hms(self) -> str:
        return f"{self.hours:02d}:{self.mins:02d}:{self.secs:02d}"

    @classmethod
    def from_string(cls, string):
        """Парсит строку формата "HH:MM:SS"."""
        parts = string.split(':')
        if len(parts) != 3:
            raise ValueError(f"Неверный формат HMS: {string}")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))


class MsInterval(TimeInterval):
    """Интервал в миллисекундах."""
    def __init__(self, ms):
        self.ms = ms

    def get_seconds(self):
        return round(self.ms / 1000, 2)

    def format(self):
        hours, mins, secs = self.get_components(self.get_seconds())
        parts = []
        if hours > 0:
            parts.append(f"{hours} h")
        if mins > 0:
            parts.append(f"{mins} min")
        if secs > 0 or not parts:
            parts.append(f"{secs} s")
        return " ".join(parts)

    def format_hms(self):
        hours, mins, secs = self.get_components(self.get_seconds())
        return f"{hours:02d}:{mins:02d}:{secs:02d}"

    @classmethod
    def from_string(cls, string):
        """Парсит строку с миллисекундами."""
        return cls(int(string))

class MinSecInterval(TimeInterval):
    """Интервал в формате минуты и секунды."""
    
    def __init__(self, mins, secs):
        self.mins = mins
        self.secs = secs

    def get_seconds(self):
        return self.mins * 60 + self.secs

    def format(self):
        parts = []
        if self.mins > 0:
            parts.append(f"{self.mins} min")
        if self.secs > 0 or not parts:
            parts.append(f"{self.secs} s")
        return " ".join(parts)

    def format_hms(self):
        hours = 0
        return f"{hours:02d}:{self.mins:02d}:{self.secs:02d}"

    @classmethod
    def from_string(cls, string):
        """Парсит строку формата "M S"."""
        parts = string.split()
        if len(parts) != 2:
            raise ValueError(f"Неверный формат MinSec: {string}")
        return cls(int(parts[0]), int(parts[1]))

class HoursInterval(TimeInterval):
    """Интервал в часах."""
    
    def __init__(self, hours):
        self.hours = hours

    def get_seconds(self):
        return self.hours * 3600

    def format(self):
        hours, mins, secs = self.get_components(self.get_seconds())
        parts = []
        if hours > 0:
            parts.append(f"{hours} h")
        if mins > 0:
            parts.append(f"{mins} min")
        if secs > 0 or not parts:
            parts.append(f"{secs} s")
        return " ".join(parts)

    def format_hms(self):
        hours, mins, secs = self.get_components(self.get_seconds())
        return f"{hours:02d}:{mins:02d}:{secs:02d}"

    @classmethod
    def from_string(cls, string):
        """Парсит строку с часами (вещественное число)."""
        return cls(float(string))

class IntervalCollection:
    """Коллекция временных интервалов с возможностью выполнения операций."""
    def __init__(self):
        self.intervals = []

    def add(self, interval):
        self.intervals.append(interval)

    def sum(self):
        total_seconds = sum(interval.get_seconds() for interval in self.intervals)
        return self._seconds_to_interval(total_seconds)

    def avg(self):
        total_seconds = sum(interval.get_seconds() for interval in self.intervals)
        avg_seconds = total_seconds / len(self.intervals)
        return self._seconds_to_interval(avg_seconds)

    def max(self):
        result = max(interval.get_seconds() for interval in self.intervals)
        return self._seconds_to_interval(result)

    def _seconds_to_interval(self, seconds):
        """Преобразует секунды в нормализованный интервал."""
        total_secs = int(seconds)
        hours = total_secs // 3600
        mins = (total_secs % 3600) / 60
        secs = total_secs % 60
        return HmsInterval(hours, mins, secs)

class IntervalParser:
    """Парсер для различных форматов временных интервалов."""
    
    @staticmethod
    def parse(interval):
        """
        Парсит строку с временным интервалом
        в форматах: чч:мм:сс, миллисекунды, 
        минуты и секунды, часы.
        """
        interval = interval.strip().lower()

        if interval.startswith('hms '):
            time_str = interval[4:].strip()
            return HmsInterval.from_string(time_str)

        elif interval.startswith("ms "):
            ms_str = interval[3:].strip()
            return MsInterval.from_string(ms_str)

        elif interval.startswith("minsec "):
            time_str = interval[7:].strip()
            return MinSecInterval.from_string(time_str)

        elif interval.startswith("hours "):
            hours_str = interval[6:].strip()
            return HoursInterval.from_string(hours_str)
        else:
            raise ValueError(f"Неизвестный формат: {interval}")

def format_result(interval: TimeInterval, operation: str) -> str:
    """Форматирует результат операции."""
    
    human = interval.format()
    hms = interval.format_hms()
    seconds = int(interval.get_seconds())
    result = f"{operation.capitalize()}: {human}"
    result += f" ({hms}, {seconds} s)"
    return result

def main():
    """Основная функция программы."""
    
    print("Система работы с временными интервалами")
    print("\nВведите временные интервалы (по одному на строку).")
    print("Форматы:")
    print("  hms HH:MM:SS   - часы:минуты:секунды")
    print("  ms N           - миллисекунды")
    print("  minsec MM SS   - минуты и секунды")
    print("  hours HH       - часы (вещественное число)")
    print("\nДля завершения ввода введите пустую строку.")
    collection = IntervalCollection()

    while True:
        try:
            line = input("\nВведите интервал: ").strip()
            if not line:
                break
            interval = IntervalParser.parse(line)
            collection.add(interval)
            print(f"Добавлен: {interval.format()}")

        except Exception as e:
            print(f"Ошибка: {e}")

    if not collection.intervals:
        print("\nНет интервалов для обработки.")
        return

    print("Доступные команды:")
    print("  sum  - сумма всех интервалов")
    print("  avg  - среднее значение")
    print("  max  - максимальный интервал")
    print("  exit - выход")

    while True:
        try:
            command = input("\nВведите команду: ").strip().lower()
            if command == "exit":
                break
            elif command == "sum":
                result = collection.sum()
                if result:
                    print(format_result(result, "Total"))
            elif command == "avg":
                result = collection.avg()
                if result:
                    print(format_result(result, "Average"))
            elif command == "max":
                result = collection.max()
                if result:
                    print(format_result(result, "Max"))
            else:
                print("Неизвестная команда. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\nВыход...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
