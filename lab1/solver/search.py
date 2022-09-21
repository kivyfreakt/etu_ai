'''
    Реализации неинформированного поиска
'''

from collections import deque

from solver import common
from solver.tree import Node, Action


def check_final(current_state: list) -> bool:
    ''' Проверка, является ли данное состояние конечным '''
    return current_state == common.get_finish_state()


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
    # НЕ ПОЛУЧИТСЯ ЗАМЕНИТЬ, ТАК КАК В СТЕКЕ МОЖЕТ БЫТЬ ТАКОЕ СОСТОЯНИЕ, ПО ИДЕЕ
    visited = set()
    stack = []

    stack += common.TREE.get_root()

    steps = 1
    iterations = 0

    while len(stack) != 0:
        current_node = stack.pop()
        visited.add(current_node.node_id)

        iterations += 1
        if check_final(current_node.current_state):
            stack.append(current_node)
            break

        new_states = get_new_states(current_node.current_state)
        neighbors = []
        level = current_node.depth
        for action, new_state in new_states.items():

            new_state_hash = hash(tuple(new_state))
            if new_state_hash in visited_states_hash:
                continue

            new_node = Node(new_state, current_node,
                            action, level + 1, level + 1)
            neighbors.append(new_node)
            visited_states_hash.add(new_state_hash)
            common.TREE.add_node(level + 1, new_node)

        for next_node in neighbors:
            if next_node.node_id not in visited:
                stack.append(next_node)

        steps += 1

    return common.TREE.get_path(stack.pop()), iterations


# todo: refactor
def bidirectional_search():
    ''' Двунаправленный поиск '''

    start = Node(common.get_initial_state(), None, None, 0, 0)
    goal = Node(common.get_finish_state(), None, None, 0, 0)

    found, fringe1, visited1, came_from1 = False, deque(
        [start]), set([start]), {start: None}
    meet, fringe2, visited2, came_from2 = None, deque(
        [goal]), set([goal]), {goal: None}

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
                node = Node(node_state, current1, action,
                            current1.depth + 1, current1.depth + 1)
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
                node = Node(node_state, current2, action,
                            current2.depth + 1, current2.depth + 1)
                if node.node_id not in visited2:
                    visited2.add(node.node_id)
                    fringe2.appendleft(node)
                    came_from2[node] = current2

    if found:
        return came_from1, came_from2, meet

    print(f"No path between {start} and {goal}")
    return None, None, None
