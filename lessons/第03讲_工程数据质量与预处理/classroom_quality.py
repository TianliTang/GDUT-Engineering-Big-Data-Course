"""第3次课课堂用数据质量检查函数。

函数只封装R04和R06的带做流程，便于Python初学者把注意力放在
规则、问题记录、处理动作和理由上。正式章级Notebook包含完整R01—R11管线。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


MISSING_TOKENS = {"", "na", "n/a", "--", "null", "none"}
TIME_FORMATS = (
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%Y年%m月%d日 %H:%M",
)
BUSINESS_KEY = ["component_id", "inspection_round"]


def normalize_missing(value):
    """把课堂数据中的常见特殊缺失码统一为pandas缺失值。"""
    text = "" if pd.isna(value) else str(value).strip()
    return pd.NA if text.lower() in MISSING_TOKENS else text


def parse_teaching_time(value):
    """只按数据卡列出的显式时间格式解析，解析失败返回NaT。"""
    value = normalize_missing(value)
    if pd.isna(value):
        return pd.NaT
    for time_format in TIME_FORMATS:
        try:
            return pd.to_datetime(str(value), format=time_format, errors="raise")
        except (ValueError, TypeError, OverflowError):
            continue
    return pd.NaT


def load_classroom_inputs(base_dir: str | Path = "."):
    """读取课堂数据、规则、映射和数据字典。"""
    base_dir = Path(base_dir)
    data_dir = base_dir / "data"
    raw = pd.read_csv(data_dir / "M03_安装质检示例数据.csv", dtype="string")
    rules = pd.read_csv(data_dir / "M04_质量规则表.csv", dtype="string")
    mapping = pd.read_csv(data_dir / "M05_类别与单位映射表.csv", dtype="string")
    dictionary = pd.read_csv(data_dir / "M06_数据字典.csv", dtype="string")
    raw.insert(0, "source_row_number", np.arange(1, len(raw) + 1))
    return raw, rules, mapping, dictionary


def _mapping_for(mapping: pd.DataFrame, field_name: str) -> dict[str, str]:
    part = mapping.loc[mapping["field_name"].eq(field_name)]
    return dict(zip(part["raw_value"].astype(str), part["canonical_value"].astype(str)))


def standardize_for_classroom(raw: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    """保留原值，并生成R04/R06所需的规范字段。"""
    standardized = raw.copy()
    original_fields = [column for column in raw.columns if column != "source_row_number"]

    for field in original_fields:
        standardized[f"raw_{field}"] = standardized[field]
        standardized[field] = standardized[field].map(normalize_missing)

    for field in ["install_time", "inspection_time", "record_created_time"]:
        standardized[f"{field}_parsed"] = standardized[field].map(parse_teaching_time)

    standardized["deviation_value_numeric"] = pd.to_numeric(
        standardized["vertical_deviation_value"], errors="coerce"
    )
    standardized["deviation_unit_standard"] = standardized["deviation_unit"].map(
        _mapping_for(mapping, "deviation_unit")
    )
    standardized["vertical_deviation_mm"] = np.where(
        standardized["deviation_unit_standard"].eq("cm"),
        standardized["deviation_value_numeric"] * 10.0,
        np.where(
            standardized["deviation_unit_standard"].eq("mm"),
            standardized["deviation_value_numeric"],
            np.nan,
        ),
    )
    return standardized


def duplicate_overview(standardized: pd.DataFrame) -> pd.DataFrame:
    """生成课堂讲解用重复概况，不执行删除或版本解析。"""
    raw_fields = [column for column in standardized.columns if column.startswith("raw_")]
    exact_extra = standardized.duplicated(raw_fields, keep="first")
    non_exact = standardized.loc[~exact_extra].copy()
    complete_key = non_exact[BUSINESS_KEY].notna().all(axis=1)
    group_sizes = (
        non_exact.loc[complete_key]
        .groupby(BUSINESS_KEY, dropna=False)
        .size()
    )
    business_groups = int(group_sizes.gt(1).sum())
    business_extra = int((group_sizes.loc[group_sizes.gt(1)] - 1).sum())
    return pd.DataFrame(
        {
            "检查项": ["发布记录数", "完全重复多余行", "业务重复组", "业务重复多余版本"],
            "数量": [len(standardized), int(exact_extra.sum()), business_groups, business_extra],
        }
    )


def _rule_meta(rules: pd.DataFrame, rule_id: str) -> dict[str, str]:
    selected = rules.loc[rules["rule_id"].eq(rule_id)]
    if selected.empty:
        raise ValueError(f"规则表中不存在{rule_id}")
    return selected.iloc[0].fillna("").astype(str).to_dict()


def build_classroom_issue_log(
    standardized: pd.DataFrame,
    rules: pd.DataFrame,
) -> pd.DataFrame:
    """运行课堂聚焦规则R04和R06，输出可追踪的问题清单。"""
    issues: list[dict[str, object]] = []

    def add(mask: pd.Series, rule_id: str, affected_fields: str, detail: str):
        meta = _rule_meta(rules, rule_id)
        columns = [
            "source_row_number",
            "inspection_id",
            "component_id",
            "inspection_round",
            "raw_install_time",
            "raw_inspection_time",
            "raw_deviation_unit",
            "raw_vertical_deviation_value",
        ]
        for row in standardized.loc[mask, columns].itertuples(index=False):
            if rule_id == "R04":
                raw_values = f"install_time={row.raw_install_time}; inspection_time={row.raw_inspection_time}"
            else:
                raw_values = (
                    f"vertical_deviation_value={row.raw_vertical_deviation_value}; "
                    f"deviation_unit={row.raw_deviation_unit}"
                )
            issues.append(
                {
                    "rule_id": rule_id,
                    "source_row_number": int(row.source_row_number),
                    "inspection_id": "" if pd.isna(row.inspection_id) else str(row.inspection_id),
                    "component_id": "" if pd.isna(row.component_id) else str(row.component_id),
                    "inspection_round": "" if pd.isna(row.inspection_round) else str(row.inspection_round),
                    "affected_fields": affected_fields,
                    "raw_values": raw_values,
                    "issue_detail_zh": detail,
                    "severity": meta["severity"],
                    "reference_action": meta["suggested_action"],
                }
            )

    install = standardized["install_time_parsed"]
    inspection = standardized["inspection_time_parsed"]
    r04_mask = install.isna() | inspection.isna() | inspection.lt(install)
    add(
        r04_mask,
        "R04",
        "install_time;inspection_time",
        "时间无法解析或检查早于安装",
    )

    r06_mask = standardized["deviation_unit_standard"].isna()
    add(
        r06_mask,
        "R06",
        "vertical_deviation_value;deviation_unit",
        "偏差单位无法按显式映射表识别",
    )

    return pd.DataFrame(issues).sort_values(
        ["rule_id", "source_row_number"]
    ).reset_index(drop=True)


def issue_count_table(issue_log: pd.DataFrame) -> pd.DataFrame:
    """按规则汇总问题记录数。"""
    return (
        issue_log.groupby("rule_id", as_index=False)["source_row_number"]
        .nunique()
        .rename(columns={"source_row_number": "issue_count"})
        .sort_values("rule_id")
        .reset_index(drop=True)
    )


def select_student_evidence(
    issue_log: pd.DataFrame,
    focus_rule_id: str,
    selected_result_row: int,
    student_action: str,
    student_reason: str,
) -> pd.DataFrame:
    """选出一条问题记录，并附上学生填写的动作与理由。"""
    focus = issue_log.loc[issue_log["rule_id"].eq(focus_rule_id)].reset_index(drop=True)
    if focus.empty:
        raise ValueError(f"{focus_rule_id}没有问题记录")
    if not 0 <= selected_result_row < len(focus):
        raise IndexError(
            f"SELECTED_RESULT_ROW应在0到{len(focus) - 1}之间，当前为{selected_result_row}"
        )
    result = focus.iloc[[selected_result_row]].copy()
    result["student_action"] = student_action.strip()
    result["student_reason"] = student_reason.strip()
    return result

