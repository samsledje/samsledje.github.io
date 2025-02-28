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
<li>
{% assign authors = publication.authors | split: ", " %}
{% for member in authors %}
    {% if member == "Sledzieski" or member == "Sledzieski*" %}
        <b>{{ member }}</b>,
    {% else %}
        {{ member }},
    {% endif %}
{% endfor %}
"{{ publication.title }},"
<i>{{ publication.venue }}</i>{% if publication.extra %}, {{ publication.extra }}{% endif %}.
    <!-- {% if publication.pdf %} <a href="{{ publication.pdf }}" target="_blank"><b>[PDF]</b></a> {% endif %} -->
    {% if publication.pdf %} <a href="{{ publication.pdf }}" target="_blank"><i class="fas fa-fw fa-file-pdf icon-pad-right"></i></a> {% endif %}
    {% if publication.code %} <a href="{{ publication.code }}" target="_blank"><i class="fab fa-fw fa-github icon-pad-right"></i></a> {% endif %}
    {% if publication.talk %} <a href="{{ publication.talk }}" target="_blank"><i class="fas fa-fw fa-video icon-pad-right"></i></a> {% endif %}
</li>
{% endfor %}
</ul>
{% endfor %}

### PhD Thesis: [Learning the Language of Biomolecular Interactions]({{ baseurl }}/assets/files/Sledzieski_PhD_Thesis.pdf) ([Defense](https://www.youtube.com/watch?v=lJkTFrfQ510))