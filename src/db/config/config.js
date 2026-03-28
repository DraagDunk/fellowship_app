// This file is used to configure access to the database during migration

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
