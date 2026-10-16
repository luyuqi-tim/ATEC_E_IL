# Task E 面试演示指南

这份仓库公开推理接口、模型结构与一段完整成功的仿真录像。模型权重不公开；本地复现需要预先配置好的 ATEC Task E / Isaac Lab 环境、场景资产及兼容的本机 checkpoint。

[观看 seed 100 完整成功录像（MP4，约 61 秒）](../demo/task_e_seed100_success.mp4)。该回合实际终止于 `basket_success`，得分 18/18。视频只裁剪放大了工作台；seed 100 曾用于示范，不能据此推断未见场景成功率。

## 现场演示顺序（约 2 分钟）

1. **成功录像。** 播放上方视频，说明这是 seed 100 的一次完整成功回合，非跨种子成功率。
2. **接口检查。** 在本仓库运行 `python examples\inference_smoke.py --checkpoint <本机权重路径>`。展示输入只含 RGB 与 `proprio`，返回形状为 `(1, 8)` 的有限关节动作。这里使用合成黑图，只证明模型和接口可以加载。
3. **结构说明。** 打开 [README](../README.md) 中的流程图：RGB 经 ResNet-18，关节位置与时间特征进入 ACT，预测 30 步动作块，按时间聚合后送入环境。
4. **闭环任务。** 在已安装 Task E 的本机工程中运行其 `scripts/play_atec_task.py`，启用相机并指定 checkpoint。展示机械臂依次操作糖盒、芥末瓶、香蕉，以及终端的 `score` 和 `termination_reason`。
5. **如实解释结果。** 已记录的 seed 100 回合曾达到 18/18 并触发 `basket_success`；该种子在示范中出现过，不能作为未见场景成功率。其他摆放可能在芥末瓶阶段抓空。

## 面试时可讲的三个工程难点

- **专家动作可靠性。** 芥末瓶的侧抓需要先在外侧下降，再水平接近瓶身；抬升时固定水平目标，避免因追踪物体状态而摆动。先验证专家，才能解释后续策略的错误来源。
- **观测与动作约定。** 环境给出相对默认关节位姿，而 ACT 学到的是归一化后的动作。推理时必须恢复绝对关节状态、添加时间编码，并按训练统计反归一化到 8 维环境动作。
- **闭环误差累积。** 离线动作误差小，不等于连续操作成功。抓取前几厘米的偏差可能让芥末瓶保持在工作区，随后阻碍香蕉阶段；因此现场展示应同时看分数、物体位置和失败阶段。

## 两种演示命令

仅验证接口（无需启动仿真）：

```powershell
python examples\inference_smoke.py --checkpoint .\local_checkpoint.pt
```

完整任务（在配置好场景资产的 Task E 工程根目录执行；将本仓库的 `demo/` 放入该工程）：

```powershell
conda activate atec_task_e
$env:PYTHONPATH="$PWD\source\atec_rl_lab;$PWD"
python scripts\play_atec_task.py --task ATEC-TaskE-Piper --num_envs 1 --enable_cameras --seed 100 --checkpoint .\local_checkpoint.pt
```

公开仓库不包含权重、仿真资产、训练轨迹、测试日志或私人路径。现场可用本机兼容权重运行。

