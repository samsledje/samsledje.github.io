function showBibtexModal(publicationId) {
  console.log(publicationId);
  // Get all publication data
  const publications = window.publicationsData;

  // Find the matching publication
  const publication = publications.find(p =>
    p.title.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-') === publicationId
  );

  if (!publication) {
    console.error(`Publication with ID "${publicationId}" not found.`);
    return;
  }

  // Generate BibTeX
  const bibtex = generateBibtex(publication);

  if (!bibtex) {
    console.error(`Failed to generate BibTeX for publication:`, publication);
    return;
  }

  // Display the BibTeX
  const bibtexContentElement = document.getElementById(`bibtex-content-${publicationId}`);
  if (bibtexContentElement) {
    bibtexContentElement.textContent = bibtex;
  } else {
    console.error(`BibTeX content element for ID "${publicationId}" not found.`);
  }

  const modalElement = document.getElementById(`bibtex-modal-${publicationId}`);
  if (modalElement) {
    modalElement.style.display = "block";
  } else {
    console.error(`Modal element for ID "${publicationId}" not found.`);
  }
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
    author.replace('*', '')
  ).join(' and ');

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
};
