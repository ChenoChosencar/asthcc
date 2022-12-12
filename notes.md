# Requirements

Buildings are given in order of importance
* more important -> earlier start date or finish date?
    * all installs are done in 1 day so it doesn't matter

Employee role types
* CI = Certified installers
* PC = Installers pending certification
* LB = Laborers

^ class inheritance OOP model (not really needed)

Building types
* Single story homes = SSH
* Two story homes = TSH
* Commercial buildings = COM

SSH:
    1CI
TSH:
    1CI && 1(PC || LB)
COM:
    2CI && 2PC && 4(CI || PC || LB)

Inputs:
    employees: Employee[]
    buildings: Building[]


# Implementation

## Classes

EmployeeTypes = [CI, PC, LB]
EmployeeType = enum(EmployeeTypes)

Employee
    type = EmployeeType
    availability = [True/False for _d in range(DAYS)]

### Building

Building
    requirements = Requirement[]
    finished = False

    # returns None if cannot be staffed given resources
    def get_staffing(resources):
        _resources = copy.deepcopy(resources)  # to play with
        staffing = {}
        for req in requirements:
            reqStaffing = req.get_staffing(_resources)
            if not reqStaffing:
                return None
            addStaffings(staffing, reqStaffing)
        return staffing

### Requirements
BasicRequirement -- one possible employee type
FlexRequirement -- multiple possible employee type

Requirement
    number = int

    @abstractmethod
    get_staffing(resources) -> {}

BasicRequirement(Requirement)
    type = EmployeeType

    get_staffing(resources):
        if len(resources[type]) < number:
            return None
        resources[type] -= 1
        staffing = {[type]: 1 }
        return staffing

FlexRequirement(Requirement)
    types = EmployeeType[]  # stored in ascending rank

    get_staffing(resources):
        remaining = number
        staffing = {}
        for type in types:
            while len(resources[type]) > 0 and remaining > 0:
                staffing[type] += 1
                remaining -= 1

        if remaining > 0:
            return None
        return staffing


## Scheduler

Gut feeling: this is an assignment problem, probably NP-Complete or NP-Hard. Not worth optimizing 
Brute force (greedy) solution:

class Scheduler:
    def __init__(self, employees, buildings):
        self.buildings = buildings
        self.rosters = self._build_daily_rosters(employees)

    def _build_daily_rosters(self, employees)
        """Builds the available roster for each day"""
        rosters = [{ CI: Employee[], PC: Employee[], LB: Employee[] } for _i in range(DAYS)]
        for e in employees:
            for d in range(DAYS):
                if e.availability[d]:
                    rosters[d][e.type].append(e)
        return rosters

    def schedule(self):
        for d in range(DAYS):
            roster = self.rosters[d]

            Iterate through buildings:
                if building.finished:
                    continue

                # 1) Get staffing
                try:
                    staffing = building.get_staffing(resources)
                except: # if get_staffing fails
                    break -> prioritize finishing buildings in order
                    continue -> prioritize attempting buildings in order
                        # I like this better
                    
                # 2) Staff

                # remove staffing employees from roster and add to tuple
                for type, employees in roster.items():
                    for i in range(staffing[type]):
                        e = employees.pop()
            
            ### End of day

### Utilities

* addStaffings(s1, s2):
    """Adds s2 staffing to s1"""
    for k, v in s2.items():
        if k in s1:
            s1[k] += s2[k]
        else:
            s1[k] = s2[k]

## Sketchpad: things to implement
* Error handling when staffing doesn't work
* Edge cases
    * buildings with more than one flex requirement
        * greedy will be suboptimal in these scenarios
    * when you literally can't finish the buildings in a week

# Improvements to be made (running list)
* Fix scheduler tests for ordering -- see note about employee queue
* Support for different types of certifications
* Employee queue to avoid burnout
    * guarantee ordering
* Add names for employees, hard to tell who is who
* Better interface for updating employee availability
* logging scheduler efficiency (% of employees staffed each day)
* Deal with a single building type cannot staff
    * throw it out and move on
* Dockerize, deploy, etc

# Choices I'm making
* prioritizing attempting buildings in order
    * ex: A->B->C
        * if B requires a lot and A and C can be fit into one day
        * Day 1: staff A, ignore B, staff C
        * Day 2: staff B
    * means that commercial buildings will get delayed in favor of single story homes   


