# Video Presentation Outline (12 Minutes)
# 视频演示大纲（12分钟）

---

## Team | 团队
**Alan (Xiangyu Wu 吴翔宇) | Zheng Congyun 郑聪云 | He Yu 何雨 | Ma Shuting 马舒婷**

---

## Timing Guide | 时间分配

| Section 部分 | Speaker 演讲者 | Time 时间 |
|--------------|----------------|-----------|
| Slides 1-2: Intro 介绍 | Alan | 1:30 |
| Slides 3-4:  | Zheng Congyun | 3:00 |
| Slides 5-8:  | He Yu | 4:00 |
| Slides 9-13:  | Ma Shuting | 3:30 |

---

# SLIDES | 幻灯片

---

## SLIDE 1: Title (0:00-0:30)
## 幻灯片1：标题（0:00-0:30）

**Speaker | 演讲者:** Alan

### Title | 标题
**EN:** Does US Energy Structure Change Affect CO2 Emission Intensity?
**中文:** 美国能源结构变化是否影响CO2排放强度？

### Content | 内容
- Team members | 团队成员: Alan, Zheng Congyun, He Yu, Ma Shuting
- Course | 课程: CA6003
- Institution | 机构: NTU 南洋理工大学

### Script | 演讲稿
**EN:** "Welcome to our presentation. Today we explore how changes in the US energy structure affect CO2 emission intensity, demonstrating key data governance practices."

**中文:** "欢迎观看我们的演示。今天我们将探讨美国能源结构的变化如何影响CO2排放强度，同时展示关键的数据治理实践。"

---

## SLIDE 2: Research Question (0:30-1:30)
## 幻灯片2：研究问题（0:30-1:30）

**Speaker | 演讲者:** Alan

### Title | 标题
**EN:** Research Question & Data Sources
**中文:** 研究问题与数据来源

### Key Points | 要点
- **Question | 问题:** Does energy structure affect CO2 intensity? | 能源结构是否影响CO2强度？
- **Data | 数据:** EIA Monthly Energy Review | 美国能源信息署月度报告
- **Period | 期间:** 1973-2024 (52 years | 52年)

### Script | 演讲稿
**EN:** "Our research examines whether the changing mix of fossil fuels, renewables, and nuclear affects how much CO2 we emit per unit of energy. We used official US government data covering 52 years."

**中文:** "我们的研究探讨化石燃料、可再生能源和核能的比例变化是否影响每单位能源的CO2排放量。我们使用了覆盖52年的美国政府官方数据。"

---

## SLIDE 3: Data Quality Issues (1:30-3:00)
## 幻灯片3：数据质量问题（1:30-3:00）

**Speaker | 演讲者:** Zheng Congyun 郑聪云

### Title | 标题
**EN:** Data Profiling: Issues Discovered
**中文:** 数据分析：发现的问题

### Key Points | 要点

| Issue 问题 | Impact 影响 | Solution 解决方案 |
|------------|-------------|-------------------|
| Wrong data type 数据类型错误 | Cannot calculate 无法计算 | Convert to numeric 转换为数值 |
| "Not Available" strings | Missing values 缺失值 | Convert to NaN |
| Mixed granularity 混合粒度 | Double counting 重复计算 | Filter to annual 过滤为年度 |

### Script | 演讲稿
**EN:** "Before analysis, we profiled the raw data. We found critical issues - wrong data types, missing values coded as strings, and mixed monthly/annual data. These would have broken our analysis if not addressed."

**中文:** "在分析之前，我们对原始数据进行了分析。我们发现了关键问题——数据类型错误、以字符串形式编码的缺失值、以及月度和年度数据混合。如果不处理这些问题，我们的分析将无法进行。"

---

## SLIDE 4: Data Preparation (3:00-4:30)
## 幻灯片4：数据准备（3:00-4:30）

**Speaker | 演讲者:** Zheng Congyun 郑聪云

### Title | 标题
**EN:** Data Cleaning & Feature Engineering
**中文:** 数据清洗与特征工程

### Key Points | 要点
1. Filter to annual data (month code = "13") | 过滤为年度数据（月份代码="13"）
2. Convert to numeric types | 转换为数值类型
3. Merge energy + CO2 datasets | 合并能源和CO2数据集
4. Calculate derived features | 计算衍生特征:
   - FossilShare = Fossil / Total × 100
   - RenewableShare = Renewable / Total × 100
   - **CO2Intensity = CO2 / TotalEnergy**

### Script | 演讲稿
**EN:** "We systematically cleaned the data - filtering to annual records, converting types, and merging datasets. The key feature engineering step was creating CO2 Intensity, our target variable measuring emissions per unit energy."

**中文:** "我们系统地清洗了数据——过滤为年度记录、转换类型、合并数据集。关键的特征工程步骤是创建CO2强度，这是我们衡量每单位能源排放量的目标变量。"

---

