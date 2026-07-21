# 📚 Study Manager — CS50W Final Project

A web-based study management system built with Django and JavaScript. Study Manager helps students organize their academic life in one place: create subjects and topics, review content with spaced repetition flashcards, track focus time with a Pomodoro timer, set weekly study goals, and visualize progress on a personal dashboard.

---

## 🎥 Video Demo



---

## Distinctiveness and Complexity

### Why this project is distinct from all previous CS50W projects

Study Manager is fundamentally different from every project built throughout this course. Project 0 was a static frontend exercise with no backend whatsoever. Project 1 (Wiki) introduced Django but was limited to a single model and basic CRUD operations over Markdown files — there was no real-time interactivity, no user-specific data, and no JavaScript beyond what was minimally needed. Project 2 (Commerce) introduced multiple Django models and user authentication, but its domain was e-commerce: auction listings, bids, and watchlists. Project 3 (Mail) was a single-page email client driven almost entirely by JavaScript consuming a pre-built API — no custom models were designed by the student. Project 4 (Network) introduced asynchronous JavaScript and pagination, but its domain was a social network: posts, likes, followers, and a feed.

Study Manager operates in an entirely different domain — personal productivity and education — and combines features that none of the previous projects approached individually, let alone together. It is not a social network, it does not have listings or bids, it does not replicate email, and it does not present a content feed. It is a tool built specifically for students who want to manage their study routine, and every feature of the application exists to serve that purpose.

### Why this project is more complex than all previous CS50W projects

The complexity of Study Manager comes from several dimensions working together.

**Data architecture.** The application uses six custom Django models: `Subject`, `Topic`, `Flashcard`, `FlashcardReview`, `PomodoroSession`, and `WeeklyGoal`. These models are interconnected through multiple ForeignKey relationships and contain business logic directly on the model layer — not just in views. For example, `Subject.progress()` computes the percentage of completed topics dynamically, `WeeklyGoal.current_hours()` runs an aggregated query filtering Pomodoro sessions by date range to calculate how many hours a student has studied toward a goal in the current week, and `WeeklyGoal.percentage()` derives a completion ratio from that. This is a level of relational data modeling and model-layer logic that surpasses every previous project in the course.

**Spaced Repetition System (SRS).** The flashcard module implements a simplified but real algorithm for spaced repetition — the same cognitive science technique used by tools like Anki. After reviewing a flashcard, the student rates their performance as "Easy", "Hard", or "Wrong". The `Flashcard.apply_review()` method in Python then calculates the next review date based on the current interval: an "Easy" rating doubles the interval (minimum 7 days), "Hard" resets to 2 days, and "Wrong" resets to 1 day. This `interval_days` field grows over time as the student demonstrates mastery, and the `next_review_date` field is updated accordingly. Every day, the dashboard and flashcard list surface only the cards that are due for review, creating a prioritized study queue. This algorithm required careful design of the model, the review endpoint, and the frontend session flow — it did not exist in any form in previous projects.

**Asynchronous JavaScript across multiple modules.** While Project 3 and Project 4 introduced `fetch()` calls, Study Manager applies asynchronous JavaScript across three distinct modules with different interaction patterns. In the Topics module, checking a topic as complete triggers a `fetch POST` that updates the database and immediately re-renders the subject's progress bar and percentage badge without any page reload — the DOM is updated surgically based on the JSON response. In the Flashcard review session, the entire study flow (loading cards one by one, flipping them, submitting ratings, advancing the queue, and detecting session completion) is handled entirely in JavaScript consuming a JSON payload rendered by Django into the page. In the Pomodoro timer, a completed focus cycle triggers a `fetch POST` that saves the session to the database automatically, without any user action.

**CSS 3D Flip Animation.** The flashcard review interface implements a genuine CSS 3D card flip using `transform-style: preserve-3d`, `perspective`, `backface-visibility: hidden`, and `rotateY(180deg)`. Both the front and back faces of the card are absolutely positioned elements that coexist in 3D space, and JavaScript controls the flip by toggling a single CSS class. This is a technique that requires understanding of how the browser renders 3D transformations and was not covered or required in any previous project.

