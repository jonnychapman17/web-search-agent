from src.collectors.parser import extract_relevant_links


def test_extract_relevant_links_filters_by_keyword_and_extracts_date() -> None:
    html = """
    <html>
      <body>
        <article>
          <time datetime="2026-04-10">10 April 2026</time>
          <a href="/guidance/new-epc-rules">New EPC rules for landlords</a>
          <p>Updated guidance for private rented housing.</p>
        </article>
        <article>
          <a href="/guidance/unrelated">Unrelated fisheries update</a>
        </article>
      </body>
    </html>
    """

    items = extract_relevant_links(
        html=html,
        page_url="https://example.com/search",
        include_keywords=["landlord", "epc", "tenant"],
        max_items=10,
    )

    assert len(items) == 1
    assert items[0].url == "https://example.com/guidance/new-epc-rules"
    assert items[0].published_date == "2026-04-10"
    assert items[0].updated_date == ""
