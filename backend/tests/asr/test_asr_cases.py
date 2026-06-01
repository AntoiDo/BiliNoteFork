"""ASR 测试用例集"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Ensure backend/app is importable when running tests from anywhere
BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.transcriber.whisper import WhisperTranscriber


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_006_core_normal(mock_model_class):
    """
    TC-ASR-006 正常识别流程（核心用例）
    Mock: segments -> ["你好", "世界"], info.language="zh"
    预期: full_text == "你好 世界"，language == "zh"，segments 长度 == 2
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [
        Mock(start=0, end=1, text="你好"),
        Mock(start=1, end=2, text="世界"),
    ]
    fake_info = Mock(language="zh")
    mock_model.transcribe.return_value = (fake_segments, fake_info)

    t = WhisperTranscriber()
    res = t.transcript("ok.wav")

    assert res is not None
    assert res.full_text == "你好 世界"
    assert res.language == "zh"
    assert len(res.segments) == 2


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_007_multi_concat(mock_model_class):
    """
    TC-ASR-007 多段拼接
    Mock: segments -> ["a","b","c"]
    预期: full_text == "a b c"
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="a"), Mock(text="b"), Mock(text="c")]
    fake_info = Mock(language="en")
    mock_model.transcribe.return_value = (fake_segments, fake_info)

    res = WhisperTranscriber().transcript("f.wav")
    assert res.full_text == "a b c"


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_008_single_segment(mock_model_class):
    """
    TC-ASR-008 单段文本
    Mock: segments -> ["hello"]
    预期: full_text == "hello"
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="hello")]
    fake_info = Mock(language="en")
    mock_model.transcribe.return_value = (fake_segments, fake_info)

    res = WhisperTranscriber().transcript("s.wav")
    assert res.full_text == "hello"


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_009_empty_segments(mock_model_class):
    """
    TC-ASR-009 空segments
    Mock: segments -> []
    预期: full_text == ""，segments == []
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    mock_model.transcribe.return_value = ([], Mock(language="en"))
    res = WhisperTranscriber().transcript("empty.wav")
    assert res is not None
    assert res.full_text == ""
    assert res.segments == []


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_010_strip_handling(mock_model_class):
    """
    TC-ASR-010 strip 处理
    Mock: single segment text = "  hello  "
    预期: 去掉首尾空白 -> "hello"
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="  hello  ")]
    mock_model.transcribe.return_value = (fake_segments, Mock(language="en"))

    res = WhisperTranscriber().transcript("strip.wav")
    assert res.full_text == "hello"


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_011_multi_space_concat(mock_model_class):
    """
    TC-ASR-011 多空格拼接
    Mock: segments -> ["hello", " world"]
    预期: "hello world"
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="hello"), Mock(text=" world")]
    mock_model.transcribe.return_value = (fake_segments, Mock(language="en"))

    res = WhisperTranscriber().transcript("ms.wav")
    assert res.full_text == "hello world"


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_012_special_chars(mock_model_class):
    """
    TC-ASR-012 特殊字符
    Mock: segments -> ["你好！", "？"]
    预期: 保留特殊字符，不丢失
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="你好！"), Mock(text="？")]
    mock_model.transcribe.return_value = (fake_segments, Mock(language="zh"))

    res = WhisperTranscriber().transcript("spec.wav")
    assert "你好！" in res.full_text
    assert "？" in res.full_text


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_014_segments_structure_correct(mock_model_class):
    """
    TC-ASR-014 segments 结构正确
    检查 segment 是否包含 start/end/text
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(start=0.0, end=0.5, text="x")]
    fake_info = Mock(language="en")
    mock_model.transcribe.return_value = (fake_segments, fake_info)

    res = WhisperTranscriber().transcript("struct.wav")
    seg = res.segments[0]
    assert hasattr(seg, "start")
    assert hasattr(seg, "end")
    assert hasattr(seg, "text")


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_015_language_field(mock_model_class):
    """
    TC-ASR-015 language 字段
    Mock: info.language = "zh"
    预期: result.language == "zh"
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    fake_segments = [Mock(text="ok")]
    fake_info = Mock(language="zh")
    mock_model.transcribe.return_value = (fake_segments, fake_info)

    res = WhisperTranscriber().transcript("lang.wav")
    assert res.language == "zh"


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_017_model_exception(mock_model_class):
    """
    TC-ASR-017 模型异常
    Mock: transcribe -> raise Exception
    预期: 不崩溃，函数返回 None 并打印错误
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    mock_model.transcribe.side_effect = Exception("boom")

    res = WhisperTranscriber().transcript("bad.wav")
    assert res is None


@patch("app.transcriber.whisper.WhisperModel")
def test_tc_asr_018_return_none_from_model(mock_model_class):
    """
    TC-ASR-018 返回 None
    Mock: transcribe -> (None, None)
    预期: 正确处理，返回 None
    """
    mock_model = Mock()
    mock_model_class.return_value = mock_model

    # 模型返回 (None, None)
    mock_model.transcribe.return_value = (None, None)
    res = WhisperTranscriber().transcript("none.wav")
    assert res is None