**Pomodoro Timer with Web Notifications API.** The timer module implements a full Pomodoro cycle manager in vanilla JavaScript: 25-minute focus intervals alternate with 5-minute short breaks, and every fourth cycle triggers a 15-minute long break. The state machine tracks whether the current phase is focus or rest, counts cycles, and updates a progress bar in real time. At the end of each focus cycle, the browser's Web Notifications API is called to send a desktop notification alerting the student, even if the tab is not in focus. This required requesting notification permissions and handling the asynchronous permission response. None of this was present in previous projects.

**Activity Heatmap.** The dashboard renders a 12-week activity heatmap entirely with vanilla JavaScript — no external charting library. A dedicated Django API endpoint (`/dashboard/activity/`) returns a JSON object mapping date strings to session counts. The JavaScript then iterates over the past 84 days, creates a colored cell for each one, and applies a green intensity scale based on the number of Pomodoro sessions completed that day, replicating the well-known GitHub contributions graph. The data pipeline from Django queryset to JSON to DOM required designing both the backend aggregation and the frontend rendering logic.

**Weekly Goals with dynamic progress.** The goals module introduces the concept of time-bounded targets: each `WeeklyGoal` is tied to a specific calendar week (anchored to the Monday of that week), and its progress is computed in real time by summing completed Pomodoro sessions within that date range. The `update_or_create()` pattern ensures that creating a goal for a subject that already has one this week updates it rather than duplicating it. The dashboard surfaces the current week's goals with live progress bars, giving students immediate feedback on where they stand.

In summary, Study Manager combines a domain-specific data model, a cognitive science algorithm, multiple asynchronous JavaScript flows, CSS 3D animation, browser APIs, and dynamic data visualization into a single cohesive application — making it distinctly more complex than any individual project in this course, and distinct in purpose from all of them.

---

## 📁 Files and Directories

```
study-manager/
├── study_manager/
│   ├── settings.py         — project configuration: installed apps, templates dir,
│   │                         static files, login redirects
│   ├── urls.py             — root URL config, delegates all routes to core.urls
│   └── wsgi.py             — WSGI entry point for deployment
│
├── core/
│   ├── migrations/         — auto-generated database migration files
│   ├── admin.py            — registers all six models in the Django admin panel
│   │                         with list_display, list_filter, and search_fields
│   ├── apps.py             — app configuration
│   ├── models.py           — all six custom models (described below)
│   ├── urls.py             — all 20 URL patterns for the application
│   └── views.py            — all views: dashboard, auth, subjects, topics,
│                             flashcards, pomodoro, goals, and JSON API endpoints
│
├── templates/
│   ├── layout.html         — base Bootstrap 5 template with navbar (including
│   │                         POST logout form), flash messages, and block tags
│   ├── dashboard.html      — summary cards, flashcard alert, weekly goal bars,
│   │                         recent sessions, and heatmap container
│   ├── login.html          — login form extending layout
│   ├── register.html       — registration form extending layout
│   ├── subjects/
│   │   ├── list.html       — grid of subject cards with color, progress bar,
│   │   │                     and action buttons
│   │   ├── detail.html     — topic list with inline create form, checkboxes
│   │   │                     for toggle, and delete buttons (all via fetch/AJAX)
│   │   ├── form.html       — shared create/edit form with color picker input
│   │   └── confirm_delete.html — confirmation screen before cascading delete
│   ├── flashcards/
│   │   ├── list.html       — filterable card grid with due-today badges
│   │   │                     and per-card delete via fetch
│   │   ├── form.html       — flashcard creation form
│   │   └── review.html     — full review session: CSS 3D flip card, rating
│   │                         buttons, progress bar, completion screen
│   ├── pomodoro/
│   │   └── timer.html      — subject selector, large timer display, play/pause/
│   │                         reset controls, cycle badge, and session history
│   └── goals/
│       ├── list.html       — weekly goal cards with dynamic progress bars
│       └── form.html       — goal creation form with hours input
│
├── static/
│   ├── css/
│   │   └── styles.css      — all custom styles: CSS variables for the color
│   │                         palette, navbar, cards, forms, buttons, flashcard
│   │                         3D flip, Pomodoro timer display, heatmap, alerts,
│   │                         badges, list groups, and mobile responsive rules
│   └── js/
│       ├── topics.js       — handles topic checkbox toggle and delete via fetch;
│       │                     updates progress bar and badge without page reload
│       ├── flashcard.js    — manages the full review session: loads cards from
│       │                     JSON, controls CSS flip, handles rating submission
│       │                     via fetch, advances the queue, shows completion screen
│       ├── pomodoro.js     — full Pomodoro state machine: setInterval countdown,
│       │                     pause/reset controls, focus/break cycle management,
│       │                     Web Notifications API, and auto-save via fetch POST
│       └── dashboard.js    — fetches activity data from /dashboard/activity/ and
│                             renders a 12-week heatmap grid with color intensity
│
├── requirements.txt        — Python dependencies (Django)
├── manage.py               — Django management entry point
└── README.md               — this file
```

