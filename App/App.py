from rich.traceback import install
import pandas as pd
import os

# Enable rich traceback for better debugging
install(show_locals=True)

def extract_prospects(file_name="Examplar Prospects List.csv"):
    """
    Reads a CSV file and extracts 'Prospect Name' (Column A) and 'Website' (Column C).
    
    Returns:
        list of tuples: [(prospect_name, website), ...]
    """
    file_path = os.path.join(os.getcwd(), file_name)

    # Load the CSV
    df = pd.read_csv(file_path)

    # Extract required columns
    df_selected = df.iloc[:, [0, 2]]  # Adjust index if needed
    df_selected.columns = ["Prospect Name", "Website"]  # Rename columns

    # Convert to a list of tuples
    prospects_list = [
        (str(row["Prospect Name"]), str(row["Website"]) if pd.notna(row["Website"]) else "N/A")
        for _, row in df_selected.iterrows()
    ]

    return prospects_list  # Store it for later use
