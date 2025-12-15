#!/usr/bin/env python3
"""
Generate a numbered list of publications from publications.yml
Includes only journal and conference publications (no preprints)
"""

import yaml
import argparse
import sys
from pathlib import Path


def format_authors(authors):
    """Format author string, removing asterisks used for equal contribution"""
    return authors.replace('*', '')


def format_publication(pub, number):
    """Format a single publication entry"""
    authors = format_authors(pub['authors'])
    title = pub['title']
    venue = pub['venue']

    # Build the citation string
    citation = f"{number}. {authors}. \"{title}.\" {venue}"

    # Add volume/issue/pages for journal articles
    if pub['type'] == 'journal' and 'volume' in pub:
        citation += f" {pub['volume']}"
        if 'number' in pub:
            citation += f"({pub['number']})"
        if 'pages' in pub:
            citation += f": {pub['pages']}"

    # Add extra info for conferences (typically the year)
    if pub['type'] == 'conference' and 'extra' in pub:
        citation += f" {pub['extra']}"

    # Add year from date
    year = pub['date'].year if hasattr(pub['date'], 'year') else str(pub['date'])[:4]
    citation += f" ({year})."

    return citation


def main():
    parser = argparse.ArgumentParser(
        description='Generate a numbered list of publications from publications.yml'
    )
    parser.add_argument(
        '--sort',
        choices=['ascending', 'descending'],
        default='descending',
        help='Sort order by date (default: descending, newest first)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Read publications.yml
    script_dir = Path(__file__).parent
    yml_path = script_dir.parent / '_data' / 'publications.yml'

    with open(yml_path, 'r') as f:
        publications = yaml.safe_load(f)

    # Filter for journal and conference publications only
    filtered_pubs = [pub for pub in publications
                     if pub['type'] in ['journal', 'conference']]

    # Sort by date
    reverse_order = (args.sort == 'descending')
    filtered_pubs.sort(key=lambda x: x['date'], reverse=reverse_order)

    # Generate numbered list
    output_lines = ["PUBLICATIONS\n"]
    for i, pub in enumerate(filtered_pubs, 1):
        output_lines.append(format_publication(pub, i))
        output_lines.append("")  # Blank line between entries

    output_text = "\n".join(output_lines)

    # Write to file or stdout
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_text)
        print(f"Publication list written to {args.output}")
    else:
        print(output_text)


if __name__ == '__main__':
    main()
