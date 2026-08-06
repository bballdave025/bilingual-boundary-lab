from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

API_URL = "https://ru.wikisource.org/w/api.php"

PAGE_TITLES = [
    "Война и мир (Толстой)/Том 1",
    "Война и мир (Толстой)/Том 2",
    "Война и мир (Толстой)/Том 3",
    "Война и мир (Толстой)/Том 4",
    "Война и мир (Толстой)/Эпилог",
]

DEFAULT_OUTPUT_PATH = Path(
    "data/raw/war_and_peace_ru_fr_wikisource.txt"
)

HEADERS = {
    "User-Agent": (
        "bilingual-boundary-lab/0.1 "
        "(educational research; repository corpus builder)"
    )
}


def fetch_parsed_html(
    session: requests.Session,
    title: str,
) -> str:
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "formatversion": "2",
    }
    response = session.get(
        API_URL,
        params=params,
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    if "error" in payload:
        raise RuntimeError(
            f"MediaWiki error for {title!r}: {payload['error']}"
        )

    return payload["parse"]["text"]


def remove_non_book_material(soup: BeautifulSoup) -> None:
    selectors = [
        "style",
        "script",
        "table",
        ".mw-editsection",
        ".reference",
        ".references",
        ".noprint",
        ".ws-noexport",
        ".sisitem",
        ".header",
        ".footer",
        ".licenseContainer",
        "sup",
    ]

    for selector in selectors:
        for node in soup.select(selector):
            node.decompose()


def insert_structural_breaks(soup: BeautifulSoup) -> None:
    block_names = {
        "p",
        "div",
        "section",
        "blockquote",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "br",
    }

    for node in soup.find_all(block_names):
        if not isinstance(node, Tag):
            continue
        if node.name == "br":
            node.replace_with("\n")
        else:
            node.insert_before("\n")
            node.insert_after("\n")


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    lines: list[str] = []

    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
        elif lines and lines[-1] != "":
            lines.append("")

    text = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def html_to_plain_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    remove_non_book_material(soup)
    insert_structural_breaks(soup)
    return normalize_text(soup.get_text(separator=" ", strip=False))


def build_corpus(
    output_path: Path,
    *,
    pause_seconds: float = 1.0,
) -> str:
    sections: list[str] = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for title in PAGE_TITLES:
            print(f"Fetching {title}...")
            html = fetch_parsed_html(session, title)
            text = html_to_plain_text(html)
            sections.append(
                f"{'=' * 72}\n"
                f"{title}\n"
                f"{'=' * 72}\n\n"
                f"{text}"
            )
            time.sleep(pause_seconds)

    corpus = "\n\n".join(sections) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(corpus, encoding="utf-8", newline="\n")
    return corpus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
    )
    parser.add_argument(
        "--pause-seconds",
        type=float,
        default=1.0,
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    corpus = build_corpus(
        arguments.output,
        pause_seconds=arguments.pause_seconds,
    )
    print(
        f"Wrote {arguments.output} "
        f"({len(corpus):,} characters)."
    )


if __name__ == "__main__":
    main()
