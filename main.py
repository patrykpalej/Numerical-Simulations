import streamlit as st
from st_pages import Page, show_pages


st.set_page_config(layout="wide", page_title="Numerical simulations")


custom_css = """

<style> 
    .stNumberInput [data-testid=stNumberInputContainer]{
        width: 90%;
    } 
    
    .stSelectbox{
        width: 90%;
    } 
    
   div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
        }
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem;
    }
</style>

"""

# Display the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)


show_pages(
    [
        Page("main.py", "Project description", "💻"),
        Page("pages/page_gravity.py", "Gravity modeling", "🏡"),
        Page("pages/test.py", "Test", "🏡"),

    ])


if __name__ == "__main__":
    st.title("Project description")
    st.markdown("Project description...")
