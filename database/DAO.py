from database.DB_connect import DBConnect
from model.Stati import Stato


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getShape():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct  s.shape 
                from sighting s """

        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
            from state s """

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(row["id"], row["Name"], row["Lat"], row["Lng"]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getPesi(forma, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.state, count(*) as peso
                from sighting s
                where s.shape = %s and YEAR (s.`datetime`)=%s
                group by s.state"""

        cursor.execute(query,(forma, anno))

        for row in cursor:
            result.append((row["state"], row["peso"]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getVicini():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 , n.state2 
                from neighbor n 
                where n.state1 < n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result
