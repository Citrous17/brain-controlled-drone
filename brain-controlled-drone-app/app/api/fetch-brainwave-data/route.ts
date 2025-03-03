import { NextResponse } from "next/server";
import { BrainwaveData } from "@/app/lib/definitions";
import pool from "@/app/lib/db";

export async function GET() {
  try {
    const client = await pool.connect();
    const res = await client.query("SELECT * FROM brainwave_data");
    console.log(res.rows);
    const data: BrainwaveData[] = res.rows.map((row: any) => ({
        id: row.id,
        timestamp: row.timestamp,
        alpha: row.alpha,
        beta: row.beta,
        gamma: row.gamma,
        delta: row.delta,
        theta: row.theta,
        channel_1: row.channel_1,
        channel_2: row.channel_2,
        channel_3: row.channel_3,
        channel_4: row.channel_4,
        channel_5: row.channel_5,
        channel_6: row.channel_6,
        channel_7: row.channel_7,
        channel_8: row.channel_8,
    }));
    client.release();

    return NextResponse.json({ success: true, data});
  } catch (error) {
    console.error("Database connection error:", error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
