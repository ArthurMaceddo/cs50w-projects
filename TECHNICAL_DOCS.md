# Technical Documentation — Study Manager

This document records the development history of Study Manager, a project built as the Final Project for CS50W. Documentation follows a semantic commit structure, detailing each incremental change made to the codebase.

## Commit Format

```
<type>(<optional scope>): <description>
```

**Example:** `feat(auth): configure authentication URL patterns`

**Further reading on semantic commits:**
- https://www.conventionalcommits.org/en/v1.0.0/
- https://dev.to/diegobrandao/padronizando-commits-git-com-um-script-bash-uma-solucao-simples-para-um-problema-comum-2bdl

---

## `feat(auth): configure authentication URL patterns`

Sets up the URL routing for all authentication-related endpoints.

- **Imports:** Loads `path` for routing, Django's built-in `auth_views`, and the app's custom `views`.
- **`urlpatterns`:** List that maps HTTP routes to Python functions or classes.
- **Routes:**
  - `""` → maps the base URL (`/`) to the `dashboard` view.
  - `"login/"` → uses Django's built-in `LoginView`, injecting `login.html` as the template.
  - `"logout/"` → uses Django's built-in `LogoutView` to end the session.
  - `"register/"` → maps the URL to the custom `register` view.
- **`name`:** Assigns an alias to each route, allowing `{% url 'name' %}` in templates without hardcoding paths.

> **Note on `.as_view()`:** `LoginView` is a class-based view. Since Django's URL dispatcher expects a callable function, `.as_view()` returns a wrapper function that instantiates the class, sets up the request, runs the appropriate method (`get` or `post`), and returns the HTTP response.

---

## `feat(models): create Subject model`

Defines the data structure for academic subjects.

- `user` — `ForeignKey` to `User` (1:N), with `CASCADE` deletion.
- `name` — text field for the subject name.
- `description` — optional text field for additional details.
- `color` — stores the hex color code associated with the subject (default: `#5B88A5`).
- `created_at` — auto-populated creation timestamp.
- **`Meta.ordering`** — default ordering by name.
- **`__str__`** — returns a human-readable label with the subject name and owner username.

---

## `feat(models): create Topic model`

Defines the data structure for study topics linked to a subject.

- `subject` — `ForeignKey` to `Subject` (1:N), with `CASCADE` deletion.
- `name` — topic name.
- `notes` — optional text field for detailed notes.
- `is_completed` — boolean flag to track completion.
- `order` — integer field for manual ordering.
- `created_at` — auto-populated creation timestamp.
- **`Meta.ordering`** — composite ordering by `order` then `created_at`.
- **`__str__`** — returns the topic name alongside its parent subject.

---

## `feat(models): create PomodoroSession model`

Defines the data structure for recording Pomodoro focus sessions.

- `user` — `ForeignKey` to `User` (1:N).
- `subject` — `ForeignKey` to `Subject` (1:N).
- `started_at` — date and time the session began.
- `duration_minutes` — session length in minutes (default: 25).
- `completed` — boolean flag for session status.
- **`Meta.ordering`** — descending by `started_at` (most recent first).
- **`__str__`** — formatted string showing a status icon, subject name, duration, and date.

---

## `feat(models): implement business logic methods for Subject model`

Adds computed methods directly on the `Subject` model.

- **`progress()`**
  - Queries all related `Topic` objects via the `related_name`.
  - Guards against division by zero when no topics exist.
  - Returns the percentage of topics marked `is_completed=True` as an integer.

- **`total_study_minutes()`**
  - Filters `PomodoroSession` records linked to this subject where `completed=True`.
  - Uses a list comprehension inside `sum()` to aggregate `duration_minutes`.

---

## `feat(models): create Flashcard model`

Defines the data structure for memory cards with spaced repetition support.

- `subject` — `ForeignKey` to `Subject` (1:N).
- `front` / `back` — text fields for the question and answer sides.
- `next_review_date` — date of the next scheduled review (default: today).
- `interval_days` — current interval between reviews in days (default: 1).
- **`__str__`** — truncates `front` to 50 characters for readability in the admin panel.
- **`is_due_today()`** — returns `True` if `next_review_date` is on or before today.
- **`apply_review(rating)`** — implements the SRS algorithm:
  - `"easy"` → doubles the current interval (minimum 7 days).
  - `"hard"` → sets interval to 2 days.
  - `"wrong"` → resets interval to 1 day.
  - After computing the new `interval_days`, adds it to `date.today()` using `timedelta` and saves the updated `next_review_date` to the database.
