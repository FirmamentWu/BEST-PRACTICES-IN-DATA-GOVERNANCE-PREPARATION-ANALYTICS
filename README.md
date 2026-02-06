# US Energy Structure and CO2 Emission Intensity Analysis
# 美国能源结构与二氧化碳排放强度分析

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Team | 团队

| Name | Chinese Name | Role |
|------|--------------|------|
| **Alan** | 吴翔宇 (Xiangyu Wu) | Project Lead & Data Engineering 项目负责人与数据工程 |
| **Zheng Congyun** | 郑聪云 | Data Analysis & Visualization 数据分析与可视化 |
| **He Yu** | 何雨 | Machine Learning & Modeling 机器学习与建模 |
| **Ma Shuting** | 马舒婷 | Documentation & Presentation 文档与演示 |

**Course | 课程:** CA6003 - Best Practices in Data Governance, Preparation and Analytics

**Institution | 机构:** Nanyang Technological University (NTU) | 南洋理工大学

---

## Research Question | 研究问题

**EN:** Does the change in US energy structure (fossil/renewable/nuclear shares) affect CO2 emission intensity?

**中文:** 美国能源结构的变化（化石燃料/可再生能源/核能占比）是否影响二氧化碳排放强度？

### Answer | 答案: **YES | 是**

| Metric 指标 | Value 数值 |
|-------------|------------|
| Model R² | **0.9197** |
| Fossil → CO2 | r = **+0.881** |
| Renewable → CO2 | r = **-0.946** |
| CO2 Intensity Change (1973-2024) | **-20.8%** |

---

## Project Structure | 项目结构

```
CA6003_Energy_CO2_Analysis/
│
├── README.md                 # This file | 本文件
├── main.py                   # Main entry point | 主程序入口
├── requirements.txt          # Dependencies | 依赖
│
├── src/                      # Source code | 源代码
│   ├── __init__.py
│   ├── data_loader.py       # Data loading 数据加载
│   ├── data_preparation.py  # Cleaning & features 清洗与特征
│   ├── visualization.py     # Plotting 可视化
│   └── analysis.py          # ML & statistics 机器学习与统计
│
├── data/
│   ├── raw/                 # Original EIA data | 原始EIA数据
│   │   ├── MER_T01_01.csv  # Energy data 能源数据
│   │   └── MER_T11_01.csv  # CO2 data CO2数据
│   └── processed/
│       └── clean_energy_co2_data.csv  # Clean dataset 清洗后数据
│
├── outputs/figures/          # 12 PNG visualizations | 12张可视化图
│
├── notebooks/
│   └── CA6003_Energy_CO2_Analysis.ipynb  # Complete notebook 完整笔记本
│
└── docs/
    ├── EXECUTIVE_SUMMARY.md  # Summary (EN/中文) 摘要
    └── VIDEO_SLIDES_OUTLINE.md  # Presentation guide (EN/中文) 演示指南
```

---

## Quick Start | 快速开始

### Installation | 安装

```bash
# Install dependencies | 安装依赖
pip install -r requirements.txt
```

### Run Analysis | 运行分析

```bash
# Option 1: Run main script | 方法1：运行主脚本
python main.py

# Option 2: Open Jupyter notebook | 方法2：打开Jupyter笔记本
jupyter lab notebooks/CA6003_Energy_CO2_Analysis.ipynb
```

### Use as Module | 作为模块使用

```python
from src.data_loader import load_raw_data
from src.data_preparation import prepare_full_dataset
from src.analysis import run_full_analysis

energy_df, co2_df = load_raw_data("data/raw")
df = prepare_full_dataset(energy_df, co2_df)
results = run_full_analysis(df)
print(f"Model R²: {results['full_model']['metrics']['r2']:.4f}")
```

---

## Key Results | 主要结果

### 52-Year Change (1973-2024) | 52年变化

| Metric 指标 | 1973 | 2024 | Change 变化 |
|-------------|------|------|-------------|
| Fossil Share 化石能源 | 95.3% | 82.2% | -13.1% |
| Renewable Share 可再生能源 | 3.4% | 9.2% | +5.8% |
| CO2 Intensity CO2强度 | 64.05 | 50.69 | **-20.8%** |

### Model Interpretation | 模型解释

- 1% ↑ Fossil → +0.31 ↑ CO2 Intensity | 化石能源增加1% → CO2强度增加0.31
- 1% ↑ Renewable → -1.60 ↓ CO2 Intensity | 可再生能源增加1% → CO2强度降低1.60
- **Renewables have 5x the impact** | **可再生能源影响是化石燃料的5倍**

---

## Data Governance Insights | 数据治理洞察

### Issues Addressed | 已处理的问题

| Issue 问题 | Solution 解决方案 |
|------------|-------------------|
| String types 字符串类型 | Convert to numeric 转为数值 |
| "Not Available" | Handle as NaN |
| Mixed granularity 混合粒度 | Filter annual 过滤年度 |
| Multicollinearity 多重共线性 | Use 2 predictors 使用2个预测变量 |

