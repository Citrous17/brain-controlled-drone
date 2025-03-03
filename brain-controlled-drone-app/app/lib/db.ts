import { Pool } from 'pg';

const pool = new Pool({
  host: 'localhost', 
  port: 5434,      
  user: 'postgres',
  password: 'password',
  database: 'dronedb',
});

export default pool;