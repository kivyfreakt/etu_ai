'''
    Общие функции и переменные модуля
'''
MANUAL = None
TREE = None  # дерево решения
TREE2 = None
SIZE = 3
INITIAL_STATE = [6, 0, 8,
            5, 2, 1,
            4, 3, 7, ]
FINISH_STATE = [1, 2, 3,
            8, 0, 4,
            7, 6, 5, ]

def print_state(state: list):
    ''' Вывод состояния на экран '''
    for i, num in enumerate(state):
        print(num, end=" ")
        if (i + 1) % 3 == 0:
            print("")

    print("---")


def get_initial_state() -> list:
    ''' Получение начального состояния игры (Вариант 4) '''
    return INITIAL_STATE


def get_finish_state() -> list:
    ''' Получение конечного состояния игры (Вариант 4) '''
    return FINISH_STATE
