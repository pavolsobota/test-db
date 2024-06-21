import pandas as pd
from pymongo import MongoClient

# MongoDB connection setup
def connect_to_mongo(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# Import data from CSV into MongoDB
def import_csv_to_mongo(db, collection_name, csv_file_path):
    df = pd.read_csv(csv_file_path)
    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    # Access the collection
    collection = db[collection_name]
    # Delete existing documents in the collection
    collection.delete_many({})
    # Insert new data into the collection
    collection.insert_many(data)

# Reload the database (assuming you want to ensure data is online)
def reload_database(db, collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    print(f"Collection '{collection_name}' has {count} documents.")

if __name__ == "__main__":
    # MongoDB URI and database/collection details
    username = "sobotapavol9"
    password = "6ttKmK5zbuwdLWxu"
    cluster_url = "testdatabase.gblbwaz.mongodb.net"
    database_name = "movies-api"
    collection_name = "movies"
    csv_file_path = "public/output.csv"
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"

    # Connect to MongoDB
    db = connect_to_mongo(mongo_uri, database_name)

    # Import CSV data into MongoDB
    import_csv_to_mongo(db, collection_name, csv_file_path)

    # Reload the database
    reload_database(db, collection_name)
