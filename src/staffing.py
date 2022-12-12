from abc import ABC, abstractmethod
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List

from src.employee import Employee, EmployeeType

# A mapping of employee type to a list of available employees
Resources = Dict[EmployeeType, List[Employee]]

# A mapping of employee type to # needed
Staffing = Dict[EmployeeType, int]


def add_staffings(s1: Staffing, s2: Staffing) -> None:
    """Adds s2 staffing to s1"""
    for e_type, num in s2.items():
        s1[e_type] += num


class Requirement(ABC): 
    @abstractmethod
    def get_staffing(self, resources: Resources) -> Staffing:
        """Generates a valid staffing that satisfies the requirement,
        with the given resources. Modifies the resources parameter.
        """
        pass


class BasicReq(Requirement):
    """A basic single-type requirement, i.e. 'requires 1 laborer'"""
    def __init__(self, number: int, type: EmployeeType):
        self.number = number
        self.type = type

    def get_staffing(self, resources: Resources) -> Staffing:
        if len(resources[self.type]) < self.number:
            return None

        staffing = defaultdict(int)
        staffing[self.type] += self.number
        for i in range(self.number):
            resources[self.type].pop()

        return staffing


class FlexReq(Requirement):
    """An OR requirement which can be satisfied by any of a set of types.
    i.e. 'requires a laborer OR an installer pending certification'

    The order of types provided determines preference of selection.
    """
    def __init__(self, number: int, types: List[EmployeeType]):
        self.number = number
        self.types = types

    def get_staffing(self, resources: Resources) -> Staffing:
        staffing = defaultdict(int)

        remaining = self.number
        for e_type in self.types:
            while len(resources[e_type]) > 0 and remaining > 0:
                staffing[e_type] += 1

                resources[e_type].pop()
                remaining -= 1
        
        if remaining > 0:
            # means we've gone through all the possible types and haven't
            # fulfilled the requirement
            return None

        return staffing


def get_staffing_for_requirements(
    resources: Resources,
    requirements: List[Requirement]
) -> Staffing:
    """Basic greedy algorithm to iterate over a requirement set
    and determine if provided resources can satisfy the requirements.

    Suboptimal when:
        - TODO

    Returns:
        - a valid Staffing if one is found
    """
    _resources = deepcopy(resources)
    staffing = defaultdict(int)
    for req in requirements:
        # Note: will modify _resources
        reqStaffing = req.get_staffing(_resources)
        if not reqStaffing:
            # means we don't have sufficient resources
            # to staff this building
            return None
        # Add the staffing for this req to the total staffings
        add_staffings(staffing, reqStaffing)
    return staffing
