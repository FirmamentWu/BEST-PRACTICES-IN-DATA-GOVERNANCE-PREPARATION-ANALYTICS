# Executive Summary | 执行摘要

## US Energy Structure and CO2 Emission Intensity Analysis
## 美国能源结构与二氧化碳排放强度分析

---

### Team | 团队
**Alan (Xiangyu Wu 吴翔宇) | Zheng Congyun 郑聪云 | He Yu 何雨 | Ma Shuting 马舒婷**

**Course | 课程:** CA6003 - Best Practices in Data Governance, Preparation and Analytics

**Institution | 机构:** Nanyang Technological University (NTU) | 南洋理工大学

---

## Research Question | 研究问题

**EN:** Does the change in US energy structure (fossil/renewable/nuclear shares) affect CO2 emission intensity?

**中文:** 美国能源结构的变化（化石燃料/可再生能源/核能占比）是否影响二氧化碳排放强度？

---

## Answer | 答案

### YES - Strong Relationship Confirmed | 是 - 确认存在强相关性

| Metric 指标 | Value 数值 |
|-------------|------------|
| Model R² 模型R² | **0.9197** (92% variance explained 方差解释率92%) |
| Fossil → CO2 化石能源→CO2 | r = **+0.881** (strong positive 强正相关) |
| Renewable → CO2 可再生能源→CO2 | r = **-0.946** (very strong negative 极强负相关) |

---

## Key Results | 主要结果

### 52-Year Change (1973-2024) | 52年变化（1973-2024）

| Metric 指标 | 1973 | 2024 | Change 变化 |
|-------------|------|------|-------------|
| Fossil Share 化石能源占比 | 95.3% | 82.2% | **-13.1%** |
| Renewable Share 可再生能源占比 | 3.4% | 9.2% | **+5.8%** |
| Nuclear Share 核能占比 | 1.2% | 8.6% | +7.4% |
| CO2 Intensity CO2强度 | 64.05 | 50.69 | **-20.8%** |

### Model Interpretation | 模型解释

**EN:**
- 1% increase in Fossil Share → +0.31 increase in CO2 Intensity
- 1% increase in Renewable Share → -1.60 decrease in CO2 Intensity
- **Renewables have 5x greater impact than fossil fuel reduction**

**中文:**
- 化石能源占比每增加1% → CO2强度增加0.31
- 可再生能源占比每增加1% → CO2强度降低1.60
- **可再生能源的影响是化石燃料减少影响的5倍**

---

## Critical Data Governance Discovery | 关键数据治理发现

### Structural Break (2014) | 结构性断裂（2014年）

**EN:**
Models trained on 1973-2013 data **underestimate** the CO2 decline after 2014. CO2 intensity dropped **faster** than historical patterns predicted. This reveals accelerating decarbonization.

**中文:**
基于1973-2013年数据训练的模型**低估了**2014年后的CO2下降。CO2强度的下降**快于**历史模式预测。这揭示了加速脱碳的趋势。

**Causes | 原因:**
- Rapid renewable adoption | 可再生能源快速普及
- Coal plant retirements | 煤电厂退役
- Policy changes (Paris Agreement) | 政策变化（巴黎协定）

**Lesson | 经验:**
Time-based train/test splits can reveal structural changes that random splits would hide.
基于时间的训练/测试拆分可以揭示随机拆分会隐藏的结构性变化。

---

## Data Governance Issues Addressed | 已处理的数据治理问题

| Issue 问题 | Solution 解决方案 |
|------------|-------------------|
| String data types 字符串数据类型 | Convert to numeric 转换为数值 |
| "Not Available" values "Not Available"值 | Handle as NaN 处理为NaN |
| Mixed granularity 混合粒度 | Filter to annual only 仅保留年度数据 |
| Multicollinearity 多重共线性 | Use subset of predictors 使用预测变量子集 |

---

## Conclusions | 结论

### EN:
1. **YES** - Energy structure significantly affects CO2 intensity (R² = 0.92)
2. The shift from fossil fuels to renewables reduced CO2 intensity by **20.8%** over 52 years
3. Data governance practices were **essential** for meaningful analysis
4. Understanding data > chasing accuracy metrics

### 中文:
1. **是的** - 能源结构显著影响CO2强度（R² = 0.92）
2. 从化石燃料向可再生能源的转变在52年间使CO2强度降低了**20.8%**
3. 数据治理实践对于有意义的分析**至关重要**
4. 理解数据比追求准确性指标更重要

---

## Caveats | 注意事项

- Correlation ≠ Causation | 相关性 ≠ 因果关系
- Confounders exist: GDP, technology, policy | 存在混杂因素：GDP、技术、政策
- Time series autocorrelation present | 存在时间序列自相关

---

## Data Source | 数据来源

**U.S. Energy Information Administration (EIA) Monthly Energy Review**
**美国能源信息署（EIA）月度能源报告**

- Energy: Table 1.1 (1949-2025) | 能源：表1.1
- CO2: Table 11.1 (1973-2025) | CO2：表11.1
- Analysis Period: 1973-2024 (52 years) | 分析期间：1973-2024（52年）
