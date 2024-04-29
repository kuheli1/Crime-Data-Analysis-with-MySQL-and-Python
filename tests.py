from crime_project import *
import unittest

class CrimeTests(unittest.TestCase):

    def test_connect_db(self):
        conn = connect_db()
        self.assertEqual(conn.open, True)

    def test_get_total_records(self):
        conn = connect_db()
        result = get_total_records(conn)
        self.assertEqual(next(iter(result)), 499)

    def test_get_unique_values_of(self):
        conn = connect_db()
        col_name = 'AREA_NAME'
        result = get_unique_values_of(conn, "AREA_NAME")
        expected = ["Southwest", "Central",
                    "N Hollywood", "Mission", "Van Nuys"]
        self.assertEqual(expected, result[0:5])

    def test_get_unique_crime_codes(self):
        conn = connect_db()
        df = get_unique_crime_codes(conn)
        self.assertEqual(len(df), 42)

    

    
