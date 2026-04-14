from src.pipeline.classify import classify_jurisdiction, infer_category


def test_classify_jurisdiction_handles_both() -> None:
    assert classify_jurisdiction("Applies in England and Wales") == "England and Wales"


def test_infer_category_maps_tenant() -> None:
    assert infer_category("tenant") == "tenant_concern"
