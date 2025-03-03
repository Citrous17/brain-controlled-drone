"use client"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { BrainwaveData } from '../lib/definitions';

interface BrainwaveGraphProps {
    data: BrainwaveData[];
}

export default function BrainwaveGraph({ data }: BrainwaveGraphProps) {
    if(data.length === 0) {
        return <p>Loading...</p>;
    }
    return (
        <>
            <LineChart width={800} height={400} data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="channel_1" stroke="#8884d8" />
                <Line type="monotone" dataKey="channel_2" stroke="#82ca9d" />
                <Line type="monotone" dataKey="channel_3" stroke="#ff7300" />
                <Line type="monotone" dataKey="channel_4" stroke="#ff0000" />
                <Line type="monotone" dataKey="channel_5" stroke="#00ff00" />
                <Line type="monotone" dataKey="channel_6" stroke="#0000ff" />
                <Line type="monotone" dataKey="channel_7" stroke="#ff00ff" />
                <Line type="monotone" dataKey="channel_8" stroke="#00ffff" />
            </LineChart>
        </>
    );
}
