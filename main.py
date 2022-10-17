import PySimpleGUI as sg
from counter import Counter
from psgtray import SystemTray


def image_gui():
    layout = [[sg.Text('Это ClickCounter. Посмотрите, как сильно вы мучаете кнопки своей верной серой подруги.')],
              [sg.T('', key="log")],
              [sg.Text('Левая кнопка: '), sg.Text(key='left')],
              [sg.Text('Правая кнопка: '), sg.Text(key='right')],
              [sg.Text('Средняя кнопка: '), sg.Text(key='middle')],
              [sg.Text('Первая боковая: '), sg.Text(key='x1')],
              [sg.Text('Вторая боковая кнопка: '), sg.Text(key='x2')],
              [sg.Multiline(size=(60, 10), disabled=True, reroute_stdout=False, reroute_cprint=True, key='-OUT-')]
              ]

    window = sg.Window('ClickCounter', layout, finalize=True)

    # creating a mouse click monitoring stream
    Counter.counting_clicks()

    # infinity window update cycle
    while True:
        event, values = window.Read(timeout=100)
        if Counter.log:
            sg.cprint(Counter.log)
            Counter.log = ''
            window['left'](Counter.counter['left'][1])
            window['right'](Counter.counter['right'][1])
            window['middle'](Counter.counter['middle'][1])
            window['x1'](Counter.counter['x1'][1])
            window['x2'](Counter.counter['x2'][1])
            window['log']('была нажата кнопка')
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        window.Refresh()


def main():
    image_gui()


if __name__ == "__main__":
    main()
