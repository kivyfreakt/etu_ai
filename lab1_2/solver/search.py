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


def heuristic1(state):
    ''' не на своих местах '''
    count = 0
    for i, num in enumerate(state):
        if common.get_finish_state()[i] == num:
            count += 1

    return count


def heuristic2(state):
    ''' Manhatten '''
    res = 0
    for i in range(common.SIZE**2):
        if state[i] != 0 and state[i] != common.get_finish_state()[i]:
            c_i = common.get_finish_state().index(state[i])
            diff_y = (i // common.SIZE) - (c_i // common.SIZE)
            diff_x = (i % common.SIZE) - (c_i % common.SIZE)
            res += abs(diff_y) + abs(diff_x)
    return res


def dfs(heuristic):
    ''' Поиск в глубину '''
    visited = set()
    stack = []
    iterations = 0

    stack += common.TREE.get_root()

    while stack:
        current_node = stack.pop()
        visited.add(current_node.node_id)

        iterations += 1

        if common.MANUAL:
            print(f"Iteration {iterations}")
            print("Current node: ")
            common.print_state(current_node.current_state)
            print("---")

        if check_final(current_node.current_state):
            if common.MANUAL:
                print("SOLUTION FIND")
                common.print_state(current_node.current_state)
                print("---")

            return common.TREE.get_path(current_node), iterations

        new_states = get_new_states(current_node.current_state)
        if not isinstance(heuristic, int):
            new_states = dict(
                sorted(new_states.items(), key=lambda item: heuristic(item[1])))

        neighbors = []
        level = current_node.depth
        for action, new_state in new_states.items():
            new_state_hash = hash(tuple(new_state))
            if common.TREE.is_in_tree(new_state_hash):
                if common.MANUAL:
                    print("Find existing state: ")
                    common.print_state(new_state)
                    print("---")
                continue

            new_node = Node(new_state, current_node,
                            action, level + 1, level + 1)
            neighbors.append(new_node)
            common.TREE.add_node(new_node)

        if common.MANUAL:
            print("Nodes descendants: ")
        for next_node in neighbors:
            if common.MANUAL:
                common.print_state(next_node.current_state)
                print("---")
            if next_node.node_id not in visited:
                stack.append(next_node)

        if common.MANUAL:
            print("Press Enter to continue... ")
            input()

    return None, None


def bidirectional_search(heuristic):
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

            if common.MANUAL:
                print(f"Iteration {iterations}")
                print("First subtree current node: ")
                common.print_state(current1.current_state)
                print("---")

            if current1.node_id in visited2:
                # print("VARIANT 1")
                if common.MANUAL:
                    print("MEET POINT FIND")
                    common.print_state(current1.current_state)
                    print("---")

                meet = common.TREE2.get_node(current1.node_id)
                path2 = common.TREE2.get_path(meet)
                del path2[0]
                path = list(reversed(path2)) + common.TREE.get_path(current1)
                
                common.TREE2.get_node(hash(tuple(common.FINISH_STATE))).depth = meet.depth + current1.depth
                return path, iterations

            new_states = get_new_states(current1.current_state)
            if not isinstance(heuristic, int):
                new_states = dict(
                    sorted(new_states.items(), key=lambda item: heuristic(item[1])))

            neighbors1 = []
            for action, node_state in new_states.items():
                node = Node(node_state, current1, action,
                            current1.depth + 1, current1.depth + 1)

                neighbors1.append(node)

            if common.MANUAL:
                print("Nodes descendants: ")
            for next_node in neighbors1:
                if common.MANUAL:
                    common.print_state(next_node.current_state)
                    print("---")
                if next_node.node_id not in visited1:
                    visited1.add(next_node.node_id)
                    fringe1.append(next_node)
                    common.TREE.add_node(next_node)

        if fringe2:
            current2 = fringe2.pop()

            if common.MANUAL:
                print(f"Iteration {iterations}")
                print("Second subtree current node: ")
                common.print_state(current2.current_state)
                print("---")

            if current2.node_id in visited1:
                if common.MANUAL:
                    print("MEET POINT FIND")
                    common.print_state(current2.current_state)
                    print("---")
                # print("VARIANT 2")
                meet = common.TREE.get_node(current2.node_id)
                path2 = common.TREE2.get_path(meet)
                del path2[0]
                path = list(reversed(path2)) + common.TREE.get_path(current2)
                common.TREE2.get_node(hash(tuple(common.FINISH_STATE))).depth = meet.depth + current1.depth
                return list(reversed(path)), iterations

            new_states = get_new_states(current2.current_state)
            if not isinstance(heuristic, int):
                new_states = dict(
                    sorted(new_states.items(), key=lambda item: heuristic(item[1])))

            neighbors2 = []
            for action, node_state in new_states.items():
                node = Node(node_state, current2, action,
                            current2.depth + 1, current2.depth + 1)
                neighbors2.append(node)

            if common.MANUAL:
                print("Nodes descendants: ")
            for next_node in neighbors2:
                if common.MANUAL:
                    common.print_state(next_node.current_state)
                    print("---")
                if next_node.node_id not in visited2:
                    visited2.add(next_node.node_id)
                    fringe2.append(next_node)
                    common.TREE2.add_node(next_node)

        if common.MANUAL:
            print("Press Enter to continue... ")
            input()

    return None, None


def a_star(algorithm, heuristic):
    ''' Враппер модифицированных алгоритмов '''
    if algorithm == "bds":
        return bidirectional_search(heuristic)
    if algorithm == "dfs":
        return dfs(heuristic)

    print("Incorrect input")
    return None, None
