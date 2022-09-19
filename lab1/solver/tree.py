'''
    Структуры данных
'''

from enum import Enum

from solver import common

class Tree:
    ''' Класс представления дерева '''
    __nodes = None  # все узлы

    def __init__(self):
        node = Node(common.get_initial_state(), None, None, 0, 0)
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

    def get_path(self, node) -> list:
        ''' Получение пути'''
        path = []
        current_node = node

        while current_node.parent_node:
            path.append(current_node.current_state)
            current_node = current_node.parent_node

        path.append(current_node.current_state)

        return path


# вообще может нахуй убрать, это только мешает, при этом нигде не используется
# но по заданию это формально надо)
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
    node_id = None  # уникальный идентификатор узла

    nodes_count = 0

    def __init__(self, state, parent, action, cost, depth):
        self.current_state = state
        self.parent_node = parent
        self.previous_action = action
        self.path_cost = cost
        self.depth = depth
        self.node_id = hash(tuple(state))
        Node.nodes_count += 1

    @classmethod
    def get_nodes_count(cls) -> int:
        ''' Статический метод класса, возвращающий количество узлов '''
        return cls.nodes_count + 1
