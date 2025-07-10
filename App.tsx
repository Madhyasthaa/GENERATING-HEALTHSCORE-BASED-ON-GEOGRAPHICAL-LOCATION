import React, { useState } from 'react';
import { HealthForm } from './components/HealthForm';
import { HealthScoreDisplay } from './components/HealthScore';
import { HealthData, HealthScore } from './types/health';
import { calculateHealthScore } from './utils/healthCalculator';
import { Activity } from 'lucide-react';

function App() {
  const [healthScore, setHealthScore] = useState<HealthScore | null>(null);

  const handleSubmit = (data: HealthData) => {
    const score = calculateHealthScore(data);
    setHealthScore(score);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <Activity className="w-12 h-12 text-blue-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Indian Health Score Calculator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Enter your health metrics to receive a comprehensive health score and
            personalized recommendations based on your location in India.
          </p>
        </div>

        {!healthScore ? (
          <HealthForm onSubmit={handleSubmit} />
        ) : (
          <div>
            <HealthScoreDisplay score={healthScore} />
            <div className="text-center mt-8">
              <button
                onClick={() => setHealthScore(null)}
                className="bg-gray-600 text-white px-6 py-2 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
              >
                Calculate Again
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;