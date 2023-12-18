import streamlit as st
from streamlit_extras.grid import grid

from zombies.zombie_simulator import ZombieSimulator
from zombies.animation import animate_points


st.set_page_config(layout="wide", page_title="Humans vs. Zombies")

custom_css = """
<style>
    div.block-container {
        padding: 3rem;
   }
    .stNumberInput [data-testid=stNumberInputContainer]{
        width: 90%;
        margin-bottom: 3rem;
    } 
    .stSelectbox {
        width: 90%;
        margin-bottom: 3rem;
    } 
   div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
        }

    div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.4rem;
        }

    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
    }

    h3 {
      text-align: center;
    }

    h5 {
      text-align: center;
    }

    div[data-testid="stNumberInput"] label {
         text-align: center !important;
         display: block;
     }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

form, _, chart = st.columns([10, 2, 10])

with form:
    my_grid = grid([5, 0.5, 5], [1, 8, 1], [1], [4, 2.2, 4],
                   [2, 2, 0.5, 1, 0.5, 2, 2], [2, 2, 0.5, 1, 0.5, 2, 2],
                   [2, 2, 0.5, 1, 0.5, 2, 2], [2, 2, 0.5, 1, 0.5, 2, 2])

    # row 1 - n of characters
    n_of_humans = my_grid.number_input("Select number of humans [2 - 12]", 2, 12, None)
    my_grid.empty()
    n_of_zombies = my_grid.number_input("Select number of zombies [2 - 12]", 2, 12, None)

    if all(n is not None for n in [n_of_humans, n_of_zombies]):
        # row 2 - info)
        my_grid.empty()
        my_grid.info("""Map of the simulation is a square with shape 100x100

(x, y) coordinates, velocity and power of characters are described
by **normal distributions** $N(\mu, \sigma)$. Select parameters of all distributions.""")

        my_grid.empty()

        # row 3 empty
        my_grid.markdown("---")

        # row 4 headers
        my_grid.markdown("### Humans")
        my_grid.empty()
        my_grid.markdown("### Zombies")

        # row 5
        mean_human_x = my_grid.number_input("$\mu$", 10, 90, 50, key='mean_human_x')
        std_human_x = my_grid.number_input("$\sigma$", 0, 20, 5, key='std_human_x')

        my_grid.empty()
        my_grid.markdown("<br> <h5>X</h5>", unsafe_allow_html=True)
        my_grid.empty()

        mean_zombie_x = my_grid.number_input("$\mu$", 10, 90, 50, key='mean_zombie_x')
        std_zombie_x = my_grid.number_input("$\sigma$", 0, 20, 5, key='std_zombie_x')

        # row 6
        mean_human_y = my_grid.number_input("$\mu$", 10, 90, 50, key='mean_human_y')
        std_human_y = my_grid.number_input("$\sigma$", 0, 20, 5, key='std_human_y')

        my_grid.empty()
        my_grid.markdown("<br> <h5>Y</h5>", unsafe_allow_html=True)
        my_grid.empty()

        mean_zombie_y = my_grid.number_input("$\mu$", 10, 90, 50, key='mean_zombie_y')
        std_zombie_y = my_grid.number_input("$\sigma$", 0, 20, 5, key='std_zombie_y')

        # row 7 - velocity
        mean_human_velo = my_grid.number_input("$\mu$", 1.0, 4.0, 2.0, step=0.5, key='mean_human_velo')
        std_human_velo = my_grid.number_input("$\sigma$", 0.5, 3.0, 1.0, step=0.1, key='std_human_velo')

        my_grid.empty()
        my_grid.markdown("<br><h5>Velocity</h5>", unsafe_allow_html=True)
        my_grid.empty()

        mean_zombie_velo = my_grid.number_input("$\mu$", 1.0, 4.0, 2.0, step=0.5, key='mean_zombie_velo')
        std_zombie_velo = my_grid.number_input("$\sigma$", 0.5, 3.0, 1.0, step=0.1, key='std_zombie_velo')

        # row 8 - power
        mean_human_power = my_grid.number_input("$\mu$", 1, 5, 3, key='mean_human_power')
        std_human_power = my_grid.number_input("$\sigma$", 1, 3, 2, key='std_human_power')

        my_grid.empty()
        my_grid.markdown("<br><h5>Power</h5>", unsafe_allow_html=True)
        my_grid.empty()

        mean_zombie_power = my_grid.number_input("Mean", 1, 5, 3, key='mean_zombie_power')
        std_zombie_power = my_grid.number_input("$\sigma$", 1, 3, 2, key='std_zombie_power')

with chart:
    my_grid = grid(1, [10], [1, 4, 2, 4], [1], [1])

    my_grid.markdown("<br><br><br>", unsafe_allow_html=True)

    if all(n is not None for n in [n_of_humans, n_of_zombies]):
        speed = my_grid.slider("Simulation speed", 10, 100, 50)

        my_grid.empty()
        start = my_grid.button("Start Animation")
        my_grid.empty()
        stop = my_grid.button("Stop Animation")
        my_grid.empty()

        my_grid.markdown("---")
        chart_placeholder = my_grid.empty()

        if start:
            config = {
                "n_humans": n_of_humans,
                "n_zombies": n_of_zombies,

                "human_x": [mean_human_x, std_human_x],
                "zombie_x": [mean_zombie_x, std_zombie_x],

                "human_y": [mean_human_y, std_human_y],
                "zombie_y": [mean_zombie_y, std_zombie_y],

                "human_v": [mean_human_velo, std_human_velo],
                "zombie_v": [mean_zombie_velo, std_zombie_velo],

                "human_power": [mean_human_power, std_human_power],
                "zombie_power": [mean_zombie_power, std_zombie_power],

                "simulation_speed": speed
            }
            simulator = ZombieSimulator(config)
            animate_points(chart_placeholder, simulator)

        if stop:
            pass
