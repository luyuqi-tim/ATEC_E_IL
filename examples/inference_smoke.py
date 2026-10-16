"""Check the public inference package without launching Isaac Sim.

The black image and fixed joint state are synthetic. This checks the interface,
model loading, and output shape; it does not measure task success.
"""

from pathlib import Path
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo.solution import AlgSolution  # noqa: E402


def main() -> None:
    if not torch.cuda.is_available():
        raise SystemExit("This policy requires a CUDA GPU.")

    policy = AlgSolution()
    proprio = torch.zeros((1, 24), dtype=torch.float32)
    proprio[:, :8] = (policy.teleop_home_joint_pos - policy.default_joint_pos).cpu()
    observation = {
        "proprio": proprio,
        "image": {"video_rgb": torch.zeros((1, 480, 640, 3), dtype=torch.uint8)},
    }

    for _ in range(policy._startup_zero_steps + policy._home_hold_steps):
        policy.predicts(observation, 0.0)
    action = policy.predicts(observation, 0.0)["action"]
    values = torch.tensor(action)
    assert values.shape == (1, 8), values.shape
    assert torch.isfinite(values).all()
    print(f"PASS: observation -> {tuple(values.shape)} finite action")


if __name__ == "__main__":
    main()

