import PySimpleGUI as sg
import styling as st


class Layout:
    def __init__(self, menu):
        self.menu = menu

    def getMainLayout(self) -> list:
        """
        Create the layout for the main window.
        """
        layout = [
            [sg.Menu(k='-MENU-', menu_definition=self.menu.getMenu())],
            [sg.Text(text='Enter log file name: ', font=st.FONT_DESCR),
             sg.Input(k='-INP-FILE-NAME-', size=(20, 1))],
            [sg.Col(element_justification='c', expand_x=True, layout=[
                [sg.Button(k='-BTN-TOGGLE-LOG-', button_text='Start Logging', font=st.FONT_BTN, border_width=3,
                           pad=((0, 0), (5, 5)), disabled=True)]])],
            [sg.Text(text='Lines logged: ', font=st.FONT_DESCR),
             sg.Text(k='-TXT-LINES-LOGGED-', font=st.FONT_DESCR)]
        ]

        return layout

    def getImuWindowLayout(self, availableComPorts, comPort, baudRate) -> list:
        """
        Create the layout for the IMU connection window.

        Args:
            availableComPorts (list): A list of available COM ports.
            comPort (string): Default COM port to show in COMBO box.
            baudRate (int): Default baud rate to show in COMBO box.

        Returns:
            layout (list): Layout in the form of a list.
        """
        layout = [
            [sg.Button(k='-BTN-COM-REFRESH-', button_text='', image_source='icons/refresh_icon.png',
                       image_subsample=4, border_width=3, pad=((0, 10), (20, 0))),
             sg.Combo(k='-COMBO-COM-PORT-', values=availableComPorts, size=7, font=st.FONT_COMBO,
                      enable_events=True, readonly=True, default_value=comPort, pad=((0, 0), (20, 0))),
             sg.Text('Baud Rate:', justification='right', font=st.FONT_DESCR, pad=((20, 0), (20, 0))),
             sg.Combo(k='-COMBO-BAUD-RATE-', values=c.COMMON_BAUD_RATES, size=7, font=st.FONT_COMBO,
                      enable_events=True, readonly=True, default_value=baudRate, pad=((0, 0), (20, 0)))],
            [sg.HSeparator(pad=((10, 10), (20, 20)))],
            [sg.Button(k='-BTN-IMU-CONNECT-', button_text='Connect', border_width=3, font=st.FONT_BTN)]
        ]

        return layout
