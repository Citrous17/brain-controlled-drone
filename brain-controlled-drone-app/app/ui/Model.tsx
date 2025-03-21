"use client"
import { useState } from "react";
import * as tf from "@tensorflow/tfjs";

export default function TrainModelPage() {
  const [dataset, setDataset] = useState<any[]>([]);
  const [features, setFeatures] = useState<string[]>([]);
  const [target, setTarget] = useState("");
  const [epochs, setEpochs] = useState(10);
  const [batchSize, setBatchSize] = useState(32);
  const [model, setModel] = useState<tf.Sequential | null>(null);
  const [trainingLogs, setTrainingLogs] = useState<string[]>([]);

  const handleFileUpload = (e: any) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      if (event.target && typeof event.target.result === 'string') {
        const data = JSON.parse(event.target.result);
        setDataset(data);
        // Only include numeric features
        const keys = Object.keys(data[0] || {});
        const numericKeys = keys.filter(key => typeof data[0][key] === 'number');
        setFeatures(numericKeys);
      }
    };
    reader.readAsText(file);
  };

  const trainModel = async () => {
    if (!dataset || !target) return;

    // Use numericFeatures for inputs
    const inputs = dataset.map((row) => features.map((f) => row[f]));
    const labels = dataset.map((row) => row[target]);

    const xs = tf.tensor2d(inputs);
    const ys = tf.tensor2d(labels, [labels.length, 1]);

    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 16, activation: "relu", inputShape: [features.length] }));
    model.add(tf.layers.dense({ units: 1, activation: "linear" }));

    model.compile({ optimizer: "adam", loss: "meanSquaredError" });
    setModel(model);

    await model.fit(xs, ys, {
      epochs: epochs,
      batchSize: batchSize,
      callbacks: {
        onEpochEnd: (epoch, logs) => {
          setTrainingLogs((prev) => [...prev, `Epoch ${epoch + 1}: Loss = ${logs?.loss?.toFixed(4) ?? 'N/A'}`]);
        },
      },
    });
  };

  return (
    <div className="p-6 max-w-2xl mx-auto bg-gray-900 text-white rounded-lg shadow-lg dark">
      <h1 className="text-2xl font-bold mb-4 text-yellow-400">Train The Brain Drone Neural Network</h1>
      <input type="file" onChange={handleFileUpload} accept=".json" className="mb-4 p-2 bg-gray-700 text-white rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
      {dataset && (
        <div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-yellow-400 mb-2">Target Feature</label>
            <select onChange={(e) => setTarget(e.target.value)} className="p-2 bg-gray-700 text-white rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500">
              {features.map((feature) => (
                <option key={feature} value={feature}>{feature}</option>
              ))}
            </select>
          </div>
          <label className="block text-sm font-medium text-yellow-400 mb-2">Training Parameters</label>
          <label className="block text-sm font-medium text-gray-300 mb-2">Epochs</label>
          <input type="number" value={epochs} onChange={(e) => setEpochs(+e.target.value)} placeholder="Epochs" className="mb-2 p-2 bg-gray-700 text-white rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
          <label className="block text-sm font-medium text-gray-300 mb-2">Batch Size</label>
          <input type="number" value={batchSize} onChange={(e) => setBatchSize(+e.target.value)} placeholder="Batch Size" className="mb-2 p-2 bg-gray-700 text-white rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
          <button onClick={trainModel} className="p-2 mt-4 bg-yellow-500 text-gray-900 font-semibold rounded hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-500">
            Train Model
          </button>
        </div>
      )}
      <div className="mt-4">
        <h2 className="text-lg font-semibold text-yellow-400">Training Logs</h2>
        {trainingLogs.map((log, index) => (
          <p key={index} className="text-gray-300">{log}</p>
        ))}
      </div>
    </div>
  );
}