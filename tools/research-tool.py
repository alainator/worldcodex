#!/usr/bin/env python3
"""
Research Paper Tool v4 — Search, Download, Convert
===================================================
Searches open-access academic sources, downloads PDFs,
converts to markdown, and organizes in _source/research/.

Default sources (no API key needed):
  - arXiv (physics, math, cs, q-bio)
  - Crossref (all disciplines, 150M+ papers)
  - Unpaywall (finds open-access PDFs by DOI)
  - PubMed Central (biomedical, open access)

Humanities sources (--source humanities or individually):
  - Semantic Scholar (broad academic, all disciplines)
  - Open Library (books — foundational texts, monographs)
  - Stanford Encyclopedia of Philosophy (peer-reviewed entries)
  - PhilPapers (search URL generation — no API available)

Usage:
  python3 tools/research-tool.py search "quantum time operator"
  python3 tools/research-tool.py search "percolation theory" --source arxiv --max 10
  python3 tools/research-tool.py search "autopoiesis Maturana" --source humanities
  python3 tools/research-tool.py search "structural realism" --source sep --download
  python3 tools/research-tool.py search "Lakatos methodology" --source openlibrary
  python3 tools/research-tool.py search "coherentism" --source philpapers
  python3 tools/research-tool.py search "topic" --download
  python3 tools/research-tool.py download <url_or_id>
  python3 tools/research-tool.py convert <pdf_path>
  python3 tools/research-tool.py convert-all
  python3 tools/research-tool.py list
  python3 tools/research-tool.py list --topic "collapse"
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = PROJECT_ROOT / "_source" / "research"
PAPERS_DIR = RESEARCH_DIR / "papers"
MARKDOWN_DIR = RESEARCH_DIR / "markdown"
SEP_DIR = RESEARCH_DIR / "sep-entries"
INDEX_FILE = RESEARCH_DIR / "INDEX.md"

# Customize this for your project — used for polite API access
CONTACT_EMAIL = os.environ.get(
    "RESEARCH_TOOL_EMAIL", "worldcodex-research@example.com"
)

RATE_LIMITS = {
    "arxiv": 3.0,
    "crossref": 1.0,
    "unpaywall": 1.0,
    "semantic": 4.0,
    "pmc": 1.0,
    "openlibrary": 1.0,
    "sep": 2.0,
    "download": 2.0,
}

SOURCE_GROUPS = {
    "default": ["arxiv", "crossref", "pmc"],
    "humanities": ["semantic", "openlibrary", "sep", "philpapers"],
    "all": ["arxiv", "crossref", "pmc", "semantic", "openlibrary", "sep", "philpapers"],
}

# Retry configuration
MAX_RETRIES = 3
BACKOFF_BASE = 5
BACKOFF_MULTIPLIER = 2

# Track last request time per source
_last_request_time = {}

# User agent for API requests
USER_AGENT = f"WorldCodex-Research/4.0 (mailto:{CONTACT_EMAIL})"


def ensure_dirs():
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    SEP_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Rate Limiting and Retry Logic
# ============================================================

def _rate_limit(source):
    """Enforce minimum delay between requests to the same source."""
    now = time.time()
    delay = RATE_LIMITS.get(source, 2.0)
    last = _last_request_time.get(source, 0)
    elapsed = now - last
    if elapsed < delay:
        wait = delay - elapsed
        print(f"  [RATE LIMIT] Waiting {wait:.1f}s before next {source} request...")
        time.sleep(wait)
    _last_request_time[source] = time.time()


def _fetch_with_retry(url, source, headers=None, max_retries=MAX_RETRIES):
    """Fetch a URL with rate limiting, retry, and exponential backoff."""
    _rate_limit(source)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)

    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait = int(retry_after) + 1
                    except ValueError:
                        wait = BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)
                else:
                    wait = BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)

                if attempt < max_retries:
                    print(f"  [429 RATE LIMITED] {source} — retry {attempt + 1}/{max_retries} in {wait}s...")
                    time.sleep(wait)
                    _last_request_time[source] = time.time()
                    continue
                else:
                    print(f"  [429 RATE LIMITED] {source} — all {max_retries} retries exhausted. Skipping.")
                    return None
            elif e.code in (500, 502, 503, 504):
                wait = BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)
                if attempt < max_retries:
                    print(f"  [{e.code} SERVER ERROR] {source} — retry {attempt + 1}/{max_retries} in {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    print(f"  [{e.code} SERVER ERROR] {source} — all retries exhausted. Skipping.")
                    return None
            elif e.code == 404:
                print(f"  [404] {source} — not found. Skipping.")
                return None
            else:
                print(f"  [HTTP {e.code}] {source} — {e.reason}")
                return None
        except urllib.error.URLError as e:
            wait = BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)
            if attempt < max_retries:
                print(f"  [NETWORK ERROR] {source} — {e.reason} — retry {attempt + 1}/{max_retries} in {wait}s...")
                time.sleep(wait)
                continue
            else:
                print(f"  [NETWORK ERROR] {source} — all retries exhausted. Skipping.")
                return None
        except Exception as e:
            print(f"  [ERROR] {source} — {e}")
            return None

    return None


# ============================================================
# Search Functions
# ============================================================

def search_arxiv(query, max_results=5):
    """Search arXiv API for open-access papers."""
    base_url = "http://export.arxiv.org/api/query"
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    })
    url = f"{base_url}?{params}"

    data = _fetch_with_retry(url, "arxiv")
    if data is None:
        return []
    data = data.decode("utf-8")

    results = []
    entries = data.split("<entry>")[1:]
    for entry in entries:
        title = _extract_xml(entry, "title").strip().replace("\n", " ")
        summary = _extract_xml(entry, "summary").strip().replace("\n", " ")[:300]
        arxiv_id = _extract_xml(entry, "id").strip().split("/abs/")[-1]
        published = _extract_xml(entry, "published").strip()[:10]

        authors = []
        for author_block in entry.split("<author>")[1:]:
            name = _extract_xml(author_block, "name").strip()
            if name:
                authors.append(name)

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        results.append({
            "source": "arxiv",
            "id": arxiv_id,
            "title": title,
            "authors": authors[:5],
            "date": published,
            "summary": summary,
            "pdf_url": pdf_url,
            "web_url": f"https://arxiv.org/abs/{arxiv_id}",
            "doi": None
        })

    return results


def search_crossref(query, max_results=5):
    """Search Crossref for papers. No API key needed — just polite email."""
    base_url = "https://api.crossref.org/works"
    params = urllib.parse.urlencode({
        "query": query,
        "rows": max_results,
        "sort": "relevance",
        "order": "desc",
        "select": "DOI,title,author,published-print,published-online,abstract,link,URL",
        "mailto": CONTACT_EMAIL
    })
    url = f"{base_url}?{params}"

    data = _fetch_with_retry(url, "crossref")
    if data is None:
        return []

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] Crossref response parse failed: {e}")
        return []

    results = []
    for item in parsed.get("message", {}).get("items", []):
        doi = item.get("DOI", "")
        title_list = item.get("title", ["Untitled"])
        title = title_list[0] if title_list else "Untitled"

        authors = []
        for author in (item.get("author") or [])[:5]:
            given = author.get("given", "")
            family = author.get("family", "")
            authors.append(f"{given} {family}".strip())

        # Get date
        date_parts = None
        for date_field in ("published-print", "published-online"):
            dp = item.get(date_field, {}).get("date-parts", [[]])
            if dp and dp[0]:
                date_parts = dp[0]
                break
        date = str(date_parts[0]) if date_parts else "unknown"

        # Get abstract (Crossref sometimes includes it)
        abstract = item.get("abstract", "")
        if abstract:
            abstract = re.sub(r"<[^>]+>", "", abstract)[:300]
        else:
            abstract = "No abstract available."

        # PDF link
        pdf_url = ""
        for link in (item.get("link") or []):
            if link.get("content-type") == "application/pdf":
                pdf_url = link.get("URL", "")
                break

        results.append({
            "source": "crossref",
            "id": doi,
            "title": title,
            "authors": authors,
            "date": date,
            "summary": abstract,
            "pdf_url": pdf_url,
            "web_url": f"https://doi.org/{doi}" if doi else "",
            "doi": doi
        })

    return results


def search_unpaywall_for_pdf(doi):
    """Find an open-access PDF for a given DOI via Unpaywall. No key needed."""
    if not doi:
        return None

    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi, safe='')}?email={CONTACT_EMAIL}"

    data = _fetch_with_retry(url, "unpaywall")
    if data is None:
        return None

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    best_oa = parsed.get("best_oa_location")
    if best_oa:
        pdf = best_oa.get("url_for_pdf") or best_oa.get("url")
        if pdf:
            return pdf

    for loc in (parsed.get("oa_locations") or []):
        pdf = loc.get("url_for_pdf") or loc.get("url")
        if pdf and pdf.endswith(".pdf"):
            return pdf

    return None


def enrich_with_unpaywall(results):
    """For results that have a DOI but no PDF, try Unpaywall to find one."""
    enriched = 0
    for r in results:
        if r.get("doi") and not r.get("pdf_url"):
            print(f"  [UNPAYWALL] Looking up OA PDF for DOI: {r['doi']}...")
            pdf_url = search_unpaywall_for_pdf(r["doi"])
            if pdf_url:
                r["pdf_url"] = pdf_url
                enriched += 1
                print(f"  [UNPAYWALL] Found: {pdf_url}")
            else:
                print(f"  [UNPAYWALL] No OA version found.")
    if enriched:
        print(f"  [UNPAYWALL] Enriched {enriched} results with open-access PDFs.")
    return results


def search_semantic_scholar(query, max_results=5):
    """Search Semantic Scholar API. Covers all disciplines."""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = urllib.parse.urlencode({
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,openAccessPdf,externalIds,url,citationCount,fieldsOfStudy"
    })
    url = f"{base_url}?{params}"

    data = _fetch_with_retry(url, "semantic", max_retries=4)
    if data is None:
        return []

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] Semantic Scholar response parse failed: {e}")
        return []

    results = []
    for paper in parsed.get("data", []):
        pdf_info = paper.get("openAccessPdf") or {}
        pdf_url = pdf_info.get("url", "")
        authors = [a.get("name", "") for a in (paper.get("authors") or [])[:5]]
        ext_ids = paper.get("externalIds") or {}
        citations = paper.get("citationCount", 0) or 0
        fields = paper.get("fieldsOfStudy") or []

        abstract = (paper.get("abstract") or "No abstract available.")[:250]
        if citations:
            abstract += f" [Cited {citations}x]"
        if fields:
            abstract += f" Fields: {', '.join(fields[:3])}"

        results.append({
            "source": "semantic_scholar",
            "id": ext_ids.get("DOI", ext_ids.get("ArXiv", paper.get("paperId", "unknown"))),
            "title": paper.get("title", "Untitled"),
            "authors": authors,
            "date": str(paper.get("year", "unknown")),
            "summary": abstract[:300],
            "pdf_url": pdf_url,
            "web_url": paper.get("url", ""),
            "doi": ext_ids.get("DOI"),
            "citations": citations,
        })

    results.sort(key=lambda r: r.get("citations", 0), reverse=True)
    return results


def search_pmc(query, max_results=5):
    """Search PubMed Central for open-access biomedical papers."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = urllib.parse.urlencode({
        "db": "pmc",
        "term": f"{query} AND open access[filter]",
        "retmax": max_results,
        "retmode": "json"
    })
    url = f"{base_url}?{params}"

    data = _fetch_with_retry(url, "pmc")
    if data is None:
        return []

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] PMC search response parse failed: {e}")
        return []

    id_list = parsed.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        return []

    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = urllib.parse.urlencode({
        "db": "pmc",
        "id": ",".join(id_list),
        "retmode": "json"
    })
    url = f"{summary_url}?{params}"

    data = _fetch_with_retry(url, "pmc")
    if data is None:
        return []

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] PMC summary parse failed: {e}")
        return []

    results = []
    for pmcid in id_list:
        doc = parsed.get("result", {}).get(pmcid, {})
        if not doc:
            continue

        authors = []
        for author in (doc.get("authors") or [])[:5]:
            authors.append(author.get("name", ""))

        article_ids = doc.get("articleids", [])
        doi = ""
        for aid in article_ids:
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
                break

        results.append({
            "source": "pmc",
            "id": f"PMC{pmcid}",
            "title": doc.get("title", "Untitled"),
            "authors": authors,
            "date": doc.get("pubdate", "unknown"),
            "summary": doc.get("title", ""),
            "pdf_url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/pdf/",
            "web_url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/",
            "doi": doi
        })

    return results