## SLIDE 5: Energy Structure Evolution (4:30-5:30)
## 幻灯片5：能源结构演变（4:30-5:30）

**Speaker | 演讲者:** He Yu 何雨

### Title | 标题
**EN:** 52 Years of US Energy Structure Change
**中文:** 美国能源结构52年的变化

### Visual | 可视化
**fig1_energy_structure.png** (Stacked Area Chart | 堆叠面积图)

### Key Statistics | 关键统计
- Fossil 化石能源: 95.3% (1973) → 82.2% (2024) = **-13.1%**
- Renewable 可再生能源: 3.4% → 9.2% = **+5.8%**
- Nuclear 核能: 1.2% → 8.6% = +7.4%

### Script | 演讲稿
**EN:** "This visualization shows 52 years of energy evolution. Fossil fuels dominated at 95% in 1973 but declined to 82% by 2024. Renewables nearly tripled their share."

**中文:** "这张可视化图展示了52年的能源演变。1973年化石燃料占95%的主导地位，但到2024年下降到82%。可再生能源的份额几乎增加了两倍。"

---

## SLIDE 6: CO2 Intensity Trend (5:30-6:30)
## 幻灯片6：CO2强度趋势（5:30-6:30）

**Speaker | 演讲者:** He Yu 何雨

### Title | 标题
**EN:** CO2 Intensity Declining Over Time
**中文:** CO2强度随时间下降

### Visual | 可视化
**fig2_co2_intensity_trend.png** (Dual-axis chart | 双轴图)

### Key Statistics | 关键统计
- CO2 Intensity CO2强度: 64.0 → 50.7 = **-20.8%**
- Accelerated decline after 2014 | 2014年后加速下降

### Script | 演讲稿
**EN:** "CO2 intensity has fallen by over 20% since 1973. Notice the decline accelerates after 2014, suggesting the energy transition is having real impact."

**中文:** "自1973年以来，CO2强度下降了超过20%。注意2014年后下降加速，表明能源转型正在产生实际影响。"

---

## SLIDE 7: Correlation Analysis (6:30-7:30)
## 幻灯片7：相关性分析（6:30-7:30）

**Speaker | 演讲者:** He Yu 何雨

### Title | 标题
**EN:** Strong Correlations Confirmed
**中文:** 确认存在强相关性

### Visual | 可视化
**fig4_correlation_matrix.png** + **fig5_scatter_shares_vs_intensity.png**

### Key Statistics | 关键统计
| Variable 变量 | Correlation 相关性 |
|---------------|---------------------|
| Fossil Share 化石能源占比 | r = **+0.881** (strong positive 强正相关) |
| Renewable Share 可再生能源占比 | r = **-0.946** (very strong negative 极强负相关) |
| Nuclear Share 核能占比 | r = -0.662 (moderate negative 中等负相关) |

### Script | 演讲稿
**EN:** "Correlation analysis confirms strong relationships. Fossil share has strong positive correlation with CO2 intensity. Renewables show the strongest negative correlation at -0.946."

**中文:** "相关性分析确认了强关系。化石能源占比与CO2强度呈强正相关。可再生能源显示出最强的负相关，达到-0.946。"

---

## SLIDE 8: Multicollinearity (7:30-8:00)
## 幻灯片8：多重共线性（7:30-8:00）

**Speaker | 演讲者:** He Yu 何雨

### Title | 标题
**EN:** Data Governance Insight: Multicollinearity
**中文:** 数据治理洞察：多重共线性

### Key Points | 要点
- Fossil + Renewable + Nuclear ≈ 100%
- Creates perfect multicollinearity | 产生完全多重共线性
- Solution | 解决方案: Use only 2 predictors | 仅使用2个预测变量
- **This is structural, not an error | 这是结构性的，不是错误**

### Script | 演讲稿
**EN:** "We discovered multicollinearity - the three shares sum to 100%. This means we can't use all three as predictors. This is an important data governance consideration, not a data error."

**中文:** "我们发现了多重共线性——三个份额之和为100%。这意味着我们不能同时使用这三个作为预测变量。这是一个重要的数据治理考虑因素，而不是数据错误。"

---

## SLIDE 9: Model Performance (8:00-9:00)
## 幻灯片9：模型性能（8:00-9:00）

**Speaker | 演讲者:** Ma Shuting 马舒婷

### Title | 标题
**EN:** Machine Learning Results
**中文:** 机器学习结果

### Visual | 可视化
**fig9_model_comparison.png**

### Key Results | 关键结果
| Model 模型 | R² Score |
|------------|----------|
| Full Data Linear Regression 全数据线性回归 | **0.920** |
| Decision Tree 决策树 | 0.996 |
| Time-Split Test 时间拆分测试 | -3.91 |

### Script | 演讲稿
**EN:** "Our Linear Regression achieves R² of 0.92 - excellent fit. But notice the time-split test shows negative R². This reveals something important..."

**中文:** "我们的线性回归达到了0.92的R²——非常好的拟合。但注意时间拆分测试显示负R²。这揭示了一些重要的东西..."

