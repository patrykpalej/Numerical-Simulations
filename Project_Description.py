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

    st.markdown("""This project is (going to be) a set of numerical simulations regarding
             various phenomena such as:""")

    with st.expander("Gravity"):
        st.markdown("""In this simulation you choose initial conditions for a group of
         material points ("planets"). You can also read them from file. Then you choose
         what to show in the animation (planets, gravity field, trace of the planets) and
         other details like whether or not to save logs or what to do in case of collision.
         """)

        st.markdown("""Note that both saving logs and saving initial conditions to file is
         possible only when running locally.""")