def search_openlibrary(query, max_results=5):
    """Search Open Library for books matching query."""
    base_url = "https://openlibrary.org/search.json"
    params = urllib.parse.urlencode({
        "q": query,
        "limit": max_results,
        "fields": "key,title,author_name,first_publish_year,subject,isbn,number_of_pages_median,publisher,edition_count",
    })
    url = f"{base_url}?{params}"

    data = _fetch_with_retry(url, "openlibrary")
    if data is None:
        return []

    try:
        parsed = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] Open Library response parse failed: {e}")
        return []

    results = []
    for doc in parsed.get("docs", [])[:max_results]:
        authors = (doc.get("author_name") or ["Unknown"])[:5]
        year = str(doc.get("first_publish_year", "unknown"))
        ol_key = doc.get("key", "")
        subjects = (doc.get("subject") or [])[:5]

        summary = f"Subjects: {', '.join(subjects)}" if subjects else "No subject data available."
        if doc.get("publisher"):
            publishers = doc["publisher"][:2]
            summary += f" Publisher: {', '.join(publishers)}."
        if doc.get("edition_count"):
            summary += f" {doc['edition_count']} editions."

        web_url = f"https://openlibrary.org{ol_key}" if ol_key else ""

        results.append({
            "source": "openlibrary",
            "id": ol_key,
            "title": doc.get("title", "Untitled"),
            "authors": authors,
            "date": year,
            "summary": summary[:300],
            "pdf_url": "",
            "web_url": web_url,
            "doi": None,
        })

    return results


