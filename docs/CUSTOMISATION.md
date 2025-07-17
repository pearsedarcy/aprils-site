# 🎨 Customisation Guide: White-Labeled Wagtail Blog

## Table of Contents
1. Project Overview
2. Branding
3. Templates & Layout
4. Static Assets (CSS, JS, Images)
5. Content Structure
6. Advanced Customisation
7. Customising the Admin
8. Accessibility & Performance
9. Best Practices
10. Walkthroughs
11. Further Reading

---

## 1. Project Overview
This guide explains how to customize the look, feel, and structure of your white-labeled Wagtail blog and portfolio application. The project is modular, with each app (blog, portfolio, CV, timeline, etc.) providing its own templates, blocks, and models for maximum flexibility.

---

## 2. Branding

### 2.1. Site Name & Metadata
- Change the site name and default metadata in the Wagtail admin under Settings > Sites.
- Update SEO settings in the Wagtail admin or in the relevant templates (see `theme/templates/base.html`).

### 2.2. Logo & Favicon
- Replace logo and favicon files in `theme/static/images/` or `static/images/`.
- Update references in `theme/templates/base.html` or other relevant templates.

---

## 3. Templates & Layout

### 3.1. Editing Templates
- All main templates are in `theme/templates/` and app-specific templates (e.g., `blog/templates/`, `portfolio/templates/`).
- Edit HTML files to change layout, add or remove sections, or adjust structure.
- For example, to change the blog index layout, edit `blog/templates/blog/blog_index_page.html`.

### 3.2. Blocks & Components
- Reusable blocks are in `base/templates/base/blocks/` and similar folders in each app.
- Modify or add new blocks for custom content types. See `home/blocks.py` and `portfolio/blocks.py` for examples.
- To add a new block, define it in the relevant `blocks.py` and register it in the StreamField in `models.py`.

---

## 4. Static Assets (CSS, JS, Images)

### 4.1. CSS (Tailwind)
- Main styles are in `theme/static_src/src/` and compiled to `theme/static/css/`.
- To change styles, edit the source files and run:
  ```bash
  cd theme/static_src
  npm run build
  ```
- For Tailwind config, see `theme/static_src/postcss.config.js`.

### 4.2. JavaScript
- Custom JS is in `theme/static/js/` or app-specific static folders.
- Update or add scripts as needed.

### 4.3. Images
- Store new images in `theme/static/images/` or `static/images/`.
- Reference them in templates or via the Wagtail image chooser.

---

## 5. Content Structure

### 5.1. Page Types
- Add or modify page types in each app's `models.py` (e.g., `blog/models.py`).
- Use Wagtail StreamField for flexible content blocks. See `home/models.py` for an example HomePage with StreamField.

### 5.2. Menus & Navigation
- Edit navigation templates in `base/templates/base/includes/` or similar.
- Update menu logic in `base/templatetags/navigation_tags.py` if needed.

---

## 6. Advanced Customisation

### 6.1. Adding New Apps or Features
- Create new Django apps and register them in `INSTALLED_APPS` in your settings (`poxed/settings/base.py`).
- Add templates, static files, and models as needed.

### 6.2. Custom Functionality
- Add custom Python logic in app directories.
- Use Django signals, middleware, or Wagtail hooks for advanced features.

### 6.3. Extending StreamField Blocks
- Define new blocks in `blocks.py` and add them to the StreamField in `models.py`.
- Example: To add a new card block to the portfolio, see `portfolio/blocks.py` and `portfolio/models.py`.

### 6.4. Translation & Localization
- To enable translation, use Wagtail's i18n features and Django's translation framework.
- Mark strings for translation in templates and Python code.
- See [Wagtail i18n docs](https://docs.wagtail.org/en/stable/topics/i18n.html).

---

## 7. Customising the Admin
- Change branding and colors in the Wagtail admin via custom CSS or by overriding admin templates.
- See [Wagtail admin theming](https://docs.wagtail.org/en/stable/advanced_topics/admin_customisation.html).
- Add custom panels or dashboard widgets in your app's `wagtail_hooks.py`.

---

## 8. Accessibility & Performance
- Use semantic HTML and ARIA attributes in templates.
- Test with screen readers and keyboard navigation.
- Optimize images and use responsive image tags.
- Minimize CSS/JS bundle size (Tailwind build, code splitting).
- Use Lighthouse or similar tools to audit accessibility and performance.

---

## 9. Best Practices
- Keep customizations modular (use separate apps, blocks, and templates).
- Use version control for all code and configuration.
- Document custom blocks and templates for future maintainers.
- Test changes in a staging environment before deploying to production.
- Follow Django and Wagtail security best practices.

---

## 10. Walkthroughs

### 10.1. How to Add a New Page Type
1. Create a new app (if needed): `python manage.py startapp myapp`
2. Define a new Page model in `myapp/models.py` (subclass `wagtail.models.Page`).
3. Add fields and StreamField blocks as needed.
4. Create a template in `myapp/templates/myapp/`.
5. Register the app in `INSTALLED_APPS`.
6. Run migrations and create a page in the Wagtail admin.

### 10.2. How to Add a New Block
1. Define a new block in `blocks.py` (e.g., `class MyBlock(StructBlock): ...`).
2. Add the block to a StreamField in `models.py`.
3. Create a template for the block in the appropriate `templates/blocks/` folder.
4. Reference the block in your page template.

---

## 11. Further Reading
- [Wagtail documentation](https://docs.wagtail.org/)
- [Django documentation](https://docs.djangoproject.com/)
- [Wagtail StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html)
- [Wagtail admin customization](https://docs.wagtail.org/en/stable/advanced_topics/admin_customisation.html)
- [Wagtail i18n](https://docs.wagtail.org/en/stable/topics/i18n.html)
- See `home/blocks.py`, `portfolio/blocks.py`, and `theme/templates/` for examples. 