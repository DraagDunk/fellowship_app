import fs from 'fs';
import path from 'path';
import { Sequelize, DataTypes, Options } from 'sequelize';
import { DbInterface } from '../types';
import config from '../config/config';
import { Env } from '../config/config';

const basename = path.basename(__filename);
const env: Env = (process.env.NODE_ENV as Env) || 'development';
const typedConfig = config[env];

const sequelize = new Sequelize(
  typedConfig.database,
  typedConfig.username,
  typedConfig.password,
  {
    host: typedConfig.host,
    dialect: typedConfig.dialect,
  } as Options
);

const db: DbInterface = {
  sequelize,
  Sequelize,
};

fs.readdirSync(__dirname)
  .filter((file) => {
    return (
      file.indexOf('.') !== 0 &&
      file !== basename &&
      (file.slice(-3) === '.js' || file.slice(-3) === '.ts') &&
      file.indexOf('.test.') === -1
    );
  })
  .forEach((file) => {
    const model = require(path.join(__dirname, file)).default(sequelize, DataTypes);
    db[model.name] = model;
  });

Object.keys(db).forEach((modelName) => {
  if (modelName !== 'sequelize' && modelName !== 'Sequelize') {
    const model = db[modelName] as any;
    if (model.associate) {
      model.associate(db);
    }
  }
});

export = db;
