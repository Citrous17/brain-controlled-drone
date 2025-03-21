import pool from './db';

export async function testDb() {
      try {
        const client = await pool.connect();
        const res = await client.query("SELECT * FROM brainwave_data");
        client.release();
    
        console.log("Database connection successful");
      } catch (error) {
        console.error("Database connection error:", error);
    }
}

export async function getData() {
    const client = await pool.connect();
    const res = await client.query('SELECT * FROM brainwave_data');
    client.release();
    console.log(res.rows);
    return res.rows;
}
