## 一、输入校验类（最基础但必须有）
----
TC-ASR-001 正常音频路径
输入：合法 .wav 文件路径
Mock：返回正常识别结果
预期：
返回 TranscriptResult
full_text 正确
TC-ASR-002 空路径
输入：""
预期：
抛异常 或 返回错误提示
TC-ASR-003 None 输入
输入：None
预期：
处理异常（不崩溃）
TC-ASR-004 文件不存在
输入：不存在路径
Mock：transcribe 抛异常
预期：
捕获异常
输出错误信息
TC-ASR-005 非音频文件
输入：.txt 文件
预期：
报格式错误 / 失败处理

## 二、核心功能类（最重要，必须写）
TC-ASR-006 正常识别流程（核心用例）

Mock：

["你好", "世界"]

预期：

full_text == "你好 世界"
segments 数量正确
TC-ASR-007 多段拼接

Mock：

["a", "b", "c"]

预期：

"a b c"
TC-ASR-008 单段文本

Mock：

["hello"]

预期：

full_text == "hello"
TC-ASR-009 空segments

Mock：

[]

预期：

full_text == ""
segments == []
## 三、数据处理类（白盒重点）
TC-ASR-010 strip处理

Mock：

"  hello  "

预期：

"hello"
TC-ASR-011 多空格拼接

Mock：

["hello", " world"]

预期：

"hello world"
TC-ASR-012 特殊字符

Mock：

["你好！", "？"]

预期：

正常拼接，不丢字符
TC-ASR-013 中文英文混合

Mock：

["hello", "世界"]

预期：

"hello 世界"
##  四、返回结构类（非常加分）
TC-ASR-014 segments结构正确

检查：

start
end
text
TC-ASR-015 language字段

Mock：

info.language = "zh"

预期：

result.language == "zh"
TC-ASR-016 raw字段保留

预期：

result.raw == info
##  五、异常处理类（老师最喜欢）
TC-ASR-017 模型异常（重点）

Mock：

transcribe -> raise Exception

预期：

不崩溃
打印“转写失败”
TC-ASR-018 返回None

Mock：

(None, None)

预期：

正确处理或报错
TC-ASR-019 segments异常结构

Mock：

[None, None]

预期：

不崩溃
TC-ASR-020 info缺失字段

Mock：

info 没有 language

预期：
不崩溃

##  六、边界情况类（补充用，显得专业）
TC-ASR-021 超长文本

Mock：

很长字符串

预期：

正常返回
TC-ASR-022 大量segments

Mock：

100+ segments

预期：

正常拼接
TC-ASR-023 时间戳异常

Mock：

start > end

预期：
不崩溃

##  七、初始化相关（可选加分）
TC-ASR-024 CPU模式
device="cpu"
TC-ASR-025 CUDA不可用

Mock：

is_cuda_available=False
TC-ASR-026 模型不存在

Mock：

Path.exists=False
TC-ASR-027 模型已存在

Mock：

Path.exists=True