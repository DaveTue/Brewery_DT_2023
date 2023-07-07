import argparse
from pythonfmu import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real

def Heat_exchange(T, Tamb):
    h = 0.25
    Q = h * (T - Tamb)
    return Q

class HeatTransfer(Fmi2Slave):

    description = "Heat transfer model"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.T = 0.0
        self.Tamb = 0.0
        self.Q = 0.0

        self.register_variable(Real("T", causality=Fmi2Causality.input))
        self.register_variable(Real("Tamb", causality=Fmi2Causality.input))
        self.register_variable(Real("Q", causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        self.Q = Heat_exchange(self.T, self.Tamb)
        return True

# for testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("T", type=float)
    parser.add_argument("Tamb", type=float)
    args = parser.parse_args()
    print(Heat_exchange(args.T, args.Tamb))