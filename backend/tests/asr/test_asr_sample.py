import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# 允许在任意工作目录运行 pytest 时都能导入 backend/app
BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.transcriber.whisper import WhisperTranscriber


@patch("app.transcriber.whisper.WhisperModel")  # mock 掉模型
def test_transcript_basic(mock_model_class):
    # 1️⃣ 创建假的模型实例
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    # 2️⃣ 模拟 transcribe 返回值
    fake_segments = [
        Mock(start=0, end=1, text="你好"),
        Mock(start=1, end=2, text="世界")
    ]
    fake_info = Mock(language="zh")

    mock_model.transcribe.return_value = (fake_segments, fake_info)

    # 3️⃣ 创建对象
    transcriber = WhisperTranscriber()

    # 4️⃣ 调用方法
    result = transcriber.transcript("test.wav")

    # 5️⃣ 断言结果（最关键！）
    assert result.full_text == "你好 世界"
    assert result.language == "zh"
    assert len(result.segments) == 2