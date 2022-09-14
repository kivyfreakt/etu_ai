# -*- coding: utf-8 -*-

''' 
в глубину, двунаправленный

НАЧАЛО
6	0	8
5	2	1
4	3	7

КОНЕЦ
1	2	3
8	0	4
7	6	5


Рассел С, Норвиг П. Искусственный интеллект: современный подход, 2-е изд., М. «Вильямс», 2006. – 1408 с.:
Двунаправленный	135–136

'''

import os
import sys
from enum import Enum
from time import process_time

start_time = 0  # время запуска программы
tree = None  # дерево решения todo: RENAME?


class Tree:  # todo: RENAME & FIX?
    ''' Класс представления дерева '''
    __nodes = None  # все узлы

    def __init__(self):
        node = Node(get_initial_state(), None, None, 0, 0)
        self.__nodes = {0: [node]}

    def get_root(self) -> list:
        return list(self.__nodes[0])

    def add_node(self, level, new_node):
        if level not in self.__nodes:
            self.__nodes[level] = [new_node]
        else:
            self.__nodes[level].append(new_node)

    # todo: ))
    def print_node(self, node):
        print(node.id)

    def print_path(self, node):
        path = []
        current_node = node

        while (current_node.parent_node != None):
            path.append(current_node)
            current_node = current_node.parent_node

        path.append(current_node)

        for n in path:
            self.print_node(n)


class Action(Enum):
    ''' Перечисление действий над полем '''
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Node:
    ''' Класс представления узла '''
    current_state = None  # Состояние в пространстве состояний, которому соответствует данный узел
    parent_node = None  # Указатель на родительский узел
    # Действие, которое было применено к родительскому узлу для формирования данного узла
    previous_action = None
    # Стоимость пути от начального состояния до данного узла g(n)
    path_cost = None
    depth = None  # Количество этапов пути от начального состояния (глубина)
    id = None

    nodes_count = 0

    def __init__(self, state, parent, action, cost, depth):
        self.current_state = state
        self.parent_node = parent
        self.previous_action = action
        self.path_cost = cost
        self.depth = depth
        self.id = Node.nodes_count
        Node.nodes_count += 1

    # А НУЖЕН ЛИ ОН БУДЕТ?
    @classmethod
    def get_nodes_count(cls) -> int:
        ''' Статический метод класса, возвращающий количество узлов '''
        return cls.nodes_count + 1


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


def check_final(current_state: list) -> bool:
    ''' Проверка, является ли данное состояние конечным '''
    return current_state == get_finish_state()


def print_results(iterations: int, current_node: Node):  # todo: RENAME?
    ''' Вывод результатов программы '''
    finish_time = process_time()

    tree.print_path(current_node)

    # todo: Добавить вывод другой информации, которую нужно по заданию (напр, память)
    print(f"Iteration count: {iterations}")
    print(f"Time: {(finish_time-start_time)*1000} ms")
    exit()


# todo: ГОВНОКОД, ПЕРЕПИСАТЬ
def get_new_states(current_state: list) -> dict:
    ''' Получение новых состояний поля '''
    new_states = {}
    pos = current_state.index(0)

    # up
    if pos not in (0, 1, 2):
        state = list(current_state)
        state[pos], state[pos-3] = state[pos-3], state[pos]
        new_states[Action.UP] = state

    # down
    if pos not in (6, 7, 8):
        state = list(current_state)
        state[pos], state[pos+3] = state[pos+3], state[pos]
        new_states[Action.DOWN] = state

    # right
    if pos not in (2, 5, 8):
        state = list(current_state)
        state[pos], state[pos+1] = state[pos+1], state[pos]
        new_states[Action.RIGHT] = state

    # left
    if pos not in (0, 3, 6):
        state = list(current_state)
        state[pos], state[pos-1] = state[pos-1], state[pos]
        new_states[Action.LEFT] = state

    return new_states


def dfs():
    ''' Поиск в глубину '''
    visited_states_hash = set()
    # Для отслеживания, что состояния поля уже где-то были, иначе - бесконечный цикл
    visited = set()
    stack = []

    stack += tree.get_root()

    steps = 1
    iterations = 0

    while (len(stack) != 0):
        current_node = stack.pop()
        visited.add(current_node.id)

        iterations += 1
        if check_final(current_node.current_state):
            print_results(iterations, current_node)

        new_states = get_new_states(current_node.current_state)

        print(new_states)

        neighbors = []
        level = current_node.depth
        for action, new_state in new_states.items():

            new_state_hash = hash(tuple(new_state))
            if (new_state_hash in visited_states_hash):
                continue

            # todo: КАКАЯ СТОИМОСТЬ НАДО ВПИСАТЬ
            new_node = Node(new_state, current_node, action, level + 1, 0)
            neighbors.append(new_node)
            visited_states_hash.add(new_state_hash)
            tree.add_node(level + 1, new_node)

        for next_node in neighbors:
            if (next_node.id not in visited):
                stack.append(next_node)

        steps += 1
    print("WTF")


if __name__ == '__main__':
    # начать отсчет времени
    start_time = process_time()

    # парсинг входных значений
    # todo: ГОВНОКОД ПЕРЕПИСАТЬ
    algorithm_flag = None
    if (len(sys.argv) == 2):
        if (sys.argv[1] == '--dfs'):
            algorithm_flag = 0
        elif (sys.argv[1] == '--bds'):
            algorithm_flag = 1
        elif (sys.argv[1] == '-h'):
            print(f"{sys.argv[0]} --dfs - Depth First Search algorithm")
            print(f"{sys.argv[0]} --bds - BiDirectional Search algorithm")
        else:
            print(
                f"Error! Invalid input parameter. \nPrint {sys.argv[0]} -h  \nExit")
    else:
        print(
            f"Error! Incorrect number of parameters. \nPrint {sys.argv[0]} -h \nExit")

    # создать ...
    tree = Tree()

    # запуск
    if algorithm_flag == 0:
        dfs()
    elif algorithm_flag == 1:
        bidirectional_search()
