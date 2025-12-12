---
permalink: /software
title: "Software"
---

# Software

<!-- [![Sam's GitHub stats](https://github-readme-stats.vercel.app/api?username=samsledje)](https://github.com/samsledje) -->

<button id="toggle-all-details" class="btn">Expand All</button>

{% assign types = site.data.software | group_by: "type" %}
{% for soft_group in types %}
<h3>{{ soft_group.name | title }}</h3>
<ul>
{% assign software_group = soft_group.items | sort: "title" %}
{% for software in software_group %}
<details style="margin-left: 1em;">
    <summary style="margin-left: -1em;">{{ software.title }}</summary>
    <div class="softwareitem">

<p>
{% if software.publication %}
    <!-- <a href="{{ software.publication }}"><b>[Publication]</b></a> -->
    <a href="{{ software.publication }}"><i class="fas fa-fw fa-file-pdf icon-pad-right"></i></a>
{% endif %}
{% if software.url %}
    {% if software.repo %}
        {% if software.user %}
          <!-- <div>
            <a href="{{ software.url }}" rel="external nofollow noopener" target="_blank">
              <img alt="{{ software.user }}/{{ software.repo }}" src="https://github-readme-stats.vercel.app/api/pin/?username={{ software.user }}&amp;repo={{ software.repo }}&amp;theme=default&amp;show_owner=true">
            </a>
          </div> -->
          <a href="{{ software.url }}"><i class="fab fa-fw fa-github icon-pad-right"></i></a>
        {% endif %}
    {% endif %}
{% endif %}
{% if software.description %}
    {{ software.description }}
{% endif %}
</p>

<!-- [![Repo stats](https://github-readme-stats.vercel.app/api/pin/?username={{ software.user }}&amp;repo={{ software.repo }}&amp;theme=default&amp;show_owner=true")]({{ software.url }}) -->

{% if software.pypi %}
    {% highlight bash %}
    $ pip install {{ software.pypi }}
    {% endhighlight %}
{% endif %}
    </div>
    <br>
</details>

{% endfor %}
</ul>
{% endfor %}

<script>
window.addEventListener('load', function() {
  const toggleButton = document.getElementById('toggle-all-details');
  if (toggleButton) {
    let allExpanded = false;

    toggleButton.addEventListener('click', function() {
      const allDetails = document.querySelectorAll('details');

      allExpanded = !allExpanded;

      allDetails.forEach(function(details) {
        details.open = allExpanded;
      });

      toggleButton.textContent = allExpanded ? 'Collapse All' : 'Expand All';
    });
  } else {
    console.error("Toggle button with ID 'toggle-all-details' not found!");
  }
});
</script>
