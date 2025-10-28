import pandas as pd

def load_data(*, file_path: str) -> pd.DataFrame:
    """
    Load online retail data from a CSV file
    Args:
        file_path (str): The path to the CSV file containing the online retail data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the loaded online retail data.
    
    """
    
    data = pd.read_excel(file_path)
    return data