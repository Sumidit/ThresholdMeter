import streamlit as st
import pandas as pd

# Function to load Excel data
def load_excel_data(file_url, sheet_name):
    try:
        return pd.read_excel(file_url, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        st.stop()

# Load Excel Data (from the server)
file_url = "https://github.com/Sumidit/ThresholdMeter/blob/main/data.xlsx?raw=true"  # Make sure to use the raw URL
sheet_name = "Sheet1"
data = load_excel_data(file_url, sheet_name)

# Extract unique values for dropdowns
site_a_options = sorted(data["Node A"].dropna().unique().tolist())
site_b_options = sorted(data["Node B"].dropna().unique().tolist())

# Constants
constant_a = 0.25
constant_b = 0.05
connector_loss = 2

# Streamlit UI
st.title("Threshold Meter")

# Site A Dropdown
site_a = st.selectbox("Select Site A:", site_a_options)

# Site B Dropdown
site_b = st.selectbox("Select Site B:", site_b_options)

# Get Link Distance options based on selected Site B
link_distance_options = data.loc[data["Node B"] == site_b, "Link Distance"].dropna().unique().tolist()
link_distance = st.selectbox("Select Link Distance:", link_distance_options)

# Constants Display
st.write(f"Constant A: {constant_a}")
st.write(f"Constant B: {constant_b}")
st.write(f"Connector Loss: {connector_loss}")

# Calculate Threshold (with a unique key)
if st.button("Calculate Threshold", key="threshold_button"):
    if site_a and site_b and link_distance:
        try:
            # Ensure link distance is a float
            link_distance_value = float(link_distance)
            threshold = (constant_a * link_distance_value) + (constant_b * link_distance_value) + connector_loss
            st.success(f"Threshold: {threshold:.2f}")
        except ValueError:
            st.error("Invalid value for Link Distance. Please ensure it's a valid number.")
    else:
        st.error("Please select values for all fields.")

# Additional Calculators - Loss Meter Section

st.subheader("Loss Meter")

# Calculator: Info DWDM Site A
st.subheader("Info DWDM - Site A")
tx_b = st.number_input("TX B", min_value=0.0, step=0.1)
rx_a = st.number_input("RX A", min_value=0.0, step=0.1)
vi_a = st.number_input("VI A", min_value=0.0, step=0.1)

if st.button("Calculate Fiber Loss for Site A", key="fiber_loss_a_button"):
    fiber_loss_a = tx_b - rx_a - vi_a
    st.success(f"Fiber Loss for Site A: {fiber_loss_a:.2f}")

# Calculator: Info DWDM Site B
st.subheader("Info DWDM - Site B")
tx_a = st.number_input("TX A", min_value=0.0, step=0.1)
rx_b = st.number_input("RX B", min_value=0.0, step=0.1)
vi_b = st.number_input("VI B", min_value=0.0, step=0.1)

if st.button("Calculate Fiber Loss for Site B", key="fiber_loss_b_button"):
    fiber_loss_b = tx_a - rx_b - vi_b
    st.success(f"Fiber Loss for Site B: {fiber_loss_b:.2f}")

# Calculator: Threshold Meter (Link Budget)
st.subheader("Threshold Meter (As per Link Budget)")

# Input fields for the Threshold Meter calculation
fiber_length = st.number_input("Fiber Length (KM)", min_value=0.0, step=0.1)
fiber_attenuation = 0.3
splice_loss = 0.05
num_splices = st.number_input("Number Of Splices", min_value=0, step=1)
connector_loss_input = 0.5
connector_count = 2

# Safety margin selection
safety_margin = st.selectbox(
    "Safety Margin",
    options=["10KM or below", "Above 10 KM"]
)

# Assign safety margin value based on selection
if safety_margin == "10KM or below":
    safety_margin_value = 2.5
else:
    safety_margin_value = 3.0

# Calculate Threshold (with a unique key)
if st.button("Calculate Threshold (Link Budget)", key="link_budget_threshold_button"):
    if fiber_length and num_splices:
        threshold = (fiber_length * fiber_attenuation) + (splice_loss * num_splices) + (connector_loss_input * connector_count) + safety_margin_value
        st.success(f"Threshold: {threshold:.2f}")
    else:
        st.error("Please fill in all required fields.")
