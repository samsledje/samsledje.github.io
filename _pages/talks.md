---
permalink: /talks
title: "Talks"
---

# Talks

<ul>
{% assign talks = site.data.talks | sort: "date" | reverse %}
{% for talk in talks %}
<li>
<b>{{ talk.title }}</b> @ {{ talk.venue }} ({{ talk.date | date: "%Y" }})
{% if talk.url %}
    <a href="{{ talk.url }}" target="_blank"><i class="fas fa-fw fa-video icon-pad-right"></i></a>
{% endif %}

</li>
{% endfor %}
</ul>