/**
 * ConnectHub – Main JavaScript
 * Handles: likes (AJAX), follow (AJAX), mobile menu, post menus, alerts
 */

// ── Get CSRF token from cookies (required by Django for POST requests) ──
function getCookie(name) {
  let value = null;
  document.cookie.split(';').forEach(function(cookie) {
    const [k, v] = cookie.trim().split('=');
    if (k === name) value = decodeURIComponent(v);
  });
  return value;
}
const csrfToken = getCookie('csrftoken');

// ── Like / Unlike a Post ──
function toggleLike(postId, btn) {
  fetch(`/post/${postId}/like/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
  })
  .then(res => res.json())
  .then(data => {
    // Update the like count on the page
    const countEl = document.getElementById(`like-count-${postId}`);
    if (countEl) countEl.textContent = data.likes_count;

    // Toggle the heart icon and styling
    const icon = btn.querySelector('.like-icon');
    if (data.liked) {
      btn.classList.add('liked');
      if (icon) icon.textContent = '❤️';
    } else {
      btn.classList.remove('liked');
      if (icon) icon.textContent = '🤍';
    }

    // Small bounce animation
    btn.style.transform = 'scale(1.2)';
    setTimeout(() => { btn.style.transform = 'scale(1)'; }, 150);
  })
  .catch(() => {
    // If user is not logged in, redirect to login
    window.location.href = '/login/';
  });
}

// ── Follow / Unfollow a User ──
function toggleFollow(username, btn) {
  fetch(`/follow/${username}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
      return;
    }

    // Update button text and style
    if (data.following) {
      btn.textContent = 'Unfollow';
      btn.classList.remove('btn-primary');
      btn.classList.add('btn-outline');
    } else {
      btn.textContent = 'Follow';
      btn.classList.remove('btn-outline');
      btn.classList.add('btn-primary');
    }

    // Update follower count if visible on page
    const countEl = document.getElementById('followers-count');
    if (countEl) countEl.textContent = data.followers_count;
  })
  .catch(() => {
    window.location.href = '/login/';
  });
}

// ── Toggle Post 3-dot Menu ──
function toggleMenu(menuId) {
  // Close all other open menus first
  document.querySelectorAll('.post-menu-dropdown.open').forEach(function(m) {
    if (m.id !== menuId) m.classList.remove('open');
  });

  const menu = document.getElementById(menuId);
  if (menu) menu.classList.toggle('open');
}

// ── Close menus when clicking anywhere else on the page ──
document.addEventListener('click', function(e) {
  if (!e.target.closest('.post-menu')) {
    document.querySelectorAll('.post-menu-dropdown.open').forEach(function(m) {
      m.classList.remove('open');
    });
  }
});

// ── Mobile Hamburger Menu ──
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', function() {
    mobileMenu.classList.toggle('open');
  });
}

// ── Auto-dismiss alert messages after 4 seconds ──
document.querySelectorAll('.alert').forEach(function(alert) {
  setTimeout(function() {
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-10px)';
    alert.style.transition = 'all 0.4s ease';
    setTimeout(function() { alert.remove(); }, 400);
  }, 4000);
});