- **`Meta.ordering`** — ordered by `next_review_date` so overdue cards appear first.

---

## `feat(models): create FlashcardReview model`

Defines an audit log for every flashcard review event.

- `RATING_CHOICES` — enforces valid values (`easy`, `hard`, `wrong`) at the database level.
- `flashcard` — `ForeignKey` to `Flashcard` (1:N), enabling full review history per card.
- `rating` — stores the selected evaluation.
- `reviewed_at` — auto-populated review timestamp (`auto_now_add`).
- **`__str__`** — readable log entry with card reference, rating, and date.
- **`Meta.ordering`** — descending by `reviewed_at` (most recent first).

> **Why this model?** While `Flashcard` stores the *current state* (when to review next), `FlashcardReview` stores the *effort history*. This enables future features like accuracy charts per subject or identification of the hardest cards.

---

## `feat(models): create WeeklyGoal model`

Defines the data structure for weekly study hour targets.

- `subject` — `ForeignKey` to the target subject.
- `target_hours` — `FloatField` representing the weekly hour goal.
- `week_start` — date anchored to Monday of the target week.
- **`current_hours()`** — filters completed `PomodoroSession` records within the 7-day window starting at `week_start`, converts the total minutes to hours, and rounds to one decimal place.
- **`percentage()`** — returns completion ratio capped at 100%.
- **`Meta.ordering`** — ordered by `week_start` and `subject`.
- **`unique_together`** — prevents duplicate goals for the same user, subject, and week.

> **Technical note:** The `started_at__date__range` filter in `current_hours()` isolates exactly the current week. `update_or_create` in the view layer makes goal creation idempotent — updating an existing goal instead of creating duplicates.

---

## `feat(urls): configure CRUD URL patterns for Subject model`

Maps the five standard CRUD endpoints for `Subject`:

| URL | View | Action |
|---|---|---|
| `subjects/` | `subjects_list` | List all subjects |
| `subjects/new/` | `subject_create` | Create new subject |
| `subjects/<int:pk>/` | `subject_detail` | View subject details |
| `subjects/<int:pk>/edit/` | `subject_edit` | Edit subject |
| `subjects/<int:pk>/delete/` | `subject_delete` | Delete subject |

> **`<int:pk>`** is a path converter that captures an integer from the URL and passes it to the view as the `pk` argument, used to identify specific model instances.
> Reference: https://docs.djangoproject.com/en/5.0/topics/http/urls/

---

## `feat(urls): add URL patterns for Topic`

Maps the three Topic API endpoints:

| URL | View | Action |
|---|---|---|
| `topics/new/` | `topic_create` | Create a new topic |
| `topics/<int:pk>/toggle/` | `topic_toggle` | Toggle `is_completed` status |
| `topics/<int:pk>/delete/` | `topic_delete` | Delete a topic |

> **`toggle`** is designed for JavaScript `fetch` calls. It updates the database and returns a JSON response with the new status and subject progress, enabling real-time DOM updates without a page reload.

---

## `feat(urls): add URL patterns for Flashcard`

| URL | View | Action |
|---|---|---|
| `flashcards/` | `flashcard_list` | List all flashcards |
| `flashcards/new/` | `flashcard_create` | Create a new flashcard |
| `flashcards/review/` | `flashcard_review_session` | Start a review session |
| `flashcards/<int:pk>/delete/` | `flashcard_delete` | Delete a flashcard |
| `flashcards/<int:pk>/submit/` | `flashcard_submit_review` | Submit a review rating |

> **`review` vs `submit`:** `review` prepares the context for the study session; `submit` is an API endpoint that receives the rating, runs `apply_review()`, and returns the updated schedule.

---

## `feat(urls): add URL patterns for Pomodoro`

| URL | View | Action |
|---|---|---|
| `pomodoro/` | `pomodoro` | Render the timer interface |
| `pomodoro/save/` | `pomodoro_save` | Save a completed session |

> **Separation of concerns:** `pomodoro` renders the page; `pomodoro_save` acts as an async callback triggered by JavaScript when the 25-minute cycle ends, persisting the session without a page reload.

---

## `feat(urls): add URL patterns for Goals`

