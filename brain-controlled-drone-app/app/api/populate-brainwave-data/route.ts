import { NextResponse } from "next/server";
import pool from "@/app/lib/db"; // Make sure your DB connection is correct

export async function POST() {
    try {
        const client = await pool.connect();

        // Generate random brainwave values
        const randomData = {
            alpha: Math.random() * 100,
            beta: Math.random() * 100,
            gamma: Math.random() * 100,
            delta: Math.random() * 100,
            theta: Math.random() * 100,
            timestamp: new Date(),
            channel_1: Math.random() * 100,
            channel_2: Math.random() * 100,
            channel_3: Math.random() * 100,
            channel_4: Math.random() * 100,
            channel_5: Math.random() * 100,
            channel_6: Math.random() * 100,
            channel_7: Math.random() * 100,
            channel_8: Math.random() * 100,
        };

        await client.query(
            `INSERT INTO brainwave_data (alpha, beta, gamma, delta, theta, timestamp, channel_1, channel_2, channel_3, channel_4, channel_5, channel_6, channel_7, channel_8) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)`,
            [
                randomData.alpha,
                randomData.beta,
                randomData.gamma,
                randomData.delta,
                randomData.theta,
                randomData.timestamp,
                randomData.channel_1,
                randomData.channel_2,
                randomData.channel_3,
                randomData.channel_4,
                randomData.channel_5,
                randomData.channel_6,
                randomData.channel_7,
                randomData.channel_8,
            ]
        );

        client.release();
        return NextResponse.json({ success: true, message: "Brainwave data inserted." });
    } catch (error) {
        console.error("Error inserting brainwave data:", error);
        return NextResponse.json({ success: false, error: error.message }, { status: 500 });
    }
}
