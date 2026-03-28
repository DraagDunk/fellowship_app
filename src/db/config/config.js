// This file is used during migration of the db

module.exports = {
  development: {
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    database: process.env.DB_SCHEMA || 'postgres',
    host: process.env.DB_HOST || 'postgres',
    dialect: 'postgres',
  },
  test: {
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    database: `${process.env.DB_SCHEMA || 'postgres'}_test`,
    host: process.env.DB_HOST || 'postgres',
    dialect: 'postgres',
  },
  production: {
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    database: process.env.DB_SCHEMA || 'postgres',
    host: process.env.DB_HOST || 'postgres',
    dialect: 'postgres',
  },
};
