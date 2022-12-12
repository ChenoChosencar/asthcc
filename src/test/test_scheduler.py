import pytest

from src.building import SingleStoryHome, TwoStoryHome, CommercialBuilding
from src.employee import Employee, EmployeeType
from src.scheduler import Scheduler

class TestDailyRosters:
    def test_build_daily_rosters(self):
        e1 = Employee('Lionel', EmployeeType.CI)
        e2 = Employee('Lautaro', EmployeeType.PC)
        e3 = Employee('Julian', EmployeeType.LB)
        e4 = Employee('Enzo', EmployeeType.LB)

        e1.availability[0] = False
        e2.availability[1] = False
        
        e3.availability[3] = False
        e3.availability[4] = False

        e4.availability[1] = False
        e4.availability[2] = False
        e4.availability[3] = False

        scheduler = Scheduler([e1, e2, e3, e4], [])

        assert scheduler.rosters == [
            {
                EmployeeType.CI: [],
                EmployeeType.PC: [e2],
                EmployeeType.LB: [e3, e4]
            },
            {
                EmployeeType.CI: [e1],
                EmployeeType.PC: [],
                EmployeeType.LB: [e3]
            },
            {
                EmployeeType.CI: [e1],
                EmployeeType.PC: [e2],
                EmployeeType.LB: [e3] 
            },
            {
                EmployeeType.CI: [e1],
                EmployeeType.PC: [e2],
                EmployeeType.LB: []
            },
            {
                EmployeeType.CI: [e1],
                EmployeeType.PC: [e2],
                EmployeeType.LB: [e4]
            }
        ]


class TestScheduler:
    def test_get_schedule(self):
        """NOTE: not currently passing because of ordering
        See notes.md"""

        e1 = Employee('Richarlison', EmployeeType.CI)
        e2 = Employee('Neymar', EmployeeType.CI)
        e3 = Employee('Vinicius', EmployeeType.PC)
        e4 = Employee('Paqueta', EmployeeType.PC)
        e5 = Employee('Casemiro', EmployeeType.LB)
        e6 = Employee('Silva', EmployeeType.LB)
        e7 = Employee('Marquinhos', EmployeeType.LB)
        e8 = Employee('Danilo', EmployeeType.LB)
        employees = [e1, e2, e3, e4, e5, e6, e7, e8]

        b1 = SingleStoryHome('Training Ground')
        b2 = TwoStoryHome('Neo Química Arena')
        b3 = CommercialBuilding('Maracana Stadium')
        buildings = [b1, b2, b3]

        scheduler = Scheduler(employees, buildings)

        result = scheduler.get_schedule()
        expected = [
            [
                (b1, [e1]), (b2, [e2, e5])
            ],
            [
                (b3, [e1, e2, e3, e4, e5, e6, e7, e8])
            ],
            [],
            [],
            [],
        ]
        print(result)
        print(expected)

        assert result == expected
