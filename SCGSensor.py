"""
Main class for logging accelerations for a heart rate monitor.

todo Add link to logging folder.
"""

import PySimpleGUI as sg
import time
import IMU
import Layout
import Menu
import styling as st
import os

from pathlib import Path
from datetime import datetime


class SCGSensor:
    def __init__(self):
        # Initial directory creation.
        self.loggingPath = None
        self.createInitialDirectories()
        # Menu object.
        self.menu = Menu.Menu()
        # Layout object.
        self.layout = Layout.Layout(self.menu)

        # IMU object instantiated with default values.
        self.imu = IMU.IMU()
        self.availableComPorts = IMU.availableComPorts()

        # IMU connect window
        self.windowImuConnect = None

        self.windowMain = sg.Window('Heart Rate Monitor', self.layout.getMainLayout(), finalize=True,
                                    use_default_focus=True)

        self.run()

    def run(self):
        """
        Main loop/thread for displaying the GUI and reacting to events, in standard PySimpleGUI fashion.
        """
        while True:

            event, values = self.windowMain.read(timeout=20)

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
                self.windowMain['-TXT-IMU-ACC-'].update(f'{self.imu.getNorm():.2f}')
            if self.imu.enableLogging:
                self.windowMain['-TXT-LINES-LOGGED-'].update(f'{self.imu.linesLogged}')

    def toggleLogging(self):
        """
        Toggle the logging state of the IMU object.
        """
        if self.imu.isConnected:
            if not self.imu.enableLogging:
                logFileName = self.windowMain['-INP-FILE-NAME-'].get()
                if logFileName == '':
                    logFileName = str(int(time.time_ns()))
                    dt
                    self.windowMain['-INP-FILE-NAME-'].update(logFileName)

                if self.doesLogFileExist(logFileName):
                    print(f'{logFileName} exits, appending time.')
                    logFileName = f'{logFileName}_{int(time.time() * 1000)}'

                self.imu.startLogging(Path(self.loggingPath, logFileName + '.txt'))
            else:
                self.imu.stopLogging()
                self.windowMain['-INP-FILE-NAME-'].update('')
                self.windowMain['-TXT-LINES-LOGGED-'].update(self.imu.linesLogged)

            self.windowMain['-BTN-TOGGLE-LOG-'].update(
                text='Stop Logging' if self.imu.enableLogging else 'Start Logging',
                button_color=st.COL_BTN_ACTIVE if self.imu.enableLogging else sg.DEFAULT_BUTTON_COLOR)
        else:
            print('IMU is not connected.')

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
