from collectors.dart_collector import DartCollector

dart = DartCollector()

corp_code = dart.get_corp_code("삼성전자")

raw = dart.get_disclosure_list(
    corp_code,
    "20240101",
    "20251231",
)

# 원본 그대로 저장
dart.save_json(
    raw,
    "data/raw/samsung/disclosure_list.json",
)

# 분석용 DataFrame 생성
df = dart.to_dataframe(raw)

# 사업/반기/분기보고서만 추출
reports = dart.filter_reports(df)

print(reports.head())