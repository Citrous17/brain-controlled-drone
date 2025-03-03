"use client";
import { useState } from "react";
import OscilloscopeGraph from "./OscilliscopeGraph";

const trainingOptions: (keyof typeof images)[] = [
    "Train Forward",
    "Train Backwards",
    "Train Left",
    "Train Right",
    "Train Up",
    "Train Down",
    "Train Rotate",
];

const images = {
    "Train Forward": ["/images/forward1.jpg"],
    "Train Backwards": ["/images/backward1.jpg"],
    "Train Left": ["/images/left1.jpg"],
    "Train Right": ["/images/right1.jpg"],
    "Train Up": ["/images/up1.jpg"],
    "Train Down": ["/images/down1.jpg"],
    "Train Rotate": ["/images/rotate1.jpg",]
};

const videos = {
    "Train Forward": ["/videos/forward1.mp4"],
    "Train Backwards": ["/videos/backward1.mp4"],
    "Train Left": ["/videos/left1.mp4"],
    "Train Right": ["/videos/right1.mp4"],
    "Train Up": ["/videos/up1.mp4"],
    "Train Down": ["/videos/down1.mp4"],
    "Train Rotate": ["/videos/rotate1.mp4"],
};

export default function TrainBrainwaves() {
    const [selectedTraining, setSelectedTraining] = useState<keyof typeof images>(trainingOptions[0]);
    const [mediaSrc, setMediaSrc] = useState<string | null>(null);
    const [mediaType, setMediaType] = useState<"image" | "video" | null>(null);
    const [brainwaveData, setBrainwaveData] = useState(null);

    const showRandomMedia = (type: "image" | "video") => {
        const mediaList = type === "image" ? images[selectedTraining] : videos[selectedTraining];
        if (mediaList.length > 0) {
            const randomIndex = Math.floor(Math.random() * mediaList.length);
            setMediaSrc(mediaList[randomIndex]);
            setMediaType(type);
        }
    };

    const fetchBrainwaveData = async () => {
        try {
            const response = await fetch("/api/fetch-brainwaves");
            const data = await response.json();

            if (data.success) {
                setBrainwaveData(data.data);
            } else {
                console.error("Failed to fetch brainwave data:", data.message);
            }
        } catch (error) {
            console.error("Error fetching brainwave data:", error);
        }
    };

    return (
        <div className="flex flex-col items-center gap-6 p-6">
            <h1 className="text-2xl font-bold">Brainwave Training</h1>

            {/* Training Dropdown */}
            <style jsx>{`
                select {
                    background-color: #1a202c; /* Dark background */
                    color: #cbd5e0; /* Light text */
                    border-color: #4a5568; /* Dark border */
                }
                select option {
                    background-color: #1a202c; /* Dark background for options */
                    color: #cbd5e0; /* Light text for options */
                }
            `}</style>
            <select
                className="px-4 py-2 border border-gray-300 rounded"
                value={selectedTraining}
                onChange={(e) => setSelectedTraining(e.target.value as keyof typeof images)}
            >
                {trainingOptions.map((option) => (
                    <option key={option} value={option}>
                        {option}
                    </option>
                ))}
            </select>

            {/* Media Buttons */}
            <div className="flex gap-4">
                <button
                    onClick={() => showRandomMedia("image")}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg"
                >
                    Show Image
                </button>
                <button
                    onClick={() => showRandomMedia("video")}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg"
                >
                    Show Video
                </button>
            </div>

            {/* Media Display */}
            {mediaSrc && mediaType === "image" && (
                <img src={mediaSrc} alt="Training Image" className="max-w-md mt-4 rounded shadow" />
            )}

            {mediaSrc && mediaType === "video" && (
                <video src={mediaSrc} width={800} height={800} controls className="max-w-md mt-4 rounded shadow" />
            )}

            <OscilloscopeGraph />

        </div>
    );
}
