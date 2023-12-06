import streamlit as st
import numpy as np
import json
from random import randint

from gravity.animation import animate_points
from gravity.gravity_simulator import GravitySimulator


st.set_page_config(layout="wide", page_title="Gravity")


custom_css = """
<style> 
    div.block-container {
        padding: 3rem;
   }
    .stNumberInput [data-testid=stNumberInputContainer]{
        width: 90%;
        margin-bottom: 1rem;
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
    n_of_points_widget, _, file_uploader = form_container.columns([3, 1, 3])
    with n_of_points_widget:
        n_of_points = n_of_points_widget.number_input("How many planets do you want?", 2, 4, 2)

    input_method_widget, _, json_info = form_container.columns([3, 1, 3])
    with input_method_widget:
        input_method = input_method_widget.selectbox(
            "How would you like to set input data?", ["Custom values", "From file"])  # Predefined, from file

    angles = np.linspace(0, 2 * np.pi, n_of_points, endpoint=False)
    default_mass = 5

    default_x_values = np.cos(angles) * 0.8
    default_y_values = np.sin(angles) * 0.8
    default_mass_values = np.ones(n_of_points, dtype=int) * default_mass
    default_x_velocity = np.zeros(n_of_points)
    default_y_velocity = np.zeros(n_of_points)

    if input_method == "From file":
        with file_uploader:
            file = file_uploader.file_uploader("JSON file with data (optional)")
            if file:
                try:
                    data = json.loads(file.read().decode("utf-8"))
                    default_x_values = [item["x"] for item in data]
                    default_y_values = [item["y"] for item in data]
                    default_mass_values = [item["m"] for item in data]
                    default_x_velocity = [item["vx"] for item in data]
                    default_y_velocity = [item["vy"] for item in data]
                except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                    st.error("Invalid file")
                    data = []

        with json_info:
            json_info.info("JSON file should contain an array of objects (list of strings) with"
                           " the following keys: x, y, m, vx, vy")

    if True:
        x_input_values = default_x_values
        y_input_values = default_y_values
        mass_input_values = default_mass_values
        x_velocity_input_values = default_x_velocity
        y_velocity_input_values = default_y_velocity

        for i, (default_x, default_y, default_mass, default_x_velocity, default_y_velocity) in enumerate(
                zip(default_x_values, default_y_values, default_mass_values, default_x_velocity, default_y_velocity)):
            st.markdown(f"Point #{i+1}:")
            x_input, y_input, mass_input, x_velo_input, y_velo_input = st.columns(5)

            with x_input:
                value = x_input.number_input(f"X coordinate", key=f"x {i}", min_value=-1.0,
                                             max_value=1.0, value=float(default_x), step=0.01)
                x_input_values[i] = value

            with y_input:
                value = y_input.number_input(f"Y coordinate", key=f"y {i}", min_value=-1.0,
                                             max_value=1.0, value=float(default_y), step=0.01)
                y_input_values[i] = value

            with mass_input:
                value = mass_input.number_input(f"Mass", key=f"m {i}", min_value=1,
                                                max_value=1000, value=default_mass, step=1)
                mass_input_values[i] = value

            with x_velo_input:
                value = x_velo_input.number_input("X velocity", key=f"vx {i}", min_value=-2.0,
                                                  max_value=2.0, value=float(default_x_velocity),
                                                  step=0.01)
                x_velocity_input_values[i] = value

            with y_velo_input:
                value = y_velo_input.number_input("Y velocity", key=f"vy {i}", min_value=-1115.0,
                                                  max_value=1115.0, value=float(default_y_velocity),
                                                  step=0.01)
                y_velocity_input_values[i] = value

    with chart:
        chart_container = chart.container(border=False)

        show_multiselect, toggle_logs, toggle_disappear = chart_container.columns([7, 3, 3])

        with show_multiselect:
            selected_options = show_multiselect.multiselect(
                "Show:", ["Planets", "Gravity", "Trace"], ["Planets"])

            show_points = "Planets" in selected_options
            show_field = "Gravity" in selected_options
            show_trace = "Trace" in selected_options

        with toggle_logs:
            logs = toggle_logs.toggle("Save logs", False)

        with toggle_disappear:
            on_collision = toggle_disappear.selectbox("On collision",
                                                      ["Annihilate", "Freeze", "Bounce"])

        time_speed = chart_container.slider("Time speed", 10, 100, 50)

        start_button, _, save_button, _, stop_button = chart_container.columns([2, 1, 5, 1, 2])

        with start_button:
            start = start_button.button("Start Animation")

        with save_button:
            save = save_button.button("Stop and save initial conditions")

        with stop_button:
            stop = stop_button.button("Stop Animation")

        chart_placeholder = chart_container.empty()

        if start:
            st.session_state.simulator = GravitySimulator(show_points, show_field, show_trace, logs,
                                                          on_collision,
                                                          time_speed, x_input_values,
                                                          y_input_values,
                                                          mass_input_values,
                                                          x_velocity_input_values,
                                                          y_velocity_input_values)
            animate_points(chart_placeholder, st.session_state.simulator)
            if st.session_state.simulator.save_logs:
                st.session_state.simulator.dump_logs_to_file()

        if stop:
            if st.session_state.simulator.save_logs:
                st.session_state.simulator.dump_logs_to_file()

        if save:
            simulator = st.session_state.simulator

            initial_x = simulator.x_history[0].tolist()
            initial_y = simulator.y_history[0].tolist()
            initial_m = simulator.m.tolist()
            initial_vx = simulator.vx_history[0].tolist()
            initial_vy = simulator.vy_history[0].tolist()
            on_collision = simulator.on_collision

            initial_conditions = [
                {"x": x, "y": y, "m": m, "vx": vx, "vy": vy}
                for x, y, m, vx, vy in zip(initial_x, initial_y, initial_m, initial_vx, initial_vy)
            ]
            filename = f"gravity/initial_conditions/init-cond-{randint(1, 999)}-{on_collision}.json"
            with open(filename, "w") as f:
                json.dump(initial_conditions, f)

            if simulator.save_logs:
                simulator.dump_logs_to_file()
