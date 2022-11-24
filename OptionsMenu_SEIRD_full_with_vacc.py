# 3rd party modules
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class OptionsMenu_SEIRD_full_with_vacc(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Create the "SIR Coefficients" options
        self.beta_unvac_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.beta_unvac_vac_sb = QtWidgets.QDoubleSpinBox()
        self.beta_vac_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.beta_vac_vac_sb = QtWidgets.QDoubleSpinBox()

        self.gamma_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.gamma_vac_sb = QtWidgets.QDoubleSpinBox()

        self.alpha_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.alpha_vac_sb = QtWidgets.QDoubleSpinBox()

        self.mu_sb = QtWidgets.QDoubleSpinBox()
        self.l_sb = QtWidgets.QDoubleSpinBox()

        self.theta_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.theta_vac_sb = QtWidgets.QDoubleSpinBox()

        self.t_incubation = QtWidgets.QDoubleSpinBox()
        self.t_recovery = QtWidgets.QDoubleSpinBox()
        self.R0 = QtWidgets.QDoubleSpinBox()

      #  self.t_incubation.valueChanged.connect(self.onTIncChanged)
       # self.alpha_sb.valueChanged.connect(self.onAlphaChanged)
       # self.gamma_sb.valueChanged.connect(self.onGammaChanged)
       # self.t_recovery.valueChanged.connect(self.onTrecChanged)

      #  self.beta_sb = QtWidgets.QDoubleSpinBox()
     #   self.beta_sb.valueChanged.connect(self.onBetaChanged)

        for widget in (self.beta_unvac_unvac_sb, self.beta_unvac_vac_sb, self.beta_vac_unvac_sb, self.beta_vac_vac_sb,
                       self.gamma_unvac_sb, self.gamma_vac_sb, self.alpha_unvac_sb, self.alpha_vac_sb, self.mu_sb, self.l_sb,
                       self.theta_unvac_sb, self.theta_vac_sb):
            widget.setRange(0, 2)
            widget.setDecimals(10)
            widget.setSingleStep(0.001)

        for widget in (self.t_recovery, self.R0, self.t_incubation):
            widget.setRange(0, 100)
            widget.setDecimals(10)
            widget.setSingleStep(0.01)



        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість передачі захворювання від невакцинованих до невакцинованих'), 0, 0)
        coeff_grid.addWidget(self.beta_unvac_unvac_sb, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість передачі захворювання від невакцинованих до вак'), 1, 0)
        coeff_grid.addWidget(self.beta_unvac_vac_sb, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість передачі захворювання від вакцинованих до невакцинованих'), 2, 0)
        coeff_grid.addWidget(self.beta_vac_unvac_sb, 2, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість передачі захворювання від вакцинованих до невакцинованих'), 3, 0)
        coeff_grid.addWidget(self.beta_vac_vac_sb, 3, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість одужання невакцинованих'), 4, 0)
        coeff_grid.addWidget(self.gamma_unvac_sb, 4, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість одужання вакцинованих'), 5, 0)
        coeff_grid.addWidget(self.gamma_vac_sb, 5, 1)

        #coeff_grid.addWidget(QtWidgets.QLabel('Cередній час одужання після інфекції'), 2, 0)
       # coeff_grid.addWidget(self.t_recovery, 2, 1)

        #coeff_grid.addWidget(QtWidgets.QLabel('Передаваність хвороби'), 3, 0)
        #coeff_grid.addWidget(self.R0, 3, 1)

        #coeff_grid.addWidget(QtWidgets.QLabel('Інкубаційний період'), 4, 0)
        #coeff_grid.addWidget(self.t_incubation, 4, 1)

        #coeff_grid.addWidget(QtWidgets.QLabel('Швидкість передачі захворювання через взаємодію населення u'), 5, 0)
        #coeff_grid.addWidget(self.u_sb, 5, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість переходу від інкубаційної стадії до відкритої у невакцинованих'), 6, 0)
        coeff_grid.addWidget(self.alpha_unvac_sb, 6, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Швидкість переходу від інкубаційної стадії до відкритої у вакцинованих'), 7, 0)
        coeff_grid.addWidget(self.alpha_vac_sb, 7, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Природня смертність'), 8, 0)
        coeff_grid.addWidget(self.mu_sb, 8, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Народжуваність'), 9, 0)
        coeff_grid.addWidget(self.l_sb, 9, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Смертність від вірусу невакцинованих'), 10, 0)
        coeff_grid.addWidget(self.theta_unvac_sb, 10, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Смертність від вірусу вакцинованих'), 11, 0)
        coeff_grid.addWidget(self.theta_vac_sb, 11, 1)

        coeff_gb = QtWidgets.QGroupBox('Коефіцієнти SEIRD-моделі з вакцинацією:')
        coeff_gb.setLayout(coeff_grid)


        # Create the "Other Parameters" options
        self.sus_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.sus_unvac_sb.setRange(0, 10000000)
        self.sus_unvac_sb.setSingleStep(1)

        self.sus_vac_sb = QtWidgets.QDoubleSpinBox()
        self.sus_vac_sb.setRange(0, 10000000)
        self.sus_vac_sb.setSingleStep(1)

        self.exp_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.exp_unvac_sb.setRange(0, 10000000)
        self.exp_unvac_sb.setSingleStep(1)

        self.exp_vac_sb = QtWidgets.QDoubleSpinBox()
        self.exp_vac_sb.setRange(0, 10000000)
        self.exp_vac_sb.setSingleStep(1)

        self.inf_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.inf_unvac_sb.setRange(0, 10000000)
        self.inf_unvac_sb.setSingleStep(1)

        self.inf_vac_sb = QtWidgets.QDoubleSpinBox()
        self.inf_vac_sb.setRange(0, 10000000)
        self.inf_vac_sb.setSingleStep(1)

        self.rec_unvac_sb = QtWidgets.QDoubleSpinBox()
        self.rec_unvac_sb.setRange(0, 10000000)
        self.rec_unvac_sb.setSingleStep(1)

        self.rec_vac_sb = QtWidgets.QDoubleSpinBox()
        self.rec_vac_sb.setRange(0, 10000000)
        self.rec_vac_sb.setSingleStep(1)

        self.dead_sb = QtWidgets.QDoubleSpinBox()
        self.dead_sb.setRange(0, 100000)
        self.dead_sb.setSingleStep(1)

        self.days_sb = QtWidgets.QSpinBox()
        self.days_sb.setRange(0, 100000)
        self.days_sb.setSingleStep(100)

       # self.timedelta_sb = QtWidgets.QDoubleSpinBox()
       # self.timedelta_sb.setRange(0, 100)
       # self.timedelta_sb.setSingleStep(0.05)

        other_grid = QtWidgets.QGridLayout()
        other_grid.addWidget(QtWidgets.QLabel('Сприятливі невакциновані:'), 0, 0)
        other_grid.addWidget(self.sus_unvac_sb, 0, 1)
        other_grid.addWidget(QtWidgets.QLabel('Сприятливі вакциновані:'), 1, 0)
        other_grid.addWidget(self.sus_vac_sb, 1, 1)

        other_grid.addWidget(QtWidgets.QLabel('Із хворобою у інкубаційному періоді невакциновані:'), 2, 0)
        other_grid.addWidget(self.exp_unvac_sb, 2, 1)
        other_grid.addWidget(QtWidgets.QLabel('Із хворобою у інкубаційному періоді вакциновані:'), 3, 0)
        other_grid.addWidget(self.exp_vac_sb, 3, 1)

        other_grid.addWidget(QtWidgets.QLabel('Інфіковані невакциновані:'), 4, 0)
        other_grid.addWidget(self.inf_unvac_sb, 4, 1)

        other_grid.addWidget(QtWidgets.QLabel('Інфіковані вакциновані:'), 5, 0)
        other_grid.addWidget(self.inf_vac_sb, 5, 1)

        other_grid.addWidget(QtWidgets.QLabel('Одужавші невакциновані:'), 6, 0)
        other_grid.addWidget(self.rec_unvac_sb, 6, 1)

        other_grid.addWidget(QtWidgets.QLabel('Одужавші вакциновані:'), 7, 0)
        other_grid.addWidget(self.rec_vac_sb, 7, 1)

        other_grid.addWidget(QtWidgets.QLabel('Померші:'), 8, 0)
        other_grid.addWidget(self.dead_sb, 8, 1)

        other_grid.addWidget(QtWidgets.QLabel('Дні:'), 9, 0)
        other_grid.addWidget(self.days_sb, 9, 1)
        #other_grid.addWidget(QtWidgets.QLabel('Час дельта:'), 5, 0)
        #other_grid.addWidget(self.timedelta_sb, 5, 1)

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

       # self.inf_btn = QtWidgets.QPushButton('Інфіковані')
       # self.preyPredator_btn = QtWidgets.QPushButton('Хищники-жертвы')

        self.reset_values_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Зброс значень')
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Очистити графік')
        self.ukrainian_values_btn = QtWidgets.QPushButton('Коефіцієнти для України')
        self.reset_values_btn.clicked.connect(self.reset_values)
        self.ukrainian_values_btn.clicked.connect(self.ukrainian_values)
     #   self.preySuperpredator_btn.clicked.connect(self.preySuperpredator)
      #  self.preyPredator_btn.clicked.connect(self.preyPredator)

        # Create the main layout
        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(graph_gb)
        container.addWidget(self.update_btn)
      #  container.addStretch()
     #   container.addWidget(self.preySuperpredator_btn)
     #   container.addWidget(self.preyPredator_btn)
     #
        container.addWidget(self.ukrainian_values_btn)
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)
        container.addStretch()
        self.setLayout(container)

        # Populate the widgets with values
        self.reset_values()

    #    def onAlphaChanged(self):
    #        if self.alpha_sb.value() == 0:
    #            return
    #        newVal = 1/self.alpha_sb.value()
    #        if newVal != self.t_incubation.value():
    #            self.t_incubation.setValue(newVal)
    #
    #    def onTIncChanged(self):
    #        if self.t_incubation.value() == 0:
    #            return
    #
    #        newVal = 1/self.t_incubation.value()
    #        if newVal != self.alpha_sb.value():
    #            self.alpha_sb.setValue(newVal)
    #
    #    def onGammaChanged(self):
    #        if self.gamma_sb.value() == 0:
    #            return
    #        newVal = 1/self.gamma_sb.value()
    #        new = self.beta_sb.value() / self.gamma_sb.value()
    #        if newVal != self.t_recovery.value():
    #            self.t_recovery.setValue(newVal)
    #            self.R0.setValue(new)
    #
    #    def onBetaChanged(self):
    #        if self.gamma_sb.value() == 0:
    #            return
    #        newVal = self.beta_sb.value() / self.gamma_sb.value()
    #        if newVal != self.gamma_sb.value():
    #            self.R0.setValue(newVal)

 # def onR0Changed(self):
   #     if self.gamma_sb.value() == 0:
   #         return
   #     newVal = self.beta_sb.value()/self.gamma_sb.value()
   #     self.R0.setValue(newVal)

#    def onTrecChanged(self):
#        if self.t_recovery.value() == 0:
#            return
#        newVal = 1 / self.t_recovery.value()
#        if newVal != self.gamma_sb.value():
#            self.gamma_sb.setValue(newVal)
    def ukrainian_values(self):
        self.beta_unvac_unvac_sb.setValue(0.4)
        self.beta_unvac_vac_sb.setValue(0.04)
        self.beta_vac_unvac_sb.setValue(0.2)
        self.beta_vac_vac_sb.setValue(0.02)

        self.mu_sb.setValue(0.0000418105)
        self.l_sb.setValue(0.0000181008)

        self.gamma_unvac_sb.setValue(0.0714)
        self.gamma_vac_sb.setValue(0.125)

        self.sus_unvac_sb.setValue(62.949)
        self.sus_vac_sb.setValue(36.851)

        self.inf_unvac_sb.setValue(1)
        self.inf_vac_sb.setValue(1)

        self.rec_unvac_sb.setValue(0)
        self.rec_vac_sb.setValue(0)

        self.alpha_unvac_sb.setValue(0.17858)
        self.alpha_vac_sb.setValue(0.17858)

        self.theta_vac_sb.setValue(0.0000052474)
        self.theta_unvac_sb.setValue(0.0000052474)
        self.days_sb.setValue(100)

    def reset_values(self):
        self.beta_unvac_unvac_sb.setValue(0.1)
        self.beta_unvac_vac_sb.setValue(0.1)
        self.beta_vac_unvac_sb.setValue(0.1)
        self.beta_vac_vac_sb.setValue(0.1)

        self.mu_sb.setValue(1)
        self.l_sb.setValue(1)

        self.gamma_unvac_sb.setValue(0.1)
        self.gamma_vac_sb.setValue(0.1)

        self.sus_unvac_sb.setValue(120)
        self.sus_vac_sb.setValue(100)

        self.inf_unvac_sb.setValue(20)
        self.inf_vac_sb.setValue(20)

        self.rec_unvac_sb.setValue(0)
        self.rec_vac_sb.setValue(0)

        self.alpha_unvac_sb.setValue(0.1)
        self.alpha_vac_sb.setValue(0.1)

        self.theta_vac_sb.setValue(1)
        self.theta_unvac_sb.setValue(1)
        self.days_sb.setValue(100)
       # self.timedelta_sb.setValue(0.02)

    def legend_change(self):
        self.legend_loc_cb.setEnabled(self.legend_cb.isChecked())
        self.legend_loc_lbl.setEnabled(self.legend_cb.isChecked())
