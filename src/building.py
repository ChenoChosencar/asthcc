from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List

from src.employee import EmployeeType
from src.staffing import (
    BasicReq,
    FlexReq,
    Requirement,
)

class Building(ABC):
    def __init__(self, name: str):
        self.name = name
        self.finished = False

    def __repr__(self):
        return self.name

    @abstractmethod
    def get_requirements(self) -> List[Requirement]:
        pass

    def mark_finished(self):
        self.finished = True


class SingleStoryHome(Building):
    def get_requirements(self) -> List[Requirement]:
        return [
            BasicReq(1, EmployeeType.CI)
        ]


class TwoStoryHome(Building):
    def get_requirements(self) -> List[Requirement]:
        return [
            BasicReq(1, EmployeeType.CI),
            FlexReq(1, [EmployeeType.LB, EmployeeType.PC])
        ]


class CommercialBuilding(Building):
    def get_requirements(self) -> List[Requirement]:
        return [
            BasicReq(2, EmployeeType.CI),
            BasicReq(2, EmployeeType.PC),
            FlexReq(4, [EmployeeType.LB, EmployeeType.PC, EmployeeType.LB])
        ]
