from databaseConnection import DataBaseConnection

if __name__ == "__main__":
    print("Rebuilding the database...")
    db = DataBaseConnection()
    db.delete()
    db.connect()
    db.build()
    db.disconnect()
    print ("Done.")