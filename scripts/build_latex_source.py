#%%
import argparse
import yaml
from collections import defaultdict

YAML_INPUT = "_data/publications.yml"
SOFTWARE_INPUT = "_data/software.yml"
DOWNLOADS_INPUT = "_data/package_downloads.yml"
LATEX_TEMPLATE = "latex/main_template.tex"
LATEX_OUTPUT = "latex/main.tex"

parser = argparse.ArgumentParser()
parser.add_argument("--pypi", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--github", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()
# %%

# Read YAML file
with open(YAML_INPUT, "r") as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

journal_pubs = [i for i in data if i["type"] == "journal"]
journal_pubs.sort(key= lambda x: x["date"], reverse=True)

conference_pubs = [i for i in data if i["type"] == "conference"]
conference_pubs.sort(key= lambda x: x["date"], reverse=True)

preprint_pubs = [i for i in data if i["type"] == "preprint"]
preprint_pubs.sort(key= lambda x: x["date"], reverse=True)

#%%

# Read LaTeX template
with open(LATEX_TEMPLATE, "r") as file:
    latex_template = file.read()

#%%
def format_citation(number, data):
    """
    Format a citation in the specified LaTeX style.
    
    Args:
        number (int): The citation number
        data (dict): Dictionary containing publication data
    
    Returns:
        str: Formatted citation string
    """

    authors = data["authors"]
    title = data["title"]
    venue = data["venue"]
    volume = data.get("volume", "")
    number_field = data.get("number", "")
    pages = data.get("pages", "")
    doi = data.get("doi", "")
    year = data["date"].year
    print(data)

    # Format each author, making only Sledzieski bold
    authors = authors.split(", ")
    formatted_authors = []
    for author in authors:
        if "Sledzieski" in author:
            formatted_authors.append("\\textbf{" + author + "}")
        else:
            formatted_authors.append(author)
    
    author_str = ", ".join(formatted_authors)
    author_str.lstrip()
    
    # Construct the full citation
    citation = (
        "\\Gap\n"
        "\\NumberedItem{[" + str(number) + "]}\n{"
        "{" + author_str + "}, \n"
        "``" + title + ",'' \n"
        "\\textit{" + venue + "}"
    )

    if volume:
        citation += f", {volume}"
    if number_field:
        citation += f"({number_field})"
    if pages:
        citation += f":{pages}"
    citation += f", {year}."
    if doi and data["type"] == "preprint":
        citation += f" {doi}."

    citation += "\n}\n\n"
    print(citation)
    
    return citation
#%%

# Generate LaTeX source
new_text = ""

# Journal
new_text += """
\BigGap
\hrule
\Section
{Journal}
{Journal}
{PDF:Journal}
"""
for i, row in enumerate(journal_pubs):
    new_text += format_citation(len(journal_pubs) - i, row)

# Conference
new_text += """
\BigGap
\hrule
\Section
{Conference and Workshops}
{Conference and Workshops}
{PDF:Conference and Workshops}
"""
for i, row in enumerate(conference_pubs):
    new_text += format_citation(len(conference_pubs) - i, row)

# Preprint
new_text += """
\BigGap
\hrule
\Section
{Preprints}
{Preprints}
{PDF:Preprints}
"""
for i, row in enumerate(preprint_pubs):
    new_text += format_citation(len(preprint_pubs) - i, row)

print(new_text)
# %%
# Load software data and download counts
with open(SOFTWARE_INPUT, "r") as f:
    software_data = yaml.safe_load(f)

pypi_downloads = {}
github_stars = {}
try:
    with open(DOWNLOADS_INPUT, "r") as f:
        downloads_cache = yaml.safe_load(f)
    if args.pypi:
        pypi_downloads = downloads_cache.get("pypi", {})
    if args.github:
        github_stars = downloads_cache.get("github_stars", {})
except FileNotFoundError:
    print(f"Warning: {DOWNLOADS_INPUT} not found. Run 'make downloads' first.")

def format_software_entry(item, pypi_downloads, github_stars):
    title = item["title"]
    url = item.get("url", "")
    pypi = item.get("pypi")
    gh_key = f"{item['user']}/{item['repo']}" if "user" in item and "repo" in item else None

    entry = f"\\Entry\n{{\\textbf{{{title}}}}}\n\\hfill {url}\n"

    stats = []
    if pypi:
        count = pypi_downloads.get(pypi, 0)
        if count:
            stats.append(f"{count // 1000}k+ PyPI downloads")
    if gh_key:
        stars = github_stars.get(gh_key, 0)
        if stars:
            stats.append(f"{stars:,} GitHub stars")
    if stats:
        entry += f"\\Gap\n\\Item\n{', '.join(stats)}\n"

    entry += "\\BigGap\n"
    return entry

def sort_key(item, pypi_downloads, github_stars):
    pypi = item.get("pypi")
    gh_key = f"{item['user']}/{item['repo']}" if "user" in item and "repo" in item else None
    downloads = pypi_downloads.get(pypi, 0) if pypi else 0
    stars = github_stars.get(gh_key, 0) if gh_key else 0
    return -(downloads + stars)

def generate_software_section(software_data, pypi_downloads, github_stars):
    by_category = defaultdict(list)
    for item in software_data:
        by_category[item["type"]].append(item)

    section = ""
    for category, items in sorted(by_category.items()):
        section += f"\\Gap\n\\textit{{{category}}}\n\\Gap\n"
        sorted_items = sorted(items, key=lambda i: sort_key(i, pypi_downloads, github_stars))
        for item in sorted_items:
            section += format_software_entry(item, pypi_downloads, github_stars)

    return section

software_text = generate_software_section(software_data, pypi_downloads, github_stars)

# %%
# Insert the new text into the LaTeX source
latex_source = latex_template

before, after = latex_source.split(r"%%{REPLACE_WITH_PUBLICATIONS}%%")
latex_source = before + new_text + after

before, after = latex_source.split(r"%%{REPLACE_WITH_SOFTWARE}%%")
latex_source = before + software_text + after

# Write the new LaTeX source to a file
with open(LATEX_OUTPUT, "wb") as file:
    file.write(latex_source.encode("utf-8"))

# %%
