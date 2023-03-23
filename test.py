
import pandas as pd
import datetime
import databaseConnection
if __name__ == '__main__':
    print('Hello World')

    """
    requiredColumns = {
            "maatschappij_naam": str,
            "maatschappij_code": str,
            "vertrek_airport_code": str,
            "vertrek_luchthaven_naam": str,
            "aankomst_airport_code": str,
            "aankomst_luchthaven_naam": str,
            "opgehaald_tijdstip": datetime.datetime,
            "prijs": float,
            "vrije_plaatsen": int,
            "flightkey": str,
            "vluchtnummer": str,
            "aankomst_tijdstip": datetime.datetime,
            "vertrek_tijdstip": datetime.datetime,
            "aantal_stops": int,
        }
"""
    # Create a dataFrame 
    df = {
        "maatschappij_naam": ["KLM", "KLM", "KLM"],
        "maatschappij_code": ["KL", "KL", "KL"],
        "vertrek_airport_code": ["AMS", "AMS", "AMS"],
        "vertrek_luchthaven_naam": ["Schiphol", "Schiphol", "Schiphol"],
        "aankomst_airport_code": ["LHR", "LHR", "LHR"],
        "aankomst_luchthaven_naam": ["London Heathrow", "London Heathrow", "London Heathrow"],
        "opgehaald_tijdstip": [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()],
        "prijs": [100.0, 200.0, 300.0],
        "vrije_plaatsen": [10, 20, 30],
        "flightkey": ["FDAKJLMICVJAMAJI", "YZPVCHABFQMWVJI5AMV", "FDQKV8ZLKMAWVJMANT"],
        "vluchtnummer": ["KL123", "KL456", "KL789"],
        "aankomst_tijdstip": [datetime.datetime(2023, 3, 5, 12, 30), datetime.datetime(2023, 3, 8, 5, 15), datetime.datetime(2023, 3, 10, 17, 0)],
        "vertrek_tijdstip": [datetime.datetime(2023, 3, 5, 17), datetime.datetime(2023, 3, 8, 9, 45), datetime.datetime(2023, 3, 11, 12, 30)],
        "aantal_stops": [1, 1, 5],
    }
    df = pd.DataFrame(df)
    # Create the database connection
    c = databaseConnection()
    