| URL | View | Action |
|---|---|---|
| `goals/` | `goals_list` | List current week's goals |
| `goals/new/` | `goal_create` | Create a new goal |
| `goals/<int:pk>/delete/` | `goal_delete` | Delete a goal |

---

## `feat(urls): add URL patterns for Dashboard`

| URL | View | Action |
|---|---|---|
| `dashboard/activity/` | `dashboard_activity` | Return activity heatmap JSON |

> This endpoint acts as a **summary view**, consuming model methods (`progress()`, `current_hours()`) to generate productivity visualizations.

---

## `feat(views): create initial view stubs for all application endpoints`

Creates placeholder functions for every URL pattern to ensure the Django server starts without `ImportError` or `AttributeError`. Each stub returns a temporary `HttpResponse`, validating endpoint connectivity before real logic is implemented.

---

## `feat(auth): implement registration and logout logic`

- **`register(request)`**
  - `POST`: Validates `UserCreationForm`, saves the user, logs them in automatically, and redirects to `dashboard` with a success message via `django.contrib.messages`.
  - `GET`: Renders a blank registration form.

> **Security note:** `UserCreationForm` is Django's recommended approach — it handles password validation, strength checking, and data sanitization out of the box.
> Reference: https://docs.djangoproject.com/en/5.0/topics/auth/default/

---

## `feat(views): implement CRUD views for Subject model`

- **`subjects_list`** — filters subjects by `request.user` to ensure data isolation.
- **`subject_create`** — sanitizes input with `.strip()` and sets a default color value.
- **`subject_detail`** — retrieves a specific subject with `get_object_or_404` and passes its topics to the template.
- **`subject_edit`** — updates subject fields and persists changes.
- **`subject_delete`** — processes deletion via `POST` to prevent accidental removal.

> **`get_object_or_404`:** Returns a 404 page automatically if the object does not exist or does not belong to the current user, preventing `DoesNotExist` server errors.

---

## `feat(views): implement CRUD views for Topic model`

- **`topic_create`** — decorated with `@require_POST`; validates the parent subject belongs to the authenticated user before creating the topic.
- **`topic_toggle`** — async API endpoint that flips `is_completed` and returns a JSON response containing the new status and the updated subject progress percentage.
- **`topic_delete`** — removes the topic and returns JSON with deletion confirmation and the recalculated subject progress.

> Returning `progress()` in JSON responses from `toggle` and `delete` enables the frontend to update the progress bar in real time without a page reload.

---

## `feat(views): implement Pomodoro session management`

- **`pomodoro`** — renders the timer page with the user's subject list and the 10 most recent completed sessions.
- **`pomodoro_save`** — parses the JSON body sent by the frontend timer, creates a `PomodoroSession` instance, and returns a confirmation response.

> **`json.loads(request.body)`:** Since the timer runs client-side, `pomodoro_save` expects structured JSON rather than a standard form submission. Consider using `django.utils.timezone.now()` instead of `datetime.now()` for timezone-aware timestamps in production.

---

## `feat(views): implement WeeklyGoal CRUD operations`

- **`goals_list`** — computes the current week's Monday using `date.today()` and `weekday()`, then filters goals for that week only.
- **`goal_create`** — uses `update_or_create` to prevent duplicate goals for the same subject and week.
- **`goal_delete`** — removes the goal after validating user ownership.

> **Calendar logic:** `today - timedelta(days=today.weekday())` normalizes any date to its week's Monday, standardizing all database records for consistent querying.

---

## `feat(views): implement dashboard and activity analytics views`

- **`dashboard`** — aggregates all productivity metrics: due flashcards, weekly study hours, goal progress, recent sessions, and study streak (calculated with a reverse `while` loop checking consecutive days with completed sessions).
- **`dashboard_activity`** — API endpoint that groups completed `PomodoroSession` records by day over the last 12 weeks and returns a `JsonResponse` mapping date strings to session counts.

> **Performance:** Using `.values("started_at__date")` extracts only the required field from the database, keeping the heatmap data query efficient as session volume grows.

---

## `fix(views): enforce authentication and HTTP method constraints`

- **`@login_required`** — applied to all management views to redirect unauthenticated users to the login page.
- **`@require_POST`** — applied to all state-changing endpoints to prevent accidental or malicious `GET` requests from modifying data.

> Combined with Django's `{% csrf_token %}` template tag, `@require_POST` creates a strong defense layer against Cross-Site Request Forgery (CSRF) attacks.

---

## `feat(templates): implement base layout with navigation and global messaging`

