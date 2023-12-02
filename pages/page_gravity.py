import streamlit as st
import numpy as np

from gravity.functions import animate_points


st.set_page_config(layout="wide", page_title="Gravity")


custom_css = """
<style> 
    .stNumberInput [data-testid=stNumberInputContainer]{
        width: 90%;
        margin-bottom: 2rem;
    } 
    
    .stSelectbox {
        width: 90%;
        margin-bottom: 3rem;
    } 
    
   div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
        }
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


form, _, chart = st.columns([7, 1, 6])

with form:
    form_container = form.container(border=False)

    # Form
    n_of_points_widget, _, _ = form_container.columns([3, 1, 1])
    with n_of_points_widget:
        n_of_points = n_of_points_widget.number_input("How many data points do you want?", 2, 4, 3)

    input_method_widget, _, _ = form_container.columns([3, 1, 1])
    with input_method_widget:
        input_method = input_method_widget.selectbox(
            "How would you like to set input data?",
            ("", "Automatically", "Specific positions", "Random"))

    # ---
    angles = np.linspace(0, 2 * np.pi, n_of_points, endpoint=False)
    default_x_values = np.cos(angles) * 0.8
    default_y_values = np.sin(angles) * 0.8
    default_mass_values = np.ones(n_of_points) * 5

    if input_method == "Automatically":
        x_input_values = default_x_values + np.random.normal(0, 0.02, n_of_points)
        y_input_values = default_y_values + np.random.normal(0, 0.02, n_of_points)
        mass_input_values = default_mass_values + np.random.normal(0, 1, n_of_points)

        st.markdown(f"""Automatic X positions are:
        
                        x={np.round(x_input_values, 3)}""")

        st.markdown(f"""Automatic Y positions are:
        
                        x={np.round(y_input_values, 3)}""")

        st.markdown(f"""Automatic mass values are:

                                x={np.round(mass_input_values, 1)}""")

    if input_method == "Specific positions":
        x_input_values = default_x_values
        y_input_values = default_y_values
        mass_input_values = default_mass_values

        for i, (default_x, default_y) in enumerate(zip(default_x_values, default_y_values)):
            x_input, _, y_input, _, mass_input = st.columns([9, 1, 9, 1, 9])

            with x_input:
                value = x_input.number_input(f"Point #{i+1} - x coordinate", min_value=-0.9,
                                             max_value=0.9, value=float(default_x), step=0.01)
                x_input_values[i] = value

            with y_input:
                value = y_input.number_input(f"Point #{i+1} - y coordinate", min_value=-0.9,
                                             max_value=0.9, value=float(default_y), step=0.01)
                y_input_values[i] = value

            with mass_input:
                value = mass_input.number_input(f"Point #{i + 1} - mass", min_value=1.0,
                                                max_value=10.0, value=5.0, step=0.1)
                mass_input_values[i] = value

    if input_method == "Random":
        x_input_values = np.random.uniform(-0.9, 0.9, n_of_points)
        y_input_values = np.random.uniform(-0.9, 0.9, n_of_points)
        mass_input_values = np.random.uniform(1, 10) * n_of_points

        st.markdown(f"""Random X positions are:

                                x={np.round(x_input_values, 3)}""")

        st.markdown(f"""Random Y positions are:

                                x={np.round(y_input_values, 3)}""")

        st.markdown(f"""Random mass values are:
            
            m={np.round(mass_input_values, 3)}""")

# ---

with chart:
    chart_container = chart.container(border=False)
    start_button = chart_container.button("Start Animation")

    chart_placeholder = chart_container.empty()

    if start_button:
        animate_points(chart_placeholder, x_input_values, y_input_values, mass_input_values)
