from itertools import chain
from typing import List, Tuple

from src.building import Building
from src.constants import DAYS
from src.employee import Employee, EmployeeType
from src.staffing import get_staffing_for_requirements

class Scheduler:
    def __init__(self, employees: List[Employee], buildings: List[Building]):
        self.buildings = buildings
        self.rosters = self._build_daily_rosters(employees)


    def _build_daily_rosters(self, employees: List[Employee]):
        """Builds the available roster for each day"""
        rosters = [
            {
                EmployeeType.CI: [],
                EmployeeType.PC: [],
                EmployeeType.LB: []
            }
            for _d in range(DAYS)
        ]
        for e in employees:
            for d in range(DAYS):
                if e.availability[d]:
                    rosters[d][e.type].append(e)
        return rosters


    def get_schedule(self) -> List[List[Tuple[Building, List[Employee]]]]:
        """Builds a daily schedule of building->employees assignments
        
        Basic greedy implementation, attempting to staff one building at a time.
        When it can't staff a building, it keeps trying to staff other buildings until either:
            1) the roster empties
            2) there are no more buildings to try staffing
        Does not look at flex reqs across multiple buildings
        or any other fancy optimization for that matter. 
        """
        schedule = []

        for d in range(DAYS):
            schedule.append([])
            roster = self.rosters[d]

            for building in self.buildings:
                if not chain.from_iterable([emps for emps in roster.values()]):
                    # Bit complicated but checks if anyone is left on the roster
                    break
                if building.finished:
                    continue
                
                staffing = get_staffing_for_requirements(
                    roster, building.get_requirements()
                )
                if not staffing:
                    # Could not staff this building
                    # Continue to attempt other buildings
                    continue
                
                # Add (building, staffed_employees) tuple to the schedule
                staffed_employees = []
                for e_type, employees in roster.items():
                    for i in range(staffing[e_type]):
                        staffed_employees.append(employees.pop())
                schedule[d].append((building, staffed_employees))

                # Mark this building as finished
                building.mark_finished()

        
        return schedule
