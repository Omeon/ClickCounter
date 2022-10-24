import PySimpleGUI as sg
from counter import Counter
from psgtray import SystemTray


def refresh_count(window: sg.Window, keys: list):
    for key in keys:
        if Counter.counter[key][1]:
            window[key](Counter.counter[key][1])


def image_gui():
    layout = [[sg.Text('Это ClickCounter.')],
              [sg.Text('Посмотрите, как сильно вы мучаете кнопки своей верной серой подруги.')],
              [sg.Text()],
              [sg.Text('Левая кнопка: '), sg.Text(key='left')],
              [sg.Text('Правая кнопка: '), sg.Text(key='right')],
              [sg.Text('Средняя кнопка: '), sg.Text(key='middle')],
              [sg.Text('Первая боковая кнопка: '), sg.Text(key='x1')],
              [sg.Text('Вторая боковая кнопка: '), sg.Text(key='x2')],
              [sg.Multiline(size=(60, 10), disabled=True, reroute_stdout=False, reroute_cprint=True, key='-OUT-')],
              [sg.Button('Свернуть в трей', key='Hide')]
              ]

    menu_tray = ['',
                 ['Show Window', 'Exit']
                 ]

    window = sg.Window('ClickCounter', layout, finalize=True)

    tray = SystemTray(menu_tray, window=window, icon='mouseclick.ico', tooltip='ClickCounter', single_click_events=False)
    # creating a mouse click monitoring stream
    Counter.counting_clicks()

    # infinity window update cycle
    while True:
        event, values = window.read(timeout=100)

        if event == tray.key:
            event = values[event]  # use the System Tray's event as if was from the window

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Hide':
            window.hide()
            tray.show_icon()
        elif Counter.log:
            sg.cprint(Counter.log)
            Counter.log = ''
            refresh_count(window, ['left', 'right', 'middle', 'x1', 'x2'])
            window.Refresh()
        elif event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

    window.close()
    tray.close()


def main():
    image_gui()


if __name__ == "__main__":
    main()
