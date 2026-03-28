import { Sequelize } from 'sequelize';

export interface DbInterface {
  [key: string]: any; // Allow dynamic model properties
  sequelize: Sequelize;
  Sequelize: typeof Sequelize;
}