def search_sep(query, max_results=5):
    """Search Stanford Encyclopedia of Philosophy."""
    params = urllib.parse.urlencode({"query": query})
    url = f"https://plato.stanford.edu/search/search?{params}"

    data = _fetch_with_retry(url, "sep")
    if data is None:
        return []

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    results = []
    listings = re.findall(
        r'<div class="result_listing">(.*?)(?=<div class="result_listing"|<!-- end search_results -->|$)',
        text, re.DOTALL
    )

    for listing in listings[:max_results]:
        title_div = re.search(
            r'<div class="result_title">(.*?)</div>', listing, re.DOTALL
        )
        if not title_div:
            continue

        title_content = title_div.group(1)
        anchor_match = re.search(r'<a[^>]*>(.*?)</a>', title_content, re.DOTALL)
        if not anchor_match:
            continue

        title = re.sub(r"<[^>]+>", "", anchor_match.group(1)).strip()

        slug_match = re.search(r'/entries/([^/]+)/', title_content)
        slug = slug_match.group(1) if slug_match else ""

        href_match = re.search(r'href="([^"]*)"', title_content)
        href = href_match.group(1) if href_match else ""

        snippet_match = re.search(
            r'<div class="result_snippet">(.*?)</div>', listing, re.DOTALL
        )
        snippet = ""
        if snippet_match:
            snippet = re.sub(r"<[^>]+>", "", snippet_match.group(1)).strip()[:300]

        author_match = re.search(
            r'<div class="result_author">(.*?)</div>', listing, re.DOTALL
        )
        authors = []
        if author_match:
            author_text = re.sub(r"<[^>]+>", "", author_match.group(1)).strip()
            if author_text:
                authors = [a.strip() for a in author_text.split(",") if a.strip()]

        entry_url = f"https://plato.stanford.edu/entries/{slug}/" if slug else href

        results.append({
            "source": "sep",
            "id": slug or href,
            "title": title,
            "authors": authors,
            "date": "",
            "summary": snippet,
            "pdf_url": "",
            "web_url": entry_url,
            "doi": None,
        })

    return results


