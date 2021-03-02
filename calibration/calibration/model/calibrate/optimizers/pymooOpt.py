from .optimize import Optimizer
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_algorithm, get_termination
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.model.problem import Problem
from pymoo.optimize import minimize
from calibration import global_
from calibration.model import log
from inspect import currentframe
import traceback
import numpy as np
import os

class PymooOptimizer(Optimizer):
    def setAnalysis(self, analysis):
        # set analysis
        pass

    def setParams(self, params):
        """
        @param {"param1": [lowerBound, upperBound], "param2": [lowerBound, upperBound], ...}
        """
        self._setMask(params.keys())
        self.lower, self.upper = [], []
        for bounds in params.values():
            self.lower.append(bounds[0])
            self.upper.append(bounds[1])
        log.w(id=self.id, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"Lower bounds = {self.lower} | Upper bounds = {self.upper}"])

    def _setMask(self, paramNames):
        self.mask = []
        for name in paramNames:
            if name.lower() == "filvary":
                self.mask.append("real")
            else:
                self.mask.append("int")
        log.w(id=self.id, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"mask = {self.mask}"])

    def setObjectives(self, objectives):
        self.objs = objectives

    def setLossFn(self, lossFn):
        self.fn = lossFn.getLosses

    def setAlgo(self, algoName):
        algo = get_algorithm(algoName)
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Algorithm obtained. Object = {algo}"])
        sampling = self._getSampling()
        crossover = self._getCrossover()
        mutation = self._getMutation()
        self.algo=algo
        self._configAlgo(sampling, crossover, mutation)

    def _configAlgo(self, sampling, crossover, mutation):
        self.algo.pop_size=40 # 40
        self.algo.n_offsprings=10 # 10
        self.algo.sampling=sampling
        self.algo.crossover=crossover
        self.algo.mutation=mutation
        self.algo.eliminate_duplicates=True

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
        self.termination = get_termination("n_gen", 40) # 40
        self._minimize()
        self._getResult()

    def _setupProblem(self):
        lower, upper, objs, fn = self.lower, self.upper, self.objs, self.fn
        class MyProblem(Problem):
            def __init__(self):
                super().__init__(n_var=len(lower),
                                n_obj=len(objs),
                                #  n_constr=2,
                                xl=np.array(lower),
                                xu=np.array(upper)
                )

            def _evaluate(self, X, out, *args, **kwargs):
                f = {}
                for obj in objs:
                    f[obj] = [] 
                for solution in X:
                    losses = fn(solution)
                    for obj, val in losses.items():
                        if obj in objs: # only add the loss values for objectives specified by user
                            f[obj].append(val)
                    
                out["F"] = np.column_stack(np.array(list(f.values())))

        self.problem = MyProblem()
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Defined problem class. Object = {self.problem}"])

    def _minimize(self):
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Calling minimize()"])
        try:
            self.res = minimize(self.problem,
                                self.algo,
                                self.termination,
                                seed=1,
                                save_history=True,
                                verbose=True)
        except: 
            tb = traceback.format_exc()
            log.w(id=self.id, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to run minimize()"])
            log.w(id=self.id, exc=tb)
            raise       # Throw the caught exception

    def _getResult(self):
        output = ""
        for i in range(len(self.res.X)):
            output += "--- SOLUTION ("+str(i)+") \n"
            output += "Solution: %s" % self.res.X[i] + "\n"
            output += "Loss values: %s" % self.res.F[i] + "\n"
        print(output)
        self._saveOutput(output)

    def _saveOutput(self, output):
        file = os.path.join(global_.getRoot(), f"calibration/output/calibrationResults/result_{self.id}.res")
        try:
            with open(file, "w") as f:
                f.write(output)
        except:
            tb = traceback.format_exc()
            log.w(id=self.id, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to open or write to {file}"])
            log.w(id=self.id, exc=tb)
            raise       # Throw the caught exception
        log.w(id=self.id, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"Done. Wrote to result file {file}"])

# if __name__ == "__main__":
#     opt = PymooOptimizer(sys.argv[1])
#     opt.optimize()