import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image."""
    import io
    from PIL import Image

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    return img


# Create a 2D array (replace this with your data)
data = np.zeros((10, 10))

# Create a figure and plot the initial data
fig, ax = plt.subplots()
img = ax.imshow(data, cmap='viridis', vmin=0, vmax=1, extent=(0, 10, 0, 10))
plt.colorbar(img, ax=ax)

# Streamlit app
st.set_page_config(layout="wide")

st.write("# Click on the 2D area to set a number")

# Display the matplotlib figure using st.image
st.image(fig2img(fig), use_column_width=True)

# Placeholder for the coordinates
coordinates_placeholder = st.empty()

# Function to convert matplotlib figure to image

# Function to handle button clicks
def on_button_click(x, y):
    st.write(f"Clicked on coordinates: ({x}, {y})")
    # Perform any further actions based on the clicked coordinates

# Capture button clicks
if st.button("Submit Coordinates"):
    x, y = st.number_input("X coordinate:"), st.number_input("Y coordinate:")
    on_button_click(x, y)
