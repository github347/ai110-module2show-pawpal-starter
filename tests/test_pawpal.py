from datetime import datetime
from pawpal_system import Task, Pet



def test_task_completion():
    t = Task(title="Test Task", scheduled_at=datetime.now())
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_task_addition_to_pet():
    pet = Pet(name="TestPet")
    initial = len(pet.tasks)
    # create a task and add by id
    t = Task(title="Feed", scheduled_at=datetime.now())
    pet.add_task(t.id)
    assert len(pet.tasks) == initial + 1
    assert t.id in pet.tasks
