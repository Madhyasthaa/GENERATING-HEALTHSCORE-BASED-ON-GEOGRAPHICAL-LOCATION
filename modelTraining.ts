import * as tf from '@tensorflow/tfjs';
import { INDIAN_STATES } from './constants';

interface StateMetrics {
  healthIndex: number;
  aqi: number;
  healthcareDensity: number;
  altitude: number;
  humidity: number;
}

export class HealthMetricsModel {
  private model: tf.LayersModel | null = null;
  private normalizedRanges: Map<string, { min: number; max: number }> = new Map();

  constructor() {
    this.initializeModel();
  }

  private async initializeModel() {
    // Create a simple neural network
    const model = tf.sequential();
    
    model.add(tf.layers.dense({
      units: 16,
      activation: 'relu',
      inputShape: [5] // healthIndex, aqi, healthcareDensity, altitude, humidity
    }));
    
    model.add(tf.layers.dense({
      units: 8,
      activation: 'relu'
    }));
    
    model.add(tf.layers.dense({
      units: 3, // outputs: [minRange, maxRange, adjustmentFactor]
      activation: 'sigmoid'
    }));

    model.compile({
      optimizer: tf.train.adam(0.01),
      loss: 'meanSquaredError'
    });

    this.model = model;
    await this.trainModel();
  }

  private async trainModel() {
    const stateMetrics = Object.entries(INDIAN_STATES).map(([_, metrics]) => [
      metrics.healthIndex / 100,
      metrics.aqi / 100,
      metrics.healthcareDensity / 10,
      metrics.altitude / 2500,
      metrics.humidity / 100
    ]);

    // Generate synthetic training data based on state metrics
    const inputData = tf.tensor2d(stateMetrics);
    
    // Generate target ranges based on state health indices
    const targetRanges = stateMetrics.map(metrics => {
      const healthIndex = metrics[0] * 100;
      return [
        Math.max(0.4, healthIndex / 100 - 0.2), // minRange
        Math.min(1.0, healthIndex / 100 + 0.2), // maxRange
        healthIndex / 100 // adjustmentFactor
      ];
    });

    const outputData = tf.tensor2d(targetRanges);

    // Train the model
    await this.model!.fit(inputData, outputData, {
      epochs: 100,
      batchSize: 4,
      shuffle: true
    });
  }

  public predictRanges(state: string): { minRange: number; maxRange: number; adjustmentFactor: number } {
    const stateData = INDIAN_STATES[state as keyof typeof INDIAN_STATES];
    
    const input = tf.tensor2d([[
      stateData.healthIndex / 100,
      stateData.aqi / 100,
      stateData.healthcareDensity / 10,
      stateData.altitude / 2500,
      stateData.humidity / 100
    ]]);

    const prediction = this.model!.predict(input) as tf.Tensor;
    const [minRange, maxRange, adjustmentFactor] = prediction.dataSync();

    return {
      minRange: Math.max(0, minRange * 100),
      maxRange: Math.min(100, maxRange * 100),
      adjustmentFactor: adjustmentFactor
    };
  }

  public adjustScore(score: number, state: string): number {
    const ranges = this.predictRanges(state);
    const normalizedScore = (score - ranges.minRange) / (ranges.maxRange - ranges.minRange);
    return Math.min(100, Math.max(0, normalizedScore * 100 * ranges.adjustmentFactor));
  }
}