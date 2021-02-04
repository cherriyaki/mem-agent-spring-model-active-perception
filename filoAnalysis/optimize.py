import numpy as np
import ksTest as ks
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.factory import get_termination
from pymoo.optimize import minimize
import getopt
import sys

#--
# Parse command line arguments for the parameters to be optimized 
# and the lower and upper bound of each
#--
lowerBounds = {}
upperBounds = {}
objectiveNames = []
try:
    opts, args = getopt.getopt(sys.argv[1:],"",["filvary=","filtipmax=","filspacing=","actinmax=","objectives="])
except getopt.GetoptError:
    print('optimize.py --filvary "<lowerBound> <upperBound>" --filtipmax "<lowerBound> <upperBound>" --filspacing "<lowerBound> <upperBound>" --actinmax "<lowerBound> <upperBound>" --objectives "maxLen averageExtendingTime averageRetractingTime timeAtMax"')
    sys.exit(2)
for opt, arg in opts:
    if opt ==  "--filvary":
        bounds = list(map(float, arg.split()))
        lowerBounds["filvary"] = bounds[0]
        upperBounds["filvary"] = bounds[1]
    elif opt ==  "--filtipmax":
        bounds = list(map(int, arg.split()))
        lowerBounds["filtipmax"] = bounds[0]
        upperBounds["filtipmax"] = bounds[1]
    elif opt ==  "--filspacing":
        bounds = list(map(int, arg.split()))
        lowerBounds["filspacing"] = bounds[0]
        upperBounds["filspacing"] = bounds[1]
    elif opt ==  "--actinmax":
        bounds = list(map(int, arg.split()))
        lowerBounds["actinmax"] = bounds[0]
        upperBounds["actinmax"] = bounds[1]
    elif opt == "--objectives":
        objectiveNames = arg.split()

mask = []
for param in lowerBounds.keys():
    if param == "filvary":
        mask.append("real")
    else:
        mask.append("int")
class MyProblem(Problem):

    # The parameters are filVary, filTipMax, filSpacing, actinMax
    def __init__(self):
        super().__init__(n_var=len(lowerBounds),
                         n_obj=len(objectiveNames),
                        #  n_constr=2,
                         xl=np.array(list(lowerBounds.values())),
                         xu=np.array(list(upperBounds.values()))
        )

    # Evaluates a stack of candidate solutions
    def _evaluate(self, X, out, *args, **kwargs):
        """
        For solutions s0, s1, s2, And say f1 = [2,3,4]
        This means for objective 1, s0's loss is 2, s1's loss is 3 and s2's loss is 4.
        """
        f = {}
        for obj in objectiveNames:
            f[obj] = []
        print(f)
        for solution in X:
            ksValues = ks.getKsValues(solution)
            for obj, val in ksValues.items():
                if obj in objectiveNames: # only add the loss values for objectives specified by user
                    f[obj].append(val)
            
        out["F"] = np.column_stack(np.array(list(f.values())))

problem = MyProblem()

# Thanks to pymoo's website for this code https://pymoo.org/customization/mixed_variable_problem.html

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
    pop_size=80, # 40
    n_offsprings=20, # 10
    sampling=sampling,
    crossover=crossover,
    mutation=mutation,
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 80) # 40

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

output = ""
for i in range(len(res.X)):
    output += "--- SOLUTION ("+str(i)+") \n"
    output += "Solution: %s" % res.X[i] + "\n"
    output += "Loss values: %s" % res.F[i] + "\n"

text_file = open("filoAnalysis/mooOutput.txt", "w")
text_file.write(output)
text_file.close()
print(output)