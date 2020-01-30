from PyQt5 import QtWidgets
import sys
from functions import *
from methods import *
import numpy as np
import qdarkstyle


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Optimisation Algorithm Demonstration")

        self.init_UI()

    def init_UI(self):
        self.setFixedSize(1000, 700)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.vbox_left = QtWidgets.QVBoxLayout()
        self.vbox_right = QtWidgets.QVBoxLayout()
        self.function_features = QtWidgets.QHBoxLayout()
        self.optim_features = QtWidgets.QHBoxLayout()

        self.t_label = QtWidgets.QLabel("Choose a function:")
        self.m_label = QtWidgets.QLabel("Choose optimisation method:")
        self.c_label = QtWidgets.QLabel("Optimisation process:")
        self.tol_label = QtWidgets.QLabel("Set method tolerance:")
        self.stp_label = QtWidgets.QLabel("Choose starting point (comma separated):")

        self.changing_panel = QtWidgets.QVBoxLayout()
        self.d_label = QtWidgets.QLabel("Choose step length (Default: 1):")
        self.int_label = QtWidgets.QLabel("Choose helper function interval (Default: [-5,5]):")
        self.d_field = QtWidgets.QLineEdit()
        self.int_field = QtWidgets.QLineEdit()
        self.changing_panel.addWidget(self.d_label)
        self.changing_panel.addWidget(self.d_field)
        self.changing_panel.addWidget(self.int_label)
        self.changing_panel.addWidget(self.int_field)

        self.start_btn = QtWidgets.QPushButton("START")
        self.plot_btn = QtWidgets.QPushButton("PLOT")

        self.info1 = QtWidgets.QTextEdit()
        self.info1.setReadOnly(True)
        self.tol = QtWidgets.QLineEdit()
        self.stp = QtWidgets.QLineEdit()

        self.info2 = QtWidgets.QTextEdit()
        self.info2.setReadOnly(True)

        self.result_console = QtWidgets.QTextEdit()
        self.result_console.setReadOnly(True)

        self.screen_layout = QtWidgets.QHBoxLayout()

        self.fun_box = QtWidgets.QComboBox()
        for name in get_function_names():
            self.fun_box.addItem(name)

        self.get_fun_info()
        self.fun_box.currentIndexChanged.connect(self.get_fun_info)

        self.met_box = QtWidgets.QComboBox()
        for name in get_method_names():
            self.met_box.addItem(name)

        self.get_met_info()
        self.met_box.currentIndexChanged.connect(self.get_met_info)

        self.function_features.addWidget(self.fun_box)
        self.function_features.addWidget(self.plot_btn)
        self.optim_features.addWidget(self.met_box)
        self.optim_features.addWidget(self.start_btn)

        self.vbox_left.addWidget(self.t_label)
        self.vbox_left.addLayout(self.function_features)
        self.vbox_left.addWidget(self.info1)
        self.vbox_left.addSpacing(20)
        self.vbox_left.addWidget(self.m_label)
        self.vbox_left.addLayout(self.optim_features)
        self.vbox_left.addWidget(self.info2)
        self.vbox_left.addWidget(self.tol_label)
        self.vbox_left.addWidget(self.tol)
        self.vbox_left.addWidget(self.stp_label)
        self.vbox_left.addWidget(self.stp)
        self.vbox_left.addLayout(self.changing_panel)

        self.vbox_right.addWidget(self.c_label)
        self.vbox_right.addWidget(self.result_console)

        self.screen_layout.addLayout(self.vbox_left)
        self.screen_layout.addLayout(self.vbox_right)
        self.setLayout(self.screen_layout)

        self.plot_btn.clicked.connect(self.plot_function)
        self.start_btn.clicked.connect(self.start_optim_process)

        self.show()

    def get_fun_info(self):
        self.info1.setText(function_info[self.fun_box.currentText()])

    def get_met_info(self):
        self.info2.setText(methods_info[self.met_box.currentText()])

        if self.met_box.currentText() == "Hooke-Jeeves":
            self.int_field.setReadOnly(True)
            self.d_field.setReadOnly(False)
        else:
            self.d_field.setReadOnly(True)
            self.int_field.setReadOnly(False)

    def start_optim_process(self):
        try:
            tolerance = float(self.tol.text().strip())
            start_p = self.stp.text().strip().split(",")

            for num in range(len(start_p)):
                start_p[num] = float(start_p[num])

            arr = np.array(start_p)

        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid params. Try again.")
            return

        if self.fun_box.currentText() == "Three Hump Camel" and len(start_p) > 2:
            QtWidgets.QMessageBox.critical(self, "Error", "Unlike other 2 functions, THC can only be optimised in 3D.")
            return

        self.result_console.setText("")
        self.result_console.append(
            "Starting optimisation process with {} algorithm:\n".format(self.met_box.currentText()))

        if self.met_box.currentText() == "Powell":
            if self.int_field.text().strip() == "":
                gr_int = [-5, 5]
            else:
                gr_int = self.int_field.text().strip().split(",")
                try:
                    for num in range(2):
                        gr_int[num] = float(gr_int[num])
                except ValueError:
                    QtWidgets.QMessageBox.critical(self, "Error", "Invalid params. Try again.")
                    return
            x = methods[self.met_box.currentText()](functions[self.fun_box.currentText()], golden_ratio, arr, tolerance,
                                                    True, self, gr_int[0], gr_int[1])
        else:
            if self.d_field.text().strip() == "":
                step = 1
            else:
                try:
                    step = float(self.d_field.text().strip())
                except ValueError:
                    QtWidgets.QMessageBox.critical(self, "Error", "Invalid params. Try again.")
                    return
            x = methods[self.met_box.currentText()](functions[self.fun_box.currentText()], arr, step, tolerance, True,
                                                    self)

        result = "Final solution achieved in {} iterations.\nX: {}\nY= {}".format(x[2], x[0], x[1])
        self.result_console.append(result)

    def plot_function(self):
        plot_function_3D(functions[self.fun_box.currentText()], -2.048, 2.048, "viridis", self.fun_box.currentText())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
