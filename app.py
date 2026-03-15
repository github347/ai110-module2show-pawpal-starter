import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Owner creation UI
col_owner1, col_owner2 = st.columns([2, 1])

# ensure a serializable owner slot
if "owner" not in st.session_state:
    st.session_state.owner = None
if "owner_obj" not in st.session_state:
    st.session_state.owner_obj = None

with col_owner1:
    if st.button("Create owner"):
        # store a simple serializable fallback (keeps across refreshes)
        st.session_state.owner = {"name": owner_name}
        # try to also create the Owner instance if available
        try:
            st.session_state.owner_obj = Owner(name=owner_name)
        except Exception:
            st.session_state.owner_obj = None

with col_owner2:
    st.write("Current owner:")
    if st.session_state.owner:
        st.write(st.session_state.owner.get("name", "Unknown"))
    else:
        st.info("No owner yet. Create one above.")

# Add-pet UI + session handling
if "pets" not in st.session_state:
    st.session_state.pets = []

col_pet1, col_pet2 = st.columns([2, 1])
with col_pet1:
    if st.button("Add pet"):
        # Try to instantiate a Pet object, fall back to dict if signature differs
        try:
            pet_obj = Pet(name=pet_name, species=species)
        except TypeError:
            try:
                pet_obj = Pet(pet_name, species)
            except Exception:
                pet_obj = {"name": pet_name, "species": species}

        # Link pet to owner if an owner exists in session_state
        owner = st.session_state.get("owner")
        if owner:
            # preferred: call owner's add_pet if available
            if hasattr(owner, "add_pet"):
                try:
                    owner.add_pet(pet_obj)
                except Exception:
                    pass
            else:
                # fallback: attach owner reference to pet
                try:
                    if isinstance(pet_obj, dict):
                        pet_obj["owner"] = owner.get("name") if isinstance(owner, dict) else getattr(owner, "name", None)
                    else:
                        setattr(pet_obj, "owner", owner)
                except Exception:
                    pass

        st.session_state.pets.append(pet_obj)

with col_pet2:
    st.write("Current pets:")
    if st.session_state.pets:
        pets_display = []
        for p in st.session_state.pets:
            if isinstance(p, dict):
                pets_display.append({"name": p.get("name"), "species": p.get("species"), "owner": p.get("owner")})
            else:
                name = getattr(p, "name", None) or getattr(p, "title", None)
                species_attr = getattr(p, "species", None)
                # try to get linked owner name
                owner_attr = None
                owner_obj = getattr(p, "owner", None)
                if owner_obj:
                    owner_attr = owner_obj if isinstance(owner_obj, str) else getattr(owner_obj, "name", None)
                pets_display.append({"name": name, "species": species_attr, "owner": owner_attr})
        st.table(pets_display)
    else:
        st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
