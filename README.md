# Mathematical Modeling Casebook

一个可复现的数学建模案例库，集中展示评价、优化与预测三类常见问题。所有核心算法均使用 Python 标准库实现，便于面试官直接阅读公式对应的代码与单元测试。

## 案例一：TOPSIS 多指标综合评价

对候选方案构建决策矩阵，进行向量归一化与加权，分别计算到正理想解、负理想解的距离：

```text
C_i = D_i^- / (D_i^+ + D_i^-)
```

`C_i` 越大，方案越接近理想解。实现支持效益型指标与成本型指标，并处理零向量、权重异常等边界情况。

## 案例二：加权 p-median 设施选址

在候选设施点中选择 `p` 个，使需求点到最近设施的加权距离之和最小：

```text
min Σ_i w_i · min_j d(i, j)
```

案例采用穷举法求解小规模离散选址问题，优点是结果可验证，可作为整数规划模型的基线答案。

## 案例三：线性趋势预测

使用最小二乘法拟合 `y = a + bt`，输出未来多期预测及拟合优度 `R²`。该模型适合展示从数据、假设、参数到评价指标的完整建模链路。

## 快速开始

```bash
python -m modeling_casebook.demo
python -m unittest discover -s tests -v
```

运行演示会读取 `data/decision_matrix.csv`，并输出三个模型的结构化 JSON 结果。

## 项目结构

```text
src/modeling_casebook/
├── topsis.py             # 多指标决策
├── facility_location.py  # 离散选址优化
├── forecasting.py        # 线性趋势预测
└── demo.py               # 可复现实验入口
```

## 建模规范

- 在代码和 README 中明确目标、约束、假设和评价指标；
- 对输入维度、权重、指标方向和参数范围做验证；
- 用小规模、可手算的单元测试验证关键结论；
- 区分“演示模型”与可直接用于业务决策的生产模型。

## 仓库标签建议

`mathematical-modeling` `operations-research` `topsis` `forecasting` `optimization` `python`

## License

MIT
