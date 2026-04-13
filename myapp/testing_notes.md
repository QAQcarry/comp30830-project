# Sprint 4 – Prediction Feature Testing & Usability Notes

## Overview
This document describes testing carried out for the bike availability prediction feature (US6), including unit-level checks, integration testing, system testing, and usability observations.

---

## 1. Unit Testing (Frontend Logic)

### Test 1: Missing Input
- **Input**: Station not selected (missing station ID)
- **Expected**: Error message displayed:  
  *"Please enter station ID, date, and time."*
- **Result**: PASS

### Test 2: Valid Prediction Response
- **Input**: Valid API response from `/predict`
- **Expected**: Predicted bikes and availability status displayed correctly
- **Result**: PASS

### Test 3: Station Selection
- **Action**: Click a station on the map
- **Expected**: Station name appears in prediction panel
- **Result**: PASS

---

## 2. Integration Testing (Frontend ↔ Backend)

### Test: Prediction API Integration

**Steps:**
1. User selects a station
2. User selects date and time
3. User clicks "Predict"

**Expected:**
- POST request sent to `/predict`
- JSON response returned
- UI updates with prediction result

**Result**: PASS

---

### Test: API Response Handling

- **Action**: Submit prediction request
- **Expected**: UI displays:
  - Station name
  - Predicted bikes
  - Availability status
- **Result**: PASS

---

### Test: Dynamic Behaviour

- **Action**: Change station, date, and time inputs
- **Expected**: Different prediction values returned
- **Result**: PASS

**Observation:**
- The value of `predicted_bikes` changes across inputs, indicating that the model is being used dynamically.
- The status label remained *"Likely available"* in most cases due to the threshold rule (≥ 1 bike).

---

## 3. System / Acceptance Testing

### Scenario: Predict Bike Availability

**Steps:**
1. User logs into the system
2. User selects a station from the map
3. Station is displayed in prediction panel
4. User selects date and time
5. User clicks "Predict"

**Expected:**
- Prediction result displayed clearly
- Availability status shown

**Result**: PASS

---

### Scenario: Multiple Inputs

- Tested different stations and times
- System returned varying prediction values

**Result**: PASS

---

### Scenario: Error Handling

- Missing inputs produce appropriate error messages
- No crashes or unexpected behaviour observed

**Result**: PASS

---

## 4. Usability Testing

### Observations

- Selecting stations via the map was intuitive
- Displaying station name instead of ID improved usability
- Prediction results were clear and easy to understand
- Input validation helped prevent user errors
- Dark-themed interface improved visual clarity

---

## Improvements Made

- Replaced manual station ID input with map-based selection
- Displayed station name instead of numeric ID
- Improved layout and spacing of prediction panel
- Redesigned UI with a modern urban-themed style

---

## Conclusion

The prediction feature is successfully integrated:

- Frontend correctly communicates with backend
- Predictions are dynamic and responsive
- Interface is intuitive and user-friendly
- System handles both valid and invalid inputs effectively

The implementation meets all Sprint 4 requirements for frontend integration, testing, and usability.