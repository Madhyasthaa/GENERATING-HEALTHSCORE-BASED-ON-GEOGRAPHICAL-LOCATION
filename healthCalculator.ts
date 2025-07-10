import { HealthData, HealthScore, CategoryScores } from '../types/health';
import { INDIAN_STATES } from './constants';
import { HealthMetricsModel } from './modelTraining';

const healthModel = new HealthMetricsModel();

export function calculateBMI(height: number, weight: number): number {
  const heightInMeters = height / 100;
  return weight / (heightInMeters * heightInMeters);
}

function calculateBodyCompositionScore(bmi: number, state: string): number {
  const baseScore = bmi >= 18.5 && bmi <= 24.9 ? 100 :
                   bmi >= 25 && bmi <= 29.9 ? 70 :
                   bmi >= 30 ? 40 : 50;
  
  return healthModel.adjustScore(baseScore, state);
}

function calculateCardiovascularScore(systolic: number, diastolic: number, state: string): number {
  const baseScore = systolic <= 120 && diastolic <= 80 ? 100 :
                   systolic <= 130 && diastolic <= 85 ? 80 :
                   systolic <= 140 && diastolic <= 90 ? 60 : 40;
  
  return healthModel.adjustScore(baseScore, state);
}

function calculateMetabolicScore(
  sugar: number,
  ldl: number,
  hdl: number,
  alt: number,
  ast: number,
  state: string
): number {
  let baseScore = 100;
  if (sugar > 100) baseScore -= 20;
  if (ldl > 100) baseScore -= 20;
  if (hdl < 40) baseScore -= 20;
  if (alt > 40) baseScore -= 20;
  if (ast > 40) baseScore -= 20;
  
  return healthModel.adjustScore(Math.max(baseScore, 0), state);
}

function calculateLifestyleScore(sleepDuration: number, state: string): number {
  const baseScore = sleepDuration >= 7 && sleepDuration <= 9 ? 100 :
                   sleepDuration >= 6 && sleepDuration < 7 ? 70 :
                   sleepDuration > 9 ? 60 : 40;
  
  return healthModel.adjustScore(baseScore, state);
}

function calculateEnvironmentalScore(state: string): number {
  const stateData = INDIAN_STATES[state as keyof typeof INDIAN_STATES];
  let baseScore = 100;

  if (stateData.aqi > 50) baseScore -= 20;
  if (stateData.aqi > 100) baseScore -= 20;
  if (stateData.healthcareDensity < 6) baseScore -= 15;
  if (stateData.healthcareDensity < 5) baseScore -= 15;
  if (stateData.healthIndex < 70) baseScore -= 10;
  if (stateData.healthIndex < 60) baseScore -= 10;

  return healthModel.adjustScore(Math.max(baseScore, 0), state);
}

function generateRecommendations(data: HealthData, scores: CategoryScores): string[] {
  const recommendations: string[] = [];
  const stateData = INDIAN_STATES[data.state as keyof typeof INDIAN_STATES];

  // State-specific recommendations based on altitude
  if (stateData.altitude > 1500) {
    recommendations.push(
      "High altitude location: Consider regular oxygen level monitoring and maintain proper hydration."
    );
  }

  // Humidity-based recommendations
  if (stateData.humidity > 70) {
    recommendations.push(
      "High humidity area: Stay well-hydrated and watch for respiratory issues."
    );
  } else if (stateData.humidity < 40) {
    recommendations.push(
      "Low humidity area: Use humidifiers and maintain skin hydration."
    );
  }

  if (scores.bodyComposition < 70) {
    recommendations.push(
      "Consider consulting an Ayurvedic nutritionist for personalized diet advice."
    );
  }

  if (scores.cardiovascular < 70) {
    recommendations.push(
      "Regular yoga and cardiovascular exercise recommended. Monitor BP regularly."
    );
  }

  if (scores.metabolic < 70) {
    recommendations.push(
      "Schedule check-ups at your nearest government health center or private clinic."
    );
  }

  if (scores.lifestyle < 70) {
    recommendations.push(
      "Practice meditation and maintain regular sleep schedule (7-9 hours)."
    );
  }

  if (scores.environmental < 70) {
    if (stateData.aqi > 80) {
      recommendations.push(
        `Air quality in ${data.state} is concerning. Use air purifiers indoors.`
      );
    }
    if (stateData.healthcareDensity < 6) {
      recommendations.push(
        "Register with your nearest primary health center for regular check-ups."
      );
    }
  }

  return recommendations;
}

export function calculateHealthScore(data: HealthData): HealthScore {
  const bmi = calculateBMI(data.height, data.weight);
  
  const categoryScores: CategoryScores = {
    bodyComposition: calculateBodyCompositionScore(bmi, data.state),
    cardiovascular: calculateCardiovascularScore(
      data.bloodPressureSystolic,
      data.bloodPressureDiastolic,
      data.state
    ),
    metabolic: calculateMetabolicScore(
      data.sugarLevel,
      data.cholesterolLDL,
      data.cholesterolHDL,
      data.liverEnzymeALT,
      data.liverEnzymeAST,
      data.state
    ),
    lifestyle: calculateLifestyleScore(data.sleepDuration, data.state),
    environmental: calculateEnvironmentalScore(data.state)
  };
  
  const overallScore = Math.round(
    (categoryScores.bodyComposition * 0.2 +
     categoryScores.cardiovascular * 0.25 +
     categoryScores.metabolic * 0.25 +
     categoryScores.lifestyle * 0.15 +
     categoryScores.environmental * 0.15) * 100
  ) / 100;

  return {
    overallScore,
    categoryScores,
    recommendations: generateRecommendations(data, categoryScores)
  };
}