from app.core.pipeline import PipelineService


def test_detect_type():
    s = PipelineService()
    assert s._detect_type("PCAP.pdf") == "administrative"
    assert s._detect_type("ppt_tecnico.pdf") == "technical"
