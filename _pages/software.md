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
<details>
    <summary>{{ software.title }}</summary>
    <p>
{% if software.url %}
    <!-- <a href="{{ software.url }}"><b>[Code]</b></a> -->
    <a href="{{ software.url }}"><i class="fab fa-fw fa-github icon-pad-right"></i></a>
{% endif %}

{% if software.publication %}
    <!-- <a href="{{ software.publication }}"><b>[Publication]</b></a> -->
    <a href="{{ software.publication }}"><i class="fas fa-fw fa-file-pdf icon-pad-right"></i></a>
{% endif %}

{% if software.description %}
    {{ software.description }}
{% endif %}

{% if software.pypi %}
    {% highlight bash %}
    $ pip install {{ software.pypi }}
    {% endhighlight %}
{% endif %}
    </p>
</details>

{% endfor %}
</ul>
{% endfor %}

<script>
// Wait for the document to be fully loaded
window.addEventListener('load', function() {
  // Look for the button
  const toggleButton = document.getElementById('toggle-all-details');
  
  // Only proceed if we found the button
  if (toggleButton) {
    // Set initial state
    let allExpanded = false;
    
    // Add click event listener
    toggleButton.addEventListener('click', function() {
      // Get all details elements
      const allDetails = document.querySelectorAll('details');
      
      // Toggle state
      allExpanded = !allExpanded;
      
      // Apply to all details elements
      allDetails.forEach(function(details) {
        details.open = allExpanded;
      });
      
      // Update button text
      toggleButton.textContent = allExpanded ? 'Collapse All' : 'Expand All';
    });
  } else {
    console.error("Toggle button with ID 'toggle-all-details' not found!");
  }
});
</script>