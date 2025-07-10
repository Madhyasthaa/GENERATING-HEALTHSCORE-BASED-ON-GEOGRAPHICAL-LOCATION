import React from 'react';
import { HealthScore } from '../types/health';
import { Activity, Heart, Brain, Moon, Wind } from 'lucide-react';

interface HealthScoreProps {
  score: HealthScore;
}

export function HealthScoreDisplay({ score }: HealthScoreProps) {
  const getScoreColor = (value: number) => {
    if (value >= 80) return 'text-green-600';
    if (value >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const categories = [
    {
      name: 'Body Composition',
      score: score.categoryScores.bodyComposition,
      icon: Activity,
    },
    {
      name: 'Cardiovascular',
      score: score.categoryScores.cardiovascular,
      icon: Heart,
    },
    {
      name: 'Metabolic',
      score: score.categoryScores.metabolic,
      icon: Brain,
    },
    {
      name: 'Lifestyle',
      score: score.categoryScores.lifestyle,
      icon: Moon,
    },
    {
      name: 'Environmental',
      score: score.categoryScores.environmental,
      icon: Wind,
    },
  ];

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <h2 className="text-2xl font-bold mb-2">Overall Health Score</h2>
        <div className={`text-6xl font-bold ${getScoreColor(score.overallScore)}`}>
          {score.overallScore}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Category Scores</h3>
        <div className="grid gap-4">
          {categories.map((category) => (
            <div key={category.name} className="flex items-center">
              <category.icon className="w-6 h-6 mr-2" />
              <div className="flex-1">
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    {category.name}
                  </span>
                  <span className={`text-sm font-medium ${getScoreColor(category.score)}`}>
                    {category.score}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      category.score >= 80
                        ? 'bg-green-600'
                        : category.score >= 60
                        ? 'bg-yellow-600'
                        : 'bg-red-600'
                    }`}
                    style={{ width: `${category.score}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Recommendations</h3>
        <ul className="space-y-2">
          {score.recommendations.map((recommendation, index) => (
            <li key={index} className="flex items-start">
              <span className="inline-block w-4 h-4 mt-1 mr-2 bg-blue-600 rounded-full" />
              <span>{recommendation}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}