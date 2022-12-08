import sys
import time
from CountDown_GUI import Ui_Form
from PyQt5 import QtGui, QtWidgets

# class Main(QtGui.QGuiApplication):
#     def __init__(self):
#         super(Main, self).__init__()

#         # build ui
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)

         
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    Countwindow = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Countwindow)
    Countwindow.show()

    for i in range(10):
        ui.lcdNumber.display(i)
        Countwindow.repaint()
        time.sleep(0.5)
    Countwindow.close()

    

    #sys.exit(app.exec_())
    