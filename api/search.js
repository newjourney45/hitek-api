import duckdb from 'duckdb';

const db = new duckdb.Database(':memory:');
const BASE_URL = 'https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/';

export default async function handler(req, res) {
  // Allow CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { query, file = 'part1.parquet', limit = 100 } = req.query;
    const url = BASE_URL + file;

    // Simple query
    let sql = `SELECT * FROM read_parquet('${url}')`;
    if (query) {
      sql += ` WHERE name ILIKE '%${query}%' OR district ILIKE '%${query}%' OR phoneNumber ILIKE '%${query}%'`;
    }
    sql += ` LIMIT ${parseInt(limit)}`;

    // Get data
    const rows = await new Promise((resolve, reject) => {
      db.all(sql, (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });

    // RAW DATA - No masking
    res.json({
      success: true,
      count: rows.length,
      data: rows
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
