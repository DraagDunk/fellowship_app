import { Dialect } from 'sequelize';

// Used by the server to connect to the database
interface DbConnectionConfig {
  username: string;
  password: string;
  database: string;
  host: string;
  dialect: Dialect;
}

// A type to hold the different configurations needed for the diffent application environments
interface AppEnvDbConfigs {
  development: DbConnectionConfig;
  test: DbConnectionConfig;
  production: DbConnectionConfig;
}

// An instance holding the different configurations needed for connecting to the database depending on the application environment type
// Default values are set in case no values are provided through environment variables
// dialect is hardcoded to postgres as that is the supported DB type
const config: AppEnvDbConfigs = {
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

export default config;
export type Env = keyof AppEnvDbConfigs;