---

## 🗃️ Models

### `Subject`
Represents an academic subject or course. Belongs to a `User`. Has a `color` (hex string) used throughout the interface for visual identification. The `progress()` method computes the percentage of associated `Topic` objects marked as completed.

### `Topic`
Represents a chapter, unit, or subtopic within a `Subject`. Has a `name`, optional `notes` text, an `is_completed` boolean, and an `order` integer. The `is_completed` field is toggled asynchronously via JavaScript without page reload.

### `Flashcard`
Represents a question/answer pair linked to a `Subject`. Implements the SRS algorithm through `next_review_date`, `interval_days`, and `ease_factor` fields. The `apply_review(rating)` method updates these fields based on the student's self-assessment. The `is_due_today()` method returns `True` when the card is ready for review.

### `FlashcardReview`
An audit log of every flashcard review event. Records which `Flashcard` was reviewed, the rating given (`easy`, `hard`, or `wrong`), and the timestamp. Used to track study history.

### `PomodoroSession`
Records a completed (or interrupted) Pomodoro focus session. Linked to both a `User` and a `Subject`. Stores the start time, duration in minutes, and whether the session was completed. These records feed the dashboard heatmap and the weekly goal progress calculations.

### `WeeklyGoal`
A target number of study hours for a specific `Subject` in a specific calendar week (anchored to Monday via `week_start`). The `current_hours()` method sums the duration of all completed `PomodoroSession` records for that subject within the goal's week. The `percentage()` method returns the completion ratio capped at 100%. A `unique_together` constraint prevents duplicate goals for the same subject and week.

---

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/study-manager.git
cd study-manager
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Open in browser

Navigate to **http://127.0.0.1:8000** and create an account to get started.

The Django admin panel is available at **http://127.0.0.1:8000/admin** using the superuser credentials.

---

## 📝 Additional Notes

- **Authentication:** All views are protected with `@login_required`. Every database query filters by `request.user`, ensuring complete data isolation between users — no user can access another user's subjects, flashcards, or sessions under any route.

- **CSRF protection:** All `fetch` POST and DELETE requests include the `X-CSRFToken` header using the token rendered into the template. The logout action uses a `<form method="POST">` instead of a plain link, complying with Django 5's default requirement that logout be performed via POST.

- **Color palette:** The interface uses a five-color palette defined as CSS custom properties (`--blue-dark: #243A69`, `--blue-mid: #5B88A5`, `--white-ice: #F4F4F2`, `--beige: #D4CDC5`, `--dark-wine: #191013`) applied consistently across all components.

- **Mobile responsiveness:** All pages use Bootstrap 5's responsive grid system (`col-12 col-md-6 col-lg-4`) and custom media queries in `styles.css`. The navbar collapses into a hamburger menu on small screens. The flashcard flip scene and the Pomodoro timer display scale down for narrow viewports.

- **No external JavaScript libraries:** All JavaScript in this project is written in vanilla JS. The flashcard flip, Pomodoro timer, fetch calls, DOM manipulation, and heatmap rendering use no jQuery, no React, and no charting libraries — only browser-native APIs.

- **SRS algorithm note:** The spaced repetition implementation is a simplified version inspired by the SM-2 algorithm. It does not implement the full SuperMemo formula but demonstrates the core principle: intervals grow with successful recall and reset with failure, reducing review frequency for well-learned material over time.