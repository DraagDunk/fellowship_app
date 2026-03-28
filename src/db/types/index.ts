import { Model, Sequelize } from 'sequelize';

export interface DbInterface {
  [key: string]: Model<any, any> | Sequelize | typeof Sequelize; // Allow any of these types for dynamic keys
  sequelize: Sequelize;
  Sequelize: typeof Sequelize;
}
