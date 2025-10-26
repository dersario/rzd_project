import re
from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy import String, TypeDecorator


class Snils(TypeDecorator):
    """Кастомный тип SQLAlchemy для российского СНИЛС"""

    impl = String(14)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> Optional[str]:
        """Обработка при сохранении в БД"""
        if value is None:
            return None

        if isinstance(value, str):
            cleaned = self.clean_snils(value)
            if not self.validate_snils(cleaned):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"Неверный СНИЛС: {value}"
                )
            return self.format_snils(cleaned)

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Неподдерживаемый тип для СНИЛС: {type(value)}",
        )

    def process_result_value(self, value: Optional[str], dialect: Any) -> Optional[str]:
        """Обработка при чтении из БД"""
        return value

    @staticmethod
    def clean_snils(snils_str: str) -> str:
        """Очистка СНИЛС от нецифровых символов"""
        return re.sub(r"\D", "", snils_str)

    @staticmethod
    def validate_snils_format(snils_str: str) -> bool:
        """Проверка формата XXX-XXX-XXX YY"""
        pattern = r"^\d{3}-\d{3}-\d{3} \d{2}$"
        return bool(re.match(pattern, snils_str))

    @staticmethod
    def has_three_identical_digits(snils_numeric: str) -> bool:
        """Проверка на три одинаковые цифры подряд в номере"""
        number_part = snils_numeric[:9]

        for i in range(len(number_part) - 2):
            if number_part[i] == number_part[i + 1] == number_part[i + 2]:
                return True
        return False

    @classmethod
    def validate_snils(cls, snils_numeric: str) -> bool:
        """Полная валидация СНИЛС"""
        if len(snils_numeric) != 11:
            return False

        # Проверка на три одинаковые цифры подряд
        if cls.has_three_identical_digits(snils_numeric):
            return False

        number_part = int(snils_numeric[:9])
        control_sum = int(snils_numeric[9:11])

        # Проверка по специальному диапазону
        if number_part <= 1001998:  # 001-001-998 в числовом виде
            return False

        # Расчет контрольной суммы
        numbers = [int(char) for char in snils_numeric[:9]]
        calculated_sum = 0

        for i, digit in enumerate(numbers):
            calculated_sum += digit * (9 - i)

        # Приведение контрольной суммы согласно алгоритму
        if calculated_sum < 100:
            result_sum = calculated_sum
        elif calculated_sum == 100 or calculated_sum == 101:
            result_sum = 0
        else:
            result_sum = calculated_sum % 101
            if result_sum == 100:
                result_sum = 0

        return result_sum == control_sum

    @staticmethod
    def format_snils(snils_numeric: str) -> str:
        """Форматирование СНИЛС в стандартный вид XXX-XXX-XXX YY"""
        if len(snils_numeric) != 11:
            return snils_numeric
        return f"{snils_numeric[:3]}-{snils_numeric[3:6]}-{snils_numeric[6:9]} {snils_numeric[9:11]}"

    @classmethod
    def create(cls, snils_str: str) -> str:
        """Создание валидного СНИЛС с проверкой"""
        cleaned = cls.clean_snils(snils_str)
        if not cls.validate_snils(cleaned):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Неверный СНИЛС: {snils_str}"
            )
        return cls.format_snils(cleaned)