def fetch_sep_entry(slug):
    """Fetch a SEP entry and save as markdown."""
    ensure_dirs()
    url = f"https://plato.stanford.edu/entries/{slug}/"

    md_path = SEP_DIR / f"{slug}.md"
    if md_path.exists():
        print(f"  [EXISTS] {md_path}")
        return md_path

    data = _fetch_with_retry(url, "sep")
    if data is None:
        return None

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    meta_title = ""
    meta_date = ""

    for tag_name in ("DC.title", "citation_title"):
        match = re.search(rf'<meta\s+name="{tag_name}"\s+content="([^"]*)"', text)
        if match:
            meta_title = html.unescape(match.group(1))
            break

    for tag_name in ("DCTERMS.issued", "citation_publication_date"):
        match = re.search(rf'<meta\s+name="{tag_name}"\s+content="([^"]*)"', text)
        if match:
            meta_date = html.unescape(match.group(1))
            break

    all_authors = []
    for tag_name in ("DC.creator", "citation_author"):
        all_authors = re.findall(rf'<meta\s+name="{tag_name}"\s+content="([^"]*)"', text)
        if all_authors:
            all_authors = [html.unescape(a) for a in all_authors]
            break

    main_match = re.search(r'<div id="(?:main-text|aueditable)"[^>]*>(.*?)</div>\s*<!--\s*End', text, re.DOTALL)
    if not main_match:
        main_match = re.search(r'<div id="main-text"[^>]*>(.*?)<div id="bibliography"', text, re.DOTALL)
    if not main_match:
        main_match = re.search(r'<div id="aueditable"[^>]*>(.*)', text, re.DOTALL)

    body_html = main_match.group(1) if main_match else ""
    body = _html_to_markdown(body_html)

    with open(md_path, "w") as f:
        f.write("---\n")
        f.write(f'title: "{meta_title}"\n')
        f.write(f'authors: "{", ".join(all_authors)}"\n')
        f.write(f'date: "{meta_date}"\n')
        f.write(f'source: "Stanford Encyclopedia of Philosophy"\n')
        f.write(f'url: "{url}"\n')
        f.write(f'fetched: "{datetime.now().strftime("%Y-%m-%d")}"\n')
        f.write("status: unreviewed\n")
        f.write("---\n\n")
        f.write(f"# {meta_title}\n\n")
        f.write(f"> **Authors:** {', '.join(all_authors)}\n")
        f.write(f"> **Source:** [Stanford Encyclopedia of Philosophy]({url})\n\n")
        f.write(body)

    print(f"  [OK] SEP entry saved to {md_path}")
    return md_path


