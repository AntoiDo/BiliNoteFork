**概览**
- 项目类型：Python (FastAPI) 后端 + React 前端。
- 目标：为主要功能生成“功能 → 测试工具 → 测试方法”映射，覆盖单元/集成/端到端/性能/剖析与测试管理。

**关键测试目标组件**
- 后端路由与任务：`backend/app/routers/note.py`
- 核心业务：`backend/app/services/note.py`（`NoteGenerator`）
- 下载器：`backend/app/downloaders/*`（尤其 `bilibili_downloader.py`）
- 转写器：`backend/app/transcriber/*`（尤其 `whisper.py` 与 `transcriber_provider.py`）
- GPT 集成：`backend/app/gpt/*`（`request_chunker.py`, `universal_gpt.py`）
- 数据库 DAO：`backend/app/db/video_task_dao.py` 等
- 前端表单与轮询：`BillNote_frontend/src/pages/HomePage/NoteForm.tsx` 与 `BillNote_frontend/src/hooks/useTaskPolling.ts`

**工具映射（功能 → 推荐测试工具 → 方法/说明）**

- 功能：后端核心逻辑（`NoteGenerator.generate`、下载、转写、保存）
  - 工具：`pytest` + Mock（`pytest-mock` / `unittest.mock`）
  - 方法：单元与集成测试。用 fixtures 启动 FastAPI TestClient 或调用类方法，mock 外部 GPT/transcriber/下载器，使用内存 SQLite 验证 `note_results` 与状态文件。示例命令：

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/test_note_helper.py -q
```

- 功能：下载器与字幕解析（`bilibili_downloader.py`）
  - 工具：`pytest` + Mock
  - 方法：用样例字幕文件（SRT/JSON3）做解析单元测试，覆盖边界/异常（损坏字幕、无字幕）。

- 功能：转写器（`whisper.py`）
  - 工具：`pytest` + Mock / 集成时可用本地小模型
  - 方法：单元测试分支（CUDA vs CPU）、错误处理；集成测试测量延迟/吞吐（见性能测试）。

- 功能：GPT 请求拆分与断点（`request_chunker.py`、`universal_gpt.py`）
  - 工具：`pytest`
  - 方法：已有单元测试为参考（`tests/test_request_chunker.py`），补充异常/大文本场景测试，mock GPT 适配器以验证 checkpoint 行为。

- 功能：DAO（`video_task_dao.py`）
  - 工具：`pytest`
  - 方法：使用 SQLite 内存数据库作为 fixture，测试 insert/get/delete 行为。

- 功能：前端表单提交与轮询（NoteForm、useTaskPolling）
  - 工具：`Selenium`（或 Playwright） + 测试框架（`pytest` 或 `JUnit`）
  - 方法：自动化 E2E：启动后端（或用 mock server），用 Selenium 驱动浏览器填写表单、提交、断言轮询显示状态并最终展示 Markdown。若团队偏好 Java 测试栈，可用 `JUnit + Selenium`，否则推荐 `pytest + selenium` 或 `Playwright + Playwright Test`。
  - 简单示例（pytest + selenium）：

```bash
pip install selenium pytest pytest-selenium
pytest tests/e2e/test_note_form.py -q
```

- 功能：性能/负载测试（API：`/api/generate_note`，分块逻辑）
  - 工具：`JMeter`
  - 方法：构建线程组并发提交请求，使用 CSV 数据驱动不同视频/输入，mock GPT/转写后端依赖以隔离外部服务；收集吞吐、P95/P99 延迟与错误率。

- 功能：剖析与性能分析
  - 工具选项：`JProfiler`（JVM），若不使用 JVM 则推荐 Python 的 `py-spy`/`cProfile`/`Yappi`；前端可用 Chrome DevTools/Node profiler。
  - 方法：在可复现的高负载场景下采样，生成火焰图定位 CPU/内存热点（如转写与 GPT 汇总）。

- 功能：测试管理与追踪
  - 工具：`Jira`
  - 方法：为每条测试场景创建 Test Case/Issue（示例：`BE-TEST-001`：NoteGenerator 单元测试），在 CI 中关联运行结果并记录失败的 Issue。

**关于 JUnit / JProfiler（JVM 工具）**
- 该仓库主语言为 Python/TypeScript，直接使用 JUnit 与 JProfiler 需要额外 Java 层或用 Java 来实现 Selenium 测试与用 JProfiler 对 JVM 服务剖析。
- 推荐：后端用 `pytest`，剖析用 `py-spy`（或在需要 Java 测试栈时再切换 JUnit/JProfiler）。

**示例运行与 CI 集成**
- 运行现有后端单元测试：

```bash
cd backend
python -m unittest discover -v tests
# 或
pytest tests -q
```

- 运行前端（本地）并手动测试：

```bash
cd BillNote_frontend
pnpm install
pnpm dev
```

- 在 CI 中：
  - 增加 job 运行 `pytest` 并上传测试覆盖率；
  - 增加 E2E job（Selenium grid 或 Playwright）跑关键场景；
  - 增加性能 job（触发 JMeter 脚本并保存结果）。

**下一步建议**
- 请确认：
  1) 是否接受用 `pytest`/`py-spy` 替代 `JUnit`/`JProfiler`？（若需要我可按 JVM 工具生成 Java Selenium 示例与 JProfiler 指南）
  2) 我现在是否开始实现第 2 步：为后端添加/扩展 `pytest` 测试用例（从 `request_chunker` 与 `video_task_dao` 开始）？

---
文件生成者：自动化测试映射（由 Copilot 协助生成）。