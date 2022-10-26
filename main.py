import PySimpleGUI as sg
from counter import Counter
from psgtray import SystemTray
import os
import sys


def image_gui():
    sg.theme('dark grey 13')

    count_col = [[sg.Text('Левая кнопка: '), sg.Text(key='left')],
                 [sg.Text('Правая кнопка: '), sg.Text(key='right')],
                 [sg.Text('Средняя кнопка: '), sg.Text(key='middle')],
                 [sg.Text('Первая боковая кнопка: '), sg.Text(key='x1')],
                 [sg.Text('Вторая боковая кнопка: '), sg.Text(key='x2')]]
    gif_col = [[sg.Image(resource_path('img/monkey_mouse.gif'), key='gif')]]

    layout = [[sg.Text('Это ClickCounter.', font=('Monospace', 20))],
              [sg.Text('Посмотри, как сильно ты мучаешь кнопки своей', font=('Monospace', 12))],
              [sg.Text('верной серой подруги.', font=('Monospace', 12))],
              [sg.Column(count_col), sg.Column(gif_col, justification='c')],
              [sg.Multiline(size=(55, 6), disabled=True, reroute_stdout=False, reroute_cprint=True, key='-OUT-')],
              [sg.Push(), sg.Button('Свернуть в трей', key='Hide')]
              ]

    menu_tray = ['',
                 ['Show window', 'Exit']
                 ]

    window = sg.Window('ClickCounter', layout, finalize=True, icon=resource_path('img/mouseclick.ico'))

    tray = SystemTray(menu_tray, window=window, icon=resource_path('img/mouseclick.ico'),
                      tooltip='ClickCounter', single_click_events=False)

    # creating a mouse click monitoring stream
    Counter.counting_clicks()

    # infinity window update cycle
    while True:
        event, values = window.read(timeout=50)

        # use the System Tray's event as if was from the window
        if event == tray.key:
            event = values[event]

        # work with the window and updating it
        if event == sg.WIN_CLOSED:
            break
        elif Counter.log:
            sg.cprint(Counter.log)
            Counter.log = ''
            refresh_count(window, ['left', 'right', 'middle', 'x1', 'x2'])
            window.Refresh()

        # work with the tray
        if event == 'Hide':
            window.hide()
            tray.show_icon()
        elif event in ('Show window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event == 'Exit':
            break

        window['gif'].update_animation(resource_path('img/monkey_mouse.gif'), time_between_frames=50)

    window.close()
    tray.close()


def refresh_count(window: sg.Window, keys: list):
    for key in keys:
        if Counter.counter[key][1]:
            window[key](Counter.counter[key][1])


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def main():
    image_gui()


if __name__ == "__main__":
    main()
