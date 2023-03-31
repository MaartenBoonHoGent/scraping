from databaseConnection import DataBaseConnection

if __name__ == "__main__":
    print("Rebuilding the database...")
    db = DataBaseConnection()
    db.delete()
    db.connect()
    print(f"Building the database...")
    db.build()
    db.disconnect()
    print ("Done.")