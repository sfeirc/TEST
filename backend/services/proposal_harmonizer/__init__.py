"""
Agent Proposal Harmonizer
Harmonise et standardise les présentations PowerPoint selon la charte Infotel
"""
from .pptx_extractor import extract_content_from_pptx, extract_text_summary_from_pptx
from .harmonizer_ai import harmonize_presentation_with_ai

__all__ = [
    'extract_content_from_pptx',
    'extract_text_summary_from_pptx',
    'harmonize_presentation_with_ai'
]

