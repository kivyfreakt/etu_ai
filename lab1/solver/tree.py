'''
    Структуры данных
'''

from enum import Enum

from . import common


class Tree:
    ''' Класс представления дерева '''

    def __init__(self, _flag=True):
        self.__hashset = {}  # хеши всех узлов

        if _flag:
            node = Node(common.get_initial_state(), None, None, 0, 0)
        else:
            node = Node(common.get_finish_state(), None, None, 0, 0)

        self.__hashset[node.node_id] = node

    def get_root(self) -> list:
        ''' Получить корень дерева '''
        return [list(self.__hashset.values())[0]]

    def get_node(self, node_id: int):
        ''' Получить узел по идентификатору (хэшу)'''
        return self.__hashset[node_id]

    def add_node(self, new_node):
        ''' Добавить узел в дерево '''
        if not self.is_in_tree(new_node.node_id):
            self.__hashset[new_node.node_id] = new_node

    def is_in_tree(self, node_id: int) -> bool:
        ''' Проверка, есть ли состояние в дереве '''
        return node_id in self.__hashset

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
    __nodes_count = 0

    def __init__(self, state, parent, action, cost, depth):
        # Состояние в пространстве состояний, которому соответствует данный узел
        self.current_state = state
        self.parent_node = parent  # Указатель на родительский узел
        # Действие, которое было применено к родительскому узлу для формирования данного узла
        self.previous_action = action
        # Стоимость пути от начального состояния до данного узла g(n)
        self.path_cost = cost
        # Количество этапов пути от начального состояния (глубина)
        self.depth = depth
        self.node_id = hash(tuple(state))  # уникальный идентификатор узла
        Node.__nodes_count += 1

    @classmethod
    def get_nodes_count(cls) -> int:
        ''' Статический метод класса, возвращающий количество узлов '''
        return cls.__nodes_count + 1
