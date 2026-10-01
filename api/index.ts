import type { Request, Response } from 'express';
import serverApp from '../src/serverApp.js';

export default function handler(req: Request, res: Response) {
  return serverApp(req, res);
}
