# 📚 Study Manager — CS50W Final Project

A web-based study management system built with Django and JavaScript. Students can organize subjects and topics, review content with spaced repetition flashcards, track focus time with a Pomodoro timer, set weekly study goals, and visualize progress on a personal dashboard.

## 🎥 Video Demo

> [Link do vídeo]

---

## Distinctiveness and Complexity

Study Manager is distinct from all previous projects in this course. It is not a social network like Project 4, nor an e-commerce site like Project 2. It operates in the domain of personal productivity and education, which was not explored in any previous assignment.

The project is more complex than previous work for several reasons. It uses six custom Django models (`Subject`, `Topic`, `Flashcard`, `FlashcardReview`, `PomodoroSession`, and `WeeklyGoal`) with interconnected ForeignKey relationships and business logic embedded directly in the model layer — for example, `Subject.progress()` calculates topic completion dynamically, and `WeeklyGoal.current_hours()` aggregates Pomodoro sessions filtered by the current calendar week.

The flashcard module implements a spaced repetition algorithm (SRS): after reviewing a card, the student rates their performance as Easy, Hard, or Wrong, and the `apply_review()` method updates the card's `next_review_date` and `interval_days` accordingly. This is real learning science applied in Python, and it drove the design of both the model and the review session interface.

JavaScript is used non-trivially across three modules. Topic checkboxes update the database and re-render the progress bar via `fetch` without reloading the page. The flashcard review session loads all due cards as JSON and manages the entire flow — including a CSS 3D flip animation — in the browser. The Pomodoro timer uses `setInterval` to count down, manages focus and break cycles, triggers desktop notifications via the Web Notifications API, and saves completed sessions automatically via `fetch POST`.

The application is fully mobile-responsive using Bootstrap 5's grid system and custom media queries.

---

## Files

### `study_manager/`
- `settings.py` — project configuration: installed apps, templates directory, static files, login redirects
- `urls.py` — root URL config, delegates all routes to `core.urls`

### `core/`
- `models.py` — all six custom models with their fields and business logic methods
- `views.py` — all views for dashboard, authentication, subjects, topics, flashcards, pomodoro, goals, and JSON API endpoints
- `urls.py` — 20 URL patterns covering all pages and API routes
- `admin.py` — all models registered in the Django admin panel

### `templates/`
- `layout.html` — base Bootstrap 5 template with navbar and flash messages
- `dashboard.html` — summary cards, flashcard alert, weekly goals, session history, and activity heatmap
- `login.html` / `register.html` — authentication pages
- `subjects/list.html` — subject cards with progress bars
- `subjects/detail.html` — topic list with inline create form and async toggle/delete
- `subjects/form.html` — shared create and edit form with color picker
- `subjects/confirm_delete.html` — confirmation screen before cascading delete
- `flashcards/list.html` — filterable card grid with due-today badges
- `flashcards/form.html` — flashcard creation form
- `flashcards/review.html` — full review session with 3D flip card and rating buttons
- `pomodoro/timer.html` — timer display, controls, cycle counter, and session history
- `goals/list.html` — weekly goal cards with progress bars
- `goals/form.html` — goal creation form

### `static/css/styles.css`
All custom styles: CSS variables for the color palette, navbar, cards, forms, buttons, flashcard 3D flip, Pomodoro timer display, heatmap, alerts, and mobile responsive rules.

### `static/js/`
- `topics.js` — topic toggle and delete via fetch, updates progress bar in real time
- `flashcard.js` — review session logic: loads cards from JSON, controls CSS flip, submits ratings, advances queue
- `pomodoro.js` — Pomodoro state machine: countdown, focus/break cycles, Web Notifications, auto-save
- `dashboard.js` — fetches activity data and renders a 12-week heatmap grid

---

## How to Run

1. Clone the repository and enter the project folder
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the server:
   ```bash
   python manage.py runserver
   ```
6. Open **http://127.0.0.1:8000** and create an account.

The admin panel is available at `/admin` after running `python manage.py createsuperuser`.

---

## Additional Notes

- All views are protected with `@login_required` and filter data by `request.user`, so users can never access each other's data.
- Logout uses a `POST` form to comply with Django 5's security requirement.
- No external JavaScript libraries were used — all JS is vanilla.
- Bootstrap 5 and Bootstrap Icons are loaded via CDN.