const fs = require('fs');
const path = require('path');

const migrationName = process.argv[2];
if (!migrationName) {
  console.error('Please provide a migration name');
  process.exit(1);
}

const timestamp = new Date().getTime();
const migrationFileName = `${timestamp}-${migrationName}.ts`;
const migrationsPath = path.resolve('src', 'db', 'migrations');
const migrationFilePath = path.join(migrationsPath, migrationFileName);

const migrationTemplate = `import { QueryInterface, DataTypes } from 'sequelize';

module.exports = {
  up: async (queryInterface: QueryInterface, Sequelize: typeof DataTypes) => {
    // Migration code here
  },
  down: async (queryInterface: QueryInterface, Sequelize: typeof DataTypes) => {
    // Rollback code here
  },
};
`;

fs.writeFileSync(migrationFilePath, migrationTemplate);
console.log(`Generated migration: ${migrationFilePath}`);
