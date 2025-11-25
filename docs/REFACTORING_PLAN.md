# Refactoring Plan for April's Site

This document outlines recommended improvements identified during code review.

## Progress Tracker

| Phase | Status | Completed |
|-------|--------|-----------|
| Phase 1: Critical Fixes | ✅ Complete | 2024-11-25 |
| Phase 2: Code Quality | 🟡 In Progress | - |
| Phase 3: Configuration | 🟡 Started | - |
| Phase 4: Testing | 🟢 Ongoing | - |

## Priority Matrix

| Priority | Category | Issue Count | Effort |
|----------|----------|-------------|--------|
| 🔴 High | Security & Testing | 4 | Medium |
| 🟡 Medium | Code Quality | 7 | High |
| 🟢 Low | Configuration & Docs | 9 | Low |

---

## Phase 1: Critical Fixes (Week 1) ✅ COMPLETED

### 1.1 Fix Settings Organization ✅

**Status:** Complete

Changes made:
- Cleaned `dev.py` - removed all production database config (dj_database_url)
- Removed hardcoded SECRET_KEY, now uses env var with dev fallback
- Dynamic NPM path using `shutil.which('npm')`
- Uses local file storage in development (not Cloudinary)
- Cleaned `base.py` - removed duplicate TAILWIND_APP_NAME and daisyui_themes function
- Added `WAGTAILADMIN_BASE_URL` with env var support

### 1.2 Add Basic Tests ✅

**Status:** Complete (33 tests, all passing)

Created tests for:
- `base/tests.py` - NavigationSettings, FooterText, HeaderConfiguration, FooterConfiguration, SiteLogo, SiteFavicon, FormPage, template tags, context processors
- `blog/tests.py` - Author, BlogIndexPage, BlogPage, BlogTagIndexPage
- `portfolio/tests.py` - PortfolioPage
- `cv/tests.py` - CVPage  
- `timeline/tests.py` - TimelinePage

### 1.3 Remove Hardcoded Secrets ✅

**Status:** Complete

`dev.py` now uses:
```python
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-dev-only-change-in-production')
```

---

## Phase 2: Code Quality (Week 2-3) 🟡 IN PROGRESS

### 2.1 Create Shared Button Block ✅

**Status:** Complete

Created in `base/blocks.py`:
- `ButtonBlock` - Reusable single button with page/URL support and style options
- `DualButtonMixin` - Helper methods for primary/secondary button patterns

Created templates:
- `base/templates/base/blocks/button_block.html`
- `base/templates/base/includes/dual_buttons.html`

### 2.2 Create SEO Mixin for Pages ⬜

**File:** `base/models.py`

```python
class SEOMixin(models.Model):
    """Mixin for SEO and social sharing fields."""
    
    og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Social sharing image",
        help_text="Image for social media sharing (recommended: 1200x630px)"
    )
    
    promote_panels = [
        FieldPanel('og_image'),
    ]
    
    class Meta:
        abstract = True
```

Then update pages to use it:

```python
# blog/models.py
from base.models import SEOMixin

class BlogPage(SEOMixin, Page):
    # ... existing fields
    
    promote_panels = Page.promote_panels + SEOMixin.promote_panels
```

### 2.3 Standardize Block Inheritance ⬜

Update `TimelineStreamBlock` and `CVStreamBlock` to extend `BaseStreamBlock`:

```python
# timeline/blocks.py
from base.blocks import BaseStreamBlock

class TimelineStreamBlock(BaseStreamBlock):
    timeline_card = TimelineCardBlock()
    
    class Meta:
        icon = 'time'
```

### 2.4 Upgrade BlogPage to StreamField ⬜

```python
# blog/models.py
from base.blocks import BaseStreamBlock

class BlogPage(Page):
    intro = models.CharField(max_length=250, blank=True)
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    
    # ... rest of model
```

---

## Phase 3: Configuration & Polish (Week 4) 🟡 STARTED

### 3.1 Fix NPM Path ✅

**Status:** Complete

`dev.py` now uses:
```python
NPM_BIN_PATH = shutil.which('npm') or "npm"
```

### 3.2 Fix WAGTAILADMIN_BASE_URL Warning ✅

**Status:** Complete

`base.py` now uses:
```python
WAGTAILADMIN_BASE_URL = env('WAGTAILADMIN_BASE_URL', default='http://localhost:8000')
```

Updated `.env.example` with the new variable.

### 3.3 Clean Up Dependencies ⬜

**File:** `pyproject.toml`

```toml
[project]
dependencies = [
    # Remove 'environ' - use only django-environ
    "django-environ~=0.12.0",  # Use ~= for compatible releases
    # ... other deps with ~= specifiers
]
```

### 3.4 Move Inline Styles to CSS ⬜

Create dedicated CSS for blocks:

**File:** `theme/static_src/src/components/blocks.css`

```css
/* Hero Block */
.hero-gradient {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
}

/* Timeline animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```

### 3.5 Extract JavaScript ⬜

**File:** `theme/static/js/components/theme-switcher.js`

```javascript
// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeButtons = document.querySelectorAll('[data-theme]');
    // ... theme switching logic
});
```

### 3.6 Fix Template ID Naming ⬜

**File:** `base/templates/base/includes/header.html`

```html
<!-- Change from -->
<div id="page-logo-tranny">

<!-- To -->
<div id="page-logo-transition">
```

---

## Phase 4: Testing & Documentation (Ongoing) 🟢 STARTED

### 4.1 Test Coverage Goals

| App | Current | Target |
|-----|---------|--------|
| base | ~60% | 80% |
| blog | ~50% | 75% |
| portfolio | ~40% | 75% |
| cv | ~40% | 70% |
| timeline | ~40% | 70% |
| home | 0% | 60% |

### 4.2 Recommended Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── factories.py         # Model factories
├── test_base/
│   ├── test_models.py
│   ├── test_blocks.py
│   └── test_forms.py
├── test_blog/
│   └── test_models.py
└── ...
```

### 4.3 Add Type Hints ⬜

Gradually add type hints to improve code quality:

```python
# base/models.py
from typing import Optional
from wagtail.models import Page

class NavigationSettings(BaseSiteSetting):
    def get_menu_items(self) -> list[Page]:
        """Return list of pages for navigation menu."""
        ...
```

---

## Implementation Order

1. **Week 1:** Security fixes + basic tests ✅
2. **Week 2:** Shared ButtonBlock + SEO mixin 🟡
3. **Week 3:** Block standardization + BlogPage upgrade
4. **Week 4:** Configuration cleanup + JS/CSS extraction
5. **Ongoing:** Expand test coverage, add type hints

## Success Metrics

- [x] All tests pass (33 tests)
- [x] No hardcoded secrets in codebase
- [x] Button component created for reuse
- [x] WAGTAILADMIN_BASE_URL warning fixed
- [ ] SEO fields available on all content pages
- [ ] Button rendering unified across all templates  
- [ ] Test coverage > 70%
- [ ] No inline styles/scripts in templates
