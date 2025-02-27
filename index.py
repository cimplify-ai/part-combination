import streamlit as st
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus

def calculate_parts(part_lengths,number_of_tubes, tube_length, min_ord_per_par):
    prob = LpProblem("Tube Cutting Problem", LpMinimize)
    x = LpVariable.dicts("Number_of_Parts", part_lengths.keys(), min_ord_per_par, None, cat='Integer')
    prob += tube_length * number_of_tubes - lpSum(part_lengths[i] * x[i] for i in part_lengths) 
    prob += lpSum(part_lengths[i] * x[i] for i in part_lengths) <= tube_length * number_of_tubes

    # Solve the problem
    prob.solve()
    
    # Output the results
    # print(f"Status: {LpStatus[prob.status]}")
    total_wastage = tube_length * number_of_tubes - sum(part_lengths[i] * x[i].varValue for i in part_lengths)
    # print(f"Total Wastage: {tube_length * number_of_tubes - sum(part_lengths[i] * x[i].varValue for i in part_lengths)} mm")
    return part_lengths, total_wastage, x

# Streamlit UI
st.title("Tube Cutting Planner")
st.info("minimize Raw Material Wastage")

if "part_lengths" not in st.session_state:
    # part_lengths = {}
    st.session_state['part_lengths'] = {}

with st.form("part_input_form"):
    new_part_key = st.text_input("Enter Part Type:")
    new_part_value = st.number_input("Enter Part Length (mm):", value=None)
    add_part_button = st.form_submit_button("Add Part")
    tube_length = st.number_input("Enter Tube Length (mm):", value=None, )
    no_of_tubes = st.number_input("Enter the no of tubes Length", value=None)
    min_ord_per_par = st.number_input("Enter the minimum order per part", value=None)
    submit_button = st.form_submit_button("Calculate")
    
if add_part_button and new_part_key:
    st.session_state.part_lengths[new_part_key] = new_part_value

    
    
if submit_button and st.session_state.part_lengths:
    max_parts, total_waste,x = calculate_parts(st.session_state.part_lengths, no_of_tubes, tube_length, min_ord_per_par)
    st.success(f"Total Wastage: {total_waste} mm")
    for part in max_parts:
        st.write(f"Number of Part {part} to produce: {int(x[part].varValue)}")
# print(st.session_state.part_lengths)
with st.sidebar:
    st.write("### Current Part Lengths")
    st.write(st.session_state.part_lengths)