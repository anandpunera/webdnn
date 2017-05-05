from typing import Dict

from graph_builder.graph.operator import Operator
from graph_builder.graph.operators.attributes.have_weights import HaveWeights
from graph_builder.graph.operators.attributes.post_axiswise import PostAxiswise
from graph_builder.graph.operators.attributes.post_elementwise import PostElementwise
from graph_builder.graph.variable import Variable


class Sgemm(Operator):
    attributes = {PostElementwise,
                  PostAxiswise,
                  HaveWeights}

    def __init__(self, name: str, parameters: Dict[str, object]):
        assert "M" in parameters
        assert "N" in parameters
        assert "K" in parameters
        assert "out_shape" in parameters
        assert "out_order" in parameters
        assert "transpose_A" in parameters
        assert "transpose_B" in parameters

        super().__init__(name, parameters)

    def __call__(self, A: Variable, B: Variable):
        assert A.size == self.M * self.K
        assert B.size == self.N * self.K

        self.append_input("A", A)
        self.append_input("B", B)

        C = Variable(
            self.parameters["out_shape"],
            self.parameters["out_order"]
        )
        self.append_output("C", C)

        assert C.size == self.M * self.N
        return C,

    @property
    def M(self) -> int:
        return int(self.parameters["M"])

    @property
    def N(self) -> int:
        return int(self.parameters["N"])

    @property
    def K(self) -> int:
        return int(self.parameters["K"])

    @property
    def transpose_A(self) -> bool:
        return bool(self.parameters["transpose_A"])

    @property
    def transpose_B(self) -> bool:
        return bool(self.parameters["transpose_B"])
