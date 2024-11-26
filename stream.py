import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data(file_name):
    """Load CSV data into a Pandas DataFrame."""
    return pd.read_csv(file_name)

# Main Streamlit app
def main():
    st.title("Apple Health Data Dashboard")

    # Sidebar
    st.sidebar.header("Select Data")
    data_type = st.sidebar.selectbox("Choose Data Type", ["Sleep", "Heart Rate", "Step Count", "Respiratory Rate"])

    # Load data based on selection
    if data_type == "Sleep":
        file_name = "sleep_data.csv"
        df = load_data(file_name)
        st.subheader("Sleep Data")
        st.write(df.head())

        # Convert to datetime for plotting
        df['startDate'] = pd.to_datetime(df['startDate'])
        df['endDate'] = pd.to_datetime(df['endDate'])
        df['duration'] = (pd.to_datetime(df['endDate']) - pd.to_datetime(df['startDate'])).dt.total_seconds() / 3600

        # Daily total sleep
        df['date'] = df['startDate'].dt.date
        daily_sleep = df.groupby('date')['duration'].sum()

        # Plot sleep data
        st.line_chart(daily_sleep, use_container_width=True)
        st.write(f"Average Sleep Duration: {daily_sleep.mean():.2f} hours")

    elif data_type == "Heart Rate":
        file_name = "heart_rate_data.csv"
        df = load_data(file_name)
        st.subheader("Heart Rate Data")
        st.write(df.head())

        # Convert to numeric
        df['value'] = pd.to_numeric(df['value'])
        df['creationDate'] = pd.to_datetime(df['creationDate'])
        df['date'] = df['creationDate'].dt.date

        # Daily average heart rate
        daily_hr = df.groupby('date')['value'].mean()

        # Plot heart rate
        st.line_chart(daily_hr, use_container_width=True)
        st.write(f"Average Heart Rate: {daily_hr.mean():.2f} bpm")

    elif data_type == "Step Count":
        file_name = "step_count_data.csv"
        df = load_data(file_name)
        st.subheader("Step Count Data")
        st.write(df.head())

        # Convert to numeric
        df['value'] = pd.to_numeric(df['value'])
        df['creationDate'] = pd.to_datetime(df['creationDate'])
        df['date'] = df['creationDate'].dt.date

        # Daily total steps
        daily_steps = df.groupby('date')['value'].sum()

        # Plot step count
        st.line_chart(daily_steps, use_container_width=True)
        st.write(f"Average Steps: {daily_steps.mean():.0f} steps")

    elif data_type == "Respiratory Rate":
        file_name = "respiratory_rate_data.csv"
        df = load_data(file_name)
        st.subheader("Respiratory Rate Data")
        st.write(df.head())

        # Convert to numeric
        df['value'] = pd.to_numeric(df['value'])
        df['creationDate'] = pd.to_datetime(df['creationDate'])
        df['date'] = df['creationDate'].dt.date

        # Daily average respiratory rate
        daily_resp = df.groupby('date')['value'].mean()

        # Plot respiratory rate
        st.line_chart(daily_resp, use_container_width=True)
        st.write(f"Average Respiratory Rate: {daily_resp.mean():.2f} breaths/min")

# Run the Streamlit app
if __name__ == "__main__":
    main()
