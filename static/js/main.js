// ===========================
// LUXE — main.js
// ===========================

// --- Navbar scroll effect ---
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 60);
});

// --- Mobile menu toggle ---
function toggleMenu() {
  const menu = document.getElementById('mobileMenu');
  if (menu) menu.classList.toggle('open');
}

// --- Cart counter ---
function updateCartUI(count) {
  document.querySelectorAll('.cart-count').forEach(el => {
    el.textContent = count !== undefined ? count : el.textContent;
  });
}

// --- Toast notification ---
function showToast(message) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 2500);
}

// --- Get CSRF Token ---
function getCsrf() {
  const cookie = document.cookie.match(/csrftoken=([^;]+)/);
  return cookie ? cookie[1] : '';
}

// ===========================
// ADD TO CART — AJAX
// ===========================
function addToCartAjax(productId, btn) {
  fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrf(),
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'quantity=1'
  })
  .then(res => {
    if (res.status === 302 || res.redirected) {
      window.location.href = '/login/';
      return;
    }
    return res.json();
  })
  .then(data => {
    if (!data) return;
    updateCartUI(data.cart_count);
    // Button feedback
    const original = btn.textContent;
    btn.textContent = '✓ Added';
    btn.style.background = 'var(--gold)';
    btn.style.color = 'var(--bg)';
    btn.style.borderColor = 'var(--gold)';
    showToast(data.message + ' 🛍');
    setTimeout(() => {
      btn.textContent = original;
      btn.style.background = '';
      btn.style.color = '';
      btn.style.borderColor = '';
    }, 2000);
  })
  .catch(() => showToast('Please login to add to cart'));
}

// ===========================
// WISHLIST TOGGLE — AJAX
// ===========================
function toggleWishlistBtn(btn, productId) {
  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrf(),
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'added') {
      btn.textContent = '♥';
      btn.style.color = '#e05a5a';
      showToast('Added to wishlist ♥');
    } else {
      btn.textContent = '♡';
      btn.style.color = '';
      showToast('Removed from wishlist');
    }
  })
  .catch(() => showToast('Please login first'));
}

// ===========================
// QUICK VIEW MODAL
// ===========================
function quickView(productId) {
  // Create modal if not exists
  let modal = document.getElementById('quickViewModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'quickViewModal';
    modal.innerHTML = `
      <div class="qv-overlay" onclick="closeQuickView()"></div>
      <div class="qv-box">
        <button class="qv-close" onclick="closeQuickView()">✕</button>
        <div class="qv-content" id="qvContent">
          <div style="text-align:center; padding:60px; color:var(--text-muted);">
            <div class="qv-loader"></div>
            <p style="margin-top:16px;">Loading...</p>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  // Fetch product data
  fetch(`/product/quick-view/${productId}/`, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('qvContent').innerHTML = `
      <div class="qv-grid">
        <div class="qv-img">
          ${data.image
            ? `<img src="${data.image}" style="width:100%;height:100%;object-fit:cover;border-radius:8px;"/>`
            : `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:100px;background:linear-gradient(135deg,#1a1208,#3d2c10);border-radius:8px;">🛍</div>`
          }
          ${data.is_new ? '<span class="badge" style="position:absolute;top:14px;left:14px;">New</span>' : ''}
          ${data.is_sale ? '<span class="badge sale" style="position:absolute;top:14px;left:14px;">Sale</span>' : ''}
        </div>
        <div class="qv-info">
          <p style="font-size:11px;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:8px;">${data.sub_category}</p>
          <h2 style="font-family:var(--font-display);font-size:32px;font-weight:300;color:var(--cream);margin-bottom:12px;">${data.name}</h2>
          <div style="color:var(--gold);font-size:16px;margin-bottom:16px;">${data.rating} ★</div>
          <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid var(--border);">
            <span style="font-size:28px;font-weight:500;color:var(--cream);">Rs ${data.price}</span>
            ${data.old_price ? `<span style="font-size:18px;color:var(--text-muted);text-decoration:line-through;">Rs ${data.old_price}</span>` : ''}
          </div>
          <p style="font-size:14px;color:var(--text-muted);line-height:1.8;margin-bottom:24px;">${data.description || 'Premium quality product from LUXE collection.'}</p>
          <div style="display:flex;gap:12px;margin-bottom:20px;">
            <button class="btn-add-to-cart" style="flex:1;" onclick="addToCartAjax(${data.id}, this)">
              Add to Cart 🛍
            </button>
            <a href="/product/${data.slug}/" class="btn-hero-ghost" style="padding:14px 20px;">
              Full Details
            </a>
          </div>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <span style="font-size:12px;color:var(--text-muted);background:var(--surface2);padding:6px 14px;border-radius:20px;border:1px solid var(--border);">🚚 Free Delivery</span>
            <span style="font-size:12px;color:var(--text-muted);background:var(--surface2);padding:6px 14px;border-radius:20px;border:1px solid var(--border);">↩ 7 Day Return</span>
            <span style="font-size:12px;color:var(--text-muted);background:var(--surface2);padding:6px 14px;border-radius:20px;border:1px solid var(--border);">✅ Authentic</span>
          </div>
        </div>
      </div>
    `;
  })
  .catch(() => {
    document.getElementById('qvContent').innerHTML = `
      <div style="text-align:center;padding:60px;color:var(--text-muted);">
        <p style="font-size:40px;">😕</p>
        <p style="margin-top:16px;">Could not load product. Please try again.</p>
      </div>
    `;
  });
}

function closeQuickView() {
  const modal = document.getElementById('quickViewModal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

// Close on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeQuickView();
});

// --- Scroll reveal ---
const revealEls = document.querySelectorAll(
  '.cat-card, .product-card, .testi-card, .contact-info, .contact-form, .promo-text'
);
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animation = 'fadeUp 0.8s ease both';
      entry.target.style.opacity   = '1';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => {
  el.style.opacity = '0';
  observer.observe(el);
});

// --- Newsletter ---
document.querySelectorAll('.newsletter-form button').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.previousElementSibling;
    if (input && input.value.includes('@')) {
      showToast('Subscribed! 🎉');
      input.value = '';
    } else {
      showToast('⚠ Enter a valid email');
    }
  });
});

// --- Social buttons ---
document.querySelectorAll('.social-btn').forEach(btn => {
  btn.style.cssText = `display:inline-block;padding:8px 18px;border:1px solid var(--border);border-radius:4px;font-size:12px;letter-spacing:1px;color:var(--text-muted);transition:all 0.35s ease;cursor:pointer;`;
  btn.addEventListener('mouseenter', () => { btn.style.borderColor = 'var(--gold)'; btn.style.color = 'var(--gold)'; });
  btn.addEventListener('mouseleave', () => { btn.style.borderColor = 'var(--border)'; btn.style.color = 'var(--text-muted)'; });
});