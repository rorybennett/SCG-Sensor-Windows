"""
Main class for logging accelerations for a heart rate monitor.

todo Add link to logging folder.
"""

import PySimpleGUI as sg
import time

import numpy as np

import IMU
import Layout
import Menu
import styling as st
import os
from pathlib import Path
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SCGSensor:
    def __init__(self):
        # Initial directory creation.
        self.loggingPath = None
        self.createInitialDirectories()
        # Menu object.
        self.menu = Menu.Menu()
        # Layout object.
        self.layout = Layout.Layout(self.menu)
        # Plotting variables.
        self.bg = None
        self.fig_agg = None
        self.ax = None
        self.xLine = None
        self.yLine = None
        self.zLine = None
        self.normLine = None

        # IMU object instantiated with default values.
        self.imu = IMU.IMU()
        self.availableComPorts = IMU.availableComPorts()

        # IMU connect window
        self.windowImuConnect = None

        self.windowMain = sg.Window('Heart Rate Monitor', self.layout.getMainLayout(), finalize=True,
                                    use_default_focus=True)

        self.createPlot()

        self.run()

    def run(self):
        """
        Main loop/thread for displaying the GUI and reacting to events, in standard PySimpleGUI fashion.
        """
        while True:

            event, values = self.windowMain.read(timeout=50)

            if event in [sg.WIN_CLOSED, 'None']:
                # On window close clicked.
                self.close()
                break

            if event.endswith('::-MENU-IMU-CONNECT-'):
                self.showImuConnectWindow()
            elif event.endswith('::-MENU-IMU-DISCONNECT-'):
                self.imu.disconnect()
                self.updateMenus()
            elif event.endswith('::-MENU-IMU-RATE-'):
                self.imu.setReturnRate(float(event.split('Hz')[0]))
            elif event.endswith('::-MENU-IMU-CALIBRATE-'):
                self.imu.calibrateAcceleration()

            if event == '-BTN-TOGGLE-LOG-':
                self.toggleLogging()

            if self.imu.isConnected:
                self.updatePlot()
            if self.imu.enableLogging:
                self.windowMain['-TXT-LINES-LOGGED-'].update(f'{len(self.imu.logData)}')

    def toggleLogging(self):
        """
        Toggle the logging state of the IMU object.
        """
        if self.imu.isConnected:
            if not self.imu.enableLogging:
                logFileName = self.windowMain['-INP-FILE-NAME-'].get()
                if logFileName == '':
                    dt = datetime.fromtimestamp(time.time_ns() / 1000000000)
                    logFileName = dt.strftime('%d %m %Y %H-%M-%S')
                    self.windowMain['-INP-FILE-NAME-'].update(logFileName)

                if self.doesLogFileExist(logFileName):
                    print(f'{logFileName} exits, appending time.')
                    logFileName = f'{logFileName}_{int(time.time() * 1000)}'

                self.imu.startLogging(Path(self.loggingPath, logFileName + '.txt'))
            else:
                self.imu.stopLogging()
                self.windowMain['-INP-FILE-NAME-'].update('')
                self.windowMain['-TXT-LINES-LOGGED-'].update(len(self.imu.logData))

            self.windowMain['-BTN-TOGGLE-LOG-'].update(
                text='Stop Logging' if self.imu.enableLogging else 'Start Logging',
                button_color=st.COL_BTN_ACTIVE if self.imu.enableLogging else sg.DEFAULT_BUTTON_COLOR)
        else:
            print('IMU is not connected.')

    def updatePlot(self):
        """
        Update plot.
        """
        if len(self.imu.plotData) > 0:
            data = np.array(self.imu.plotData)

            data[:, 0] = (data[:, 0] - data[0, 0]) / 1000000000

            if self.windowMain['-BOX-ACC-X-'].get():
                self.xLine[0].remove()
                self.xLine = self.ax.plot(data[:, 0], data[:, 1], c='blue')  # X
            else:
                self.xLine[0].remove()
                self.xLine = self.ax.plot([], [], c='blue')

            if self.windowMain['-BOX-ACC-Y-'].get():
                self.yLine[0].remove()
                self.yLine = self.ax.plot(data[:, 0], data[:, 2], c='red')  # Y
            else:
                self.yLine[0].remove()
                self.yLine = self.ax.plot([], [], c='red')

            if self.windowMain['-BOX-ACC-Z-'].get():
                self.zLine[0].remove()
                self.zLine = self.ax.plot(data[:, 0], data[:, 3], c='green')  # Z
            else:
                self.zLine[0].remove()
                self.zLine = self.ax.plot([], [], c='green')

            if self.windowMain['-BOX-ACC-NORM-'].get():
                self.normLine[0].remove()
                self.normLine = self.ax.plot(data[:, 0], data[:, 4], c='black')  # Norm
            else:
                self.normLine[0].remove()
                self.normLine = self.ax.plot([], [], c='black')

            self.ax.relim()
            self.ax.legend([self.xLine[0], self.yLine[0], self.zLine[0], self.normLine[0]],
                           ['X Acceleration', 'Y Acceleration', 'Z Acceleration', 'Acceleration Norm'])

            self.fig_agg.draw()
            self.fig_agg.flush_events()

    def createPlot(self):
        """
        Instantiate the initial plotting variables.
        """
        fig = Figure(figsize=(10, 5), dpi=100)
        self.ax = fig.add_subplot(111)
        fig.patch.set_facecolor(sg.DEFAULT_BACKGROUND_COLOR)

        self.ax.set_title('IMU Acceleration')
        self.ax.set_xlabel('Time [s]')
        self.ax.set_ylabel('Acceleration [m/s^2]')
        self.ax.grid()

        self.xLine = self.ax.plot([], [], color='blue')
        self.yLine = self.ax.plot([], [], color='red')
        self.zLine = self.ax.plot([], [], color='green')
        self.normLine = self.ax.plot([], [], color='black')

        self.fig_agg = self.drawFigure(fig, self.windowMain['-CANVAS-PLOT-'].TKCanvas)

    def drawFigure(self, figure, canvas):
        """
        Helper function for integrating matplotlib plots with PySimpleGui. Used to draw the initial canvas.
        """
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def doesLogFileExist(self, fileName):
        """
        Check if a log file with the given name already exists.
        """
        logFiles = os.listdir(self.loggingPath)

        if fileName + '.txt' in logFiles:
            return True
        return False

    def refreshComPorts(self):
        """
        Refresh the available COM ports displayed in windowImuConnect. The variable list of available COM ports is
        updated as well as the drop-down menu/list.
        """
        self.availableComPorts = IMU.availableComPorts()
        # Set elements
        self.windowImuConnect['-COMBO-COM-PORT-'].update(values=self.availableComPorts)

    def showImuConnectWindow(self):
        """
        Show a window for the user to connect to an IMU based on COM port and baud rate selection. The user
        can refresh available COM ports, select a COM port, and select a baud rate from this window. When the CONNECT
        button is clicked an attempt is made to open the requested COM port at the specified baud rate.

        When the COM port and baud rate are changed from the combo boxes, the self.imu variable has its properties
        modified immediately (self.imu.comPort, self.imu.baudrate). If CONNECT is clicked while the COM port box is
        empty (post refresh), the currently stored self.imu.comPort will be used.

        The window will close if there is a successful connection to the COM port. There is no test to see if the
        port belongs to an IMU or not, just if the connection is made. The user will need to see if acceleration values
        are being updated in the main GUI.
        """
        self.windowImuConnect = sg.Window('Connect to IMU',
                                          self.layout.getImuWindowLayout(self.availableComPorts, self.imu.comPort,
                                                                         self.imu.baudRate),
                                          element_justification='center', modal=True)

        while True:
            event, values = self.windowImuConnect.read()

            if event in [sg.WIN_CLOSED, 'None']:
                # On window close.
                break
            elif event == '-BTN-COM-REFRESH-':
                # On refresh available COM ports clicked.
                self.refreshComPorts()
            elif event == '-COMBO-COM-PORT-':
                # On COM port changed.
                self.imu.comPort = values['-COMBO-COM-PORT-']
            elif event == '-COMBO-BAUD-RATE-':
                # On baud rate changed.
                self.imu.baudRate = int(values['-COMBO-BAUD-RATE-'])
            elif event == '-BTN-IMU-CONNECT-':
                # On connect button clicked.
                self.imu.connect()
                if self.imu.isConnected:
                    break

        self.windowMain['-BTN-TOGGLE-LOG-'].update(disabled=False if self.imu.isConnected else True)

        self.updateMenus()
        self.windowImuConnect.close()

    def updateMenus(self):
        """
        Update the main window's menu based on the current states of the self.imu object.
        """
        # Set elements.
        self.windowMain['-MENU-'].update(
            menu_definition=self.menu.getMenu(self.imu.isConnected))

    def close(self):
        """
        Delete references to IMU object for garbage collection.
        """
        if self.imu.isConnected:
            self.imu.disconnect()
            del self.imu

    def createInitialDirectories(self):
        """
        Create the logging directory where the log tests are stored.
        :return:
        """
        currentWorkingDirectory = Path.cwd()

        self.loggingPath = Path(currentWorkingDirectory, 'logging')
        self.loggingPath.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    SCGSensor()
