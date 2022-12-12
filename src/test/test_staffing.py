import pytest

from src.employee import Employee, EmployeeType
from src.staffing import BasicReq, FlexReq, get_staffing_for_requirements

@pytest.fixture
def resources():
    return {
        EmployeeType.CI: [
            Employee('Sara', EmployeeType.CI)
        ],
        EmployeeType.PC: [
            Employee('Bruno', EmployeeType.PC),
            Employee('Brittney', EmployeeType.PC)
        ],
        EmployeeType.LB: [
            Employee('Gavi', EmployeeType.LB),
            Employee('Harry', EmployeeType.LB),
            Employee('Alex', EmployeeType.LB)
        ],
    }

class TestBasicReq:
    def test_get_staffing_success(self, resources):
        req = BasicReq(2, EmployeeType.PC)
        assert req.get_staffing(resources) == {
            EmployeeType.PC: 2
        }

    def test_get_staffing_fail(self, resources):
        req = BasicReq(5, EmployeeType.CI)
        assert req.get_staffing(resources) == None


class TestFlexReq:
    def test_get_staffing_success(self, resources):
        req = FlexReq(4, [EmployeeType.LB, EmployeeType.PC])
        assert req.get_staffing(resources) == {
            EmployeeType.LB: 3,
            EmployeeType.PC: 1
        }

    def test_get_staffing_fail(self, resources):
        req = FlexReq(
            10,
            [EmployeeType.LB, EmployeeType.PC, EmployeeType.CI]
        )
        assert req.get_staffing(resources) == None


class TestStaffing:
    def test_get_staffing_for_reqs(self, resources):
        reqs = [
            BasicReq(1, EmployeeType.CI),
            BasicReq(1, EmployeeType.PC),
            FlexReq(4, [EmployeeType.LB, EmployeeType.PC, EmployeeType.CI])
        ]
        assert get_staffing_for_requirements(resources, reqs) == {
            EmployeeType.CI: 1,
            EmployeeType.PC: 2,
            EmployeeType.LB: 3
        }
