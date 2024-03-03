import streamlit as st
from tabulate import tabulate
from Algorithm import Graph

def parse_input_matrix(input_str):
    input_list = input_str.strip().split()
    if len(input_list) != 9:
        st.error("Please enter exactly 9 elements separated by spaces!")
        return None
    matrix = [input_list[i:i+3] for i in range(0, len(input_list), 3)]
    return matrix

def display_matrix(matrix):
    table = tabulate(matrix, tablefmt="fancy_grid")
    st.code(table, language='')

def main():
    st.set_page_config(page_title="8-Puzzle Solver")
    st.title("8-Puzzle Solver Using A* Algorithm")
    
    st.subheader("Enter the initial matrix sequence separated by spaces (e.g., 7 2 4 5 X 6 8 3 1):")
    input_str = st.text_input("Initial Matrix")
    
    if st.button("Display Initial Matrix"):
        initial_matrix = parse_input_matrix(input_str)
        if initial_matrix:
            st.write("**Initial Matrix:**")
            display_matrix(initial_matrix)
            
    st.subheader("Enter the target matrix sequence separated by spaces (e.g., X 1 2 3 4 5 6 7 8):")
    target_str = st.text_input("Target Matrix")
    
    if st.button("Display Target Matrix"):
        target_matrix = parse_input_matrix(target_str)
        if target_matrix:
            st.write("**Target Matrix:**")
            display_matrix(target_matrix)

    if st.button("Solve", key="solve_button"):
        initial_matrix = parse_input_matrix(input_str)
        target_matrix = parse_input_matrix(target_str)
        graph = Graph(initial_matrix, target_matrix)
        solution = graph.A_Star()
        
        if solution is not None:
            st.subheader("Solution Steps:")
            for i in range(len(solution)):
                step = solution[i]
                if i > 0:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"**Step {i}:**", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                display_matrix(step)
        else:
            st.warning("No solution found")

if __name__ == "__main__":
    main()
