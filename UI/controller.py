import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self._anno=None
        self._shape=None

    def fillDD(self):
        for i in range(1910,2015):
            self._listYear.append(i)
        for element in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(text=f"{element}", on_click=self.read_anno))
        self._listShape=self._model.getShape()
        for element in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(text=f"{element}", on_click=self.read_shape))
        pass

    def read_anno(self,e):
        self._anno = int(e.control.text)

    def read_shape(self, e):
        self._shape = e.control.text

    def handle_graph(self, e):
        if not self._anno:
            self._view.create_alert("inserisci l'anno")
            return
        if not self._shape:
            self._view.create_alert("inserisci la forma")
            return
        self._model.creaGrafo(self._shape,self._anno)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.numNodi()} Numero di archi: {self._model.numArchi()}"))
        dizio=self._model.getIncidenza()
        for element in dizio:
            self._view.txt_result.controls.append(ft.Text(f"Nodo: {element}, somma dei pesi sugli archi: {dizio[element]}"))
        self._view.update_page()
        pass
    def handle_path(self, e):
        path=self._model.getPath()
        for element in path:
            specifiche=self._model.getspecificheArco(element[0],element[1])
            self._view.txtOut2.controls.append(ft.Text(f"{element[0].id}-->{element[1].id}: weight: {specifiche[1]} distance: {specifiche[0]}"))
        self._view.update_page()