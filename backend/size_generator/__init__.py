from enum import Enum
from math import ceil


class GrowthPace(Enum):
    P1 = 2
    P2 = 1.9
    P3 = 1.8
    P4 = 1.7
    P5 = 1.6
    P6 = 1.5
    P7 = 1.4
    P8 = 1.3
    P9 = 1.1
    P10 = 1


class SizeGenerator:

    @staticmethod
    def generate_sizes(
        pace: GrowthPace,
        num_points: int = 8,
        start_size: int = 1
    ) -> list:

        factor = pace.value

        ascending_sizes = [start_size]

        for _ in range(num_points - 1):
            ascending_sizes.append(
                int((ascending_sizes[-1]+1) * factor)
            )

        ascending_sizes.reverse()

        return ascending_sizes