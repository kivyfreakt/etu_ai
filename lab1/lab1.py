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


Рассел С, Норвиг П. Искусственный интеллект: современный подход,
2-е изд., М. «Вильямс», 2006. – 1408 с.:
Двунаправленный	135–136

'''

import sys
import argparse
from enum import Enum
from time import process_time

START_TIME = 0  # время запуска программы
TREE = None  # дерево решения todo: RENAME?


class Tree:  # todo: RENAME & FIX?
    ''' Класс представления дерева '''
    __nodes = None  # все узлы

    def __init__(self):
        node = Node(get_initial_state(), None, None, 0, 0)
        self.__nodes = {0: [node]}

    def get_root(self) -> list:
        ''' Получить корень дерева '''
        return list(self.__nodes[0])

    def add_node(self, level: int, new_node):
        ''' Добавить узел в дерево '''
        if level not in self.__nodes:
            self.__nodes[level] = [new_node]
        else:
            self.__nodes[level].append(new_node)

    # todo: ))
    def print_node(self, node):
        ''' Вывод узла на экран '''
        print(node.node_id)

    def print_path(self, node):
        ''' Вывод пути на экран '''
        path = []
        current_node = node

        while current_node.parent_node:
            path.append(current_node)
            current_node = current_node.parent_node

        path.append(current_node)

        for path_node in path:
            self.print_node(path_node)


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
    node_id = None

    nodes_count = 0

    def __init__(self, state, parent, action, cost, depth):
        self.current_state = state
        self.parent_node = parent
        self.previous_action = action
        self.path_cost = cost
        self.depth = depth
        self.node_id = hash(tuple(state))
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
            4, 3, 7 ]


def get_finish_state() -> list:
    ''' Получение конечного состояния игры (Вариант 4) '''
    return [1, 2, 3,
            8, 0, 4,
            7, 6, 5 ]


def check_final(current_state: list) -> bool:
    ''' Проверка, является ли данное состояние конечным '''
    return current_state == get_finish_state()


def print_results(iterations: int, current_node: Node):
    ''' Вывод результатов программы '''
    finish_time = process_time()

    TREE.print_path(current_node)

    # todo: Добавить вывод другой информации, которую нужно по заданию (напр, память)
    print(f"Iteration count: {iterations}")
    print(f"Time: {(finish_time-START_TIME)*1000} ms")
    sys.exit(0)


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

    stack += TREE.get_root()

    steps = 1
    iterations = 0

    while len(stack) != 0:
        current_node = stack.pop()
        visited.add(current_node.node_id)

        iterations += 1
        if check_final(current_node.current_state):
            print_results(iterations, current_node)
            break

        new_states = get_new_states(current_node.current_state)
        neighbors = []
        level = current_node.depth
        for action, new_state in new_states.items():

            new_state_hash = hash(tuple(new_state))
            if new_state_hash in visited_states_hash:
                continue

            new_node = Node(new_state, current_node, action, level + 1, level + 1)
            neighbors.append(new_node)
            visited_states_hash.add(new_state_hash)
            TREE.add_node(level + 1, new_node)

        for next_node in neighbors:
            if next_node.node_id not in visited:
                stack.append(next_node)

        steps += 1
    print("WTF")


def bidirectional_search(start, goal):
    ''' Двунаправленный поиск '''
    found, fringe1, visited1, came_from1 = False, deque([start]), set([start]), {start: None}
    meet, fringe2, visited2, came_from2 = None, deque([goal]), set([goal]), {goal: None}
    iterations = 0
    while not found and (len(fringe1) or len(fringe2)):
        iterations += 1
        if len(fringe1):
            current1 = fringe1.pop()
            if current1.node_id in visited2:
                meet = current1
                found = True
                break
            for action, node_state in get_new_states(current1.current_state).items():
                node = Node(node_state, current1, action, current1.depth + 1, 0)
                if node.node_id not in visited1:
                    visited1.add(node.node_id)
                    fringe1.appendleft(node)
                    came_from1[node] = current1
        if len(fringe2):
            current2 = fringe2.pop()
            if current2.node_id in visited1:
                meet = current2
                found = True
                break
            for action, node_state in get_new_states(current2.current_state).items():
                node = Node(node_state, current2, action, current1.depth + 1, 0)
                if node.node_id not in visited2:
                    visited2.add(node.node_id)
                    fringe2.appendleft(node)
                    came_from2[node] = current2
    if found:
        finish_time = process_time()
        print(f"Iteration count: {iterations}")
        print(f"Time: {(finish_time-START_TIME)*1000} ms")
        return came_from1, came_from2, meet
    
    print(f"No path between {start} and {goal}")
    return None, None, None



if __name__ == '__main__':
    # начать отсчет времени
    START_TIME = process_time()

    # парсинг входных значений
    parser = argparse.ArgumentParser(description = "Solve 8-puzzle game")
    parser.add_argument('algorithm', type = str, help = 'name of the algorithm used (list: dfs, bds)')
    parser.add_argument("-m", "--manual", action='store_true', help = "step-by-step mode of operation of the program")
    
    args = parser.parse_args()

    MANUAL_FLAG = args.manual
    ALGORITHM_FLAG = args.algorithm != "dfs"

    # создать ...
    TREE = Tree()

    # запуск
    if ALGORITHM_FLAG == 0:
        dfs()
    elif ALGORITHM_FLAG == 1:
        start = Node(get_initial_state(), None, None, 0, 0)
        end = Node(get_finish_state(), None, None, 0, 0)
        came_from1, came_from2, meet = bidirectional_search(start, end)