# 数据质量报告

本报告由固定随机种子生成，说明本教学合成数据中有意保留的质量现象。

## 文件规模

- `household_resettlement_demand.csv`：150,000行，23.18 MiB。
- `resettlement_scheme_building_plan.csv`：120,000行，23.75 MiB。
- `scheme_multi_scenario_assessment.csv`：25,920行，3.73 MiB。

## 已设置的教学现象

- `household_resettlement_demand.csv`中约0.25%的原住房面积为空，标记为“原面积待核”。
- `resettlement_scheme_building_plan.csv`中约0.21%的记录标记为“配套面积待复核”，保留原值供学生决定处理规则。
- 方案成本、安置能力、周期和碳排估计含情景扰动；它们用于比选练习，不表示真实可研结论。
- 所有住户、片区、地块和数值均为虚构教学数据，不代表真实城市更新项目或居民调查。
