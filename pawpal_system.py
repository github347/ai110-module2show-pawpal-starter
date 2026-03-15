from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, time


@dataclass
class Task:
    title: str
    date: date
    time: Optional[time] = None
    description: str = ""
    reminder: bool = False
    repeated: bool = False
    priority: int = 0
    completed: bool = False


@dataclass
class Pet:
    name: str
    birthday: Optional[date] = None
    sex: Optional[str] = None
    allergies: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def edit_name(self, new_name: str) -> None:
        self.name = new_name

    def edit_sex(self, new_sex: str) -> None:
        self.sex = new_sex

    def edit_birthday(self, new_birthday: date) -> None:
        self.birthday = new_birthday

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, index: int) -> None:
        del self.tasks[index]


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def edit_pet(self, index: int, **kwargs) -> None:
        pet = self.pets[index]
        for key, value in kwargs.items():
            setattr(pet, key, value)

    def delete_pet(self, index: int) -> None:
        del self.pets[index]


class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def edit_task(self, index: int, **kwargs) -> None:
        task = self.tasks[index]
        for key, value in kwargs.items():
            setattr(task, key, value)

    def delete_task(self, index: int) -> None:
        del self.tasks[index]

    def view_tasks_on(self, target_date: date) -> List[Task]:
        return [t for t in self.tasks if t.date == target_date]

    def view_future_tasks(self, from_date: date) -> List[Task]:
        return [t for t in self.tasks if t.date > from_date]


if __name__ == "__main__":
    # Minimal usage example
    from datetime import date, time

    t1 = Task(title="Walk Bella", date=date.today(), time=time(hour=9, minute=0), priority=1)
    pet = Pet(name="Bella", birthday=date(2020, 5, 4), sex="F")
    pet.add_task(t1)

    owner = Owner(name="Alex")
    owner.add_pet(pet)

    sched = Scheduler()
    sched.add_task(t1)

    print(owner)
    print(pet)
    print(sched.view_tasks_on(date.today()))
