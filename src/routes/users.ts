import { Router, Request, Response, NextFunction } from 'express';
import db from '../db/models';
const router: Router = Router();

/* GET users listing. */
router.get('/', (_req: Request, res: Response) => {
  res.send('respond with a resource');
});

/* POST create user - POC to prove that we can create users. Definitely not the final version. */
router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      res.status(400).json({
        error: "Name, email and password are required."
      })
    }

    const user = await db.User.create({ name, email, password });
    const { password: _, ...userWithoutPassword } = user.toJSON();
    res.status(201).json(userWithoutPassword);
  } catch (error) {
    next(error);
  }
});

export default router;
