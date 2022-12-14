# 3rd party modules
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class OptionsMenu_SIR(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Create the "SIR Coefficients" options
        self.beta_sb = QtWidgets.QDoubleSpinBox()
        self.gamma_sb = QtWidgets.QDoubleSpinBox()
        self.t_recovery = QtWidgets.QDoubleSpinBox()
        self.R0 = QtWidgets.QDoubleSpinBox()

        self.gamma_sb.valueChanged.connect(self.onGammaChanged)
        self.t_recovery.valueChanged.connect(self.onTrecChanged)
        self.t_recovery.valueChanged.connect(self.onR0Changed)
        self.R0.valueChanged.connect(self.onR0Changed)

        self.beta_sb.valueChanged.connect(self.onBetaChanged)

        self.R0.setEnabled(False)
        self.t_recovery.setEnabled(False)

        for widget in (self.beta_sb, self.gamma_sb):
            widget.setRange(0, 10)
            widget.setDecimals(4)
            widget.setSingleStep(0.001)

        for widget in (self.t_recovery, self.R0):
            widget.setRange(0, 100)
            widget.setDecimals(4)
            widget.setSingleStep(0.001)

        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Константа швидкості β'), 0, 0)
        coeff_grid.addWidget(self.beta_sb, 0, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість одужання γ'), 1, 0)
        coeff_grid.addWidget(self.gamma_sb, 1, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Cередній час одужання після інфекції'), 2, 0)
        coeff_grid.addWidget(self.t_recovery, 2, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Передаваність хвороби'), 3, 0)
        coeff_grid.addWidget(self.R0, 3, 1)

        coeff_gb = QtWidgets.QGroupBox('Коефіцієнти SIR-моделі:')
        coeff_gb.setLayout(coeff_grid)

        # Create the "Other Parameters" options
        self.sus_sb = QtWidgets.QDoubleSpinBox()
        self.sus_sb.setRange(0, 100000)
        self.sus_sb.setSingleStep(1)

        self.inf_sb = QtWidgets.QDoubleSpinBox()
        self.inf_sb.setRange(0, 100000)
        self.inf_sb.setSingleStep(1)

        self.rec_sb = QtWidgets.QDoubleSpinBox()
        self.rec_sb.setRange(0, 100000)
        self.rec_sb.setSingleStep(1)

        self.days_sb = QtWidgets.QSpinBox()
        self.days_sb.setRange(0, 100000)
        self.days_sb.setSingleStep(10)

       # self.timedelta_sb = QtWidgets.QDoubleSpinBox()
       # self.timedelta_sb.setRange(0, 100)
       # self.timedelta_sb.setSingleStep(0.05)

        other_grid = QtWidgets.QGridLayout()
        other_grid.addWidget(QtWidgets.QLabel('Сприятливі:'), 0, 0)
        other_grid.addWidget(self.sus_sb, 0, 1)
        other_grid.addWidget(QtWidgets.QLabel('Інфіковані'), 1, 0)
        other_grid.addWidget(self.inf_sb, 1, 1)
        other_grid.addWidget(QtWidgets.QLabel('Одужавші:'), 2, 0)
        other_grid.addWidget(self.rec_sb, 2, 1)

        other_grid.addWidget(QtWidgets.QLabel('Дні:'), 3, 0)
        other_grid.addWidget(self.days_sb, 3, 1)
        #other_grid.addWidget(QtWidgets.QLabel('Час дельта:'), 4, 0)
        #other_grid.addWidget(self.timedelta_sb, 4, 1)

        other_gb = QtWidgets.QGroupBox('Інші параметри:')
        other_gb.setLayout(other_grid)

        # Create the "Graph Options" options
        self.legend_cb = QtWidgets.QCheckBox('Показати легенду:')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.legend_change)

        self.grid_cb = QtWidgets.QCheckBox('Показати сітку:')
        self.grid_cb.setChecked(True)
        self.legend_loc_lbl = QtWidgets.QLabel('Місцезнаходження легенди:')
        self.legend_loc_cb = QtWidgets.QComboBox()
        self.legend_loc_cb.addItems([x.title() for x in [
            'right',
            'center',
            'lower left',
            'center right',
            'upper left',
            'center left',
            'upper right',
            'lower right',
            'upper center',
            'lower center',
            'best',
        ]])
        self.legend_loc_cb.setCurrentIndex(6)

        cb_box = QtWidgets.QHBoxLayout()
        cb_box.addWidget(self.legend_cb)
        cb_box.addWidget(self.grid_cb)

        legend_box = QtWidgets.QHBoxLayout()
        legend_box.addWidget(self.legend_loc_cb)
        legend_box.addStretch()

        graph_box = QtWidgets.QVBoxLayout()
        graph_box.addLayout(cb_box)
        graph_box.addWidget(self.legend_loc_lbl)
        graph_box.addLayout(legend_box)

        graph_gb = QtWidgets.QGroupBox('Налаштування графіку:')
        graph_gb.setLayout(graph_box)

        # Create the update/reset buttons
        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Запуск ітерацій')

       # self.totalCases_btn = QtWidgets.QPushButton('Статистика хвороб')
        #self.onlyInfectious_btn = QtWidgets.QPushButton('onlyInfectious')

       # self.inf_btn = QtWidgets.QPushButton('Інфіковані')
       # self.preyPredator_btn = QtWidgets.QPushButton('Хищники-жертвы')

        self.reset_values_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Зброс значень')
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Очистити графік')

        #self.onlyInfectious_btn.clicked.connect(self.onlyInfectious)

        self.reset_values_btn.clicked.connect(self.reset_values)

     #   self.preySuperpredator_btn.clicked.connect(self.preySuperpredator)
      #  self.preyPredator_btn.clicked.connect(self.preyPredator)

        # Create the main layout
        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(graph_gb)
        container.addWidget(self.update_btn)
#        container.addWidget(self.totalCases_btn)
 #       container.addWidget(self.onlyInfectious_btn)
      #  container.addStretch()
     #   container.addWidget(self.preySuperpredator_btn)
     #   container.addWidget(self.preyPredator_btn)
     #
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)
        container.addStretch()
        self.setLayout(container)

        # Populate the widgets with values
        self.reset_values()

    def onGammaChanged(self):
        if self.gamma_sb.value() == 0:
            return

        newVal = 1/self.gamma_sb.value()
        new = self.beta_sb.value() / self.gamma_sb.value()
        if newVal != self.t_recovery.value():
            self.t_recovery.setValue(newVal)
            self.R0.setValue(new)

    def onBetaChanged(self):
        if self.gamma_sb.value() == 0:
            return
        newVal = self.beta_sb.value() / self.gamma_sb.value()
        if newVal != self.gamma_sb.value():
            self.R0.setValue(newVal)

    def onR0Changed(self):
        if self.t_recovery.value() == 0:
            return
        newVal = self.R0.value() / self.t_recovery.value()
        self.beta_sb.setValue(newVal)

    def onTrecChanged(self):
        if self.t_recovery.value() == 0:
            return
        newVal = 1 / self.t_recovery.value()
        if newVal != self.gamma_sb.value():
            self.gamma_sb.setValue(newVal)

    def reset_values(self):
        self.beta_sb.setValue(0.1)
        self.gamma_sb.setValue(0.1)
        self.sus_sb.setValue(5)
        self.inf_sb.setValue(20)
        self.rec_sb.setValue(5)
        self.days_sb.setValue(100)
        #self.timedelta_sb.setValue(0.02)

    def legend_change(self):
        self.legend_loc_cb.setEnabled(self.legend_cb.isChecked())
        self.legend_loc_lbl.setEnabled(self.legend_cb.isChecked())
