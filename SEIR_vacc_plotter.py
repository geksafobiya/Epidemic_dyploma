#!/usr/bin/env python

# Python standard library modules
import sys

# 3rd party modules
import matplotlib
import matplotlib.backends.backend_qt5agg as backend_qt5agg
from matplotlib.figure import Figure
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

# Local application modules
from SEIR_vacc_calculator import SEIRvaccCalculator
from OptionsMenu_SEIR_vacc import OptionsMenu_SEIR_vacc
#from options_menu_4_species import OptionsMenu_4_species
#from options_menu_2 import OptionsMenu_2_species

#import resources

APP_NAME = 'Epidemics'
AUTHOR = 'Клименко Анастасiя'

class AppForm_SEIR_vacc(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # название окна
        self.setWindowTitle(APP_NAME)

        # Создание в меню параметров в виджете док-станции
        self.options_menu = OptionsMenu_SEIR_vacc()
        dock = QtWidgets.QDockWidget('Налаштування коефіцієнтів', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        # Подключение сигналов из меню параметров
        self.options_menu.update_btn.clicked.connect(self.clear_graph)
        self.options_menu.update_btn.clicked.connect(self.calculate_data)
#        self.options_menu.update_btn.clicked.connect(self.calculate_coeffs)

         #elf.options_menu.t_recovery = self.trec

        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)
        self.options_menu.legend_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.grid_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.legend_loc_cb.currentIndexChanged.connect(self.redraw_graph)

        # создание графика
        fig = Figure((7.0, 3.0), dpi=100)
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        self.canvas.setParent(self)
        self.axes = fig.add_subplot(111)
        backend_qt5agg.NavigationToolbar2QT(self.canvas, self.canvas)

        # инициализация графа
        self.clear_graph()

        self.setCentralWidget(self.canvas)

        # создать менюбар действий

        about_action = QtWidgets.QAction('&About', self)
        about_action.setToolTip('About')
        about_action.setIcon(QtGui.QIcon(':/resources/icon_info.png'))
        about_action.triggered.connect(self.show_about)

        sir_action = QtWidgets.QAction('&SEIR vaccined', self)
        sir_action.setToolTip('SEIR vaccined')
        sir_action.triggered.connect(self.show_seir)

     # создать менюбар
        file_exit_action = QtWidgets.QAction('&Exit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('&Exit')
        file_menu.addAction(file_exit_action)

        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction(about_action)

        sir_menu = self.menuBar().addMenu('&SEIR vaccined')
        sir_menu.addAction(sir_action)


    def calculate_data(self):
        # объект GrowthCalculator
        growth = SEIRvaccCalculator()

        # Update the GrowthCalculator parameters from the GUI options
        growth.gamma = self.options_menu.gamma_sb.value()
        growth.beta = self.options_menu.beta_sb.value()
        growth.alpha = self.options_menu.alpha_sb.value()
        growth.u = self.options_menu.u_sb.value()
        growth.sus = self.options_menu.sus_sb.value()
        growth.exp = self.options_menu.exp_sb.value()
        growth.inf = self.options_menu.inf_sb.value()
        growth.rec = self.options_menu.rec_sb.value()

        growth.days = self.options_menu.days_sb.value()
        #growth.dt = self.options_menu.timedelta_sb.value()

        # Calculate the population growths
        results = growth.calculate()
        self.infectious_history.extend(results['Infectious'])
        self.exposed_history.extend(results['Exposed'])
        self.susceptible_history.extend(results['Susceptible'])
        self.recovered_history.extend(results['Recovered'])

        if (len(self.infectious_history) == 0 and
                len(self.susceptible_history) == 0 and
                len(self.recovered_history) == 0 and
                len(self.exposed_history)==0):
            QtWidgets.QMessageBox.information(self, 'Error', 'Помилка')
            return

        # последнее в векторе количество популяции на панель инструментов параметров
      #  print('self.predator_history[-1]', self.predator_history[-1])
      #  self.options_menu.predator_sb.setValue(self.predator_history[-1])
      #  self.options_menu.prey_sb.setValue(self.prey_history[-1])
      #  self.options_menu.superpredators_sb.setValue(self.superpredator_history[-1])
        # перерисовать граф
        self.redraw_graph()

    def clear_graph(self):
        # очистить историю популяций
        self.infectious_history = []
        self.exposed_history = []
        self.susceptible_history = []
        self.recovered_history = []

        # перерисовать граф
        self.redraw_graph()

    def redraw_graph(self):
        # очистить граф
        self.axes.clear()

        # Create the graph labels
        self.axes.set_title('SEIR-model with vaccines: Susceptible, Exposed, Infectious, Recovered')
        self.axes.set_xlabel('Ітерації')
        self.axes.set_ylabel('Кількість населення')

        # Plot the current population data

        if self.susceptible_history:
            self.axes.plot(self.susceptible_history, 'b-', label='ще не хворіли')
        if self.exposed_history:
            self.axes.plot(self.exposed_history, 'y-', label='інкубаційні')
        if self.infectious_history:
            self.axes.plot(self.infectious_history, 'r-', label='хворі')
        if self.recovered_history:
            self.axes.plot(self.recovered_history, 'g-', label='перехворілі')
        # если нужно, создаём легенду
        if self.options_menu.legend_cb.isChecked():
            if self.recovered_history or self.susceptible_history or self.infectious_history or self.exposed_history:
                legend_loc = str(
                    self.options_menu.legend_loc_cb.currentText()
                ).lower()
                legend = matplotlib.font_manager.FontProperties(size=10)
                self.axes.legend(loc=legend_loc, prop=legend)

        # если нужно, сетки на графике
        self.axes.grid(self.options_menu.grid_cb.isChecked())

        # рисуем график
        self.canvas.draw()

    def show_seir(self):

        message = '''<font size="+2">SEIR-модель з вакцинацією</font>
            <p>dS/dt = -βSI/N 
            <p>dE/dt = (1-u)βSI/N - αE
            <p>dI/dt = αE - ɣI
            <p>dR/dt = ɣI
            <p>де
            <p>S — кількість сприятливих до вірусу;
            <p>Е — кількість населення із хворобою у інкубаційному періоді;
            <p>I — кількість інфікованих;
            <p>R — кількість переболівших;
            <p>β — константа швидкості;
            <p>u — ефективність втручань громадської охорони здоров'я;
            <p>α — швидкість переходу хвороби від інкубаційної стадії до відкритої;
            <p>ɣ — швидкість одужання.
            '''
        QtWidgets.QMessageBox.about(self, 'SЕIR vaccined' + '', message)

    def show_about(self):

        message = '''<font size="+2">%s</font>
            <p>Дипломна робота на тему "моделювання епідеміологічних моделей".
            <p>Написана by %s, група КА-13мп.
            ''' %(APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'About' + APP_NAME, message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/resources/icon.svg'))
    form = AppForm_SEIR_vacc()
    form.show()
    app.exec_()
