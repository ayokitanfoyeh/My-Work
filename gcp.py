
#%%
from google.cloud import secretmanager
import sys
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import Column, Float, Integer, String, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Initialize the Secret Manager client
client = secretmanager.SecretManagerServiceClient()

# Function to access a secret version
def access_secret_version(project_id, secret_id, version_id="latest"):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

DB_USER = access_secret_version("kitans-first-project", "DB_USER")
DB_PASS = access_secret_version("kitans-first-project", "DB_PASS")

# initialize parameters
INSTANCE_CONNECTION_NAME = f"kitans-first-project:us-central1:kitandatabase" 
DB_NAME = "kitan1data"

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pytds",
        user='python',
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
engine = sqlalchemy.create_engine(
    "mssql+pytds://",
    creator=getconn,
)

# Execute a SELECT query and print the results
query = text("SELECT * FROM Employees")  

try:
    # Execute the query using a connection
    with engine.connect() as connection:
        result = connection.execute(query)
        
        # Fetch all results
        rows = result.fetchall()
        
        # Print out the rows
        for row in rows:
            print(row)

finally:
    # Close the connector
    connector.close()
# %%
