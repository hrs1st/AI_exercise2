import json
import sys
import pygad
import simulator


class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        sudoku = json.loads(problem)['sudoku']
        holes = simulator.find_holes(sudoku)
        gene_space = simulator.calculate_valid_genes(sudoku)

        ga_params = {
            'num_generations': 2000,
            'num_parents_mating': 2,
            'sol_per_pop': 500,
            'num_genes': len(gene_space),
            'gene_type': int,
            'gene_space': gene_space,
            'parent_selection_type': 'sss',
            'mutation_type': 'random',
            'crossover_type': 'single_point',
            'fitness_func': lambda solution, _: simulator.fitness(solution, sudoku, holes),
            'stop_criteria': 'reach_1'
        }

        ga_instance = pygad.GA(**ga_params)
        ga_instance.run()
        solution, _, _ = ga_instance.best_solution()
        simulator.fill(sudoku, solution, holes)
        print(simulator.count_conflicts(sudoku))
        return json.dumps({'sudoku': sudoku}, indent=2)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as problem_file:
        print(AI().solve(problem_file.read()))
