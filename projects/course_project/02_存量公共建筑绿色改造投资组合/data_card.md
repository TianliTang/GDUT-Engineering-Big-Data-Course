# 数据说明卡：存量公共建筑绿色改造投资组合

| 项目 | 说明 |
|---|---|
| 数据集编号与版本 | EBD-P-B02 v2.1 |
| 数据性质 | 教学合成数据 |
| 教学目的 | 支持公共建筑绿色改造前期数据中的措施梳理、长期效益测算、记录复核和实施准备 |
| 虚拟背景 | 16个片区的学校、医疗、办公、文化体育和社区服务建筑资产，以及多种前期改造措施和组合分期方案 |
| 时间范围 | 2026年资产调查与2027—2031年虚拟改造规划 |
| 生成脚本与随机种子 | `../generate_planning_project_data.py`；`SEED_B = 2026092002` |
| 文件版本 | 以`checksums.sha256`为准 |
| 使用范围 | 存量公共建筑绿色改造前期投资方案讨论教学 |
| 不支持的用途 | 真实资产台账、能耗审计、法定碳核算、财政预算或项目审批 |

## 一、三张表与分析对象

```text
public_building_asset_survey（每行一个虚拟建筑资产）
                  │ 通过asset_id关联
                  ▼
retrofit_measure_options（每行一个建筑—措施包估计）
                  │ 按片区、组合和年度汇总
                  ▼
retrofit_portfolio_phasing_estimates（每行一个投资组合—年度—情景记录）
```

资产表描述改造对象；措施表描述某建筑采用某类措施包的前期估算；组合分期表描述不同资金、能源价格和服务连续性条件下的年度投资安排。连接时需要先确定对象是建筑、建筑—措施，还是组合—年度—情景。

## 二、表说明

| 表名 | 行代表什么 | 主键 | 关联字段 | 适合的分析起点 |
|---|---|---|---|---|
| `public_building_asset_survey.csv` | 一个虚拟公共建筑资产 | `asset_id` | `district_id`、`service_cluster_id` | 建筑特征补充、关联检查和信息完整度审查 |
| `retrofit_measure_options.csv` | 一个建筑对应的一种改造措施包估计 | `option_id` | `asset_id`、`district_id` | 措施梳理、长期效益测算、记录复核和实施准备的主要分析表 |
| `retrofit_portfolio_phasing_estimates.csv` | 一个组合在某年度和情景下的分期估计 | `portfolio_record_id` | `portfolio_id`、`district_id` | 理解前期规划数据的另一种粒度；不作为本包四个项目任务的必选表 |

完整字段、单位、编码和取值规则见`data_dictionary.csv`。缺失值以空字符串保存。

## 三、主要字段组

| 字段组 | 典型字段 | 作用 |
|---|---|---|
| 建筑资产 | `building_type`、`gross_floor_area_m2`、`annual_energy_kwh`、`current_condition_score` | 描述改造对象的规模、能耗和状态 |
| 改造措施 | `measure_package`、`estimated_investment_million`、`annual_carbon_reduction_tco2e`、`service_interruption_days` | 比较不同措施的投资、减碳和服务影响 |
| 长期影响 | `simple_payback_years`、`estimated_embodied_carbon_tco2e`、`net_carbon_reduction_20y_tco2e` | 讨论回收期与长期净减碳 |
| 组合分期 | `phase_year`、`annual_investment_million`、`cumulative_carbon_reduction_tco2e` | 比较年度投入、累计收益和分期节奏 |
| 实施条件 | `implementation_window`、`technical_compatibility_level`、`implementation_risk_index` | 识别与解释实施风险 |

## 四、生成逻辑与质量现象

建筑资产由建筑类型、面积、房龄、围护结构、暖通状态、使用强度和服务连续性要求共同构成。措施估计由资产规模、措施包、技术适配、施工窗口和服务影响共同构成。组合分期估计改变资金、能源价格和服务连续性假设，形成不同年度安排。

数据中有少量面积待复核和减排系数待复核记录。投资、节能和减碳均为前期估算，含有不确定性扰动。所有建筑、资产、片区和数值均为虚构，不对应真实公共建筑台账。

## 五、建议的分析边界

- 改造措施梳理：选择连续指标前先确认它们表达的是同一个建筑—措施对象，并处理量纲差异。
- 长期效益前期测算：以建筑—措施为对象；同一结果的直接构成项不能同时用于形成测算。
- 措施估算复核：待复核记录要回到原始字段和关联记录核对，不能据此认定真实项目存在问题。
- 改造实施准备：实施风险指数不能直接用于形成需要复核的判断。
