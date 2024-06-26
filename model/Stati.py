from dataclasses import dataclass
@dataclass
class Stato:
    id:str
    Name:str
    Lat:float
    Lng:float

    def __hash__(self):
        return hash(self.id)