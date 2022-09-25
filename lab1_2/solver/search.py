'''
    Реализации неинформированного поиска
'''

from . import common
from .tree import Node, Action


def check_final(current_state: list) -> bool:
    ''' Проверка, является ли данное состояние конечным '''
    return current_state == common.get_finish_state()


def clone_and_swap(state, i, j):
    ''' Клонирование состояния и перемещение пустой ячейки '''
    clone = list(state)
    clone[i], clone[j] = clone[j], clone[i]
    return clone


def get_new_states(current_state: list) -> dict:
    ''' Получение новых состояний поля '''
    new_states = {}
    pos = current_state.index(0)

    # up
    if pos - 3 >= 0:
        new_states[Action.UP] = clone_and_swap(current_state, pos, pos-3)

    # down
    if pos + 3 < 9:
        new_states[Action.DOWN] = clone_and_swap(current_state, pos, pos+3)

    # right
    if pos % 3 + 1 < 3:
        new_states[Action.RIGHT] = clone_and_swap(current_state, pos, pos+1)

    # left
    if pos % 3 > 0:
        new_states[Action.LEFT] = clone_and_swap(current_state, pos, pos-1)

    return new_states


def dfs():
    ''' Поиск в глубину '''
    visited = set()
    stack = []
    iterations = 0

    stack += common.TREE.get_root()

    while stack:
        current_node = stack.pop()
        visited.add(current_node.node_id)

        iterations += 1

        if check_final(current_node.current_state):
            return common.TREE.get_path(current_node), iterations

        new_states = get_new_states(current_node.current_state)
        neighbors = []
        level = current_node.depth
        for action, new_state in new_states.items():

            new_state_hash = hash(tuple(new_state))
            if common.TREE.is_in_tree(new_state_hash):
                continue

            new_node = Node(new_state, current_node,
                            action, level + 1, level + 1)
            neighbors.append(new_node)
            common.TREE.add_node(new_node)

        for next_node in neighbors:
            if next_node.node_id not in visited:
                stack.append(next_node)

    return None, None


def bidirectional_search():
    ''' Двунаправленный поиск '''

    iterations = 0

    start = common.TREE.get_root()
    goal = common.TREE2.get_root()

    fringe1 = [] + start
    fringe2 = [] + goal

    visited1 = set(start)
    visited2 = set(goal)

    while fringe1 or fringe2:
        iterations += 1
        if fringe1:
            current1 = fringe1.pop()

            if current1.node_id in visited2:
                meet = common.TREE2.get_node(current1.node_id)
                # todo: fix!
                path2 = common.TREE2.get_path(meet)
                del path2[0]
                path = list(reversed(common.TREE.get_path(current1))) + path2
                return path, iterations

            for action, node_state in get_new_states(current1.current_state).items():
                node = Node(node_state, current1, action,
                            current1.depth + 1, current1.depth + 1)
                if node.node_id not in visited1:
                    visited1.add(node.node_id)
                    fringe1.append(node)
                    common.TREE.add_node(node)

        if fringe2:
            current2 = fringe2.pop()

            if current2.node_id in visited1:
                meet = common.TREE.get_node(current2.node_id)
                path2 = common.TREE2.get_path(meet)
                del path2[0]
                path = list(reversed(common.TREE.get_path(current2))) + path2
                return path, iterations

            for action, node_state in get_new_states(current2.current_state).items():
                node = Node(node_state, current2, action,
                            current2.depth + 1, current2.depth + 1)
                if node.node_id not in visited2:
                    visited2.add(node.node_id)
                    fringe2.append(node)
                    common.TREE2.add_node(node)

    return None, None

def a_star():
    ''' Поиск алгоритмом a-star '''
    print("Todo)))")
    return None, None
