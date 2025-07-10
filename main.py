import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
import joblib # type: ignore
from typing import Dict, List, TypedDict
import json

# Type definitions
class HealthData(TypedDict):
    age: int
    gender: str
    height: float
    weight: float
    blood_group: str
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    sugar_level: int
    cholesterol_ldl: int
    cholesterol_hdl: int
    liver_enzyme_alt: int
    liver_enzyme_ast: int
    sleep_duration: float
    vision: str
    hearing: str
    state: str

class CategoryScores(TypedDict):
    body_composition: float
    cardiovascular: float
    metabolic: float
    lifestyle: float
    environmental: float

class HealthScore(TypedDict):
    overall_score: float
    category_scores: CategoryScores
    recommendations: List[str]

# Extended Indian states data with more health metrics
INDIAN_STATES = {
    "Kerala": {"health_index": 82.2, "aqi": 45, "healthcare_density": 8.5, "altitude": 850, "humidity": 70, "disease_prevalence": 0.12, "healthcare_access": 0.92},
    "Tamil Nadu": {"health_index": 72.8, "aqi": 55, "healthcare_density": 7.2, "altitude": 160, "humidity": 65, "disease_prevalence": 0.15, "healthcare_access": 0.85},
    "Maharashtra": {"health_index": 69.1, "aqi": 75, "healthcare_density": 6.8, "altitude": 550, "humidity": 55, "disease_prevalence": 0.18, "healthcare_access": 0.82},
    "Gujarat": {"health_index": 65.7, "aqi": 85, "healthcare_density": 6.2, "altitude": 180, "humidity": 45, "disease_prevalence": 0.22, "healthcare_access": 0.78},
    "Punjab": {"health_index": 63.8, "aqi": 95, "healthcare_density": 5.9, "altitude": 250, "humidity": 40, "disease_prevalence": 0.25, "healthcare_access": 0.75},
    "Karnataka": {"health_index": 61.4, "aqi": 65, "healthcare_density": 6.4, "altitude": 920, "humidity": 60, "disease_prevalence": 0.20, "healthcare_access": 0.80},
    "Telangana": {"health_index": 59.8, "aqi": 70, "healthcare_density": 5.8, "altitude": 505, "humidity": 50, "disease_prevalence": 0.23, "healthcare_access": 0.77},
    "Andhra Pradesh": {"health_index": 58.2, "aqi": 60, "healthcare_density": 5.5, "altitude": 150, "humidity": 65, "disease_prevalence": 0.24, "healthcare_access": 0.76},
    "West Bengal": {"health_index": 56.9, "aqi": 90, "healthcare_density": 5.2, "altitude": 15, "humidity": 75, "disease_prevalence": 0.26, "healthcare_access": 0.74},
    "Rajasthan": {"health_index": 54.3, "aqi": 100, "healthcare_density": 4.8, "altitude": 430, "humidity": 35, "disease_prevalence": 0.28, "healthcare_access": 0.72}
}