- **`layout.html`** — master template using Django's block inheritance system (`{% block content %}`).
- **Navbar** — responsive Bootstrap 5 navigation with links to all modules, conditioned on `user.is_authenticated`. Logout uses a `POST` form for CSRF security.
- **Messages** — integrates `django.contrib.messages` to display success, error, and warning alerts above each page's content block.
- **Assets** — Bootstrap 5 CSS/JS via CDN, Bootstrap Icons, and the custom `styles.css` static file.

> **Block structure:** `{% block title %}`, `{% block content %}`, and `{% block scripts %}` allow child templates to inject page-specific content without rewriting the shared layout.

---

## `feat(frontend): implement activity heatmap rendering`

- **Fetch API** — makes an async `GET` request to `/dashboard/activity/` to retrieve the session count dictionary.
- **Dynamic Grid** — iterates retroactively over the last 84 days (12 weeks × 7), formatting each date as `YYYY-MM-DD` to match the API keys.
- **Color intensity mapping:**
  - `0 sessions` → `#ebedf0` (empty)
  - `1 session` → `#9be9a8` (light green)
  - `2 sessions` → `#40c463` (medium green)
  - `≥ 3 sessions` → `#216e39` (dark green)
- **Tooltips and legend** — native `title` attributes show date and count on hover; a text legend displays the activity scale.

> Replicates GitHub's contribution graph style using plain `div` elements with flexbox, consuming the JSON from `dashboard_activity`.

---

## `feat(templates): implement dashboard template`

- Extends `layout.html`, overriding `title`, `content`, and `scripts` blocks.
- **Summary cards** — Bootstrap grid showing `total_subjects`, `total_flashcards`, `week_hours`, and `streak`.
- **Flashcard alert** — conditional banner when `due_cards > 0` with a direct link to the review session.
- **Weekly goals** — dynamic progress bars colored by each goal's subject color.
- **Recent sessions and heatmap** — session history list and the heatmap container loaded by `dashboard.js`.

---

## `feat(templates): implement registration and login templates`

Both templates extend `layout.html` and share the same `.auth-card` layout:

- `{% csrf_token %}` injected into every form for security.
- `{{ form.as_p }}` renders all fields automatically via Django's form rendering.
- Cross-links between login and register pages for navigation convenience.

---

## `fix(config): configure static files and authentication redirect paths`

- **Static files** — added `STATIC_URL` and `STATIC_ROOT = BASE_DIR / 'staticfiles'` for `collectstatic` support in production.
- **Auth redirects** — defined `LOGIN_URL`, `LOGIN_REDIRECT_URL = "/"`, and `LOGOUT_REDIRECT_URL = "/login/"` to control session flow automatically.
- **Root URL config** — added `path('', include('core.urls'))` to connect the central router to the `core` app.

---

## `feat(templates): implement subjects list, form, detail, and delete confirmation templates`

- **`subjects/list.html`** — responsive card grid (`col-12 col-md-6 col-lg-4`) with color indicator, progress bar, and quick action buttons. Includes an empty state for new users.
- **`subjects/form.html`** — shared create/edit form with a dynamic title (`{{ action }}`), optional description field, and a color picker input (`type="color"`).
- **`subjects/detail.html`** — inline topic creation form, interactive checkbox list with strike-through for completed items, and delete buttons. Injects `TOGGLE_URL`, `DELETE_URL`, and `CSRF_TOKEN` as global JS variables for `topics.js`.
- **`subjects/confirm_delete.html`** — danger card with the subject name and a warning about cascading deletion of all linked topics, flashcards, and sessions.

---

## `feat(frontend): implement asynchronous topic toggle and deletion`

- **Toggle** — listens to `change` events on topic checkboxes, sends a `POST` via the Fetch API with the CSRF token, and updates the topic's visual state (strike-through text) and the subject's progress bar/badge in real time.
- **Delete** — listens to delete button clicks, shows a native `confirm()` dialog, sends a `DELETE` request, and removes the topic element from the DOM on success.

---

## `feat(templates): implement Pomodoro timer interface`

- **Subject selector** — dropdown to associate the session with a subject before starting.
- **Timer display** — large countdown using the `.timer-display` class, with a state label and cycle counter badge.
- **Controls** — Start, Pause, and Reset buttons with dynamic `disabled` states managed by JavaScript.
- **Progress bar** — fills in real time as the cycle progresses.
- **Session history** — conditional list of recent completed sessions with subject color, duration, and timestamp.
- **Script injection** — `SAVE_URL` and `CSRF_TOKEN` passed as global JS variables for `pomodoro.js`.

