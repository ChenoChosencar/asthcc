from enum import Enum
from typing import List

DAYS = 5

class EmployeeType(Enum):
    CI = 1  # Certified Installer
    PC = 2  # Installer Pending Certification
    LB = 3  # Laborer

employee_types = list(EmployeeType)

class Employee:
    def __init__(self, name: str, type: EmployeeType, availability: List = None):
        self.name = name
        self.type = type
        
        if availability:
            self.availability = availability
        else:
            self.availability = [True for _d in range(5)]


    def __repr__(self):
        return self.name
