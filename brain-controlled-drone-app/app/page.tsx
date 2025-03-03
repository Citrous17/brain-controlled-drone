"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import Footer from "./ui/footer";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from "recharts";

// Function to generate a sine wave data point
const generateSineWave = (time: number, amplitude: number, frequency: number) => {
  return amplitude * Math.sin(2 * Math.PI * frequency * time);
};

export default function Home() {
  const [data, setData] = useState<{ time: number; value: number }[]>([]);
  const [isClient, setIsClient] = useState(false); // Track if the component is on the client

  useEffect(() => {
    setIsClient(true); // Set to true when the component mounts (client-side)

    // Simulate real-time data updates
    const interval = setInterval(() => {
      const time = Date.now() / 1000; // Current time in seconds
      const newDataPoint = {
        time: time,
        value: generateSineWave(time, 1, 1), // Amplitude = 1, Frequency = 1 Hz
      };

      // Keep only the last 100 data points for performance
      setData((prevData) => {
        const newData = [...prevData, newDataPoint];
        if (newData.length > 100) {
          newData.shift(); // Remove the oldest data point
        }
        return newData;
      });
    }, 100); // Update every 100ms

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 w-full max-w-5xl">
        <Image
          className="dark:invert mx-auto"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <ol className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          <li className="mb-2">
            Get started by editing{" "}
            <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">
              app/page.tsx
            </code>
            .
          </li>
          <li>Save and see your changes instantly.</li>
        </ol>

        {/* Oscilloscope Graph */}
        {isClient && (
          <div className="w-full">
            <h2 className="text-xl font-semibold text-center sm:text-left mb-4">
              Oscilloscope
            </h2>
            <div className="w-full h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={data}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" type="number" domain={["auto", "auto"]} hide={false}>
                    <Label value="EEG-Waves" offset={-5} position="insideBottom" />
                  </XAxis>
                  <YAxis domain={[-1.5, 1.5]}>
                    <Label value="Hz" angle={-90} position="insideLeft" />
                  </YAxis>
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#8884d8"
                    dot={false}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Three Buttons Below the Graph */}
        <div className="flex w-full justify-between mt-4">
          <button
            className="button button-primary flex-1 mx-2"
            onClick={() => alert("Train Model Clicked!")}
          >
            Train Model
          </button>
          <button
            className="button button-secondary flex-1 mx-2"
            onClick={() => alert("Reset Readings Clicked!")}
          >
            Reset Readings
          </button>
          <button
            className="button button-tertiary flex-1 mx-2"
            onClick={() => alert("Recalibrate Clicked!")}
          >
            Recalibrate
          </button>
        </div>

        <h2 className="text-xl font-semibold text-center sm:text-left mt-6">
          Drone Controls
        </h2>

        {/* Drone Control Buttons - Left-Aligned Vertical Layout */}
        <div className="flex flex-col gap-4 w-full max-w-xs">
          <button className="button button-primary self-start" onClick={() => alert("Move Forward Clicked!")}>
            Move Forward
          </button>
          <button className="button button-primary self-start" onClick={() => alert("Move Back Clicked!")}>
            Move Back
          </button>
          <button className="button button-primary self-start" onClick={() => alert("Move Up Clicked!")}>
            Move Up
          </button>
          <button className="button button-primary self-start" onClick={() => alert("Move Down Clicked!")}>
            Move Down
          </button>
          <button className="button button-primary self-start" onClick={() => alert("Move Left Clicked!")}>
            Move Left
          </button>
          <button className="button button-primary self-start" onClick={() => alert("Move Right Clicked!")}>
            Move Right
          </button>
        </div>

      </main>
      <Footer />
    </div>
  );
}
