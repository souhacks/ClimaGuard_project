# ClimaGuard: AI-Powered Climate and Crop Protection System

ClimaGuard is an innovative solution designed to detect Marssonina disease in apple crops. This project leverages data science and machine learning to improve the efficiency and accuracy of disease detection while providing rich insights through a Power BI dashboard. 

## Project Structure

### 1. Power BI Dashboard
The Power BI dashboard provides a comprehensive view of climate and disease data, presenting valuable insights to support early detection and intervention. Key components include:

- **Overview Dashboard**: Displays total disease instances, average temperature, and general plant health status.
- **Environmental Conditions Analysis**: Visualizes trends in temperature, humidity, and moisture over time to track changes in conditions that impact plant health.
- **Disease Incidence and Trends**: Shows the incidence and progression of disease over time, categorized by disease type and seasonal variations.
- **Seasonal Analysis**: Compares plant health and environmental factors across seasons, highlighting year-over-year trends.

### 2. Extracted Insights - DAX Measures
These DAX measures were created to extract temporal insights from the `[Date/Time]` column, enhancing the dashboard’s analytical capabilities:

1. **Year (Measure)**:
   ```DAX
   YearMeasure = YEAR(MAX([Date/Time]))
   
2. **Month Number (Measure)**:
   ```DAX
   MonthNumberMeasure = MONTH(MAX([Date/Time]))
   
3. **Month Name (Measure)**:
   ```DAX
   MonthNameMeasure = FORMAT(MAX([Date/Time]), "MMMM")

4. **Day (Measure)**:
   ```DAX
   DayMeasure = DAY(MAX([Date/Time]))

5. **Day of Week Number (Measure)**:
   ```DAX
   DayOfWeekNumberMeasure = WEEKDAY(MAX([Date/Time]), 2)

6. **Day of Week Name (Measure):**
   ```DAX
   DayOfWeekNameMeasure = FORMAT(MAX([Date/Time]), "dddd")
   
7. **Hour (Measure):**
   ```DAX
   HourMeasure = HOUR(MAX([Date/Time]))

8. **Minute (Measure):**
   ```DAX
MinuteMeasure = MINUTE(MAX([Date/Time]))

8. **Second (Measure):**
   ```DAX
   SecondMeasure = SECOND(MAX([Date/Time]))

9. **Time (HH) (Measure):**
   ```DAX
   Time_HHMMMeasure = FORMAT(MAX([Date/Time]), "HH:mm")

10. **AM/PM (Measure):**
    ```DAX
    AMPMMeasure = FORMAT(MAX([Date/Time]), "tt")

11. **Date (Without Time) (Measure):**
    ```DAX
    DateOnlyMeasure = FORMAT(MAX([Date/Time]), "MM/dd/yyyy")

12. **Quarter (Measure):**
    ```DAX
    QuarterMeasure = QUARTER(MAX([Date/Time]))

** So on **

## Model Development

A predictive model was developed using various machine learning algorithms to evaluate the risk of Marssonina disease based on environmental data. Model performance metrics are as follows:

- **Logistic Regression**: 50.6%
- **Decision Tree**: 51.4%
- **Optimized Random Forest**: 49.4%
- **Support Vector Machine (SVM)**: 49.4%
- **Gradient Boosting**: 49.73%

---

## Flask API

A REST API was created using Flask to serve the best-performing predictive model. The API accepts environmental data inputs and returns disease risk predictions. This API is hosted on Heroku for easy accessibility.

---

## Deployment and Docker Setup

### Docker Setup

A Docker container was created to encapsulate the project environment, ensuring cross-platform compatibility.

### Render Deployment

The API is deployed on Render to enable remote access, scalability, and integration with the ClimaGuard dashboard.
Link: https://climaguard-project.onrender.com/predict




   
