export interface HealthData {
  age: number;
  gender: 'male' | 'female' | 'other';
  height: number;
  weight: number;
  bloodGroup: 'A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-';
  bloodPressureSystolic: number;
  bloodPressureDiastolic: number;
  sugarLevel: number;
  cholesterolLDL: number;
  cholesterolHDL: number;
  liverEnzymeALT: number;
  liverEnzymeAST: number;
  sleepDuration: number;
  vision: 'normal' | 'corrected' | 'impaired';
  hearing: 'normal' | 'partial' | 'impaired';
  state: string;
}

export interface CategoryScores {
  bodyComposition: number;
  cardiovascular: number;
  metabolic: number;
  lifestyle: number;
  environmental: number;
}

export interface HealthScore {
  overallScore: number;
  categoryScores: CategoryScores;
  recommendations: string[];
}