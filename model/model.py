import networkx as nx
from geopy.distance import geodesic
from time import time

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._dizNodi={}
        self._dizionariopesi={}
        self._dizionarioIncidenti={}
        self._bestSol=[]
        self._distanzaBest=0
        pass
    def getShape(self):
        return DAO.getShape()
    def creaGrafo(self,forma,anno):
        self._grafo.clear()
        self._dizNodi={}
        self._dizionariopesi={}
        for element in DAO.getNodi():
            self._dizNodi[element.id]=element
            self._grafo.add_node(element)
        for element in DAO.getPesi(forma, anno):
            self._dizionariopesi[element[0].upper()]=element[1]
        for element in DAO.getVicini():
            self._grafo.add_edge(self._dizNodi[element[0]],self._dizNodi[element[1]], weight=0)
        for edge in self._grafo.edges():
            if edge[0].id in self._dizionariopesi:
                self._grafo[edge[0]][edge[1]]['weight']+=self._dizionariopesi[edge[0].id]
            if  edge[1].id in self._dizionariopesi:
                self._grafo[edge[0]][edge[1]]['weight']+=self._dizionariopesi[edge[1].id]
    def getIncidenza(self):
        self._dizionarioIncidenti={}
        for element in self._dizNodi:
            somma=0
            stato=self._dizNodi[element]
            for vicino in self._grafo.neighbors(stato):
                somma+=self._grafo[stato][vicino]['weight']
            self._dizionarioIncidenti[element]=somma
        return self._dizionarioIncidenti
    def numNodi(self):
        return len(self._grafo.nodes())
    def numArchi(self):
        return len(self._grafo.edges())
    def _ricorsione(self,parziale,nodo,distanzaattuale,pesomax):
        successori=list(self._grafo.neighbors(nodo))
        for element in successori.copy():
            if (nodo,element) in parziale or self._grafo[nodo][element]['weight']<=pesomax:
                successori.remove(element)
        if len(successori)==0:
            if distanzaattuale>self._distanzaBest:
                self._bestSol=parziale
                self._distanzaBest=distanzaattuale
                print(self._distanzaBest)
            return
        else:
            for item in successori:
                nuovo_nodo = item
                parziale_nuovo = list(parziale)
                parziale_nuovo.append((nodo,nuovo_nodo))
                distanzaattuale_nuovo=distanzaattuale+geodesic((nodo.Lat,nodo.Lng),(nuovo_nodo.Lat,nuovo_nodo.Lng)).kilometers
                nuovopesomax=self._grafo[nodo][nuovo_nodo]['weight']
                self._ricorsione(parziale_nuovo,nuovo_nodo,distanzaattuale_nuovo,nuovopesomax)
    def getPath(self):
        self._bestSol = []
        self._distanzaBest = 0
        for nodes in self._grafo.nodes():
            self._ricorsione([],nodes,0,0)
            print("r")
        return self._bestSol
    def getspecificheArco(self,nodo1, nodo2):
        return (geodesic((nodo1.Lat,nodo1.Lng),(nodo2.Lat,nodo2.Lng)).kilometers,self._grafo[nodo1][nodo2]['weight'])


