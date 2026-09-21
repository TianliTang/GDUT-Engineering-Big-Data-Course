# 数据质量报告

本报告由固定随机种子生成，说明本教学合成数据中有意保留的质量现象。

## 文件规模

- `public_building_asset_survey.csv`：115,000行，18.50 MiB。
- `retrofit_measure_options.csv`：155,000行，28.92 MiB。
- `retrofit_portfolio_phasing_estimates.csv`：28,800行，4.54 MiB。

## 已设置的教学现象

- `public_building_asset_survey.csv`中约0.20%的建筑面积为空，标记为“面积待复核”。
- `retrofit_measure_options.csv`中约0.21%的记录标记为“减排系数待复核”，保留估算值供学生讨论处理规则。
- 投资、节能和减碳字段为方案阶段估计，包含价格、使用强度和技术适配的扰动，不是竣工结算或法定碳核算数据。
- 所有建筑、资产、片区、权属和数值均为虚构教学数据，不代表真实公共建筑资产台账。
