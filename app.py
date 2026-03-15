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

# ensure owner object slot
if "owner_obj" not in st.session_state:
    st.session_state.owner_obj = None

with col_owner1:
    if st.button("Create owner"):
        try:
            st.session_state.owner_obj = Owner(name=owner_name)
            st.success(f"Created owner {owner_name}")
        except TypeError:
            try:
                st.session_state.owner_obj = Owner(owner_name)
                st.success(f"Created owner {owner_name}")
            except Exception as e:
                st.error(f"Failed to create Owner: {e}")
                st.session_state.owner_obj = None

with col_owner2:
    st.write("Current owner:")
    owner_obj = st.session_state.get("owner_obj")
    if owner_obj:
        st.write(getattr(owner_obj, "name", "Unknown"))
    else:
        st.info("No owner yet. Create one above.")

# Ensure pets list exists (store objects)
if "pets" not in st.session_state:
    st.session_state.pets = []

st.markdown("### Add a pet")
with st.form("add_pet_form"):
    pet_name_input = st.text_input("Pet name", value="Mochi")
    pet_birthday = st.date_input("Birthday")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    # Owner selection inside the form (uses owner_obj or owners list if present)
    owners_for_select = []
    if "owners" in st.session_state and isinstance(st.session_state["owners"], list):
        owners_for_select = st.session_state["owners"]
    else:
        single_owner = st.session_state.get("owner_obj")
        if single_owner:
            owners_for_select = [single_owner]

    selected_owner = st.selectbox(
        "Owner",
        options=[None] + owners_for_select,
        format_func=lambda o: "No owner" if o is None else getattr(o, "name", "Unknown"),
    )

    submitted = st.form_submit_button("Add pet")

if submitted:
    try:
        pet_obj = Pet(name=pet_name_input, birthday=pet_birthday, species=pet_species)
    except TypeError:
        try:
            pet_obj = Pet(pet_name_input, pet_birthday, pet_species)
        except Exception as e:
            st.error(f"Failed to create Pet: {e}")
            pet_obj = None

    if pet_obj:
        # Use owner chosen in the form first, else fall back to session owner_obj
        owner_instance = selected_owner or st.session_state.get("owner_obj")
        if owner_instance:
            if hasattr(owner_instance, "add_pet"):
                try:
                    owner_instance.add_pet(pet_obj)
                except Exception:
                    try:
                        setattr(pet_obj, "owner", owner_instance)
                    except Exception:
                        pass
            else:
                try:
                    setattr(pet_obj, "owner", owner_instance)
                except Exception:
                    pass
        else:
            st.info("No owner to link to; pet will be created without owner.")

        st.session_state.pets.append(pet_obj)
        st.success(f"Added pet {pet_name_input}")

st.write("Current pets:")
if st.session_state.pets:
    pets_display = []
    for p in st.session_state.pets:
        name = getattr(p, "name", None) or getattr(p, "title", None)
        species_attr = getattr(p, "species", None)
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