---

## `feat(templates): implement weekly goals list and form templates`

- **`goals/list.html`** — responsive card grid showing each goal's subject color, `current_hours / target_hours`, and a dynamic progress bar. Delete buttons use a `POST` form with CSRF token and `confirm()` dialog.
- **`goals/form.html`** — subject dropdown and an hours input with step increments of 0.5, min of 0.5, and max of 40.

---

## `feat(frontend): implement Pomodoro timer state machine`

- **State variables** — `remainingSeconds`, `isFocus`, `cycleCount`, and `timerInterval` manage the full timer lifecycle.
- **Utility functions** — `formatTime()` formats seconds as `MM:SS`; `updateDisplay()` updates the DOM and progress bar; `sendNotification()` fires a browser notification if permission is granted.
- **`onTimerEnd()`** — handles cycle completion: saves the session via `fetch POST`, alternates between focus and break phases (short break every cycle, long break every 4th), and updates all UI elements.
- **Controls** — Start (validates subject selection and requests notification permission), Pause (`clearInterval`), and Reset (restores all state to defaults).

---

## `feat(styles): implement complete stylesheet`

- **CSS variables** — five-color palette defined in `:root` for consistent theming across all components.
- **Reset and base** — normalizes margins, padding, and box sizing; sets body background and text color from the palette.
- **Layout components** — navbar, container, cards with hover lift effect, Bootstrap overrides for buttons, badges, alerts, progress bars, list groups, and form controls.
- **Flashcard 3D flip** — `perspective`, `transform-style: preserve-3d`, `backface-visibility: hidden` on `.flashcard-face`; `.is-flipped` triggers `rotateY(180deg)` on `.flashcard-card`.
- **Pomodoro timer** — `.timer-display` uses `font-variant-numeric: tabular-nums` to prevent digit-width jitter during countdown.
- **Mobile responsive** — media queries at `600px` and `400px` scale the navbar, container padding, auth card, flashcard scene, and timer display.

---

## `feat(templates): implement flashcard list, form, and review session templates`

- **`flashcards/list.html`** — filterable card grid with a subject `GET` filter, per-card due-today badge, and async delete via inline JavaScript.
- **`flashcards/form.html`** — textarea fields for `front` and `back`, subject dropdown, and CSRF-protected `POST` form.
- **`flashcards/review.html`** — 3D flip card scene (`.flashcard-scene` > `.flashcard-card` > `.flashcard-front` / `.flashcard-back`), rating buttons (`easy`, `hard`, `wrong`), session progress bar, and a hidden completion screen revealed when the queue is exhausted. Injects `CARDS` (JSON), `SUBMIT_URL`, and `CSRF_TOKEN` as global JS variables.

---

## `feat(frontend): implement flashcard review session logic`

- **State management** — tracks `currentIndex` against the total `CARDS` array length; updates the counter and progress bar after each rating.
- **`loadCard(index)`** — checks for session completion, removes the `.is-flipped` class, then updates `subject`, `front`, and `back` after a 280ms delay to sync with the CSS transition.
- **Flip controls** — the "See Answer" button and a direct card click both toggle `.is-flipped`; clicks on inner buttons are excluded via `e.target.tagName` check.
- **Rating submission** — disables all rating buttons during the `fetch POST` to prevent double submission; re-enables them and advances the queue on success.
- **Empty state handling** — if `CARDS` is empty on load, the card scene is hidden and the completion screen is shown immediately.

---

## `feat(views): implement flashcard views`

- **`flashcard_list`** — scopes both subjects and flashcards to `request.user`; supports optional `?subject=` query parameter for filtering; calculates due card count for the alert banner.
- **`flashcard_create`** — sanitizes `front` and `back` inputs, validates subject ownership, and creates the `Flashcard` instance.
- **`flashcard_review_session`** — filters cards where `next_review_date <= today`, serializes `id`, `front`, `back`, and `subject` to JSON, and passes it safely to the template context.
- **`flashcard_submit_review`** — `@require_POST` endpoint that parses the rating from the JSON body, creates a `FlashcardReview` record, calls `apply_review()`, and returns the updated schedule as JSON.
- **`flashcard_delete`** — validates ownership and removes the card, returning a JSON confirmation.