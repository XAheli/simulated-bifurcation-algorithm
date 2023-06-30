from ..ising import Ising
from .ising_interface import IsingInterface
from typing import Union
import torch
import numpy as np


class BinaryPolynomial(IsingInterface):

    """
    Given a matrix `Q` (quadratic form), a vector `l`
    (linear form) and a constant `c`, the value to minimize is 
    `ΣΣ Q(i,j)b(i)b(j) + Σ l(i)b(i) + c` where the `b(i)`'s values
    are either `0` or `1`.
    """

    def __init__(self, matrix: Union[torch.Tensor, np.ndarray], vector: Union[torch.Tensor, np.ndarray, None] = None, constant: Union[float, int, None] = None,
                dtype: torch.dtype=torch.float32, device: str = 'cpu') -> None:
        super().__init__(matrix, vector, constant, [0, 1], dtype, device)

    def to_ising(self) -> Ising:
        symmetrical_matrix = .5 * (self.matrix + self.matrix.t())
        J = -.5 * symmetrical_matrix
        h = .5 * self.vector + .5 * symmetrical_matrix @ torch.ones((len(self), 1), device=self.device)
        return Ising(J, h, self.dtype, self.device)

    def from_ising(self, ising: Ising) -> torch.Tensor:
        if ising.ground_state is not None:
            return .5 * (ising.ground_state + 1)
