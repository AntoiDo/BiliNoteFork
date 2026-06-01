# ASR 测试报告

- 生成时间：2026-04-26
- 运行环境：conda 环境 `testproj`，OS: Linux
- 运行命令：

```bash
conda run -n testproj pytest backend/tests/asr -q
```

## 概要

- 测试套件：`backend/tests/asr`
- 结果：12 passed

## 每个测试项结果

- `test_transcript_basic` (sample): 通过 — 文本拼接包含空格，language 为 `zh`。
- `test_tc_asr_006_core_normal`: 通过 — full_text `你好 世界`，language `zh`，segments 长度 2。
- `test_tc_asr_007_multi_concat`: 通过 — full_text `a b c`。
- `test_tc_asr_008_single_segment`: 通过 — full_text `hello`。
- `test_tc_asr_009_empty_segments`: 通过 — full_text 为空，segments = []。
- `test_tc_asr_010_strip_handling`: 通过 — 去除前后空白，结果 `hello`。
- `test_tc_asr_011_multi_space_concat`: 通过 — 拼接为 `hello world`。
- `test_tc_asr_012_special_chars`: 通过 — 保留特殊字符 (`你好！`、`？`)。
- `test_tc_asr_014_segments_structure_correct`: 通过 — segments 包含 `start`、`end`、`text` 字段。
- `test_tc_asr_015_language_field`: 通过 — result.language == `zh`。
- `test_tc_asr_017_model_exception`: 通过 — 模型抛异常时 `transcript` 返回 `None`（不崩溃）。
- `test_tc_asr_018_return_none_from_model`: 通过 — 模型返回 `(None, None)` 时 `transcript` 返回 `None`。

## Pytest 输出（摘要）

```
conda run -n testproj pytest backend/tests/asr -q
............
12 passed in 4.27s
```

## 备注

- 所有测试通过。测试使用 `unittest.mock` mock 掉了 `WhisperModel`，因此不依赖真实模型文件或外部依赖。
- 若要将报告纳入 CI，可把上述命令加入 CI 脚本并保存此 `results.md` 为构建产物。
