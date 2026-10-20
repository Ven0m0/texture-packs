import pytest
from upscaler import validate_scale_factor, get_supported_formats

def test_validate_scale_factor_valid():
    """Test valid scale factors."""
    assert validate_scale_factor(2) is True
    assert validate_scale_factor(3) is True
    assert validate_scale_factor(4) is True

def test_validate_scale_factor_invalid():
    """Test invalid scale factors."""
    assert validate_scale_factor(1) is False
    assert validate_scale_factor(5) is False
    assert validate_scale_factor(0) is False
    assert validate_scale_factor(-1) is False
    assert validate_scale_factor(10) is False

def test_validate_scale_factor_types():
    """Test invalid types for scale factor."""
    # Based on the implementation: return scale in [2, 3, 4]
    assert validate_scale_factor("2") is False
    assert validate_scale_factor(2.0) is True  # 2.0 == 2 in Python
    assert validate_scale_factor(2.5) is False

def test_get_supported_formats():
    """Test supported formats list."""
    formats = get_supported_formats()
    assert isinstance(formats, list)
    assert '.png' in formats
    assert '.jpg' in formats
    assert '.jpeg' in formats
    assert '.webp' in formats
    assert '.tga' in formats
    assert '.bmp' in formats
    assert len(formats) == 6
