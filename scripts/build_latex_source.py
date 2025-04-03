#%%
import yaml

YAML_INPUT = "_data/publications.yml"
LATEX_TEMPLATE = "latex/main_template.tex"
LATEX_OUTPUT = "latex/main.tex"
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
# Insert the new text into the LaTeX source
latex_source = latex_template
insertion_marker = r"%%{REPLACE_WITH_PUBLICATIONS}%%"

# Put new_text into latex_source at insertion_marker
before, after = latex_source.split(insertion_marker)
latex_source = before + new_text + after

# Write the new LaTeX source to a file
with open(LATEX_OUTPUT, "wb") as file:
    file.write(latex_source.encode("utf-8"))

# %%
