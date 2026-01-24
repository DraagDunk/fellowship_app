import { Router, Request, Response, NextFunction } from 'express';
const router: Router = Router();

/* GET home page. */
router.get('/', (req: Request, res: Response, next: NextFunction) => {
  res.render('index.ejs', { title: 'The Fantasy Fellowship' });
});

export default router;
