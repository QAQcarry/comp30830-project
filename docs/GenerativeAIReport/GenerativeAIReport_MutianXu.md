# AI Generative Report

## Project Role

Throughout this project, I was responsible for the **frontend, backend, and machine learning notebook**: the user interface in HTML/CSS/JavaScript, the Flask backend (routes, blueprints, API endpoints, error handling), the bike-availability model in `ml_bike_prediction.ipynb`, and the integration between the trained model and Flask. AWS EC2 setup and MySQL database deployment were handled by other teammates and are therefore out of scope for this report.

This report focuses less on *what AI told me* and more on *why those suggestions mattered for this specific project and how I applied them*.

---

## Sprint 1: Requirements and Frontend Foundation

### 1.1 Turning interview notes into structured user stories

The raw interview notes were a mix of casual phrases ("I want to know if there'll be bikes when I get there") with no clear actor, action, or motivation. Even with the lecture template, I struggled to know where to start.

I asked AI how to convert disorganized requirements into proper user stories. It pointed me to the *As a [role], I want to [action], so that [value]* template and suggested using Trello/Jira to track them.

**Why this was useful:** the template forced me to identify the *role* behind each requirement, which immediately revealed that several "requirements" were actually the same need expressed by different users. **I applied this** by rewriting every interview snippet into the template, which collapsed redundant items and gave the team a single, deduplicated backlog. The downstream effect was that Sprint 2's planning meeting was much shorter — we already had unambiguous tickets to assign.

---

### 1.2 Designing the frontend layout

The page had a Google Map, a station selector, a weather widget, and a prediction panel, and my first sketch put everything into vertical stacking — which made the map tiny and the prediction panel get lost below the fold.

I asked AI how to lay out a page where the map should be the visual anchor but the controls also need to be obvious. It recommended a two-column layout with the map dominating one side and the controls stacked in the user's natural reading order on the other.

**Why this mattered:** the suggestion forced me to think about the layout in terms of the user's *task flow* (look at map → pick station → check weather → predict) rather than as a list of components. **I applied this** by building the index page with a `<main>` containing the map and an `<aside>` containing the stacked controls, which both reads better and is more accessible. **The improvement** was visible during testing: users immediately understood where to start without being told.

---

### 1.3 Splitting JavaScript out of `index.html`

My first version of the page had ~200 lines of inline JavaScript inside `<script>` tags, and adding any new feature meant scrolling past the entire UI markup.

I asked AI how to organize the JavaScript. The answer was to split it by responsibility — `ui.js` for DOM updates and rendering, `app.js` for bootstrapping and API calls — and to load both with `defer`.

**Why this was valuable for the project:** the split mirrored the actual mental model I was using when debugging (UI bugs vs. data-flow bugs), so navigating the code became much faster. **I applied this** with `ui.js` and `app.js`, and from that point on UI tweaks no longer touched the same file as the API logic — which removed an entire class of merge conflicts when working in parallel with my teammate on visual styling.

---

## Sprint 2: Source Control and Backend Skeleton

### 2.1 VS Code Source Control showing nothing

After editing several files locally, the Source Control panel was empty and I could not push through the UI. This blocked me for an entire afternoon because I assumed VS Code's interface was authoritative.

I asked AI why changes weren't appearing. It pointed out that VS Code may not refresh, or the wrong folder may be open, and recommended falling back to `git status` / `git add` / `git commit` / `git push` directly.

**Why this was useful:** the deeper lesson — *trust the command line over the IDE indicator* — has saved me time repeatedly since. **I applied this** by making `git status` my default first move whenever Source Control looks suspicious, instead of debugging the IDE.

---

### 2.2 Restructuring the backend before it became unmanageable

The teacher's example was a single-file Flask app, which started to feel cramped as soon as I had three routes (stations, weather, prediction).

I asked AI for the standard way to organize a multi-route Flask project. It described the application factory pattern with Blueprints — `create_app()` in `__init__.py`, one module per resource under `routes/`, configuration in `config.py`, entrypoint in `run.py`.

**Why this mattered for the project:** doing the restructure early — before the codebase grew — meant Sprint 3's API additions slotted in cleanly rather than requiring a painful refactor. **I applied this** as the actual structure under myapp/app/, and **the improvement** was that adding the `/predict` route in Sprint 4 took me about 15 minutes instead of an afternoon of untangling.

---

### 2.3 Keeping database credentials out of the repository

When my teammate handed over the database URL, my first instinct was to paste it into `config.py` and move on. I asked AI whether that was acceptable.

The answer was no — credentials should come from environment variables (`os.environ.get('DB_URL')`), and any local override should be `.gitignore`d.

**Why this was valuable:** I had not previously thought about Git history as a permanent record of secrets, and the framing — *"once committed, assume it leaked"* — has stuck with me. **I applied this** by reading the URL from environment variables in `config.py` and confirming the relevant files were excluded from version control before my first push.

---

## Sprint 3: Backend APIs, Frontend Integration, and Error Handling

### 3.1 Assigning Jira tasks via email

