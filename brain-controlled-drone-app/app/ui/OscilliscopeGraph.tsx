import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from "recharts";
import { useState, useEffect } from "react";

const generateSineWave = (time: number, amplitude: number, frequency: number) => {
    return amplitude * Math.sin(2 * Math.PI * frequency * time);
};

export default function OscilloscopeGraph() {
    const [data, setData] = useState<{ time: number; value: number }[]>([]);
    useEffect(() => {
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
    )
}

