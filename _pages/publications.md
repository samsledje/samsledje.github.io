---
permalink: /publications
title: "Publications"
---

# Publications
\* Equal contribution

{% assign types = site.data.publications | group_by: "type" %}
{% for pub_group in types %}
<h3>{{ pub_group.name | capitalize }}</h3>
<ul>
{% assign publication_group = pub_group.items | sort: "date" | reverse %}
{% for publication in publication_group %}
<p class="publicationitem">
<span class="publicationtitle"><b>{{ publication.title }}</b></span><br>
{% assign authors = publication.authors | split: ", " %}
{% for member in authors %}
    {% if member == "Sledzieski" or member == "Sledzieski*" %}
        <b>{{ member }}</b>,
    {% else %}
        {{ member }},
    {% endif %}
{% endfor %}
<i>{{ publication.venue }}</i>{% if publication.volume %}, {{ publication.volume }}{% endif %}{% if publication.number %}({{publication.number}}){% endif %}{% if publication.pages %}:{{publication.pages}}{% endif %}, {{publication.date | date: '%Y'}}.
<br>
{% if publication.pdf %} <a href="{{ publication.pdf }}" target="_blank"><i class="fas fa-fw fa-file-pdf icon-pad-right"></i></a> {% endif %}
{% if publication.code %} <a href="{{ publication.code }}" target="_blank"><i class="fab fa-fw fa-github icon-pad-right"></i></a> {% endif %}
{% if publication.talk %} <a href="{{ publication.talk }}" target="_blank"><i class="fas fa-fw fa-video icon-pad-right"></i></a> {% endif %}
<a href="#" onclick="showBibtexModal('{{ publication.title | slugify }}'); return false;"><i class="fas fa-fw fa-quote-right icon-pad-right"></i></a>

<!-- Modal for BibTeX citation -->

<div id="bibtex-modal-{{ publication.title | slugify }}" class="bibtex-modal">
  <div class="bibtex-modal-content">
    <span class="bibtex-close" onclick="hideBibtexModal('{{ publication.title | slugify }}')">&times;</span>
    <h3>BibTeX Citation</h3>
    <pre class="bibtex-content" id="bibtex-content-{{ publication.title | slugify }}"></pre>
  </div>
</div>

</p>
{% endfor %}
</ul>
{% endfor %}

### PhD Thesis: [Learning the Language of Biomolecular Interactions]({{ baseurl }}/assets/files/Sledzieski_PhD_Thesis.pdf) ([Defense](https://www.youtube.com/watch?v=lJkTFrfQ510))

<style>
/* Modal styling */
.bibtex-modal {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.bibtex-modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 800px;
  border-radius: 5px;
}

.bibtex-close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.bibtex-close:hover {
  color: black;
}

.bibtex-content {
  background-color: #f5f5f5;
  padding: 10px;
  overflow-x: auto;
  white-space: pre-wrap;
  border: 1px solid #ddd;
  font-size: 16px;
  border-radius: 3px;
}
</style>

<script>
function showBibtexModal(publicationId) {
  console.log(publicationId)
  // Get all publication data
  const publications = {{ site.data.publications | jsonify }};
  
  // Find the matching publication
  const publication = publications.find(p => 
    p.title.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-') === publicationId);
  
  if (!publication) return;
  
  // Generate BibTeX
  const bibtex = generateBibtex(publication);
  
  // Display the BibTeX
  document.getElementById(`bibtex-content-${publicationId}`).textContent = bibtex;
  document.getElementById(`bibtex-modal-${publicationId}`).style.display = "block";
}

function hideBibtexModal(publicationId) {
  document.getElementById(`bibtex-modal-${publicationId}`).style.display = "none";
}

function copyBibtex(publicationId) {
  const bibtexContent = document.getElementById(`bibtex-content-${publicationId}`).textContent;
  navigator.clipboard.writeText(bibtexContent)
    .then(() => alert('Citation copied to clipboard!'))
    .catch(err => console.error('Error copying citation:', err));
}

function generateBibtex(publication) {
  // Create citation key using first author's last name and year
  const authors = publication.authors.split(', ');
  const firstAuthor = authors[0].replace('*', '').toLowerCase(); // Remove any * from author name
  const year = new Date(publication.date).getFullYear();
  
  // Get first word of title for citation key
  const firstWord = publication.title.split(' ')[0].replace(/[^\w]/g, '').toLowerCase();
  const citationKey = `${firstAuthor}${year}${firstWord}`;
  
  // Format authors for BibTeX
  const bibtexAuthors = authors.map(author => 
    author.replace('*', '')).join(' and ');
  
  // Determine entry type based on publication type
  let entryType = 'article';
  if (publication.type === 'conference') {
    entryType = 'inproceedings';
    }
  
  // Build BibTeX entry
  let bibtex = `@${entryType}{${citationKey},
  author = {${bibtexAuthors}},
  title = {${publication.title}},`;
  
  if (publication.type === 'journal') {
    bibtex += `
  journal = {${publication.venue}},`;
  } else if (publication.type === 'conference') {
    bibtex += `
  booktitle = {${publication.venue}},`;
  } else {
    bibtex += `
  note = {${publication.venue}},`;
  }
  
  // Add volume if available
  if (publication.volume) {
    bibtex += `
  volume = {${publication.volume}},`;
  }
  
  // Add number/issue if available
  if (publication.number) {
    bibtex += `
  number = {${publication.number}},`;
  }
  
  // Add pages if available
  if (publication.pages) {
    bibtex += `
  pages = {${publication.pages}},`;
  }
  
  // Add year
  bibtex += `
  year = {${year}},`;
  
  // Add DOI if available
  if (publication.doi) {
    bibtex += `
  doi = {${publication.doi}},`;
  }
  
  // Add URL if available
  if (publication.pdf) {
    bibtex += `
  url = {${publication.pdf}},`;
  }
  
  // Close the BibTeX entry
  bibtex += `
}`;
  
  return bibtex;
}

// Close modal when clicking outside of it
window.onclick = function(event) {
  const modals = document.getElementsByClassName('bibtex-modal');
  for (let i = 0; i < modals.length; i++) {
    if (event.target === modals[i]) {
      modals[i].style.display = "none";
    }
  }
}
</script>