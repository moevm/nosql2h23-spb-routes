from neo4j import GraphDatabase
import unittest
import sys

def is_database_server_running(uri, user, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.run("MATCH (n) RETURN COUNT(n) AS count")
        driver.close()
        return True
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return False

def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.discover('.', pattern='logicTest.py'))
    suite.addTests(loader.discover('.', pattern='serverTest.py'))
    suite.addTests(loader.discover('.', pattern='DBdriverTest.py'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    uri = "bolt://0.0.0.0:7687"
    user = "neo4j"
    password = "Andrew_07072002"

    if is_database_server_running(uri, user, password):
        print("Database server is running. Proceeding with tests...")
        run_tests()
    else:
        print("Database server is not running. Please start the database server before running tests.")
        sys.exit(1)
