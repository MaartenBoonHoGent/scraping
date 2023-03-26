from database import DatabaseConnection

if __name__ == "__main__":
    print("Rebuilding the database...")
    db = DatabaseConnection()
    db.delete()
    db.connect()
    print ("Done.")