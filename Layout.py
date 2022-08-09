"""
Primary layout class for the SCG application.
"""
import PySimpleGUI as sg
import styling as st
import constants as c


class Layout:
    def __init__(self, menu):
        self.menu = menu

    def getMainLayout(self) -> list:
        """
        Create the layout for the main window.
        """
        logStartColumn = [
            [sg.Text(text='Log Start', font=st.FONT_DESCR)],
            [sg.Text(k='-TXT-LOG-START-', text='--:--:--', font=st.FONT_DESCR, size=(12, 1),
                     justification='center')]
        ]

        logEndColumn = [
            [sg.Text(text='Log End', font=st.FONT_DESCR)],
            [sg.Text(k='-TXT-LOG-END-', text='--:--:--', font=st.FONT_DESCR, size=(12, 1), justification='center')]
        ]

        logElapsedColumn = [
            [sg.Text(text='Elapsed Time', font=st.FONT_DESCR)],
            [sg.Text(k='-TXT-LOG-ELAPSED-', text='--:--:--', font=st.FONT_DESCR, size=(12, 1),
                     justification='center')]
        ]

        logLineColumn = [
            [sg.Text(text='Lines to Log', font=st.FONT_DESCR)],
            [sg.Text(k='-TXT-LINES-LOGGED-', text='0', font=st.FONT_DESCR, size=(12, 1), justification='center')]
        ]

        layout = [
            [sg.Col(element_justification='left', layout=[
                [sg.Menu(k='-MENU-', menu_definition=self.menu.getMenu())],
                [sg.Canvas(k='-CANVAS-PLOT-', pad=((0, 0), (20, 0))),
                 sg.Col(vertical_alignment='c', element_justification='c', expand_y=True, pad=((0, 0), (20, 0)),
                        layout=[
                            [sg.Button(k='-BTN-PLOT-REFRESH-', button_text='Reset Plot', font=st.FONT_BTN,
                                       border_width=3)],
                            [sg.Slider(k='-SLD-PLOT-POINTS-', default_value=1000, range=(10, 10000), orientation='v',
                                       size=(19, 15), enable_events=True, disable_number_display=True)],
                            [sg.Text(k='-TXT-PLOT-POINTS-', text='Points: 1000', size=(11, 1), font=st.FONT_DESCR)]
                        ])],
                [sg.Col(element_justification='c', expand_x=True, layout=[
                    [sg.Checkbox(k='-BOX-ACC-X-', text='X-Acceleration', default=True, font=st.FONT_DESCR,
                                 pad=(10, 0)),
                     sg.Checkbox(k='-BOX-ACC-Y-', text='Y-Acceleration', default=True, font=st.FONT_DESCR,
                                 pad=(10, 0)),
                     sg.Checkbox(k='-BOX-ACC-Z-', text='Z-Acceleration', default=True, font=st.FONT_DESCR,
                                 pad=(10, 0)),
                     sg.Checkbox(k='-BOX-ACC-NORM-', text='Acceleration Norm', default=True, font=st.FONT_DESCR,
                                 pad=(10, 0))]
                ])]])],
            [sg.HSeparator()],
            [sg.Col(element_justification='c', expand_x=True, layout=[
                [sg.Text(text='Enter log file name: ', font=st.FONT_DESCR, pad=((5, 0), (10, 5))),
                 sg.Input(k='-INP-FILE-NAME-', size=(50, 1), font=st.FONT_DESCR, pad=((5, 0), (10, 5)))],
                [sg.Button(k='-BTN-TOGGLE-LOG-', button_text='Start Logging', font=st.FONT_BTN, border_width=3,
                           pad=((5, 0), (10, 5)), disabled=True),
                 sg.Column(logStartColumn, element_justification='center', pad=(0, 0)),
                 sg.Column(logEndColumn, element_justification='center', pad=(0, 0)),
                 sg.Column(logElapsedColumn, element_justification='center', pad=(0, 0)),
                 sg.Column(logLineColumn, element_justification='center', pad=(0, 0)),
                 sg.Column(vertical_alignment='c', element_justification='c', layout=[
                     [sg.Text(k='-TXT-LOG-DIR-', text='Open Logging Folder', font=st.FONT_DESCR + ' underline',
                              text_color='blue', enable_events=True)]
                 ])
                 ]
            ])]
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
