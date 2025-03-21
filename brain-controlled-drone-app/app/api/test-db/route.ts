import { NextResponse } from "next/server";
import pool from './db';

export async function GET() {
  try {
    const client = await pool.connect();
    const res = await client.query("SELECT NOW()");
    
    client.release();

    return NextResponse.json({ success: true, timestamp: res.rows[0].now });
  } catch (error) {
    console.error("Database connection error:", error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
