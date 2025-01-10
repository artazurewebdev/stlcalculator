import streamlit as st
from stl import mesh
import numpy as np
import tempfile

def calculate_volume(stl_mesh):
    volume = 0
    for facet in stl_mesh.vectors:
        volume += np.dot(facet[0], np.cross(facet[1], facet[2])) / 6
    return abs(volume)

# Conversion factors
conversion_factors = {
    "Cubic Millimeters (mm³)": 1,
    "Cubic Centimeters (cm³)": 0.001,
    "Cubic Inches (in³)": 0.0000610237441,
}

# Streamlit App
st.title("STL Volume Calculator")

st.write("Made for Team Oceana in the Future City Project")

st.write("Upload your STL file to calculate its volume.")

# Dropdown menu for unit selection
selected_unit = st.selectbox(
    "Select the volume unit:",
    list(conversion_factors.keys())
)

uploaded_file = st.file_uploader("Choose an STL file", type=["stl"])

if uploaded_file is not None:
    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        
        # Read the STL file from the temporary file
        stl_mesh = mesh.Mesh.from_file(temp_file_path)
        
        # Calculate the volume in cubic millimeters
        volume_mm3 = calculate_volume(stl_mesh)
        
        # Convert to the selected unit
        conversion_factor = conversion_factors[selected_unit]
        converted_volume = volume_mm3 * conversion_factor
        
        st.success(f"Calculated Volume: {converted_volume:.2f} {selected_unit}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
