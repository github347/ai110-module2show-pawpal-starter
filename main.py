from datetime import datetime, date, time
from pawpal_system import Owner, Pet, Scheduler


def main():
    owner = Owner(name="Alex")

    pet1 = Pet(name="Bella", birthday=date(2020, 5, 4), sex="F")
    pet2 = Pet(name="Max", birthday=date(2019, 8, 12), sex="M")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    sched = Scheduler()

    # create three tasks at different times
    t1 = sched.create_task(
        title="Morning Walk",
        scheduled_at=datetime.combine(date.today(), time(hour=9, minute=0)),
        owner_id=owner.id,
        pet_ids=[pet1.id],
    )

    t2 = sched.create_task(
        title="Midday Meds",
        scheduled_at=datetime.combine(date.today(), time(hour=11, minute=30)),
        owner_id=owner.id,
        pet_ids=[pet2.id],
    )

    t3 = sched.create_task(
        title="Evening Play",
        scheduled_at=datetime.combine(date.today(), time(hour=18, minute=0)),
        owner_id=owner.id,
        pet_ids=[pet1.id, pet2.id],
    )

    # sync tasks into pets (so Pet.tasks lists include the task ids)
    sched.assign_task_to_pets(t1.id, [pet1.id], pet_store=owner.pets)
    sched.assign_task_to_pets(t2.id, [pet2.id], pet_store=owner.pets)
    sched.assign_task_to_pets(t3.id, [pet1.id, pet2.id], pet_store=owner.pets)

    # Print today's schedule
    print("Today's Schedule:")
    todays = sched.view_tasks_on(date.today())
    todays.sort(key=lambda t: t.scheduled_at)
    for t in todays:
        time_str = t.scheduled_at.strftime("%H:%M")
        pet_names = [owner.pets[pid].name for pid in t.pet_ids if pid in owner.pets]
        print(f"- {time_str} | {t.title} | Pets: {', '.join(pet_names)}")


if __name__ == "__main__":
    main()
