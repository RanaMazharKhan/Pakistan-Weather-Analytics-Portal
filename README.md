# ⛅ PakWeatherAnalytics

A high-performance, professional Django Web Application built to analyze, visualize, and report historical weather trends and updates across major cities in Pakistan (including Lahore, Karachi, Islamabad, Peshawar, Quetta, and more).

## 🚀 Key Features

*   **Interactive Analytics Dashboard**: Beautiful visualizations utilizing Chart.js, including temperature trend lines, weather condition distributions, and precipitation comparison bar charts.
*   **Live Open-Meteo Integration**: Dynamic syncing with the Open-Meteo API to fetch 90-day historical weather records.
*   **Automated Insights Engine**: Statistical climate calculations pointing out trends, maximum/minimum temperature extremes, and rain patterns.
*   **Daily Email Summaries**: Automated email reporting engine sending customized daily weather insights to users' registered inboxes based on city preferences.
*   **Advanced Exports**: Export filtered weather records and trends instantly to **CSV** or publication-quality **PDF reports**.
*   **Modern Glassmorphism UI**: Stunning custom interface leveraging Google's Outfit font, CSS animations, and smooth fadeInUp transitions.
*   **Full CRUD Admin Panel**: Full administrative panel to manage weather records, trigger database synchronization, and customize user accounts.
*   **Python 3.14 Compatibility**: Fully patched to work flawlessly on the latest Python 3.14.3 runtimes.

---

## 🛠️ Technology Stack

*   **Backend**: Django 4.2+ (Python)
*   **Database**: SQLite (Local Dev) / PostgreSQL (Production)
*   **Frontend**: HTML5, CSS3 (Custom Glassmorphism styling), Bootstrap 5.3, JavaScript (ES6)
*   **Data Science & Charts**: Pandas, NumPy, Chart.js v4
*   **Reporting**: ReportLab (PDF Generation)
*   **Asynchronous Tasks**: Django Background Tasks

---

## 💻 Local Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RanaMazharKhan/pakweatheranalytics.git
   cd pakweatheranalytics
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Email Configuration (SMTP/Console)
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

5. **Run migrations and start the server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🌐 SEO & Ranking Strategy

This project contains optimal `<meta>` structures in the template headers to help pages index and rank for search terms like:
*   *"Pakistan weather"*
*   *"Lahore weather data"*
*   *"Karachi climate analytics"*
*   *"Historical weather Pakistan"*
