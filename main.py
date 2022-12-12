from src.building import SingleStoryHome, TwoStoryHome, CommercialBuilding
from src.employee import Employee, EmployeeType
from src.scheduler import Scheduler

def main():
    e1 = Employee('Joe', EmployeeType.CI)
    e2 = Employee('Seb', EmployeeType.PC)
    e3 = Employee('JJ', EmployeeType.PC)
    e4 = Employee('Jon', EmployeeType.LB)
    e5 = Employee('Kiva', EmployeeType.LB)

    b1 = SingleStoryHome("Hal's Haven")
    b2 = TwoStoryHome("Lydia's Loft")
    b3 = CommercialBuilding("IRS Office")

    scheduler = Scheduler(
        [e1, e2, e3, e4, e5],
        [b1, b2, b3]
    )

    print(scheduler.get_schedule())


if __name__ == '__main__':
    main()
