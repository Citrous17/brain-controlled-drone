import { NextResponse } from "next/server";
import pool from "@/app/lib/db"; // Ensure your database connection is correct

export async function GET() {
    try {
        const client = await pool.connect();
        const result = await client.query(
            "SELECT * FROM brainwave_data ORDER BY timestamp DESC LIMIT 1"
        );
        client.release();

        if (result.rows.length === 0) {
            return NextResponse.json({ success: false, message: "No brainwave data found." });
        }

        return NextResponse.json({ success: true, data: result.rows[0] });
    } catch (error) {
        console.error("Error fetching brainwave data:", error);
        return NextResponse.json({ success: false, error: error.message }, { status: 500 });
    }
}
