"use client";
import { useState } from "react";

export default function BrainwaveTest() {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    async function insertBrainwaveData() {
        setLoading(true);
        setMessage("");

        try {
            const response = await fetch("/api/populate-brainwave-data", { method: "POST" });
            const data = await response.json();

            if (data.success) {
                setMessage("Brainwave data inserted successfully!");
            } else {
                setMessage("Error: " + data.error);
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("Failed to insert brainwave data.");
        }

        setLoading(false);
    }

    async function continouslyInsertBrainwaveData() {
        insertBrainwaveData();
        setTimeout(continouslyInsertBrainwaveData, 100);
    }

    return (
        <div className="flex flex-col items-center gap-4">
            <button
                onClick={insertBrainwaveData}
                disabled={loading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-400"
            >
                {loading ? "Inserting..." : "Insert Brainwave Data"}
            </button>
            <button 
                onClick={continouslyInsertBrainwaveData}
                disabled={loading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-400"
            >
                {loading ? "Inserting..." : "Insert Brainwave Data Continously"}
            </button>   
            {message && <p className="text-sm text-gray-700">{message}</p>}
        </div>
    );
}
