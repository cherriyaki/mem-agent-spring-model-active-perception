from .optimize import Optimizer
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_algorithm, get_termination
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.model.problem import Problem
from pymoo.optimize import minimize
from calibration import globalFile

class PymooOptimizer(Optimizer):
    def setAnalysis(self, analysis):
        # set analysis
        pass

    def setParams(self, params):
        self._setMask(params.keys())
        self.lower, self.upper = [], []
        for bounds in params.values():
            self.lower.append(bounds[0])
            self.upper.append(bounds[1])

    def _setMask(self, paramNames):
        self.mask = []
        for name in paramNames:
            if name == "filvary":
                mask.append("real")
            else:
                mask.append("int")

    def setObjectives(self, objectives):
        self.obj = objectives

    def setLossFn(self, lossFn):
        self.fn = lossFn.getLosses

    def setAlgo(self, algo):
        class_ = get_algorithm(algo)
        sampling = self._getSampling()
        crossover = self._getCrossover()
        mutation = self._getMutation()
        self.algo = class_(
            pop_size=1, # 40
            n_offsprings=1, # 10
            sampling=sampling,
            crossover=crossover,
            mutation=mutation,
            eliminate_duplicates=True
        )

    def _getSampling(self):
        sampling = MixedVariableSampling(self.mask, {
            "real": get_sampling("real_random"),
            "int": get_sampling("int_random")
        })
        return sampling

    def _getCrossover(self):
        crossover = MixedVariableCrossover(self.mask, {
            "real": get_crossover("real_sbx", prob=1.0, eta=3.0),
            "int": get_crossover("int_sbx", prob=1.0, eta=3.0)
        })
        return crossover

    def _getMutation(self):
        mutation = MixedVariableMutation(self.mask, {
            "real": get_mutation("real_pm", eta=3.0),
            "int": get_mutation("int_pm", eta=3.0)
        })
        return mutation

    def optimize(self):
        self._setupProblem()
        self.termination = get_termination("n_gen", 1) # 40
        self._minimize()
        self._getResult()

    def _setupProblem(self):
        class MyProblem(Problem):
            def __init__(self):
                super().__init__(n_var=len(self.lower),
                                n_obj=len(self.obj),
                                #  n_constr=2,
                                xl=np.array(self.lower),
                                xu=np.array(self.upper)
                )

            def _evaluate(self, X, out, *args, **kwargs):
                f = {}
                for obj in self.obj:
                    f[obj] = [] 
                for solution in X:
                    losses = self.fn(solution)
                    for obj, val in losses.items():
                        if obj in self.obj: # only add the loss values for objectives specified by user
                            f[obj].append(val)
                    
                out["F"] = np.column_stack(np.array(list(f.values())))

        # self.pbClass = MyProblem
        self.problem = MyProblem()

    def _minimize(self):
        self.res = minimize(self.problem,
                            self.algo,
                            self.termination,
                            seed=1,
                            save_history=True,
                            verbose=True)

    def _getResult(self):
        output = ""
        for i in range(len(self.res.X)):
            output += "--- SOLUTION ("+str(i)+") \n"
            output += "Solution: %s" % self.res.X[i] + "\n"
            output += "Loss values: %s" % self.res.F[i] + "\n"
        print(output)
        self._saveOutput(output)

    def _saveOutput(self, output):
        file = open(os.path.join(globalFile.getRoot(), f"calibration/output/calibrationResults/result_{self.id}.txt"), "w")
        file.write(output)
        file.close()