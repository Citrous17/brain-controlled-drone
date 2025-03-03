import pool from './db';

export async function testDb() {
    const client = await pool.connect();
    const res = await client.query('SELECT NOW()');
    client.release();
}
