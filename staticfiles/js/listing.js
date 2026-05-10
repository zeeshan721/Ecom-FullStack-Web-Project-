// ===========================
// LUXE — listing.js
// ===========================

// --- Mobile filter sidebar toggle ---
function toggleFilterSidebar() {
  const sidebar = document.getElementById('filterSidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// --- Price slider label update ---
function updatePrice(slider) {
  const val = parseInt(slider.value).toLocaleString();
  const label =
    document.getElementById('clothingPriceVal') ||
    document.getElementById('shoesPriceVal') ||
    document.getElementById('cosmeticsPriceVal');
  if (label) label.textContent = 'Rs ' + val;
  applyFilter();
}

// --- Size toggle ---
function toggleSize(btn) {
  btn.classList.toggle('active');
}

// --- Color toggle ---
function toggleColor(btn) {
  btn.classList.toggle('active');
}

// --- Clear all filters ---
function clearFilters() {
  document.querySelectorAll('.filter-check input').forEach(i => i.checked = false);
  document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.color-dot').forEach(b => b.classList.remove('active'));
  const slider = document.querySelector('.price-slider');
  if (slider) { slider.value = slider.max; updatePrice(slider); }
  document.querySelectorAll('[name="rating"]').forEach(r => { if (r.value === '0') r.checked = true; });
  applyFilter();
  showToast('Filters cleared');
}

// --- Apply filters (front-end demo) ---
function applyFilter() {
  const cards = document.querySelectorAll('.listing-grid .product-card');
  const slider = document.querySelector('.price-slider');
  const maxPrice = slider ? parseInt(slider.value) : 999999;

  // Checked categories
  const checkedCats = [...document.querySelectorAll('[name="cat"]:checked, [name="type"]:checked')].map(i => i.value);

  let visible = 0;
  cards.forEach(card => {
    const price = parseInt(card.dataset.price || 0);
    const cat   = card.dataset.cat || '';
    const priceOk = price <= maxPrice;
    const catOk   = checkedCats.length === 0 || checkedCats.includes(cat);

    if (priceOk && catOk) {
      card.style.display = '';
      card.style.animation = 'fadeUp 0.4s ease both';
      visible++;
    } else {
      card.style.display = 'none';
    }
  });

  // Update count
  const countEl =
    document.getElementById('clothingCount') ||
    document.getElementById('shoesCount') ||
    document.getElementById('cosmeticsCount');
  if (countEl) countEl.textContent = visible;

  if (visible === 0) showToast('No products match your filters');
}

// --- Sort products ---
function sortProducts() {
  const select = document.querySelector('.sort-select');
  const grid   = document.querySelector('.listing-grid');
  if (!grid || !select) return;
  const cards  = [...grid.querySelectorAll('.product-card')];

  cards.sort((a, b) => {
    const pa = parseInt(a.dataset.price || 0);
    const pb = parseInt(b.dataset.price || 0);
    if (select.value === 'price-low')  return pa - pb;
    if (select.value === 'price-high') return pb - pa;
    return 0;
  });

  cards.forEach(card => grid.appendChild(card));
  showToast('Sorted: ' + select.options[select.selectedIndex].text);
}

// --- View toggle (grid / list) ---
function setView(type, btn) {
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const grid = document.querySelector('.listing-grid');
  if (!grid) return;
  if (type === 'list') {
    grid.classList.add('list-view');
    grid.style.gridTemplateColumns = '1fr';
  } else {
    grid.classList.remove('list-view');
    grid.style.gridTemplateColumns = '';
  }
}

// --- Pagination buttons ---
document.querySelectorAll('.page-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
