# 功能 → 测试映射（BiliNote 项目）

说明：此文档列出仓库中可识别的主要功能模块、每个功能可实施的测试类型，以及推荐使用的测试工具与方法。当前不包含具体测试用例（你已说明不需直接生成用例）。

## 项目概览
- 后端：Python + FastAPI（主要路径见 `backend/app/`）。
- 前端：React + Vite（`BillNote_frontend/`）。
- 目标：对核心业务（视频下载、转写、LLM 汇总、任务管理、前端交互）进行单元、集成、端到端、性能与剖析测试，并用 Jira 做用例/缺陷管理。

## 功能清单与可测项

- 功能：视频/资源下载
  - 可测项：URL 解析、下载成功/失败路径、字幕抓取与解析（SRT/JSON3）、断点续传/超时处理、异常恢复。
  - 建议测试类型：单元测试（解析函数）、集成测试（下载流程，使用本地样例或 mock server）。
  - 推荐工具/方法：`pytest` + `unittest.mock`（后端），可用 sample files 做断言；JMeter 可用于下载接口压力测试（隔离外部服务）。

- 功能：音频提取（FFmpeg 调用）
  - 可测项：命令构建正确性、错误码处理、输出文件完整性。
  - 建议测试类型：集成测试（在 CI/本地 runner 上执行小文件转换）、单元测试（封装函数的参数与异常分支）。
  - 推荐工具/方法：`pytest` + 实际小视频/文件，或将 FFmpeg 调用抽象后 mock。

- 功能：转写/语音识别（Whisper 等）
  - 可测项：不同模型/设备分支（CPU/CUDA）、异常超时、分段合并、输出格式（segments, timestamps）。
  - 建议测试类型：单元（provider 工厂、错误处理）、集成（在受控环境运行小模型或 mock 转写结果）、性能测试（吞吐、延迟）。
  - 推荐工具/方法：`pytest` + mock；性能用 JMeter 或自定义负载脚本；剖析用 `py-spy`/`cProfile`（或 `JProfiler` 若为 JVM）。

- 功能：LLM 交互与文本汇总（gpt 工厂、chunker、断点续传）
  - 可测项：RequestChunker 的分割规则、group-by-budget、checkpoint 保存/恢复、合并部分响应、错误重试。
  - 建议测试类型：单元测试（算法边界）、集成测试（mock 外部 LLM 接口）、回归测试（大文本场景）。
  - 推荐工具/方法：`pytest` + `unittest.mock`/`responses`；对长文本使用基准测试并记录性能数据。

- 功能：Note 生成流程与任务管理（`NoteGenerator`）
  - 可测项：从请求到最终 `note_results` 文件输出、状态更新（status.json）、background task 启动/异常路径、事务一致性（DB 操作）。
  - 建议测试类型：集成测试（使用 TestClient 或直接调用服务类，mock 外部依赖）、端到端（完整流程，使用本地或 stub 服务）。
  - 推荐工具/方法：`pytest` + FastAPI `TestClient`，mock GPT/transcriber/downloader；CI 中作为关键集成测试。

- 功能：数据库 DAO（VideoTask、Model、Provider 等）
  - 可测项：insert/get/delete、迁移/模式兼容、并发写入场景。
  - 建议测试类型：单元/集成（内存 SQLite 运行）。
  - 推荐工具/方法：`pytest` fixtures（sqlite:///:memory:），事务回滚、并发模拟可用 threading 或 pytest-xdist。

- 功能：前端交互（NoteForm、轮询 useTaskPolling、Markdown/Markmap 渲染）
  - 可测项：表单校验、提交行为、文件上传、轮询逻辑（polling 停止/重试）、渲染性能（大 Markdown）、错误提示。
  - 建议测试类型：端到端（自动化浏览器）、组件单元测试（React 组件快照/逻辑）。
  - 推荐工具/方法：Selenium（或 Playwright）+ pytest / JUnit；前端单元可用 Jest/React Testing Library。若使用 Selenium 可用 Python + pytest 或 Java + JUnit（团队偏好决定）。

- 功能：导出（PDF/DOCX）与截图（FFmpeg 截图）
  - 可测项：导出文件生成、格式正确性、图片质量与时间戳精度。
  - 建议测试类型：集成测试（生成小文件并校验存在/基本内容）、回归测试（文件大小/关键断言）。
  - 推荐工具/方法：`pytest` + 文件断言；可用自动化 OCR/文本提取做更严格校验。

- 功能：向量索引/搜索（Vector DB）与 chat 服务
  - 可测项：索引写入、查询相似度正确性、错误处理、并发写入。
  - 建议测试类型：集成测试（用内存/本地轻量向量库或 mock），负载测试（并发索引）。
  - 推荐工具/方法：`pytest` + mock 或轻量向量 DB（如 FAISS 本地实例），JMeter 做负载测试 API 层。

## 测试工具与用途速览（七个工具）
- Jira：测试用例与缺陷管理、自动化执行记录（非执行工具）。
- Selenium：前端 E2E 自动化（表单提交、轮询、渲染断言）。
- JMeter：性能/负载测试（并发 API、压力场景、吞吐/延迟指标）。
- Mock：后端使用 `unittest.mock`/`pytest-mock`，前端使用 `msw` 或 mock server。用于隔离外部 GPT/转写/下载器。
- JUnit：可选—仅当团队用 Java 写 Selenium 测试或需要 JVM 测试栈时使用；否则后端使用 `pytest` 更自然。
- pytest：后端单元/集成测试首选，可运行现有 unittest 测试并扩展 fixtures。
- JProfiler：JVM 剖析工具；若后端为 Python，建议用 `py-spy`/`cProfile` 替代；前端可用 Chrome DevTools/Node profiler。

## 示例测试策略（按优先级）
1. 高优先级（立即实施）
   - `RequestChunker`、`video_task_dao`、下载器字幕解析的单元测试（`pytest`）。
   - `NoteGenerator` 的集成测试：mock GPT/transcriber，验证 `note_results` 文件输出。
   - 前端关键路径 E2E（NoteForm 提交 + 轮询）—一条稳定脚本。

2. 中优先级
   - 转写器与 GPT 的性能基准（小模型或 mock），测量平均延迟。
   - DAO 的并发测试、向量索引集成测试。

3. 低优先级
   - 大规模负载测试（JMeter）与全面剖析（py-spy/JProfiler），在复现瓶颈后执行。

## 运行与集成建议（示例命令）
- 运行后端单元/集成测试：

```bash
cd backend
python -m pytest tests -q
```

- 前端本地调试：

```bash
cd BillNote_frontend
pnpm install
pnpm dev
```

- 运行 E2E（示例，pytest + selenium）：

```bash
pip install selenium pytest pytest-selenium
pytest tests/e2e -q
```

- 运行 JMeter（命令行非 GUI）：

```bash
jmeter -n -t load_test_plan.jmx -l results.jtl -e -o report_dir
```

## 决策点与建议
- JUnit / JProfiler 是否必须：仓库以 Python/TS 为主，建议将 JUnit/JProfiler 作为可选路径，仅在团队或 CI 强制采用 Java 测试栈时使用。替代方案：`pytest` + `py-spy`/`cProfile`。
- 外部 LLM/转写服务必须被 mock 或替换为受控 stub，以保证测试稳定且可重复。

---
文档位置：已生成为 `FEATURES_TEST_MAPPING.md`（项目根）。如需我把其中某些功能拆成具体测试用例清单或直接开始为若干目标文件编写 `pytest` 案例，我可以继续下一步实现。