from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime` ) as year
                    from sighting s
                    order by year(s.`datetime` ) desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllShapesByYear(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query =  """select distinct s.shape as s
                        from sighting s 
                        where year(s.`datetime` ) = %s
                        and s.shape <> "unknown"
                        and s.shape <> ""
                        order by s.shape asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["s"])
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllNodes(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s
                        where year(s.`datetime` ) = %s
                        and s.shape = %s """
            cursor.execute(query, (anno,shape,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllEdgesPesati(anno, shape, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id s1Id, s2.id as s2Id, (s2.longitude - s1.longitude ) as peso
                        from sighting s1, sighting s2
                        where year(s1.`datetime` ) = %s and year(s2.`datetime` ) = %s
                        and s1.shape = %s and s2.shape = %s
                        and s1.state = s2.state 
                        and s1.id <> s2.id 
                        and s1.longitude < s2.longitude 
                        order by peso desc"""
            cursor.execute(query, (anno, anno, shape, shape,))

            for row in cursor:
                result.append(Arco(idMap[row["s1Id"]], idMap[row["s2Id"]],row["peso"]))
            cursor.close()
            cnx.close()
        return result