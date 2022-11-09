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
from SEIRD_full_with_vacc_calculator import SEIRDvaccCalculator
from OptionsMenu_SEIRD_full_with_vacc import OptionsMenu_SEIRD_full_with_vacc
#from options_menu_4_species import OptionsMenu_4_species
#from options_menu_2 import OptionsMenu_2_species

#import resources

APP_NAME = 'Epidemics'
AUTHOR = 'Клименко Анастасiя'

class AppForm_SEIRD_vacc(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # название окна
        self.setWindowTitle(APP_NAME)

        # Создание в меню параметров в виджете док-станции
        self.options_menu = OptionsMenu_SEIRD_full_with_vacc()
        dock = QtWidgets.QDockWidget('Налаштування коефіцієнтів', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.options_menu)
        dock.setWidget(self.scrollArea)
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

        sir_action = QtWidgets.QAction('&SEIRD vaccined', self)
        sir_action.setToolTip('SEIRD vaccined')
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

        sir_menu = self.menuBar().addMenu('&SEIRD vaccined')
        sir_menu.addAction(sir_action)


    def calculate_data(self):
        # объект GrowthCalculator
        growth = SEIRDvaccCalculator()

        # Update the GrowthCalculator parameters from the GUI options
        growth.gamma_unvac = self.options_menu.gamma_unvac_sb.value()
        growth.gamma_vac = self.options_menu.gamma_vac_sb.value()

        growth.beta_unvac_unvac = self.options_menu.beta_unvac_unvac_sb.value()
        growth.beta_unvac_vac = self.options_menu.beta_unvac_vac_sb.value()
        growth.beta_vac_unvac = self.options_menu.beta_vac_unvac_sb.value()
        growth.beta_vac_vac = self.options_menu.beta_vac_vac_sb.value()

        growth.alpha_unvac = self.options_menu.alpha_unvac_sb.value()
        growth.alpha_vac = self.options_menu.alpha_vac_sb.value()

        growth.mu = self.options_menu.mu_sb.value()
        growth.l = self.options_menu.l_sb.value()

        growth.theta_vac = self.options_menu.theta_vac_sb.value()
        growth.theta_unvac = self.options_menu.theta_unvac_sb.value()

        growth.sus_unvac = self.options_menu.sus_unvac_sb.value()
        growth.sus_vac = self.options_menu.sus_vac_sb.value()

        growth.exp_unvac = self.options_menu.exp_unvac_sb.value()
        growth.exp_vac = self.options_menu.exp_vac_sb.value()

        growth.inf_unvac = self.options_menu.inf_unvac_sb.value()
        growth.inf_vac = self.options_menu.inf_vac_sb.value()

        growth.rec_unvac = self.options_menu.rec_unvac_sb.value()
        growth.rec_vac = self.options_menu.rec_vac_sb.value()

        growth.dead = self.options_menu.dead_sb.value()

        growth.days = self.options_menu.days_sb.value()
        #growth.dt = self.options_menu.timedelta_sb.value()

        # Calculate the population growths
        results = growth.calculate()
        self.infectious_unvac_history.extend(results['Infectious_unvac'])
        self.infectious_vac_history.extend(results['Infectious_vac'])
        self.exposed_unvac_history.extend(results['Exposed_unvac'])
        self.exposed_vac_history.extend(results['Exposed_vac'])

        self.susceptible_unvac_history.extend(results['Susceptible_unvac'])
        self.susceptible_vac_history.extend(results['Susceptible_vac'])

        self.recovered_unvac_history.extend(results['Recovered_unvac'])
        self.recovered_vac_history.extend(results['Recovered_vac'])

        self.dead_history.extend(results['Dead'])

        if (len(self.infectious_unvac_history) == 0 and
                len(self.infectious_vac_history) == 0 and
                len(self.exposed_unvac_history) == 0 and
                len(self.exposed_vac_history) == 0 and
                len(self.susceptible_unvac_history) == 0 and
                len(self.susceptible_vac_history) == 0 and
                len(self.recovered_unvac_history) == 0 and
                len(self.recovered_vac_history) == 0 and
                len(self.dead_history) == 0):
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
        self.susceptible_unvac_history = []
        self.susceptible_vac_history = []
        self.exposed_unvac_history = []
        self.exposed_vac_history = []
        self.infectious_unvac_history = []
        self.infectious_vac_history = []
        self.recovered_unvac_history = []
        self.recovered_vac_history = []
        self.dead_history = []

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

        if self.susceptible_unvac_history:
            self.axes.plot(self.susceptible_unvac_history, 'b-', label='ще не хворілі невакциновані')
        if self.susceptible_vac_history:
            self.axes.plot(self.susceptible_vac_history, 'c-', label='ще не хворілі вакциновані')


        if self.exposed_unvac_history:
            self.axes.plot(self.exposed_unvac_history, 'g-', label='інкубаційні невакциновані розсадники')
        if self.exposed_vac_history:
            self.axes.plot(self.exposed_vac_history, 'y-', label='інкубаційні вакциновані розсадники')

        if self.infectious_unvac_history:
            self.axes.plot(self.infectious_unvac_history, 'r-', label='хворі на голову невакциновані')
        if self.infectious_vac_history:
            self.axes.plot(self.infectious_vac_history, 'm-', label='хворі на голову вакциновані')

        if self.recovered_unvac_history:
            self.axes.plot(self.recovered_unvac_history, 'g*', label='очухалися невакциновані')
        if self.recovered_vac_history:
            self.axes.plot(self.recovered_vac_history, 'gx', label='очухалися вакциновані')
        if self.dead_history:
            self.axes.plot(self.dead_history, 'k', label='померли смертю хоробрих')

        # если нужно, создаём легенду
        if self.options_menu.legend_cb.isChecked():
            if self.susceptible_unvac_history or self.susceptible_vac_history or self.exposed_unvac_history or self.exposed_vac_history or self.infectious_unvac_history or self.infectious_vac_history or self.recovered_unvac_history or self.recovered_vac_history or self.dead_history:

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
    form = AppForm_SEIRD_vacc()
    form.show()
    app.exec_()