class HealthCalculator:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.initialize_models()

    def initialize_models(self):
        categories = ['body_composition', 'cardiovascular', 'metabolic', 'lifestyle', 'environmental']
        
        for category in categories:
            # Initialize Random Forest model for each category
            self.models[category] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            self.scalers[category] = StandardScaler()

            # Generate synthetic training data based on state metrics
            X_train, y_train = self.generate_training_data(category)
            
            # Scale features
            X_train_scaled = self.scalers[category].fit_transform(X_train)
            
            # Train the model
            self.models[category].fit(X_train_scaled, y_train)

    def generate_training_data(self, category):
        # Generate synthetic training data based on state metrics and medical knowledge
        X_train = []
        y_train = []

        for state, metrics in INDIAN_STATES.items():
            # Generate multiple samples per state with variations
            for _ in range(50):  # 50 samples per state
                sample = [
                    metrics['health_index'],
                    metrics['aqi'],
                    metrics['healthcare_density'],
                    metrics['altitude'],
                    metrics['humidity'],
                    metrics['disease_prevalence'],
                    metrics['healthcare_access']
                ]
                
                # Add random variations to create more diverse training data
                sample = np.array(sample) * np.random.normal(1, 0.1, len(sample))
                X_train.append(sample)

                # Generate target scores based on category and state metrics
                if category == 'body_composition':
                    score = metrics['health_index'] * 0.6 + metrics['healthcare_access'] * 0.4
                elif category == 'cardiovascular':
                    score = metrics['health_index'] * 0.4 + (100 - metrics['aqi']) * 0.4 + metrics['healthcare_density'] * 0.2
                elif category == 'metabolic':
                    score = metrics['health_index'] * 0.5 + metrics['healthcare_access'] * 0.3 + metrics['healthcare_density'] * 0.2
                elif category == 'lifestyle':
                    score = metrics['health_index'] * 0.3 + (100 - metrics['disease_prevalence'] * 100) * 0.4 + metrics['healthcare_access'] * 0.3
                else:  # environmental
                    score = (100 - metrics['aqi']) * 0.4 + metrics['healthcare_density'] * 0.3 + (100 - metrics['disease_prevalence'] * 100) * 0.3

                # Add some noise to the target scores
                score = min(100, max(0, score + np.random.normal(0, 5)))
                y_train.append(score)

        return np.array(X_train), np.array(y_train)

    def predict_category_score(self, category: str, state_metrics: dict) -> float:
        features = np.array([[
            state_metrics['health_index'],
            state_metrics['aqi'],
            state_metrics['healthcare_density'],
            state_metrics['altitude'],
            state_metrics['humidity'],
            state_metrics['disease_prevalence'],
            state_metrics['healthcare_access']
        ]])
        
        # Scale features
        features_scaled = self.scalers[category].transform(features)
        
        # Predict score
        score = self.models[category].predict(features_scaled)[0]
        
        # Ensure score is within valid range
        return min(100, max(0, score))

    def calculate_health_score(self, data: HealthData) -> HealthScore:
        state_metrics = INDIAN_STATES[data['state']]
        
        # Calculate category scores using ML models
        category_scores = CategoryScores(
            body_composition=self.predict_category_score('body_composition', state_metrics),
            cardiovascular=self.predict_category_score('cardiovascular', state_metrics),
            metabolic=self.predict_category_score('metabolic', state_metrics),
            lifestyle=self.predict_category_score('lifestyle', state_metrics),
            environmental=self.predict_category_score('environmental', state_metrics)
        )
        
        # Calculate overall score with weighted average
        weights = {
            'body_composition': 0.2,
            'cardiovascular': 0.25,
            'metabolic': 0.25,
            'lifestyle': 0.15,
            'environmental': 0.15
        }
        
        overall_score = sum(getattr(category_scores, k) * v for k, v in weights.items())
        
        # Generate recommendations based on scores and state data
        recommendations = self.generate_recommendations(data, category_scores, state_metrics)
        
        return HealthScore(
            overall_score=overall_score,
            category_scores=category_scores,
            recommendations=recommendations
        )

    def generate_recommendations(self, data: HealthData, scores: CategoryScores, state_metrics: dict) -> List[str]:
        recommendations = []

        # State-specific recommendations
        if state_metrics['altitude'] > 1500:
            recommendations.append(
                "High altitude location: Consider regular oxygen level monitoring and maintain proper hydration."
            )

        if state_metrics['humidity'] > 70:
            recommendations.append(
                "High humidity area: Stay well-hydrated and watch for respiratory issues."
            )
        elif state_metrics['humidity'] < 40:
            recommendations.append(
                "Low humidity area: Use humidifiers and maintain skin hydration."
            )

        # Score-based recommendations with state context
        if scores.body_composition < 70:
            recommendations.append(
                f"Consider consulting an Ayurvedic nutritionist in {data['state']} for personalized diet advice. "
                f"Healthcare accessibility score: {state_metrics['healthcare_access']*100:.1f}%"
            )

        if scores.cardiovascular < 70:
            recommendations.append(
                f"Regular yoga and cardiovascular exercise recommended. Monitor BP regularly. "
                f"Local air quality index: {state_metrics['aqi']}"
            )

        if scores.metabolic < 70:
            recommendations.append(
                f"Schedule check-ups at your nearest government health center. "
                f"Healthcare density in your area: {state_metrics['healthcare_density']} facilities per 10,000 people"
            )

        if scores.lifestyle < 70:
            recommendations.append(
                "Practice meditation and maintain regular sleep schedule (7-9 hours). "
                f"Disease prevalence in your area: {state_metrics['disease_prevalence']*100:.1f}%"
            )

        if scores.environmental < 70:
            if state_metrics['aqi'] > 80:
                recommendations.append(
                    f"Air quality in {data['state']} is concerning (AQI: {state_metrics['aqi']}). "
                    "Use air purifiers indoors and wear masks when outside."
                )
            if state_metrics['healthcare_density'] < 6:
                recommendations.append(
                    f"Limited healthcare facilities in {data['state']}. "
                    "Register with your nearest primary health center for regular check-ups."
                )

        return recommendations

class HealthApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Indian Health Score Calculator")
        self.window.geometry("800x600")
        
        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)
        style.configure("TEntry", padding=5)

        self.calculator = HealthCalculator()
        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(main_frame, text="Health Score Calculator", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Form fields
        self.fields = {}
        row = 1

        # Personal Information
        ttk.Label(main_frame, text="Personal Information", font=("Helvetica", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        fields_config = [
            ("age", "Age", "number"),
            ("gender", "Gender", "combo", ["male", "female", "other"]),
            ("height", "Height (cm)", "number"),
            ("weight", "Weight (kg)", "number"),
            ("blood_group", "Blood Group", "combo", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
            ("blood_pressure_systolic", "Systolic BP", "number"),
            ("blood_pressure_diastolic", "Diastolic BP", "number"),
            ("sugar_level", "Sugar Level", "number"),
            ("cholesterol_ldl", "LDL Cholesterol", "number"),
            ("cholesterol_hdl", "HDL Cholesterol", "number"),
            ("liver_enzyme_alt", "ALT", "number"),
            ("liver_enzyme_ast", "AST", "number"),
            ("sleep_duration", "Sleep Duration (hours)", "number"),
            ("vision", "Vision", "combo", ["normal", "corrected", "impaired"]),
            ("hearing", "Hearing", "combo", ["normal", "partial", "impaired"]),
            ("state", "State", "combo", list(INDIAN_STATES.keys()))
        ]

        for field_name, label_text, field_type, *options in fields_config:
            ttk.Label(main_frame, text=label_text).grid(row=row, column=0, sticky=tk.W)
            
            if field_type == "number":
                self.fields[field_name] = ttk.Entry(main_frame)
            elif field_type == "combo":
                self.fields[field_name] = ttk.Combobox(main_frame, values=options[0], state="readonly")
                self.fields[field_name].set(options[0][0])
            
            self.fields[field_name].grid(row=row, column=1, sticky=(tk.W, tk.E))
            row += 1

        # Calculate button
        ttk.Button(main_frame, text="Calculate Score", command=self.calculate_score).grid(row=row, column=0, columnspan=2, pady=20)

    def calculate_score(self):
        try:
            data = HealthData(
                age=int(self.fields["age"].get()),
                gender=self.fields["gender"].get(),
                height=float(self.fields["height"].get()),
                weight=float(self.fields["weight"].get()),
                blood_group=self.fields["blood_group"].get(),
                blood_pressure_systolic=int(self.fields["blood_pressure_systolic"].get()),
                blood_pressure_diastolic=int(self.fields["blood_pressure_diastolic"].get()),
                sugar_level=int(self.fields["sugar_level"].get()),
                cholesterol_ldl=int(self.fields["cholesterol_ldl"].get()),
                cholesterol_hdl=int(self.fields["cholesterol_hdl"].get()),
                liver_enzyme_alt=int(self.fields["liver_enzyme_alt"].get()),
                liver_enzyme_ast=int(self.fields["liver_enzyme_ast"].get()),
                sleep_duration=float(self.fields["sleep_duration"].get()),
                vision=self.fields["vision"].get(),
                hearing=self.fields["hearing"].get(),
                state=self.fields["state"].get()
            )

            result = self.calculator.calculate_health_score(data)
            self.show_results(result)

        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for all fields.")

    def show_results(self, result: HealthScore):
        results_window = tk.Toplevel(self.window)
        results_window.title("Health Score Results")
        results_window.geometry("600x800")

        frame = ttk.Frame(results_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Overall Score
        ttk.Label(frame, text=f"Overall Health Score: {result['overall_score']:.1f}", 
                 font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10)

        # Category Scores
        ttk.Label(frame, text="Category Scores:", 
                 font=("Helvetica", 14, "bold")).grid(row=1, column=0, pady=10)

        row = 2
        for category, score in result["category_scores"].items():
            category_name = category.replace("_", " ").title()
            ttk.Label(frame, text=f"{category_name}: {score:.1f}").grid(row=row, column=0, sticky=tk.W)
            row += 1

        # Recommendations
        ttk.Label(frame, text="Recommendations:", 
                 font=("Helvetica", 14, "bold")).grid(row=row, column=0, pady=10)
        row += 1

        for recommendation in result["recommendations"]:
            ttk.Label(frame, text=f"• {recommendation}", wraplength=500).grid(row=row, column=0, sticky=tk.W)
            row += 1

def main():
    app = HealthApp()
    app.window.mainloop()

if __name__ == "__main__":
    main()