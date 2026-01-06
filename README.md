# 🇵🇰 Pakistan Diabetes Predictor

This project aims to **predict diabetes outcomes** among individuals in Pakistan based on medical, demographic, and lifestyle information. The model uses several machine learning algorithms to evaluate the likelihood of diabetes. An interactive **Streamlit web application** is also included for real-time prediction.

---

## Files Included

This project contains the following files:

| File | Description |
|------|-------------|
| `Pakistan_Diabetes_Predictor.ipynb` | Jupyter Notebook for full data analysis and model training |
| `Pakistani_Diabetes_Dataset.csv` | Dataset containing patient information |
| `model.pkl` | Trained machine learning model (serialized using Pickle) |
| `app.py` | Streamlit app script for local deployment |
| `README.md` | Project documentation |

---

## Dataset — Column Descriptions

| Column    | Description |
|-----------|-------------|
| `Age`     | Age of the patient (in years) |
| `Gender`  | Gender (1 = Male, 0 = Female) |
| `Rgn`     | Region code (e.g., 0 = Urban, 1 = Rural) |
| `wt`      | Weight in kilograms |
| `BMI`     | Body Mass Index (kg/m²) |
| `wst`     | Waist circumference (in inches or cm) |
| `sys`     | Systolic blood pressure |
| `dia`     | Diastolic blood pressure |
| `his`     | Family history of diabetes (1 = Yes, 0 = No) |
| `A1c`     | Hemoglobin A1c (%) |
| `B.S.R`   | Blood Sugar Random (mg/dL) |
| `vision`  | Vision issues (1 = Yes, 0 = No) |
| `Exr`     | Exercise level (in Minutes) |
| `dipsia`  | Excessive thirst (1 = Yes, 0 = No) |
| `uria`    | Sugar/protein in urine (1 = Yes, 0 = No) |
| `neph`    | Kidney complications (1 = Yes, 0 = No) |
| `HDL`     | HDL cholesterol level |
| `Outcome` | Diabetes status (1 = Diabetic, 0 = Non-diabetic) ← **Target** |

---

## Exploratory Data Analysis (EDA)

Exploration and visualization were performed using the following tools:

-  **Pie Charts** – Distribution of categorical features (Distribution of Target)
-  **Barplots & Countplots** – Categorical comparison with Outcome
-  **Histograms** – Distribution of numeric variables like Age, BMI, B.S.R
-  **Boxplots** – Detection of outliers
-  **Scatter Plots & Pairplots** – Visualizing feature relationships
-  **Correlation Heatmap** – To identify most predictive features

---

## Machine Learning Models Used

The following models were applied and evaluated:

- `LogisticRegression`
- `KNeighborsClassifier`
- `DecisionTreeClassifier`
- `RandomForestClassifier`
- `ExtraTreesClassifier`
- `AdaBoostClassifier` Final Model(100% Accuracy)
- `VotingClassifier` (Ensemble of top models)
- `StackingClassifier` (Combining base learners)

### Evaluation Metrics:
- Accuracy
- Confusion Matrix
- Classification Report (Precision, Recall, F1-Score)

### Live App
- https://diabeties-predictor-8yuszl7famckyjpzdeppja.streamlit.app/
