import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        a = self._view.ddyear.value
        s = self._view.ddshape.value
        if a is None or s is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno e una shape per procedere"))
            self._view.update_page()
            return
        try:
            anno = int(a)
        except:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("anno non numerico"))
            self._view.update_page()

        self._model.buildGraph(anno,s)
        n,a = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"grafo creato correttamente con {n} nodi e {a} archi"))
        top5archi = self._model.getTop5Archi()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore:"))
        for t in top5archi:
            self._view.txt_result1.controls.append(ft.Text(f"{t[0]}-->{t[1]} peso {t[2]["weight"]}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDYears(self):
            years = self._model.getAllYears()
            for y in years:
                self._view.ddyear.options.append(ft.dropdown.Option(y))
            self._view.ddyear.on_change = self.fillDDShape  # NO PARAMETRI
            self._view.update_page()


    def fillDDShape(self, e):  # DEVO METTERLO PERCHE VIENE SCATENATO DA ON CHANGE

            a = self._view.ddyear.value
            if a is None:
                self._view.txt_result1.controls.clear()
                self._view.txt_result1.controls.append(ft.Text("Selezionare un anno per procedere"))
                self._view.update_page()
                return
            try:
                anno = int(a)
            except:
                self._view.txt_result1.controls.clear()
                self._view.txt_result1.controls.append(ft.Text("anno non numerico"))
                self._view.update_page()

                # --- RESET COMPLETO PRIMA DI CHIEDERE I DATI ---
                self._view.ddshape.options.clear()
                self._view.ddshape.value = None
                self._view.ddshape.update()

            stati = self._model.getAllShapesByYear(anno)
            for s in stati:
                self._view.ddshape.options.append(ft.dropdown.Option(s))
            self._view.update_page()

