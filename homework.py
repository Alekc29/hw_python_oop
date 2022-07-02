
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,   # пройденная дистанция в км
                 speed: float,      # средняя скорость в км/ч
                 calories: float    # потрачено ккал
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть сообщение о тренировке в виде строки"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65     # длина одного шага в метрах
    M_IN_KM = 1000      # константа для перевода метров в километры

    def __init__(self,
                 action: int,      # количество совершённых действий
                 duration: float,  # длительность тренировки в часах
                 weight: float     # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self,
                           coeff_calorie_1: int = 18,
                           coeff_calorie_2: int = 20,
                           hour_in_minut: int = 60
                           ) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((coeff_calorie_1 * self.get_mean_speed()
                - coeff_calorie_2) * self.weight
                / self.M_IN_KM * self.duration * hour_in_minut)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int    # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self,
                           coeff_calorie_1: float = 0.035,
                           coeff_calorie_2: float = 0.029,
                           hour_in_minut: int = 60
                           ) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        return ((coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_2 * self.weight) * self.duration
                * hour_in_minut)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38     # длина одного гребка в метрах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,    # длина бассейна в метрах
                 count_pool: int        # счётчик заплывов
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self,
                           coeff_calorie_1: float = 1.1,
                           coeff_calorie_2: int = 2
                           ) -> float:
        """Получить количество затраченных калорий для плавания."""
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return dict_training.get(
        workout_type,
        'Такого вида тренировки ещё нет =('
    )(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
