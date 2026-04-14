from src.pipeline.classify import infer_theme


def test_infer_theme_matches_epc() -> None:
    assert infer_theme("Updated EPC guidance for landlords") == "epc"


def test_infer_theme_matches_repairs() -> None:
    assert infer_theme("Tenant complaint about damp and mould") == "repairs_and_disrepair"
