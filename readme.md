# Stuble - Bible Study Platform

![Stuble Logo](https://img.icons8.com/color/96/holy-bible.png)

Stuble is a modern web application designed to help you dive deeper into God's Word. Read multiple Bible versions, take rich notes, organize your insights into records, and group them into collections – all in one place.

**Live site:** [https://stuble.site](https://stuble.site)

---

## Features

- 📖 **Bible Reading** – Access multiple Bible translations, search by book, chapter, and verse.
- 📝 **Study Records** – Create individual records for your study sessions with rich text notes (powered by Quill).
- 🔖 **Scripture Attachments** – Attach Bible passages directly to your records for easy reference.
- 📂 **Collections** – Group related records into custom collections (e.g., “Faith”, “Prayer”, “Romans Study”).
- 🔍 **Powerful Search** – Search records by title or note content.
- 👤 **User Accounts** – Secure authentication (email/password) with password reset.
- 📧 **Waiting List** – Early access sign‑up (currently replaced by direct registration).
- 🖼️ **Cloudinary Integration** – Upload and manage images seamlessly.
- 📱 **Fully Responsive** – Works beautifully on desktop, tablet, and mobile.

---

## Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) (Python)
- **Database:** PostgreSQL (production) / SQLite (development)
- **Frontend:** Bootstrap 5, Bootstrap Icons, jQuery
- **Rich Text Editor:** [django-quill-editor](https://github.com/LeeHanYeong/django-quill-editor)
- **Image Hosting:** [Cloudinary](https://cloudinary.com/)
- **Email:** SMTP (Professional email)
- **Deployment:** Gunicorn + Nginx on Ubuntu
- **Other Libraries:** `django-import-export`, `python-decouple`, `Pillow`, etc.

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stuble.git
   cd stuble
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
Create a `.env` file in the project root (next to manage.py) with the following:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=Stuble <your-email@gmail.com>
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` in your browser