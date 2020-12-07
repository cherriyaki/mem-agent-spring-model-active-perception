import nevergrad as ng 

params = ng.p.Dict(
    # Scalar params are init, lower, upper?
    filConstNorm = ng.p.Scalar(2, 0.01, 150),
    filTipMax = ng.p.Scalar(15, 1, 30),
    tokenStrength = ng.p.Scalar(1, 1, 5),
    filSpacing = ng.p.Scalar(2, 1, 100),
    actinMax = ng.p.Scalar(512, 200, 700)
)

# Set the interval between value change
params["filTipMax"].set_mutation(sigma = 1)
params["tokenStrength"].set_mutation(sigma = 1)
params["filSpacing"].set_mutation(sigma = 1)
params["actinMax"].set_mutation(sigma = 1)

# Set seed. Might need tweaking TODO
RANDOM_SEED = 12
params.random_state.seed(RANDOM_SEED)

# Set other optimizer arguments
optName = "OnePlusOne"
budget = 100
# numWorkers = 10 # don't see the point of this rn TODO use or not?

# Make optimizer
optimizer = ng.optimizers.registry[optName](params, budget)

# Cost function: returns how much error a set of a params results in
def costFn(filconst, filtipmax, tokenstrength, filspacing, actinmax):
    