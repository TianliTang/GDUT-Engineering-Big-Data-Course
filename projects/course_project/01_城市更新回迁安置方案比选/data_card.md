# 数据说明卡：城市更新回迁安置方案比选

| 项目 | 说明 |
|---|---|
| 数据集编号与版本 | EBD-P-A02 v2.1 |
| 数据性质 | 教学合成数据 |
| 教学目的 | 支持区域城市更新前期数据中的方案测算、论证准备、特征梳理和记录复核 |
| 虚拟背景 | 12个更新片区、120个原居住街坊、候选建设地块与多套回迁安置方案 |
| 时间范围 | 2026年虚拟调查与方案测算轮次 |
| 生成脚本与随机种子 | `../generate_planning_project_data.py`；`SEED_A = 2026092001` |
| 文件版本 | 以`checksums.sha256`为准 |
| 使用范围 | 前期规划、可研比选和投资方案讨论教学 |
| 不支持的用途 | 真实征收补偿、住户资格认定、项目立项、土地审批或投资决策 |

## 一、三张表与分析对象

```text
household_resettlement_demand（每行一个虚拟住户调查记录）
                  │ 按更新片区、街坊汇总需求
                  ▼
resettlement_scheme_building_plan（每行一个方案构成记录）
                  │ 按方案、地块、分期汇总供给与估算
                  ▼
scheme_multi_scenario_assessment（每行一个方案—情景评估）
```

住户表描述需求；方案构成表描述备选方案中的建筑、户型、地块和分期；方案情景表记录同一方案在价格、安置意愿和建设波动条件下的估计结果。三表不是一行一行直接拼接的关系。需要先决定分析对象是住户、街坊、片区、方案，还是方案—情景。

## 二、表说明

| 表名 | 行代表什么 | 主键 | 关联字段 | 适合的分析起点 |
|---|---|---|---|---|
| `household_resettlement_demand.csv` | 一个虚拟住户调查记录 | `household_id` | `renewal_area_id`、`block_id` | 理解安置需求数据的另一种粒度与关联检查 |
| `resettlement_scheme_building_plan.csv` | 一个方案中某地块、分期、建筑类型和户型的构成记录 | `plan_record_id` | `scheme_id`、`renewal_area_id`、`block_id` | 方案特征汇总、关联检查和异常复核 |
| `scheme_multi_scenario_assessment.csv` | 一个方案在一组前期假设下的估算结果 | `assessment_id` | `scheme_id`、`renewal_area_id` | 方案前期测算、论证准备、特征梳理和记录复核的主要分析表 |

完整字段、单位、编码和取值规则见`data_dictionary.csv`。缺失值以空字符串保存；日期字段采用`YYYY-MM-DD`。

## 三、主要字段组

| 字段组 | 典型字段 | 作用 |
|---|---|---|
| 安置需求 | `registered_persons`、`preferred_unit_type`、`minimum_unit_area_m2`、`temporary_housing_need` | 识别住户规模、户型、过渡安置和服务需求 |
| 方案构成 | `parcel_id`、`phase_id`、`planned_resettlement_units`、`average_unit_area_m2` | 描述方案怎样配置地块、分期和户型供给 |
| 投资与碳排估计 | `*_cost_million`、`*_carbon_tco2e`、`estimated_total_investment_million` | 比较方案的投资结构和情景估算结果 |
| 安置成效 | `resettlement_capacity_households`、`target_coverage_pct`、`resettlement_satisfaction_score` | 比较安置能力与需求匹配情况 |
| 实施条件 | `expected_completion_months`、`peak_temporary_households`、`overall_risk_index` | 讨论分期、过渡安置压力和实施风险 |

## 四、生成逻辑与质量现象

住户需求由家庭规模、原住房面积、房龄、公共服务需求和安置偏好共同构成。方案记录由片区土地压力、地块、户型、分期和建筑类型构成。方案情景评估改变价格、安置意愿和建设波动假设，使同一方案在不同条件下呈现不同投资、安置能力、周期和风险。

数据包含少量原面积缺失、配套面积待复核和情景参数待核标记。具体数量见`quality_report.md`。所有片区、住户、地块和数值均为虚构，不对应真实居民、城市更新项目或行业分布。

## 五、建议的分析边界

- 方案前期测算：方案—情景是合适对象；同一结果的直接构成项不能同时用于形成测算。
- 方案论证准备：综合风险指数不能直接用于形成需要复核的判断。
- 方案特征梳理：先将同一方案的多个情景汇总，再形成方案层面的连续特征。
- 方案测算复核：待复核记录只能进入复核清单，不能直接推出真实项目存在错误。
