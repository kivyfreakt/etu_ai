# -*- coding: utf-8 -*-

'''

Задание на работу:

Реализовать решение задачи поиском в глубину и двунаправленным поиском

Начальное состояние
6	0	8
5	2	1
4	3	7

Конечное состояние
1	2	3
8	0	4
7	6	5

'''

import argparse
from time import process_time

from solver import common
from solver.search import dfs, bidirectional_search
from solver.visualizer import visualizer
from solver.tree import Tree, Node

if __name__ == '__main__':
    # парсинг входных значений
    parser = argparse.ArgumentParser(description="Solve 8-puzzle game")
    parser.add_argument('algorithm', type=str,
                        help='name of the algorithm used (list: dfs, bds)')
    parser.add_argument("-v", "--visualize", action='store_true',
                        help="Gui visualisation of puzzle solution")
    parser.add_argument("-m", "--manual", action='store_true',
                        help="step-by-step mode of operation of the program")

    args = parser.parse_args()

    # создать
    common.TREE = Tree()
    common.TREE2 = Tree(False)

    # начать отсчет времени
    start_time = process_time()

    # поиск решения
    solution = []
    iterations = 0
    if args.algorithm == "dfs":
        solution, iterations = dfs()
    else:
        solution, iterations = bidirectional_search()

    solution.reverse() # todo: пофиксить

    # завершить отсчет времени
    finish_time = process_time()

    # визуализация
    if args.visualize:
        visualizer(solution)
    else:
        for state in solution:
            common.print_state(state)

    # вывод результатов
    print(f"Iteration count: {iterations}")
    print(f"Nodes: {Node.get_nodes_count()}")
    print(f"Time: {(finish_time-start_time)*1000} ms")
