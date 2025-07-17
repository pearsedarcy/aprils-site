# 🛠️ Operation Guide: White-Labeled Wagtail Blog

## Table of Contents
1. Project Overview
2. Accessing the Admin
3. Managing Content
4. User Management & Permissions
5. Backups & Maintenance
6. Content Workflow
7. Monitoring & Analytics
8. Scheduled Tasks
9. Troubleshooting & FAQ
10. Useful Commands
11. Further Reading

---

## 1. Project Overview
This guide explains how to operate, manage, and maintain your white-labeled Wagtail blog and portfolio application on a day-to-day basis. It covers admin access, content management, user roles, workflow, backups, troubleshooting, and more.

---

## 2. Accessing the Admin
- Go to `/admin/` on your deployed site.
- Log in with your superuser or staff credentials.
- The Wagtail admin dashboard allows you to manage all content and settings.

---

## 3. Managing Content

### 3.1. Pages
- Add, edit, or delete pages (blog posts, portfolio items, CV, etc.) via the Pages section.
- Use StreamField blocks for flexible content layouts (see `home/models.py`, `portfolio/models.py`).
- Preview changes before publishing.

### 3.2. Images & Documents
- Upload and manage images and documents in the Media section.
- Use the image/document chooser in page editors to insert media.

### 3.3. Forms
- View form submissions (e.g., contact form) in the Forms section.
- Configure email notifications for form submissions in the Wagtail admin or settings.

---

## 4. User Management & Permissions
- Add or remove users in the Users section.
- Assign roles and permissions as needed (e.g., Editors, Moderators, Admins).
- Encourage strong passwords and two-factor authentication if available.

### 4.1. User Roles & Permissions Matrix
| Role      | Can Edit Content | Can Publish | Can Manage Users | Can Access Settings |
|-----------|-----------------|-------------|------------------|--------------------|
| Admin     | Yes             | Yes         | Yes              | Yes                |
| Editor    | Yes             | Yes         | No               | No                 |
| Moderator | Yes             | No          | No               | No                 |
| Author    | Yes (own)       | No          | No               | No                 |

- For advanced permission setup, see [Wagtail permissions docs](https://docs.wagtail.org/en/stable/topics/permissions.html).

---

## 5. Backups & Maintenance
- Regularly back up your database and media files.
- For SQLite: copy the `db.sqlite3` file and the `media/` directory.
- For other databases, use appropriate dump/export tools.
- Periodically update dependencies and apply security patches.

### 5.1. Restoring from Backup
- To restore SQLite, replace `db.sqlite3` and `media/` with your backup copies.
- For Postgres or other databases, use the appropriate restore command.
- After restoring, run `python manage.py migrate` to ensure schema is up to date.

---

## 6. Content Workflow
- Wagtail supports drafts, moderation, and publishing workflows.
- Editors can save drafts, submit for moderation, and publish content.
- Admins can approve and publish content.
- Use the "Workflow" and "Revisions" features in the Wagtail admin for advanced content review.
- See [Wagtail workflow docs](https://docs.wagtail.org/en/stable/topics/workflow.html).

---

## 7. Monitoring & Analytics
- Integrate analytics (e.g., Google Analytics) by adding tracking code to `theme/templates/base.html`.
- Monitor server logs for errors and performance issues.
- Use uptime monitoring services for production deployments.
- For Docker: `docker logs <container-id>`
- For Heroku: `heroku logs --tail`

---

## 8. Scheduled Tasks
- For regular backups, use cron jobs or scheduled tasks on your server or cloud platform.
- For periodic emails or maintenance, use Django management commands with a scheduler.
- See [Django custom commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/).

---

## 9. Troubleshooting & FAQ

### 9.1. Common Issues
- **Static files not loading:** Ensure `collectstatic` has been run and static files are served.
- **Emails not sending:** Check email configuration in `.env` and server logs.
- **Media not uploading:** Verify Cloudinary or local media configuration.
- **Page not found (404):** Check page tree in Wagtail admin and ensure the page is published.
- **Database errors:** Check your `DATABASE_URL` and database server status.
- **Permission denied:** Check user roles and permissions in the admin.
- **How do I restore from backup?** See section 5.1 above.

### 9.2. Logs
- View logs using your hosting provider's dashboard or by running:
  ```bash
  python manage.py runserver
  # or for Docker
  docker logs <container-id>
  ```

---

## 10. Useful Commands
- Run development server:  
  `python manage.py runserver`
- Create new migrations:  
  `python manage.py makemigrations`
- Apply migrations:  
  `python manage.py migrate`
- Collect static files:  
  `python manage.py collectstatic`
- Create superuser:  
  `python manage.py createsuperuser`
- Rebuild Tailwind CSS:  
  `python manage.py tailwind build`

---

## 11. Further Reading
- [Wagtail documentation](https://docs.wagtail.org/)
- [Django documentation](https://docs.djangoproject.com/)
- [Wagtail permissions](https://docs.wagtail.org/en/stable/topics/permissions.html)
- [Wagtail workflow](https://docs.wagtail.org/en/stable/topics/workflow.html)
- [Django custom management commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- See `home/models.py`, `portfolio/models.py`, and `theme/templates/` for examples. 