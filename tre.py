import xml.etree.ElementTree as ET
import pandas as pd
import csv
from typing import Generator, Tuple



def gen_records(file_name: str, record_type: str):
    """Generate elements of the specified type from the XML file."""
    for event, elmt in ET.iterparse(file_name, events=('start',)):
        if elmt.tag == 'Record' and elmt.attrib.get('type') == record_type:
            yield elmt.attrib
        elmt.clear()  # Free memory



# Specific generators for each health data type
def gen_sleep(file_name: str) -> Generator[Tuple[str, str, str], None, None]:
    """Generate sleep data records."""
    for record in gen_records(file_name, 'HKCategoryTypeIdentifierSleepAnalysis'):
        yield record['creationDate'], record['startDate'], record['endDate']


def gen_heart_rate(file_name: str) -> Generator[Tuple[str, str], None, None]:
    """Generate heart rate data records."""
    for record in gen_records(file_name, 'HKQuantityTypeIdentifierHeartRate'):
        yield record['creationDate'], record['value']


def gen_step_count(file_name: str) -> Generator[Tuple[str, str], None, None]:
    """Generate step count data records."""
    for record in gen_records(file_name, 'HKQuantityTypeIdentifierStepCount'):
        yield record['creationDate'], record['value']


def gen_resp_rate(file_name: str) -> Generator[Tuple[str, str], None, None]:
    """Generate respiratory rate data records."""
    for record in gen_records(file_name, 'HKQuantityTypeIdentifierRespiratoryRate'):
        yield record['creationDate'], record['value']


# Function to write generator output to a CSV file
def write_csv(file_name: str, header: Tuple[str], gen: Generator):
    """Write data from a generator to a CSV file."""
    with open(file_name, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # Write header
        for row in gen:
            writer.writerow(row)


# Main handler to process and save multiple data types
def process_health_data(xml_file: str):
    """Process Apple Health data from XML and save to CSV."""
    # Process sleep data
    write_csv('sleep_data.csv', ('creationDate', 'startDate', 'endDate'), gen_sleep(xml_file))

    # Process heart rate data
    write_csv('heart_rate_data.csv', ('creationDate', 'value'), gen_heart_rate(xml_file))

    # Process step count data
    write_csv('step_count_data.csv', ('creationDate', 'value'), gen_step_count(xml_file))

    # Process respiratory rate data
    write_csv('respiratory_rate_data.csv', ('creationDate', 'value'), gen_resp_rate(xml_file))

    print("Data processing complete. CSV files generated.")


# Example usage
if __name__ == "__main__":
    process_health_data('export.xml')