---

## SLIDE 10: Structural Break Discovery (9:00-10:00)
## 幻灯片10：结构性断裂发现（9:00-10:00）

**Speaker | 演讲者:** Ma Shuting 马舒婷

### Title | 标题
**EN:** Key Discovery: Structural Break (2014)
**中文:** 关键发现：结构性断裂（2014年）

### Visual | 可视化
**fig12_final_summary.png** (with 2014 highlighted | 突出显示2014年)

### Key Points | 要点
- Model trained on 1973-2013 **underestimates** 2014-2024 decline
  基于1973-2013训练的模型**低估了**2014-2024的下降
- CO2 intensity dropped **faster** than predicted
  CO2强度下降**快于**预测
- Causes | 原因: Renewable adoption, coal retirement, policy changes
  可再生能源普及、煤电退役、政策变化
- **Time-based split exposed this - random split would hide it!**
  **基于时间的拆分暴露了这一点——随机拆分会隐藏它！**

### Script | 演讲稿
**EN:** "Here's our most important insight. The model underestimates recent decline. This 'structural break' around 2014 shows accelerating decarbonization. Using time-based split - a best practice - helped us discover this."

**中文:** "这是我们最重要的发现。模型低估了最近的下降。2014年左右的这种'结构性断裂'显示脱碳正在加速。使用基于时间的拆分——一种最佳实践——帮助我们发现了这一点。"

---

## SLIDE 11: Model Interpretation (10:00-10:30)
## 幻灯片11：模型解释（10:00-10:30）

**Speaker | 演讲者:** Ma Shuting 马舒婷

### Title | 标题
**EN:** What the Model Tells Us
**中文:** 模型告诉我们什么

### Key Points | 要点
- 1% ↑ Fossil Share → **+0.31** ↑ CO2 Intensity
  化石能源占比增加1% → CO2强度增加0.31
- 1% ↑ Renewable Share → **-1.60** ↓ CO2 Intensity
  可再生能源占比增加1% → CO2强度降低1.60
- **Renewables have 5x the impact of fossil reduction**
  **可再生能源的影响是化石燃料减少的5倍**

### Script | 演讲稿
**EN:** "The model shows renewables have 5 times greater impact than fossil fuel reduction on CO2 intensity. The energy transition is highly effective."

**中文:** "模型显示，在CO2强度方面，可再生能源的影响是化石燃料减少的5倍。能源转型非常有效。"

---

## SLIDE 12: Conclusions (10:30-11:30)
## 幻灯片12：结论（10:30-11:30）

**Speaker | 演讲者:** All Members 所有成员

### Title | 标题
**EN:** Conclusions & Data Governance Lessons
**中文:** 结论与数据治理经验

### Research Answer | 研究答案
**YES** - Energy structure significantly affects CO2 intensity (R² = 0.92)
**是的** - 能源结构显著影响CO2强度（R² = 0.92）

### Data Governance Lessons | 数据治理经验
1. **Profile before analyze** | **分析前先进行数据分析**
2. **Feature engineering enables insight** | **特征工程能够产生洞察**
3. **Time-aware splits matter** | **时间感知的拆分很重要**
4. **Understanding > accuracy** | **理解比准确性更重要**

### Script | 演讲稿
**EN:** "In conclusion: Yes, energy structure significantly affects CO2 intensity. More importantly, we demonstrated how proper data governance - profiling, cleaning, feature engineering, thoughtful evaluation - leads to meaningful insights."

**中文:** "总之：是的，能源结构显著影响CO2强度。更重要的是，我们展示了适当的数据治理——数据分析、清洗、特征工程、深思熟虑的评估——如何带来有意义的洞察。"

---

## SLIDE 13: Q&A (11:30-12:00)
## 幻灯片13：问答（11:30-12:00）

### Title | 标题
**EN:** Thank You - Questions?
**中文:** 谢谢 - 有问题吗？

### Content | 内容
- Data Source 数据来源: EIA Monthly Energy Review
- Code 代码: Available in Jupyter Notebook | 可在Jupyter笔记本中获取
- Contact 联系: NTU Email

---

# Presentation Tips | 演示技巧

## Do | 应该做
- Show data profiling issues clearly | 清楚展示数据分析问题
- Explain WHY negative test R² happened | 解释为什么测试R²为负
- Emphasize data governance lessons | 强调数据治理经验
- Use figures from outputs/figures/ | 使用outputs/figures/中的图表

## Don't | 不应该做
- Don't rush data profiling section | 不要匆忙通过数据分析部分
- Don't apologize for negative R² | 不要为负R²道歉
- Don't read slides verbatim | 不要逐字阅读幻灯片
- Don't exceed 12 minutes | 不要超过12分钟

## Key Message | 关键信息
**Data governance enabled meaningful analysis - without it, nothing would work!**
**数据治理使有意义的分析成为可能——没有它，什么都行不通！**
