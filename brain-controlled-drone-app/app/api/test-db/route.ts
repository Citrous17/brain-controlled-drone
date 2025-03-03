import { NextResponse } from "next/server";
import { Pool } from "pg";

// Create a PostgreSQL connection pool
const pool = new Pool({
  user: "postgres",
  host: "brain-drone-server", // Change to "brain-drone-server" if using Docker
  database: "dronedb",
  password: "password", // Ensure this is correct
  port: 5432, // Update if needed (e.g., 5433)
});

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
