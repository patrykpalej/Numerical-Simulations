import streamlit as st


st.set_page_config(page_title="Numerical simulations")


custom_css = """
<style> 
    div[data-testid="stMarkdownContainer"] > p,
    div[data-testid="stMarkdownContainer"] > ul > li {
            font-size: 1.2rem;   
            }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


if __name__ == "__main__":
    st.title("Numerical simulations")
    st.markdown("## Project description")

    st.markdown("""This project is a set of numerical simulations regarding
             various phenomena such as:""")

    with st.expander("Gravitational interactions"):
        st.markdown("""In this simulation, you can set the initial conditions
         for a group of material points, referred to as "planets." You have the option to input
         these conditions manually or import them from a file. Once set, you can customize
         the animation by selecting elements to display, such as the planets themselves, 
         the gravity field, and the planets' trajectories. Additionally, you can choose to
         save detailed logs and decide how the simulation should respond to collisions between 
         the planets.
         """)

        st.markdown("""Note that both saving logs and saving initial conditions to file is
         possible only when running locally.""")

    with st.expander("Humans vs. Zombies battle"):
        st.markdown("""In this simulation, two groups of characters fight each other to survive.
         Each character is defined by a set of characteristics, including their coordinates (x, y),
         velocity, and power. When a zombie wins a fight, it transforms a human into
         a new zombie. However, if a human prevails in the combat, they eliminate
         their zombie opponent.""")