### Key Discovery | 关键发现

**Structural Break (2014) | 结构性断裂**

Models trained on 1973-2013 underestimate 2014-2024 CO2 decline. Time-based splits revealed this - random splits would have hidden it.

基于1973-2013训练的模型低估了2014-2024的CO2下降。基于时间的拆分揭示了这一点——随机拆分会隐藏它。

---

## Visualizations | 可视化

| Figure | Description 描述 |
|--------|------------------|
| fig1 | Energy structure stacked area 能源结构堆叠图 |
| fig2 | CO2 intensity trend CO2强度趋势 |
| fig4 | Correlation matrix 相关矩阵 |
| fig5 | Scatter plots 散点图 |
| fig6 | Distributions 分布图 |
| fig12 | Final summary 最终摘要 |

---

## Documentation | 文档

| File 文件 | Description 描述 |
|-----------|------------------|
| `docs/EXECUTIVE_SUMMARY.md` | 1-page summary (EN/中文) 单页摘要 |
| `docs/VIDEO_SLIDES_OUTLINE.md` | 12-min presentation script (EN/中文) 演示脚本 |

---

## Data Source | 数据来源

**U.S. Energy Information Administration (EIA)**
**美国能源信息署**

- Energy: Monthly Energy Review Table 1.1 | 能源：月度报告表1.1
- CO2: Monthly Energy Review Table 11.1 | CO2：月度报告表11.1
- Link 链接: https://www.eia.gov/totalenergy/data/monthly/

---

## Requirements | 依赖

```
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.12.0
scipy>=1.9.0
scikit-learn>=1.1.0
jupyter>=1.0.0
```

---

## Conclusions | 结论

### Research Answer | 研究答案

**Does US energy structure change affect CO2 emission intensity?**
**美国能源结构变化是否影响CO2排放强度？**

## **YES - Significant Impact Confirmed | 是的 - 确认存在显著影响**

---

### Key Findings | 主要发现

#### 1. Quantitative Results | 定量结果

| Metric 指标 | 1973 | 2024 | Change 变化 |
|-------------|------|------|-------------|
| Fossil Share 化石能源占比 | 95.3% | 82.2% | **-13.1%** |
| Renewable Share 可再生能源占比 | 3.4% | 9.2% | **+5.8%** |
| CO2 Intensity CO2强度 | 64.05 | 50.69 | **-20.8%** |

#### 2. Correlation Analysis | 相关性分析

| Variable 变量 | Correlation 相关性 | Interpretation 解释 |
|---------------|-------------------|---------------------|
| Fossil Share 化石能源 | r = **+0.881** | Strong positive 强正相关 |
| Renewable Share 可再生能源 | r = **-0.946** | Very strong negative 极强负相关 |

**Model Performance 模型性能:** R² = **0.9197** (explains 92% of variance | 解释92%的变异)

#### 3. Key Insight | 关键洞察

**Renewables have 5x greater impact than fossil fuel reduction:**
**可再生能源的影响是化石燃料减少的5倍：**

- 1% ↑ Fossil Share → +0.31 ↑ CO2 Intensity | 化石能源占比增加1% → CO2强度增加0.31
- 1% ↑ Renewable Share → **-1.60** ↓ CO2 Intensity | 可再生能源占比增加1% → CO2强度降低1.60

#### 4. Data Governance Discovery | 数据治理发现

**Structural Break (2014) | 结构性断裂（2014年）**

**EN:** After 2014, CO2 intensity declined **faster** than historical models predicted. Causes:
- Renewable energy technology breakthroughs
- Large-scale coal plant retirements
- Policy drivers (Paris Agreement, etc.)

**中文:** 2014年后，CO2强度下降速度**超出**历史模型预测。原因：
- 可再生能源技术突破
- 煤电厂大规模退役
- 政策推动（巴黎协定等）

---

### Final Summary | 最终总结

**EN:**
1. **Energy transition is effective** — Shifting from fossil fuels to renewables reduced CO2 intensity by 20.8% over 52 years
2. **Renewables are more efficient** — Increasing renewable share has greater impact on reducing CO2 than reducing fossil share
3. **Data governance matters** — Proper data processing and time series analysis revealed the accelerating decarbonization trend after 2014

**中文:**
1. **能源转型有效** — 从化石燃料转向可再生能源，52年间CO2强度降低了20.8%
2. **可再生能源更高效** — 增加可再生能源比减少化石燃料对降低CO2的效果更显著
3. **数据治理很重要** — 通过正确的数据处理和时间序列分析，发现了2014年后的加速脱碳趋势

---

### One-Sentence Conclusion | 一句话结论

**EN:** The US energy transition towards renewables has significantly reduced CO2 emission intensity, and this trend accelerated after 2014.

**中文:** 美国能源结构向可再生能源转型显著降低了CO2排放强度，且这一趋势在2014年后加速。

---

*CA6003 - NTU | February 2026*