As the scrum master this sprint, I needed to assign tickets to teammates by email but could not find that field in the issue interface.

I asked AI how to do this. The answer clarified that Jira does not assign by email directly — teammates must first be invited via Project Settings → People, and only then become available in the Assignee dropdown.

**Why this was useful:** I had been searching the wrong UI surface for ten minutes. **I applied this** by inviting the team once, after which assignment took seconds, and email notifications fired automatically.

---

### 3.2 Defensive programming for crawler data

While integrating the crawler data my teammate was producing, the backend started returning HTTP 500 with `KeyError: 'available_bikes'` and `TypeError: 'NoneType' object is not iterable`.

I asked AI how to handle this. It suggested defensive programming — `data.get(field, default)` instead of direct indexing, and explicit null checks before iteration.

**Why this was valuable for our project specifically:** the crawler was being developed in parallel by a teammate, so its output schema was not yet stable. The defensive style let the backend keep running even when an upstream change introduced unexpected nulls. **I applied this** to every external-data ingestion path, and **the improvement** was that subsequent crawler iterations stopped triggering 500 errors — they degraded silently and were caught in logs instead.

---

### 3.3 The Blueprint 404

I added `@app.route('/api/weather')` inside a module file, but the URL returned 404. My initial assumption was that the import or registration was broken.

I asked AI why a syntactically correct route was 404'ing. The answer: in a Blueprint-based project, routes inside modules must use `@bp.route` and the blueprint must be explicitly registered with `register_blueprint()`.

**Why this mattered:** this is exactly the kind of bug where reading the code carefully doesn't help — the symptom looks identical to "route not registered at all." **I applied this** by switching the decorator to `@bp.route` and verifying the registration in `create_app()`. The lesson — *when a Flask route 404s with no error, suspect Blueprint registration before suspecting your code* — has prevented me from going down the same rabbit hole since.

---

### 3.4 Calling the API without page reloads

My first frontend version used `<form action="/api/stations">`, which forced a full page reload every time the user picked a station — and reset the map to its default position.

I asked AI how to call the API from JavaScript without reloading. The answer was the standard `fetch()` + DOM update pattern, with a reminder to wrap the call in `try/catch` and disable the submit button while the request is pending.

**Why this was valuable:** preserving map state between actions was critical for the user experience — losing your selected station every click felt broken. **I applied this** by replacing the form submission with `fetch()` calls in `app.js`, and **the improvement** was a noticeably smoother experience: the map stayed put, the panel updated in place, and the disabled-while-loading state prevented double-submit bugs we had been seeing.

---

### 3.5 CORS during local development

When testing the frontend on a different port from the backend, every API call failed with `Access-Control-Allow-Origin` errors.

I asked AI how to fix this. The answer was `flask-cors` applied to the `/api/*` routes.

**Why this was useful:** without CORS, every parallel local test required serving frontend and backend from the same origin, which slowed down development. **I applied this** by enabling CORS in development with a permissive policy and a `TODO` to restrict origins before deployment — which the team did before the final demo.

---

## Sprint 4: Machine Learning Model and Backend Integration

### 4.1 Recognising the time-series leakage trap

My first plan was a standard random `train_test_split`. I asked AI whether that was appropriate for ~300k rows of bike-availability records spanning a single month.

The answer was no — random splitting causes data leakage on time series, because adjacent timestamps at the same station are highly correlated. The model would essentially memorize neighbouring records and look artificially accurate.

**Why this mattered enormously for the project:** without this pointer I would have shipped a model with optimistically inflated metrics, presented those numbers in the report, and been blindsided in production. **I applied this** by sorting by `last_reported` and using the earlier 80% for training and the later 20% as a temporal holdout. **The improvement** was that the metrics I now report reflect realistic deployment conditions — the model always predicts into the future, never into a window it has indirectly seen.

---

### 4.2 Aligning dataset columns with the API at inference time

The merged dataset had 78 columns; the teacher's example used `temperature, humidity, wind_speed, precipitation, hour, day_of_week`. Two of those features (`wind_speed`, `precipitation`) didn't exist in our data, and the closest matches had verbose names (`max_air_temperature_celsius` etc.).

I asked AI how to reconcile this. The reframing it offered was the most valuable part: treat the feature list as a **schema contract** between training and inference, not a fixed dataset constraint. Drop unavailable features, rename the closest matches, and pick names that match what OpenWeather will return at inference time.

**Why this was valuable:** thinking of features as a contract — rather than as "whatever's in the CSV" — saved me from a subtle bug where training and serving would have used the same feature *meanings* but different column *names*. **I applied this** by renaming columns in the notebook to align with the OpenWeather payload structure and saving the final list as `model_features.pkl`, so Flask can assemble inputs in exactly the same order at prediction time.

---

### 4.3 Why R² ≈ 0 wasn't a bug

The baseline Linear Regression came back with `R² = -0.002` and `MAE = 7.5`, and I assumed I had broken the pipeline somewhere.

