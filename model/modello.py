import copy
from cmath import inf
from xml.dom.expatbuilder import parseFragment

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._sightings = []
        self._idMapS = {}
        self._camminoOttimo = None
        self._maxPunteggio = None

    def getSolOttima(self):
        self._camminoOttimo = []
        self._maxPunteggio = float('-inf')

        #non conosciamo source:
        for nodo_partenza in self._graph.nodes():
            parziale = [nodo_partenza]
            self._ricorsione(parziale)
        return self._camminoOttimo, self._maxPunteggio

    def _ricorsione(self, parziale):
          if self.getScore(parziale) > self._maxPunteggio:
              self._maxPunteggio = (self.getScore(parziale))
              self._camminoOttimo = copy.deepcopy(parziale)


          nodo_corrente = parziale[-1]
          for vicino in self._graph.successors(nodo_corrente):  #scorro seguendo direzione archi
              if self.isAdmissible(parziale, vicino):
                  parziale.append(vicino)
                  self._ricorsione(parziale)
                  parziale.pop()

    def getScore(self, parziale):
        #+100 per ogni avvistamento nel cammino
        #+200 se avvistamento nello stesso mese del precedente
        #non applicabile al primo avvistamento
        if not parziale:
            return 0

        score_partenza = len(parziale) * 100
        for i in range(1,len(parziale)): #escludo il primo
            corrente = parziale[i]
            precedente = parziale[i-1]
            if corrente.datetime.month == precedente.datetime.month:
                score_partenza += 200

        return score_partenza


    def isAdmissible(self, parziale, n):
        #durata strettamente crescente
       #non piu di 2 avvistamenti nello stesso mese
       #segui direzione archi
       conteggio_mesi = {}
       for p in parziale:
           m = p.datetime.month
           conteggio_mesi[m] = conteggio_mesi.get(m, 0) + 1

       mese = n.datetime.month
       if conteggio_mesi.get(mese, 0) >= 3:
           return False

       precedente = parziale[-1]
       if precedente.duration >= n.duration:
           return False

       if n in parziale:  #non puo gia essere presente
           return False

       return True




    def getAllYears(self):
        return DAO.getAllYears()
    def getAllShapesByYear(self,anno):
        return DAO.getAllShapesByYear(anno)

    def buildGraph(self,anno,shape):
        self._sightings = DAO.getAllNodes(anno,shape)
        self._graph.add_nodes_from(self._sightings)
        for s in self._sightings:
            self._idMapS[s.id] = s

        myedges = DAO.getAllEdgesPesati(anno,shape, self._idMapS)
        for e in myedges:
            self._graph.add_edge(e.s1,e.s2,weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        edges = sorted(self._graph.edges(data=True),key=lambda x: x[2]["weight"], reverse=True)
        return edges[:5]