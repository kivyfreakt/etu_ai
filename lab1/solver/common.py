'''
    Общие функции и переменные модуля
'''

TREE = None  # дерево решения


def print_state(state: list):
    ''' Вывод состояния на экран '''
    for i, num in enumerate(state):
        print(num, end=" ")
        if (i + 1) % 3 == 0:
            print("")

    print("---")


def get_initial_state() -> list:
    ''' Получение начального состояния игры (Вариант 4) '''
    return [6, 0, 8,
            5, 2, 1,
            4, 3, 7, ]


def get_finish_state() -> list:
    ''' Получение конечного состояния игры (Вариант 4) '''
    return [1, 2, 3,
            8, 0, 4,
            7, 6, 5, ]
