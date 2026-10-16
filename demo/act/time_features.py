"""Episode clock features shared by ACT training and inference."""

import math

import torch


def encode_time(steps: torch.Tensor, horizon: int, encoding: str) -> torch.Tensor:
    """Return one feature row per policy step, using only an internal clock."""
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    steps = steps.float().reshape(-1, 1)
    progress = (steps / horizon).clamp(0.0, 1.0)
    if encoding == "linear":
        return progress
    if encoding == "fourier":
        periods = steps.new_tensor([200.0, 600.0, 1800.0, 6000.0]).reshape(1, -1)
        phase = 2.0 * math.pi * steps / periods
        return torch.cat((progress, torch.sin(phase), torch.cos(phase)), dim=1)
    raise ValueError(f"Unsupported time encoding: {encoding}")

