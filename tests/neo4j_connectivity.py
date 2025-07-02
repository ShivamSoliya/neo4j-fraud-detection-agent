"""
This script tests the Neo4j connectivity by checking database connection and retrieving schema.
"""

from neo4j import GraphDatabase

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

print(f"URI value: {NEO4J_URI}")

if NEO4J_URI:
    with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print(driver.session().run("RETURN 1").single())
        driver.close()

else:
    print("NEO4J_URI is not set.")