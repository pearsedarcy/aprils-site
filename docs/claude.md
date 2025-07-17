# 🤖 AI Context Guide: White-Labeled Wagtail Blog

## Project Summary
This project is a modular, white-labeled Wagtail blog and portfolio application built on Django. It features:
- Modular apps: blog, portfolio, CV, timeline, home, base, search, theme
- Highly customizable StreamField blocks for flexible content
- Tailwind CSS integration for modern styling
- Cloudinary support for media storage (optional)
- Docker and Heroku deployment support
- Custom navigation, header/footer, and social links
- Admin UI for content, users, and settings
- Email/contact form support

## Codebase Structure
- Each app (blog, portfolio, etc.) has its own models, templates, blocks, and migrations.
- Shared blocks and settings are in the `base` app.
- Static assets and theme templates are in the `theme` app.
- Project settings are in `poxed/settings/` (base, dev, prod configs).
- Deployment and customization docs are in `docs/`.

## Key Conventions
- Use StreamField for flexible, block-based page content.
- Templates are organized by app and by block/component.
- Static assets are managed with Tailwind CSS and npm.
- Environment variables are managed via `.env` (never commit secrets).
- Use Docker for local/prod parity when possible.
- Use Wagtail admin for content and user management.

## Best Practices for AI Agents
- Always check for existing documentation in `docs/` before answering or making changes.
- When adding features, prefer modularity: create new apps, blocks, or templates as needed.
- When customizing, update both code and documentation for maintainability.
- For deployment/configuration, reference `DEPLOYMENT.md` and `poxed/settings/base.py`.
- For content structure, reference `CUSTOMISATION.md` and StreamField usage in models.
- For troubleshooting, check `OPERATION.md` and relevant logs.
- When in doubt, link to or quote official Wagtail/Django docs.

## Common Tasks & Where to Look
- **Add a new page type:** Create a model in the relevant app, add a template, update `INSTALLED_APPS`.
- **Add a new block:** Define in `blocks.py`, add to StreamField in `models.py`, create a template in `templates/blocks/`.
- **Change branding:** Update static assets in `theme/static/images/` and templates in `theme/templates/`.
- **Update navigation/footer:** Edit templates in `base/templates/base/includes/` and logic in `base/templatetags/navigation_tags.py`.
- **Configure media storage:** See `poxed/settings/base.py` and `.env` for Cloudinary or local setup.
- **Run management commands:** Use `python manage.py <command>` or `uv run python manage.py <command>`.

## Tips for Effective Contributions
- Keep changes modular and well-documented.
- Update or add tests in each app's `tests.py` as needed.
- Use clear, descriptive commit messages.
- Reference relevant documentation and code files in PRs or answers.
- Follow Django and Wagtail security and accessibility best practices.

## Further Reading
- [Wagtail documentation](https://docs.wagtail.org/)
- [Django documentation](https://docs.djangoproject.com/)
- [Django Tailwind](https://django-tailwind.readthedocs.io/)
- [Cloudinary for Django](https://cloudinary.com/documentation/django_integration)
- See `docs/` for deployment, customization, and operation guides. 