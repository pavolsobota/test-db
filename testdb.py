import pymongo
import pandas as pd
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)


def connect_to_mongodb(username, password, cluster_url, database_name, collection_name):
    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]
    return collection

def export_to_csv(collection, fields, array_fields, output_file):
    
    projection = {field: 1 for field in fields}
    for field in array_fields:
        projection[field] = 1
    
    pipeline = [{"$project": projection}]

    for array_field in array_fields:
        pipeline.append({"$unwind": f"${array_field}"})

    documents = collection.aggregate(pipeline)
    df = pd.DataFrame(list(documents))
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    df.to_csv(output_file, index=False)

@app.route('/export', methods=['POST'])
def export_data():
    # Retrieve parameters from the POST request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cluster_url = data.get('cluster_url')
    database_name = data.get('database_name')
    collection_name = data.get('collection_name')
    output_file = data.get('output_file', 'output.csv')
    fields = data.get('fields', [])
    array_fields = data.get('array_fields', [])
  # Connect to MongoDB and export data to CSV
    try:
        collection = connect_to_mongodb(username, password, cluster_url, database_name, collection_name)
        export_to_csv(collection, fields, array_fields, output_file)
        return jsonify({"message": f"Data exported to {output_file}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def main():
    username = "sobotapavol9"
    password = "6ttKmK5zbuwdLWxu"
    cluster_url = "testdatabase.gblbwaz.mongodb.net"
    database_name = "movies-api"
    collection_name = "movies"
    output_file = "public/output.csv"  # Save to the public directory
    fields = ["_id", "imdbId", "title"]
    array_fields = ["genres"]
    collection = connect_to_mongodb(username, password, cluster_url, database_name, collection_name)
    export_to_csv(collection, fields, array_fields, output_file)
    print(f"Data exported to {output_file}")

if __name__ == '__main__':
    # app.run(debug=True)
    main()


# fields for production purposes on exact product
# "ID", "name.cz", "prices.base.CZ.price", "prices.base.CZ.tax",  "prices.club.CZ.price", "prices.club.CZ.tax", "validity.from", "validity.to", "visibility.from", "visibility.to", "meta.sspFutureValidity", "tags", "meta.giftStatus", "meta.cardDeposit", "timeSlotGroup", "season", "segments"