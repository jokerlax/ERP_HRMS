// Aurelia ERP Global Search Controller
// Dynamically styles and handles global search for all non-payroll modules

(function() {
  // Inject CSS Styles for global search and dropdown
  const searchStyles = `
    .global-search { position:relative; display:flex; align-items:center; background:transparent; border-radius:20px; padding:0; margin-right:16px; width:34px; height:36px; }
    .global-search svg { position:absolute; right:8px; width:18px; height:18px; color:#94a3b8; cursor:pointer; transition:color 0.2s; z-index:2; }
    .global-search:not(.expanded) svg:hover { color:#fff; }
    .global-search.expanded svg { color:#94a3b8; pointer-events:none; left:10px; right:auto; }
    .global-search input { position:absolute; right:0; top:0; background:transparent; border:none; color:transparent; font-size:13px; height:36px; width:34px; padding:0; outline:none; font-family:inherit; transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border-radius:20px; z-index:1; cursor:pointer; }
    .global-search.expanded input { width:240px; background:#1e293b; color:#f8fafc; padding:0 12px 0 36px; cursor:text; box-shadow:0 4px 12px rgba(0,0,0,0.15); border: 1px solid #334155; }
    .global-search input::placeholder { color:transparent; transition:color 0.3s; }
    .global-search.expanded input::placeholder { color:#64748b; }
    .search-dropdown { position:absolute; top:40px; right:0; width:300px; background:#fff; border-radius:8px; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1); border:1px solid #cbd5e1; z-index:100; display:none; max-height:400px; overflow-y:auto; color:#1e293b; text-align:left; }
    .search-dropdown.open { display:block; }
    .s-res { display:flex; align-items:center; gap:12px; padding:10px 12px; cursor:pointer; font-size:13px; color:#475569; border-bottom:1px solid #f1f5f9; transition:background 0.2s; }
    .s-res:hover { background:#f1f5f9; }
    .s-res:last-child { border-bottom:none; }
    .s-res .ic { width:32px; height:32px; border-radius:6px; background:#f0f9ff; color:#6366f1; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    .s-res svg { width:16px; height:16px; margin:0; display:block; }
    .s-res .lbl { font-weight:600; color:#0f172a; line-height:1.2; }
    .s-res .grp { font-size:11px; color:#64748b; margin-top:2px; }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = searchStyles;
  document.head.appendChild(styleEl);
})();

// Global URL Routing Handler on Page Load
window.handleUrlRoutingOnLoad = function(groups) {
  if (!groups) return;
  const params = new URLSearchParams(window.location.search);
  let pageId = params.get('page') || window.location.hash.substring(1);
  if (!pageId) return;

  for (const groupTitle in groups) {
    if (groups.hasOwnProperty(groupTitle)) {
      if (groups[groupTitle].some(p => p.id === pageId)) {
        if (typeof activeGroup !== 'undefined') window.activeGroup = groupTitle;
        if (typeof activePage !== 'undefined') window.activePage = pageId;
        if (typeof openTabs !== 'undefined' && !openTabs.includes(groupTitle)) {
          openTabs.push(groupTitle);
        }
        break;
      }
    }
  }
};

// Wire up the global search event listeners
window.wireGlobalSearch = function(moduleKey) {
  const inp = document.getElementById('globalSearch');
  const drop = document.getElementById('searchDropdown');
  const container = document.getElementById('globalSearchContainer');
  
  if (!inp || !drop || !container) return;

  const icon = container.querySelector('svg');
  if (icon) {
    icon.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!container.classList.contains('expanded')) {
        container.classList.add('expanded');
        inp.focus();
      }
    });
  }

  // Flatten the GROUPS object defined on the active page
  let allPages = [];
  const defaultDocIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>';

  if (typeof GROUPS !== 'undefined') {
    for (const groupTitle in GROUPS) {
      if (GROUPS.hasOwnProperty(groupTitle)) {
        GROUPS[groupTitle].forEach(page => {
          allPages.push({
            groupTitle: groupTitle,
            pageId: page.id,
            pageTitle: page.title,
            icon: page.icon || defaultDocIcon
          });
        });
      }
    }
  }

  inp.addEventListener('input', () => {
    const q = inp.value.toLowerCase().trim();
    if (!q) {
      drop.classList.remove('open');
      return;
    }

    const hits = allPages.filter(p => 
      p.pageTitle.toLowerCase().includes(q) || 
      p.groupTitle.toLowerCase().includes(q)
    );

    if (hits.length === 0) {
      drop.innerHTML = '<div style="padding:16px; text-align:center; color:#94a3b8; font-size:13px">No pages found.</div>';
    } else {
      drop.innerHTML = hits.map(h => `
        <div class="s-res" onclick="gotoSearch('${h.groupTitle.replace(/'/g, "\\'")}', '${h.pageId.replace(/'/g, "\\'")}')">
          <div class="ic">${h.icon}</div>
          <div>
            <div class="lbl">${h.pageTitle}</div>
            <div class="grp">${h.groupTitle}</div>
          </div>
        </div>
      `).join('');
    }
    drop.classList.add('open');
  });

  // Handle click outside to close dropdown
  document.addEventListener('click', (e) => {
    if (!container.contains(e.target)) {
      drop.classList.remove('open');
      container.classList.remove('expanded');
    }
  });

  // Global search keyboard shortcut (Ctrl + K)
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      container.classList.add('expanded');
      inp.focus();
    }
  });
};

// Global function to trigger search result clicks
window.gotoSearch = function(groupTitle, pageId) {
  const drop = document.getElementById('searchDropdown');
  const inp = document.getElementById('globalSearch');
  const container = document.getElementById('globalSearchContainer');

  if (drop) drop.classList.remove('open');
  if (inp) inp.value = '';
  if (container) container.classList.remove('expanded');

  // Trigger group selection & tab creation
  if (typeof addTab === 'function') {
    addTab(groupTitle);
  } else if (typeof setGroup === 'function') {
    setGroup(groupTitle);
  }

  // Trigger page selection
  if (typeof setPage === 'function') {
    setPage(pageId);
  }
};
