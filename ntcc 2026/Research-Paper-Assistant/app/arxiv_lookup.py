import arxiv

def search_arxiv(query):
    try:
        search = arxiv.Search(
            query=query,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(search.results())

        if results:
            paper = results[0]
            return {
                "title": paper.title,
                "summary": paper.summary,
                "authors": ', '.join(author.name for author in paper.authors),
                "published": paper.published.strftime("%Y-%m-%d"),
                "arxiv_url": paper.entry_id,
                "pdf_url": paper.pdf_url
            }
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
