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

<script>
  window.publicationsData = {{ site.data.publications | jsonify }};
</script>
<link rel="stylesheet" href="{{ baseurl }}/assets/css/publications.css">
<script src="{{ baseurl }}/assets/js/publications.js"></script>