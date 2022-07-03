from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float    # пройденная дистанция в км
    speed: float       # средняя скорость в км/ч
    calories: float    # потрачено ккал

    def get_message(self) -> str:
        """Вернуть сообщение о тренировке в виде строки"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65     # длина одного шага в метрах
    M_IN_KM: int = 1000
    hour_in_minut: int = 60

    def __init__(self,
                 action: int,      # количество совершённых действий
                 duration_h: float,  # длительность тренировки в часах
                 weight: float     # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration_h = duration_h
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.'
            % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_run_1: int = 18
    coeff_calorie_run_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.coeff_calorie_run_1 * self.get_mean_speed()
                - self.coeff_calorie_run_2) * self.weight
                / self.M_IN_KM * self.duration_h * self.hour_in_minut)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_wlk_1: float = 0.035
    coeff_calorie_wlk_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration_h: float,
                 weight: float,
                 height: int    # рост спортсмена
                 ) -> None:
        super().__init__(action, duration_h, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        return ((self.coeff_calorie_wlk_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.coeff_calorie_wlk_2 * self.weight) * self.duration_h
                * self.hour_in_minut)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38           # длина одного гребка в метрах
    coeff_calorie_swm_1: float = 1.1
    coeff_calorie_swm_2: int = 2

    def __init__(self,
                 action: int,
                 duration_h: float,
                 weight: float,
                 length_pool: float,    # длина бассейна в метрах
                 count_pool: int        # счётчик заплывов
                 ) -> None:
        super().__init__(action, duration_h, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        return ((self.get_mean_speed() + self.coeff_calorie_swm_1)
                * self.coeff_calorie_swm_2 * self.weight)


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return training.get(
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
