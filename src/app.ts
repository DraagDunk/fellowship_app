import cookieParser from 'cookie-parser';
import express, { Express } from 'express';
import logger from 'morgan';
import path from 'path';
import indexRouter from './routes/index';
import usersRouter from './routes/users';

const app: Express = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/views'));

app.use('/', indexRouter);
app.use('/users', usersRouter);

export default app;
