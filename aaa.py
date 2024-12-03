import pandas as pd
import matplotlib.pyplot as plt
import defusedxml.ElementTree

# Parse the XML file and extract sleep data
def parse_sleep_data(file_name):
    """Parse sleep data from Apple Health XML export."""
    tree = defusedxml.ElementTree.parse(file_name)
    root = tree.getroot()

    sleep_data = []
    for record in root.findall('Record'):
        if record.attrib.get('type') == 'HKCategoryTypeIdentifierSleepAnalysis':
            sleep_data.append({
                'startDate': record.attrib['startDate'],
                'endDate': record.attrib['endDate'],
                'value': record.attrib['value']  # Sleep stage
            })

    return pd.DataFrame(sleep_data)

# Process and analyze the data
def analyze_sleep_data(df):
    """Analyze sleep data, adding duration and stage breakdown."""
    # Convert timestamps
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    
    # Calculate duration (in hours)
    df['duration'] = (df['endDate'] - df['startDate']).dt.total_seconds() / 3600
    
    # Group by sleep stage
    stage_summary = df.groupby('value')['duration'].sum().sort_values(ascending=False)

    return df, stage_summary

# Plot sleep stage breakdown
import matplotlib.pyplot as plt

def plot_sleep_stages(stage_summary):
    """Plot a pie chart of sleep stage breakdown with improved aesthetics."""
    # Define friendly labels
    friendly_labels = {
        "HKCategoryValueSleepAnalysisInBed": "In Bed",
        "HKCategoryValueSleepAnalysisAsleepCore": "Core Sleep",
        "HKCategoryValueSleepAnalysisAsleepREM": "REM Sleep",
        "HKCategoryValueSleepAnalysisAsleepDeep": "Deep Sleep",
        "HKCategoryValueSleepAnalysisAwake": "Awake"
    }
    # Apply friendly labels to index
    stage_summary = stage_summary.rename(index=friendly_labels)

    # Remove "Awake" stage
    if "Awake" in stage_summary.index:
        stage_summary = stage_summary.drop("Awake")

    # Define custom colors
    colors = ["#4CAF50", "#2196F3", "#FFC107", "#E91E63"]  # Adjusted colors for remaining stages

    # Plot the chart
    plt.figure(figsize=(8, 8))
    stage_summary.plot.pie(
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        labels=None  # Remove labels from the chart
    )
    plt.title('Sleep Stage Breakdown', fontsize=16)
    plt.legend(stage_summary.index, title="Sleep Stages", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.ylabel('')  # Remove y-axis label
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()

# Example usage:
# plot_sleep_stages_improved(stage_summary)

# Example usage:
# plot_sleep_stages_improved(stage_summary)


# Main function
def main():
    # Parse sleep data
    file_name = 'export.xml'  # Replace with your XML file
    df = parse_sleep_data(file_name)

    # Analyze sleep data
    df, stage_summary = analyze_sleep_data(df)

    # Display results
    print("Sleep Stage Summary (hours):")
    print(stage_summary)

    # Plot sleep stage breakdown
    plot_sleep_stages(stage_summary)

    # Save processed data
    df.to_csv('processed_sleep_data.csv', index=False)
    print("Processed data saved to 'processed_sleep_data.csv'")

# Run the analysis
if __name__ == "__main__":
    main()
