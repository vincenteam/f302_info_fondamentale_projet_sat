import networkx as nx
from itertools import combinations

from pysat.solvers import Minicard
from pysat.formula import CNFPlus, IDPool
import matplotlib.pyplot as plt


g = nx.Graph() # graph chevre loup choux
g.add_nodes_from([1, 2, 3])
g.add_edges_from([(1, 2), (2, 3)])

# Q2
def gen_solution(G: nx.Graph, k: int) -> list[tuple[int, set, set]]:
    # À COMPLÉTER
    
    configs = range(len(g.nodes)*2 + 2) # max number of configs in a solvalble graph
    
    berger_side_left = 'left' # le berger est side left
    
    cnf = CNFPlus()
    vpool = IDPool(start_from=1)
    

    
    for config in configs:
        berger_side_left_id = vpool.id((berger_side_left, config))
        
        for edge in g.edges:
            # no connected nodes on the same side without berger on that side
            edge_0_side_left = vpool.id((edge[0], config))
            edge_1_side_left = vpool.id((edge[1], config))
            
            cnf.append([edge_0_side_left, edge_1_side_left, -berger_side_left_id])
            cnf.append([-edge_0_side_left, -edge_1_side_left, berger_side_left_id])
        
        
        solution_constraint = [vpool.id((node, config)) for node in g.nodes]
        solution_constraint.append(vpool.id(config)) # the idea is to use vpool.id(config) as a "solution flag", see below
        cnf.append(solution_constraint)
        
        for node in g.nodes:
            cnf.append([-vpool.id((node, config)), -vpool.id(config)])
            
        cnf.append([-berger_side_left_id] if config%2 else [berger_side_left_id]) # berger changes side at each config
        
    
    cnf.append([vpool.id(config) for config in configs]) # at least one of the solution flag is true
    
    
    # must move with berger
    for config in configs[1:]:
        for node in g.nodes:
            cnf.append([-vpool.id((node, config-1)), vpool.id((node, config)), -vpool.id((berger_side_left, config))])
            cnf.append([vpool.id((node, config-1)), -vpool.id((node, config)), vpool.id((berger_side_left, config))])
    
    
    # k constraint à changer
    def foreach_recurs(n, iter, current_elements, callback):
        if n==1:
            for e in iter:
                callback([*current_elements, e])
        else:
            for e in iter:
                foreach_recurs(n-1, iter, [*current_elements, e], callback)
    
    # super crade
    def add_kuplets_constraint(kuplet):
        print(len(kuplet))
        if len(kuplet) == len(set(kuplet)):
            for config in configs[1:]:
                c1 = [-vpool.id((node, config-1)) for node in kuplet]
                c1.extend([vpool.id((node, config)) for node in kuplet])
                cnf.append(c1)
                
                c2 = ([vpool.id((node, config-1)) for node in kuplet])
                c2.extend([-vpool.id((node, config)) for node in kuplet])
                cnf.append(c2)
                
    if k < len(g.nodes):
        for kuplet in list(combinations(g.nodes, k+1)):
         add_kuplets_constraint(kuplet)
#        foreach_recurs(k+1, g.nodes, [], add_kuplets_constraint)
    
    
    
    
    # start with everything on left
    for node in g.nodes:
        cnf.append([vpool.id((node, configs[0]))])
    
    s = Minicard()
    s.append_formula(cnf.clauses, no_return=False)
    resultat = s.solve()
    
    print(resultat)
    
    if resultat:
        model = s.get_model()
        print(model)


        fig, axes = plt.subplots(1, len(configs), figsize=(5 * len(configs), 5))

        for i, config in enumerate(configs):
            sides = {}
            for node in g.nodes:
                sides[node] = vpool.id((node, config)) in model

            print("blue: right, red: left")
            print("berger side: " + ("left" if vpool.id((berger_side_left, config)) in model else "right"))
            print("g:", vpool.id(config) in model)
            print("")
            def color_function(node):
                return sides[node]

            # Create a list of colors based on the color function
            node_colors = ['red' if color_function(node) else 'blue' for node in g.nodes()]
            pos = nx.spring_layout(g, seed=1)  # or use other layouts like `nx.circular_layout`, etc.

            nx.draw(g, ax=axes[i], pos=pos, with_labels=True, node_color=node_colors)
            axes[i].set_title(f'Configuration {i + 1}')  # Set title for each subplot

        # Adjust layout for better spacing
        plt.tight_layout()

        # Show the figure with all subplots
        plt.show()
    
    return -1

# Q3
def find_alcuin_number(G: nx.Graph) -> int:
    # À COMPLÉTER
    return

# Q5
def gen_solution_cvalid(G: nx.Graph, k: int, c: int) -> list[tuple[int, set, set, tuple[set]]]:
    # À COMPLÉTER
    return

# Q6
def find_c_alcuin_number(G: nx.Graph, c: int) -> int:
    # À COMPLÉTER
    return



gen_solution(g, 1)