def _html_to_markdown(html_text):
    """Convert HTML to readable markdown. Basic conversion for SEP entries."""
    text = html_text
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: f"\n## {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n", text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f"\n### {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n", text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', lambda m: f"\n#### {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n", text, flags=re.DOTALL)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: "\n> " + re.sub(r'\n', '\n> ', m.group(1).strip()) + "\n", text, flags=re.DOTALL)
    text = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"- {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n", text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def search_philpapers(query, max_results=5):
    """Generate PhilPapers search URLs. No API available (Cloudflare-blocked)."""
    encoded = urllib.parse.quote(query)
    search_url = f"https://philpapers.org/s/{encoded}"

    print(f"  [PHILPAPERS] No API available — generating search URL")
    print(f"  [PHILPAPERS] Open in browser: {search_url}")

    return [{
        "source": "philpapers",
        "id": f"philpapers-search-{encoded[:40]}",
        "title": f"PhilPapers search: {query}",
        "authors": [],
        "date": "",
        "summary": f"PhilPapers does not provide a public API (Cloudflare-protected). "
                   f"Open this URL in a browser to search: {search_url}",
        "pdf_url": "",
        "web_url": search_url,
        "doi": None,
    }]


# ============================================================
# Download Function
# ============================================================

def download_paper(url_or_id, title=None):
    """Download a paper PDF to _source/research/papers/."""
    ensure_dirs()

    if re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", url_or_id):
        url = f"https://arxiv.org/pdf/{url_or_id}.pdf"
        paper_id = url_or_id
    elif url_or_id.startswith("http"):
        url = url_or_id
        paper_id = re.sub(r"[^\w\-.]", "_", url.split("/")[-1].replace(".pdf", ""))
    else:
        print(f"  [ERROR] Unrecognized ID or URL: {url_or_id}")
        return None

    if title:
        safe_title = re.sub(r"[^\w\s-]", "", title)[:80].strip().replace(" ", "-").lower()
        filename = f"{safe_title}.pdf"
    else:
        filename = f"{paper_id.replace('/', '_')}.pdf"

    filepath = PAPERS_DIR / filename

    if filepath.exists():
        print(f"  [EXISTS] {filepath}")
        return filepath

    print(f"  [DOWNLOADING] {url}")
    print(f"  [TO] {filepath}")

    _rate_limit("download")

    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                if len(content) < 1000 and b"<!DOCTYPE" in content[:100]:
                    print(f"  [WARNING] Response looks like HTML, not PDF. Skipping.")
                    return None
                with open(filepath, "wb") as f:
                    f.write(content)
            print(f"  [OK] Downloaded {filepath.stat().st_size:,} bytes")
            return filepath
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                wait = int(retry_after) + 1 if retry_after else BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)
                if attempt < MAX_RETRIES:
                    print(f"  [429] Download rate limited — retry {attempt + 1}/{MAX_RETRIES} in {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    print(f"  [429] All retries exhausted for download.")
                    return None
            elif e.code == 404:
                print(f"  [404] PDF not found at {url}")
                return None
            else:
                print(f"  [HTTP {e.code}] Download failed: {e.reason}")
                return None
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait = BACKOFF_BASE * (BACKOFF_MULTIPLIER ** attempt)
                print(f"  [ERROR] {e} — retry {attempt + 1}/{MAX_RETRIES} in {wait}s...")
                time.sleep(wait)
                continue
            else:
                print(f"  [ERROR] Download failed after {MAX_RETRIES} retries: {e}")
                return None

    return None


# ============================================================
# Convert Function
# ============================================================

def convert_pdf_to_md(pdf_path):
    """Convert a PDF to markdown for Claude Code to read."""
    ensure_dirs()
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        print(f"  [ERROR] File not found: {pdf_path}")
        return None

    md_filename = pdf_path.stem + ".md"
    md_path = MARKDOWN_DIR / md_filename

    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            text = result.stdout
        else:
            raise Exception("pdftotext produced no output")
    except Exception:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_path))
            text = "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            )
        except Exception as e:
            print(f"  [ERROR] PDF conversion failed: {e}")
            return None

    with open(md_path, "w") as f:
        f.write(f"---\n")
        f.write(f"title: \"{pdf_path.stem}\"\n")
        f.write(f"source: \"{pdf_path.name}\"\n")
        f.write(f"converted: \"{datetime.now().strftime('%Y-%m-%d')}\"\n")
        f.write(f"status: unreviewed\n")
        f.write(f"---\n\n")
        f.write(f"# {pdf_path.stem}\n\n")
        f.write(f"> Original PDF: `{pdf_path.relative_to(PROJECT_ROOT)}`\n\n")
        f.write(text)

    print(f"  [OK] Converted to {md_path}")
    return md_path


