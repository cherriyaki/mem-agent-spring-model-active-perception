import numpy as np
import ksTest as ks
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.factory import get_termination
from pymoo.optimize import minimize

class MyProblem(Problem):

    # The parameters are filVary, filTipMax, filSpacing, actinMax
    def __init__(self):
        super().__init__(n_var=4,
                         n_obj=4,
                        #  n_constr=2,
                         xl=np.array([0.1,1,1,500]),
                         xu=np.array([2.0,15,4,600])
                         )

    # Evaluates a stack of candidate solutions
    def _evaluate(self, X, out, *args, **kwargs):
        """
        For solutions s0, s1, s2
        And say f1 = [2,3,4]
        This means for objective 1, s0's loss is 2, s1's loss is 3 and s2's loss is 4.
        f2 = [1,4,2]
        For objective 2, s0's loss is 1, s1's loss is 4 and s2's loss is 2.

        For each solution
            Run ksTest.py 
            For each objective i
                f[i].append(ksValues[i])
        """
        f1, f2, f3, f4 = [], [], [], []
        for solution in X:
            ksValues = ks.getKsValues(solution)
            f1.append(ksValues[0])
            f2.append(ksValues[1])
            f3.append(ksValues[2])
            f4.append(ksValues[3])
            
        out["F"] = np.column_stack([f1, f2, f3, f4])

        

# Thanks to pymoo's website for this code https://pymoo.org/customization/mixed_variable_problem.html
mask = ["real", "int", "int", "int"]

problem = MyProblem()

sampling = MixedVariableSampling(mask, {
    "real": get_sampling("real_random"),
    "int": get_sampling("int_random")
})

crossover = MixedVariableCrossover(mask, {
    "real": get_crossover("real_sbx", prob=1.0, eta=3.0),
    "int": get_crossover("int_sbx", prob=1.0, eta=3.0)
})

mutation = MixedVariableMutation(mask, {
    "real": get_mutation("real_pm", eta=3.0),
    "int": get_mutation("int_pm", eta=3.0)
})

algorithm = NSGA2(
    pop_size=40, # 40
    n_offsprings=10, # 10
    sampling=sampling,
    crossover=crossover,
    mutation=mutation,
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 40) # 40

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

for i in range(len(res.X)):
    print("SOLUTION ("+str(i)+")")
    print("Solution: %s" % res.X)
    print("Loss values: %s" % res.F)
