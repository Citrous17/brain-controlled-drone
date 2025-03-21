"use client"
import { useEffect, useState } from 'react';
import BrainwaveGraph from './BrainwaveGraph';

export default function BrainwaveChart() {
    const [brainwaveData, setBrainwaveData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/api/fetch-brainwave-data');
            const res = await response.json();
            console.log("response: ", res.data);
            setBrainwaveData(res.data);
        };

        fetchData();
        const interval = setInterval(fetchData, 500); // Refresh every 500ms
        return () => clearInterval(interval);
    }, []);

    return <BrainwaveGraph data={brainwaveData} />;
}