# ============================================================
# Index Functions
# ============================================================

def update_index():
    """Rebuild _source/research/INDEX.md with all downloaded papers and SEP entries."""
    ensure_dirs()

    papers = sorted(PAPERS_DIR.rglob("*.pdf"))
    markdowns = sorted(MARKDOWN_DIR.glob("*.md"))
    sep_entries = sorted(SEP_DIR.glob("*.md"))

    md_stems = {m.stem for m in markdowns}

    with open(INDEX_FILE, "w") as f:
        f.write("# Research Index\n\n")
        f.write(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Papers:** {len(papers)} | **Converted:** {len(markdowns)} | **SEP entries:** {len(sep_entries)}\n\n")

        by_folder = {}
        for paper in papers:
            rel = paper.relative_to(PAPERS_DIR)
            folder = str(rel.parent) if rel.parent != Path(".") else "ungrouped"
            by_folder.setdefault(folder, []).append(paper)

        for folder in sorted(by_folder.keys()):
            folder_papers = by_folder[folder]
            f.write(f"\n## {folder}\n\n")
            f.write("| # | Paper | Converted | Status |\n")
            f.write("|---|-------|-----------|--------|\n")
            for i, paper in enumerate(folder_papers, 1):
                has_md = paper.stem in md_stems
                status = "Converted" if has_md else "Needs conversion"
                f.write(f"| {i} | {paper.stem} | {'Yes' if has_md else 'No'} | {status} |\n")

        if sep_entries:
            f.write("\n## SEP Entries (Stanford Encyclopedia of Philosophy)\n\n")
            f.write("| # | Entry | File |\n")
            f.write("|---|-------|------|\n")
            for i, entry in enumerate(sep_entries, 1):
                f.write(f"| {i} | {entry.stem} | sep-entries/{entry.name} |\n")

    print(f"  [OK] Index updated: {INDEX_FILE}")


def list_papers(topic=None):
    """List all downloaded papers, optionally filtered by topic."""
    ensure_dirs()
    papers = sorted(PAPERS_DIR.rglob("*.pdf"))

    if not papers:
        print("  No papers downloaded yet.")
        return

    if topic:
        topic_lower = topic.lower()
        papers = [p for p in papers if topic_lower in str(p).lower()]

    print(f"\n  Downloaded papers ({len(papers)}):\n")
    for i, paper in enumerate(papers, 1):
        md_exists = (MARKDOWN_DIR / f"{paper.stem}.md").exists()
        status = "[converted]" if md_exists else "[pdf only]"
        size = paper.stat().st_size
        rel = paper.relative_to(PAPERS_DIR)
        print(f"  {i:3}. {rel}  ({size:,} bytes) {status}")


# ============================================================
# Helpers
# ============================================================

def _extract_xml(text, tag):
    """Extract content between XML tags."""
    pattern = f"<{tag}[^>]*>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""


def format_results(results):
    """Pretty-print search results."""
    if not results:
        print("  No results found.")
        return

    print(f"\n  Found {len(results)} results:\n")
    for i, r in enumerate(results, 1):
        authors = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            authors += " et al."
        print(f"  [{i}] {r['title']}")
        if authors:
            print(f"      Authors: {authors}")
        print(f"      Date: {r['date'] or 'n/a'} | Source: {r['source']}")
        if r['pdf_url']:
            print(f"      PDF: {r['pdf_url']}")
        print(f"      Web: {r['web_url']}")
        if r.get('doi'):
            print(f"      DOI: {r['doi']}")
        print(f"      Summary: {r['summary'][:200]}...")
        print()

    return results


# ============================================================
# CLI
# ============================================================

def _resolve_sources(source_arg):
    """Resolve a --source argument into a list of source names."""
    if source_arg in SOURCE_GROUPS:
        return SOURCE_GROUPS[source_arg]
    return [source_arg]


def main():
    parser = argparse.ArgumentParser(
        description="Research Paper Tool v4 — Search, Download, Convert"
    )
    subparsers = parser.add_subparsers(dest="command")

    all_sources = ["arxiv", "crossref", "semantic", "pmc",
                   "openlibrary", "sep", "philpapers",
                   "default", "humanities", "all"]

    search_parser = subparsers.add_parser("search", help="Search for papers and books")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--source", choices=all_sources,
                               default="default",
                               help="Source to search. "
                                    "Groups: default (arXiv+Crossref+PMC), "
                                    "humanities (Semantic+OpenLibrary+SEP+PhilPapers), all")
    search_parser.add_argument("--max", type=int, default=5, help="Max results per source")
    search_parser.add_argument("--download", action="store_true",
                               help="Auto-download open access results and SEP entries")
    search_parser.add_argument("--no-unpaywall", action="store_true",
                               help="Skip Unpaywall PDF lookup for Crossref results")

    dl_parser = subparsers.add_parser("download", help="Download a paper")
    dl_parser.add_argument("url", help="URL or arXiv ID")
    dl_parser.add_argument("--title", help="Paper title for filename")

    conv_parser = subparsers.add_parser("convert", help="Convert PDF to markdown")
    conv_parser.add_argument("path", help="Path to PDF file")

    subparsers.add_parser("convert-all", help="Convert all unconverted PDFs")

    list_parser = subparsers.add_parser("list", help="List downloaded papers")
    list_parser.add_argument("--topic", help="Filter by topic keyword")

    subparsers.add_parser("index", help="Rebuild research index")

    fetch_parser = subparsers.add_parser("fetch-sep", help="Fetch a SEP entry by slug")
    fetch_parser.add_argument("slug", help="SEP entry slug (e.g., structural-realism)")

    args = parser.parse_args()

    if args.command == "search":
        sources = _resolve_sources(args.source)
        all_results = []

        if "arxiv" in sources:
            print("  Searching arXiv...")
            all_results.extend(search_arxiv(args.query, args.max))

        if "crossref" in sources:
            print("  Searching Crossref...")
            all_results.extend(search_crossref(args.query, args.max))

        if "semantic" in sources:
            print("  Searching Semantic Scholar...")
            all_results.extend(search_semantic_scholar(args.query, args.max))

        if "pmc" in sources:
            print("  Searching PubMed Central...")
            all_results.extend(search_pmc(args.query, args.max))

        if "openlibrary" in sources:
            print("  Searching Open Library...")
            all_results.extend(search_openlibrary(args.query, args.max))

        if "sep" in sources:
            print("  Searching Stanford Encyclopedia of Philosophy...")
            all_results.extend(search_sep(args.query, args.max))

        if "philpapers" in sources:
            all_results.extend(search_philpapers(args.query, args.max))

        # Enrich Crossref results with Unpaywall PDFs
        if not getattr(args, 'no_unpaywall', False):
            needs_pdf = [r for r in all_results if r.get("doi") and not r.get("pdf_url")]
            if needs_pdf:
                print(f"\n  Looking up {len(needs_pdf)} DOIs on Unpaywall for OA PDFs...")
                enrich_with_unpaywall(needs_pdf)

        results = format_results(all_results)

        if args.download and results:
            print("\n  Auto-downloading open access content...\n")
            for r in results:
                if r["source"] == "sep" and r.get("id"):
                    fetch_sep_entry(r["id"])
                elif r["pdf_url"]:
                    filepath = download_paper(r["pdf_url"], r["title"])
                    if filepath:
                        convert_pdf_to_md(filepath)
            update_index()

        if results:
            ensure_dirs()
            results_file = RESEARCH_DIR / "last-search-results.json"
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\n  Results saved to {results_file}")

    elif args.command == "fetch-sep":
        fetch_sep_entry(args.slug)

    elif args.command == "download":
        filepath = download_paper(args.url, args.title)
        if filepath:
            convert_pdf_to_md(filepath)
            update_index()

    elif args.command == "convert":
        convert_pdf_to_md(args.path)
        update_index()

    elif args.command == "convert-all":
        ensure_dirs()
        papers = sorted(PAPERS_DIR.rglob("*.pdf"))
        converted = 0
        for paper in papers:
            md_path = MARKDOWN_DIR / f"{paper.stem}.md"
            if not md_path.exists():
                convert_pdf_to_md(paper)
                converted += 1
        print(f"\n  Converted {converted} new papers. {len(papers) - converted} already done.")
        update_index()

    elif args.command == "list":
        list_papers(args.topic)

    elif args.command == "index":
        update_index()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