I asked AI whether this was a real result or a data error. The answer reframed the problem: bike availability is dominated by user behaviour and rebalancing operations that weather and time features simply cannot capture. The advice was twofold — try non-linear models, and reframe the prediction as a binary "is at least one bike available?" decision, since that is what the user actually cares about.

**Why this changed the project direction:** without this, I might have spent days hunting an imaginary bug. More importantly, the second suggestion (binary reframing) reshaped how I evaluated every model afterwards — and ultimately how the prediction is *displayed* to the user (a verdict, not just a number). **I applied this** by adding Precision/Recall/F1 alongside MAE/RMSE/R² in the model comparison.

---

### 4.4 Choosing the model when F1 ties

Linear Regression and Gradient Boosting both produced F1 = 0.963 for the binary task, but their R² values differed dramatically (-0.002 vs. 0.242).

I asked AI which to pick and how to defend the choice. The recommendation was to use F1 as the primary criterion (because it measures the actual user-facing decision) and break ties with R² (because the UI shows the predicted *count* alongside the verdict — a better R² means a more trustworthy number on screen).

**Why this was valuable:** the framing connected model selection to product behaviour, not just statistics. **I applied this** by selecting Gradient Boosting and documenting the rationale explicitly in the notebook, so the choice reads as deliberate rather than arbitrary.

---

### 4.5 Defining a meaningful ML user story (US6)

Sprint 4 required a new ML-driven user story, but our existing API already exposed real-time availability — so the ML feature needed to deliver something the API alone could not.

I asked AI what kind of user story makes sense specifically for an ML model. The answer was forward-looking: real-time data answers "what is happening now?", but only a model can answer "what will likely happen at a future time?"

**Why this mattered:** it gave the model a clear product purpose rather than being ML-for-its-own-sake. **I applied this** as US6 — *As a tourist, I want to predict bike availability for a future date and time, so I can plan my trip in advance* — with explicit acceptance criteria mapping `predicted >= 1 → "Likely available"`. This made the model's evaluation strategy traceable back to real user value.

---

### 4.6 Persisting the model + feature list together

I initially saved only the model with `pickle.dump(model, f)`. AI flagged that this was insufficient — without the feature list, Flask would have no reliable way to assemble inputs in the right column order.

**Why this was valuable:** this is the kind of mistake that doesn't surface during local testing (where the order happens to match) but breaks immediately when the order shifts. **I applied this** by saving both `bike_availability_model.pkl` and `model_features.pkl` into the `myapp/app/ml/` folder, and the Flask `/predict` route now loads both at startup.

---

### 4.7 Resolving the Flask model path bug

Loading the model with a relative path worked when I ran Flask from the project root, but failed when launched from a different working directory.

I asked AI how to make the path stable. The answer was `os.path.join(os.path.dirname(__file__), 'model.pkl')` — anchor the path to the source file rather than the launch directory.

**Why this was valuable:** the underlying lesson — *relative paths are tied to the cwd, not the script* — is a Python footgun I had hit before without understanding why. **I applied this** in the model-loading code, and the same pattern is now my default whenever a Python module needs to find a sibling file.

---

### 4.8 Building the prediction request from real-time data

The model needed `hour`, `day_of_week`, `temperature`, `humidity`, `pressure`, and `station_id`, assembled into a single-row DataFrame with the *exact* training column names.

I asked AI how to construct this in Flask. The answer was a dictionary built from `datetime.now()` plus the latest weather record, then `pd.DataFrame([data_dict])` to produce a single-row frame.

**Why this was valuable:** the explicit reminder that column names must match training was what saved me — `pandas` will silently accept a misaligned DataFrame and the model will return nonsense. **I applied this** in the `/predict` route, with the column order pulled from `model_features.pkl` so it cannot drift from the training schema.

---

### 4.9 Translating a number into a UI verdict

The backend returned `9.9` (or similar). My first instinct was to display the raw number, but that doesn't answer the user's actual question — *"can I get a bike?"*

I asked AI how to display the result meaningfully. The suggestion was to show **two things together**: the rounded count (`~10 bikes`) and the verdict (`"Likely available"` for `predicted >= 1`), with colour cues to make the verdict scannable.

**Why this was valuable:** it closed the loop between the F1-based evaluation and the actual UI — the same threshold the model was selected against is now what the user sees. **I applied this** in the prediction panel, and **the improvement** was that the answer became readable at a glance, which matched how users actually check availability (quick visual scan, not careful reading).

---

## Reflection

Looking back across the four sprints, the most valuable thing AI offered was rarely the *answer* — it was a **reframing**:

- "Treat the feature list as a contract, not a CSV constraint."
- "Random splits leak in time-series."
- "F1 measures what your user actually cares about; R² measures what your UI displays."
- "Once it's in Git history, assume it leaked."
- "When a route 404s with no error, suspect Blueprint registration."

These reframings shaped not just the immediate fix but how I now think about similar problems. The other consistent lesson was about *how* to ask: the questions that produced useful answers were always specific — they included the error message, the dataset shape, the file structure, or the exact symptom. Vague questions produced generic answers I couldn't act on. That's the habit I'll carry forward beyond this project.
