import { Model, Optional } from "sequelize";

// The attribues a User can have
export interface UserAttributes {
  id: number;
  name: string;
  email: string;
  password: string;
  createdAt?: Date;
  updatedAt?: Date;
}

// Used to make otherwise required fields optional during creation
export type UserCreationAttributes = Optional<UserAttributes, 'id' | 'createdAt' | 'updatedAt'>;

// The UserModel used when accessing users through the database
export type UserModel = typeof Model & (new (values?: object, options?: any) => Model<UserAttributes, UserCreationAttributes>);
