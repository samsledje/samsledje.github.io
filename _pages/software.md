---
permalink: /software
title: "Software"
---

# Software

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

{% if software.description %}
    <p>{{ software.description }}</p>
{% endif %}

{% if software.url %}
    <!-- <a href="{{ software.url }}"><b>[Code]</b></a> -->
    <a href="{{ software.url }}"><i class="fab fa-fw fa-github icon-pad-right"></i></a>
{% endif %}

{% if software.publication %}
    <!-- <a href="{{ software.publication }}"><b>[Publication]</b></a> -->
    <a href="{{ software.publication }}"><i class="fas fa-fw fa-file-pdf icon-pad-right"></i></a>
{% endif %}

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