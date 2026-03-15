from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set
from datetime import datetime, date
from uuid import uuid4


@dataclass
class Task:
    id: str = field(default_factory=lambda: uuid4().hex)
    title: str = ""
    scheduled_at: datetime = field(default_factory=lambda: datetime.now())
    description: str = ""
    reminder: bool = False
    repeated: bool = False
    priority: int = 0
    completed: bool = False
    owner_id: Optional[str] = None
    pet_ids: List[str] = field(default_factory=list)  # allow assignment to multiple pets

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

@dataclass
class Pet:
    id: str = field(default_factory=lambda: uuid4().hex)
    name: str = ""
    birthday: Optional[date] = None
    sex: Optional[str] = None
    allergies: List[str] = field(default_factory=list)
    tasks: List[str] = field(default_factory=list)  # store task ids

    def edit_name(self, new_name: str) -> None:
        self.name = new_name

    def edit_sex(self, new_sex: str) -> None:
        self.sex = new_sex

    def edit_birthday(self, new_birthday: date) -> None:
        self.birthday = new_birthday

    def add_task(self, task_id: str) -> None:
        if task_id not in self.tasks:
            self.tasks.append(task_id)

    def remove_task(self, task_id: str) -> None:
        if task_id in self.tasks:
            self.tasks.remove(task_id)


class Owner:
    def __init__(self, name: str):
        self.id: str = uuid4().hex
        self.name = name
        self.pets: Dict[str, Pet] = {}

    def add_pet(self, pet: Pet) -> None:
        self.pets[pet.id] = pet

    def edit_pet(self, pet_id: str, **kwargs) -> None:
        pet = self.pets.get(pet_id)
        if not pet:
            return
        for key, value in kwargs.items():
            setattr(pet, key, value)

    def delete_pet(self, pet_id: str) -> None:
        if pet_id in self.pets:
            del self.pets[pet_id]


class Scheduler:
    """Canonical store for tasks. Indexes tasks by id, date, and pet for fast lookups.
    Pets store task ids; Scheduler maintains the authoritative Task objects."""

    def __init__(self):
        self.tasks_by_id: Dict[str, Task] = {}
        self.tasks_by_date: Dict[date, Set[str]] = {}
        self.tasks_by_pet: Dict[str, Set[str]] = {}

    def _index_task(self, task: Task) -> None:
        self.tasks_by_id[task.id] = task
        d = task.scheduled_at.date()
        self.tasks_by_date.setdefault(d, set()).add(task.id)
        for pid in task.pet_ids:
            self.tasks_by_pet.setdefault(pid, set()).add(task.id)

    def _unindex_task(self, task: Task) -> None:
        self.tasks_by_id.pop(task.id, None)
        d = task.scheduled_at.date()
        if d in self.tasks_by_date:
            self.tasks_by_date[d].discard(task.id)
            if not self.tasks_by_date[d]:
                del self.tasks_by_date[d]
        for pid in list(self.tasks_by_pet.keys()):
            self.tasks_by_pet[pid].discard(task.id)
            if not self.tasks_by_pet[pid]:
                del self.tasks_by_pet[pid]

    def create_task(self, title: str, scheduled_at: datetime, owner_id: Optional[str] = None, pet_ids: Optional[List[str]] = None, **kwargs) -> Task:
        t = Task(title=title, scheduled_at=scheduled_at, owner_id=owner_id, pet_ids=pet_ids or [], **kwargs)
        self._index_task(t)
        return t

    def add_task(self, task: Task) -> None:
        # add an existing Task object into the scheduler
        self._index_task(task)

    def edit_task(self, task_id: str, **kwargs) -> None:
        task = self.tasks_by_id.get(task_id)
        if not task:
            return
        # If scheduled_at or pet_ids change, reindex
        old_date = task.scheduled_at.date()
        old_pet_ids = set(task.pet_ids)
        for key, value in kwargs.items():
            setattr(task, key, value)
        new_date = task.scheduled_at.date()
        new_pet_ids = set(task.pet_ids)
        if old_date != new_date or old_pet_ids != new_pet_ids:
            self._unindex_task(task)
            self._index_task(task)

    def delete_task(self, task_id: str) -> None:
        task = self.tasks_by_id.get(task_id)
        if not task:
            return
        self._unindex_task(task)

    def assign_task_to_pets(self, task_id: str, pet_ids: List[str], pet_store: Dict[str, Pet] = None) -> None:
        """Assigns task to multiple pets. Optionally updates provided pet_store to include task ids in pets."""
        task = self.tasks_by_id.get(task_id)
        if not task:
            return
        # update index removal for old pet ids
        old_pet_ids = set(task.pet_ids)
        for pid in old_pet_ids - set(pet_ids):
            if pid in self.tasks_by_pet:
                self.tasks_by_pet[pid].discard(task.id)
        task.pet_ids = pet_ids
        for pid in pet_ids:
            self.tasks_by_pet.setdefault(pid, set()).add(task.id)
            if pet_store and pid in pet_store:
                pet_store[pid].add_task(task.id)

    def unassign_task_from_pet(self, task_id: str, pet_id: str, pet_store: Dict[str, Pet] = None) -> None:
        task = self.tasks_by_id.get(task_id)
        if not task:
            return
        if pet_id in task.pet_ids:
            task.pet_ids.remove(pet_id)
        if pet_id in self.tasks_by_pet:
            self.tasks_by_pet[pet_id].discard(task.id)
        if pet_store and pet_id in pet_store:
            pet_store[pet_id].remove_task(task.id)

    def view_tasks_on(self, target_date: date) -> List[Task]:
        ids = self.tasks_by_date.get(target_date, set())
        return [self.tasks_by_id[i] for i in ids]

    def view_future_tasks(self, from_date: date) -> List[Task]:
        result: List[Task] = []
        for d, ids in self.tasks_by_date.items():
            if d > from_date:
                result.extend(self.tasks_by_id[i] for i in ids)
        return result


if __name__ == "__main__":
    # Minimal usage example (updated for id/datetime-based API)
    from datetime import datetime, date, time

    owner = Owner(name="Alex")
    pet = Pet(name="Bella", birthday=date(2020, 5, 4), sex="F")
    owner.add_pet(pet)

    sched = Scheduler()
    # create a task scheduled for today at 09:00
    scheduled = datetime.combine(date.today(), time(hour=9, minute=0))
    t1 = sched.create_task(title="Walk Bella", scheduled_at=scheduled, owner_id=owner.id, pet_ids=[pet.id], priority=1)

    # ensure pet knows about the task (optionally keep pets synced via a pet_store)
    pet.add_task(t1.id)

    print("Owner:", owner.name, "id=", owner.id)
    print("Pet:", pet.name, "id=", pet.id, "tasks=", pet.tasks)
    print("Tasks today:", [t.title for t in sched.view_tasks_on(date.today())])
