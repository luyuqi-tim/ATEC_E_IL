"""Small tensor wrapper required by the ACT image backbone."""

from typing import Optional

from torch import Tensor


class NestedTensor:
    def __init__(self, tensors: Tensor, mask: Optional[Tensor]):
        self.tensors = tensors
        self.mask = mask

    def to(self, device):
        mask = self.mask.to(device) if self.mask is not None else None
        return NestedTensor(self.tensors.to(device), mask)

    def decompose(self):
        return self.tensors, self.mask

    def __repr__(self):
        return str(self.tensors)

