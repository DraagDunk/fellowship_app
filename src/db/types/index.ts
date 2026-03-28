import { Sequelize } from 'sequelize';
import { UserModel } from './user';

// The interface for the db object used to access the database.
export interface DbInterface {
  [key: string]: UserModel | Sequelize | typeof Sequelize; // Used making dynamic loading of each data type possible
  sequelize: Sequelize;
  Sequelize: typeof Sequelize;
  User: UserModel;
}
