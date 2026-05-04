# Generative AI Usage Log – John Shannon

This document records the use of generative AI tools during the development of the Dublin Bikes web application. The AI was used as a support tool for understanding concepts, implementing features, debugging, and improving documentation.

---

## Entry 1 – Frontend–Backend Communication

**Prompt**  
How do I connect a JavaScript frontend to a Flask backend?

**Summary**  
The AI explained how to use the `fetch()` API to send HTTP requests to Flask endpoints and handle JSON responses.

**How It Was Used**  
Used to understand how `apiClient.js` communicates with backend routes such as `/stations`, `/weather`, and `/predict`.

**Reflection**  
This clarified how data flows between the frontend and backend and supported implementation of API calls.

---

## Entry 2 – Implementing Prediction API Call

**Prompt**  
How do I send a POST request from JavaScript to a Flask endpoint?

**Summary**  
The AI described how to structure a `fetch()` request with method `"POST"` and include JSON data in the request body.

**How It Was Used**  
Used to implement the `fetchPrediction()` function, sending station ID, date, and time to the `/predict` route.

**Reflection**  
Enabled successful integration of the machine learning prediction feature.

---

## Entry 3 – Debugging Prediction Output

**Prompt**  
Why does my prediction always say “likely available”?

**Summary**  
The AI suggested checking the raw prediction output and verifying threshold logic.

**How It Was Used**  
Used to confirm that the model output was changing and correctly mapped to a binary result.

**Reflection**  
Improved debugging approach and confidence in the correctness of the model integration.

---

## Entry 4 – Map-Based Station Selection

**Prompt**  
How can I allow users to select a station by clicking on the map?

**Summary**  
The AI explained how to use map click events and store selected values for later use.

**How It Was Used**  
Applied in the map logic to update the selected station and pass it to the prediction interface.

**Reflection**  
Improved usability by removing the need for manual station ID input.

---

## Entry 5 – UI Behaviour Improvements

**Prompt**  
How do I hide a message once a station is selected?

**Summary**  
The AI suggested conditionally rendering UI elements based on application state.

**How It Was Used**  
Used to remove the helper message after a station is selected.

**Reflection**  
Improved user experience and interface responsiveness.

---

## Entry 6 – Structuring Frontend Modules

**Prompt**  
How should I organise JavaScript files for a web application?

**Summary**  
The AI explained how to separate concerns into modules such as API handling, UI logic, and map management.

**How It Was Used**  
Used to better understand and work with the existing structure of `apiClient.js`, `mapManager.js`, and `ui.js`.

**Reflection**  
Improved understanding of modular frontend design.

---

## Entry 7 – Flask Architecture and Routing

**Prompt**  
How does Flask structure work with routes and modules?

**Summary**  
The AI explained the use of blueprints and how routes handle HTTP requests.

**How It Was Used**  
Used to understand the roles of the Main, Auth, and API blueprints.

**Reflection**  
Strengthened understanding of backend architecture and request handling.

---

## Entry 8 – Class Diagram Design

**Prompt**  
What should the class diagram look like for this system?

**Summary**  
The AI recommended focusing on real system components such as the Flask app, blueprints, User model, and database layer rather than introducing unnecessary classes.

**How It Was Used**  
Used to design a clear and accurate class/module diagram.

**Reflection**  
Helped ensure the diagram reflected the actual implementation without unnecessary complexity.

---

## Notes

- AI was used as a support tool to assist understanding and development.
- All outputs were reviewed and adapted to the specific requirements of the project.
- AI outputs helped me to understand how things work and were a useful guide to completing objectives.
