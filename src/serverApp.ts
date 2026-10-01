import express, { Request, Response, Router } from 'express';
import path from 'path';
import fs from 'fs';
import { INITIAL_RESTAURANTS, INITIAL_FOODS } from './data/initialData.js';
import { Restaurant, Food } from './types.js';

export interface DatabaseSchema {
  restaurants: Restaurant[];
  foods: Food[];
  users: Array<{ id: number; name: string; email: string; passwordHash: string; avatar?: string }>;
  profiles: Record<number, any>;
  logs: Record<number, any[]>;
}

// In Vercel serverless environment, the root filesystem is read-only.
// We use /tmp for writes, and fallback to data/db.json or INITIAL_* data for reads.
const isServerless = Boolean(process.env.VERCEL || process.env.AWS_LAMBDA_FUNCTION_NAME);
const DB_FILE = isServerless
  ? path.join('/tmp', 'db.json')
  : path.join(process.cwd(), 'data', 'db.json');

const SEED_FILE = path.join(process.cwd(), 'data', 'db.json');

export function initDb(): DatabaseSchema {
  try {
    const dir = path.dirname(DB_FILE);
    if (!fs.existsSync(dir)) {
      try {
        fs.mkdirSync(dir, { recursive: true });
      } catch {
        // ignore
      }
    }

    // Try reading active db file first
    let fileToRead = DB_FILE;
    if (!fs.existsSync(fileToRead) && fs.existsSync(SEED_FILE)) {
      fileToRead = SEED_FILE;
    }

    if (fs.existsSync(fileToRead)) {
      const data = fs.readFileSync(fileToRead, 'utf-8');
      const parsed = JSON.parse(data);
      return {
        restaurants: parsed.restaurants || [...INITIAL_RESTAURANTS],
        foods: parsed.foods || [...INITIAL_FOODS],
        users: parsed.users || [
          {
            id: 1,
            name: 'นักศึกษาสุขภาพดี',
            email: 'student@npru.ac.th',
            passwordHash: 'password123',
            avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
          },
        ],
        profiles: parsed.profiles || {
          1: {
            weight: 65,
            height: 175,
            age: 21,
            gender: 'male',
            activity: 1.55,
            bmr: 1650,
            tdee: 2558,
            calories: 2000,
            updatedAt: new Date().toISOString(),
          },
        },
        logs: parsed.logs || {
          1: [
            {
              id: 'log-1',
              name: 'ข้าวกะเพราไก่ + ไข่ดาว',
              calories: 590,
              type: 'lunch',
              timestamp: '12:30 น.',
              protein: 28,
              carbs: 55,
              fat: 26,
            },
            {
              id: 'log-2',
              name: 'ชาไทยเย็นหวานน้อย (25%)',
              calories: 160,
              type: 'snack',
              timestamp: '14:15 น.',
              protein: 3,
              carbs: 24,
              fat: 6,
            },
          ],
        },
      };
    }
  } catch (err) {
    console.warn('Notice reading db file:', err);
  }

  const initial: DatabaseSchema = {
    restaurants: [...INITIAL_RESTAURANTS],
    foods: [...INITIAL_FOODS],
    users: [
      {
        id: 1,
        name: 'นักศึกษาสุขภาพดี',
        email: 'student@npru.ac.th',
        passwordHash: 'password123',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
      },
    ],
    profiles: {
      1: {
        weight: 65,
        height: 175,
        age: 21,
        gender: 'male',
        activity: 1.55,
        bmr: 1650,
        tdee: 2558,
        calories: 2000,
        updatedAt: new Date().toISOString(),
      },
    },
    logs: {
      1: [
        {
          id: 'log-1',
          name: 'ข้าวกะเพราไก่ + ไข่ดาว',
          calories: 590,
          type: 'lunch',
          timestamp: '12:30 น.',
          protein: 28,
          carbs: 55,
          fat: 26,
        },
        {
          id: 'log-2',
          name: 'ชาไทยเย็นหวานน้อย (25%)',
          calories: 160,
          type: 'snack',
          timestamp: '14:15 น.',
          protein: 3,
          carbs: 24,
          fat: 6,
        },
      ],
    },
  };

  try {
    fs.writeFileSync(DB_FILE, JSON.stringify(initial, null, 2), 'utf-8');
  } catch (err) {
    // In read-only filesystems, keep in memory
  }
  return initial;
}

let db = initDb();

export function saveDb() {
  try {
    fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2), 'utf-8');
  } catch (err) {
    console.warn('Notice saving db file (in-memory state active):', err);
  }
}

export const apiRouter = Router();

// Health check endpoint
apiRouter.get('/health', (_req: Request, res: Response) => {
  res.json({
    status: 'online',
    service: 'University Food Kcal API',
    database: 'persistent',
    version: '1.0.0',
    platform: process.env.VERCEL ? 'vercel-serverless' : 'node-server',
  });
});

// Auth: Register
apiRouter.post('/auth/register', (req: Request, res: Response) => {
  const { name, email, password } = req.body;
  if (!name || !email || !password) {
    return res.status(400).json({ error: 'กรุณากรอกข้อมูลให้ครบถ้วน (ชื่อ, อีเมล, รหัสผ่าน)' });
  }
  const cleanEmail = String(email).trim().toLowerCase();
  const existing = db.users.find((u) => u.email.toLowerCase() === cleanEmail);
  if (existing) {
    return res.status(400).json({ error: 'อีเมลนี้ถูกใช้งานแล้วในระบบ' });
  }

  const maxId = db.users.reduce((max, u) => Math.max(max, u.id), 0);
  const newUser = {
    id: maxId + 1,
    name: String(name).trim(),
    email: cleanEmail,
    passwordHash: String(password),
    avatar: `https://api.dicebear.com/7.x/bottts/svg?seed=${cleanEmail}`,
  };
  db.users.push(newUser);

  // Initialize default profile
  db.profiles[newUser.id] = {
    weight: 60,
    height: 170,
    age: 20,
    gender: 'male',
    activity: 1.375,
    bmr: 1545,
    tdee: 2124,
    calories: 2000,
    updatedAt: new Date().toISOString(),
  };
  db.logs[newUser.id] = [];
  saveDb();

  res.status(201).json({
    message: 'สมัครสมาชิกสำเร็จ',
    token: `token-${newUser.id}-${Date.now()}`,
    user: {
      id: newUser.id,
      name: newUser.name,
      email: newUser.email,
      avatar: newUser.avatar,
    },
  });
});

// Auth: Login
apiRouter.post('/auth/login', (req: Request, res: Response) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'กรุณากรอกอีเมลและรหัสผ่าน' });
  }
  const cleanEmail = String(email).trim().toLowerCase();
  const user = db.users.find((u) => u.email.toLowerCase() === cleanEmail);
  if (!user || user.passwordHash !== String(password)) {
    return res.status(401).json({ error: 'อีเมลหรือรหัสผ่านไม่ถูกต้อง' });
  }

  res.json({
    message: 'เข้าสู่ระบบสำเร็จ',
    token: `token-${user.id}-${Date.now()}`,
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      avatar: user.avatar,
    },
  });
});

// Auth: Me
apiRouter.get('/auth/me', (req: Request, res: Response) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: 'ไม่พบข้อมูลการเข้าสู่ระบบ' });
  }
  const match = authHeader.match(/token-(\d+)-/);
  const userId = match ? parseInt(match[1], 10) : 1;
  const user = db.users.find((u) => u.id === userId);
  if (!user) {
    return res.status(404).json({ error: 'ไม่พบผู้ใช้งาน' });
  }
  res.json({
    id: user.id,
    name: user.name,
    email: user.email,
    avatar: user.avatar,
  });
});

// Profile: Get & Save
apiRouter.get('/profile', (req: Request, res: Response) => {
  const userId = req.query.userId ? parseInt(String(req.query.userId), 10) : 1;
  const profile = db.profiles[userId] || {
    weight: 65,
    height: 175,
    age: 21,
    gender: 'male',
    activity: 1.55,
    bmr: 1650,
    tdee: 2558,
    calories: 2000,
  };
  res.json(profile);
});

apiRouter.post('/profile', (req: Request, res: Response) => {
  const { userId, weight, height, age, gender, activity, bmr, tdee, calories } = req.body;
  const uId = userId ? parseInt(String(userId), 10) : 1;
  db.profiles[uId] = {
    weight: Number(weight) || 60,
    height: Number(height) || 170,
    age: Number(age) || 20,
    gender: gender === 'female' ? 'female' : 'male',
    activity: Number(activity) || 1.2,
    bmr: Number(bmr) || 1500,
    tdee: Number(tdee) || 2000,
    calories: Number(calories) || 2000,
    updatedAt: new Date().toISOString(),
  };
  saveDb();
  res.json({ success: true, profile: db.profiles[uId] });
});

// Daily Meal Logs
apiRouter.get('/logs', (req: Request, res: Response) => {
  const userId = req.query.userId ? parseInt(String(req.query.userId), 10) : 1;
  const userLogs = db.logs[userId] || [];
  const totalCalories = userLogs.reduce((sum: number, m: any) => sum + (m.calories || 0), 0);
  const totalProtein = userLogs.reduce((sum: number, m: any) => sum + (m.protein || 0), 0);
  const totalCarbs = userLogs.reduce((sum: number, m: any) => sum + (m.carbs || 0), 0);
  const totalFat = userLogs.reduce((sum: number, m: any) => sum + (m.fat || 0), 0);

  res.json({
    meals: userLogs,
    totalCalories,
    totalProtein,
    totalCarbs,
    totalFat,
  });
});

apiRouter.post('/logs', (req: Request, res: Response) => {
  const { userId, name, calories, type, protein, carbs, fat } = req.body;
  const uId = userId ? parseInt(String(userId), 10) : 1;
  if (!name || calories === undefined) {
    return res.status(400).json({ error: 'กรุณาระบุชื่ออาหารและจำนวนแคลอรี่' });
  }
  if (!db.logs[uId]) {
    db.logs[uId] = [];
  }
  const newLog = {
    id: `log-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
    name: String(name),
    calories: Number(calories) || 0,
    type: type || 'lunch',
    timestamp: new Date().toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) + ' น.',
    protein: Number(protein) || 0,
    carbs: Number(carbs) || 0,
    fat: Number(fat) || 0,
  };
  db.logs[uId].push(newLog);
  saveDb();
  res.status(201).json(newLog);
});

apiRouter.delete('/logs/:id', (req: Request, res: Response) => {
  const userId = req.query.userId ? parseInt(String(req.query.userId), 10) : 1;
  const logId = req.params.id;
  if (db.logs[userId]) {
    db.logs[userId] = db.logs[userId].filter((l: any) => l.id !== logId);
    saveDb();
  }
  res.json({ success: true, message: 'ลบรายการอาหารเรียบร้อยแล้ว' });
});

// REST API: Menu aliases for compatibility
apiRouter.get('/menu/:restaurantId', (req: Request, res: Response) => {
  const restId = parseInt(req.params.restaurantId, 10);
  const rest = db.restaurants.find((r) => r.id === restId);
  const foods = db.foods.filter((f) => f.restaurant_id === restId);
  res.json({
    restaurant: rest || null,
    dishes: foods,
  });
});

apiRouter.get('/menu/item/:dishId', (req: Request, res: Response) => {
  const dishId = parseInt(req.params.dishId, 10);
  const food = db.foods.find((f) => f.id === dishId);
  if (!food) {
    return res.status(404).json({ error: 'ไม่พบเมนู' });
  }
  const rest = db.restaurants.find((r) => r.id === food.restaurant_id);
  res.json({
    ...food,
    restaurant: rest || null,
  });
});

// REST API: Restaurants
apiRouter.get('/restaurants', (_req: Request, res: Response) => {
  res.json(db.restaurants);
});

apiRouter.get('/restaurants/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const restaurant = db.restaurants.find((r) => r.id === id);
  if (!restaurant) {
    return res.status(404).json({ error: 'ไม่พบร้านอาหารที่ระบุ' });
  }
  res.json(restaurant);
});

apiRouter.post('/restaurants', (req: Request, res: Response) => {
  const { name, description, location, image, phone, open_hours } = req.body;
  if (!name || !location) {
    return res.status(400).json({ error: 'กรุณากรอกชื่อร้านและตำแหน่งสถานที่ตั้ง' });
  }
  const maxId = db.restaurants.reduce((max, r) => Math.max(max, r.id), 0);
  const newRestaurant: Restaurant = {
    id: maxId + 1,
    name: String(name).trim(),
    description: String(description || '').trim(),
    location: String(location).trim(),
    image: String(image || 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80').trim(),
    phone: phone ? String(phone).trim() : '',
    open_hours: open_hours ? String(open_hours).trim() : '08:00 - 18:00 น.',
    created_at: new Date().toISOString(),
  };
  db.restaurants.push(newRestaurant);
  saveDb();
  res.status(201).json(newRestaurant);
});

apiRouter.put('/restaurants/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const index = db.restaurants.findIndex((r) => r.id === id);
  if (index === -1) {
    return res.status(404).json({ error: 'ไม่พบร้านอาหารที่ต้องการแก้ไข' });
  }
  const existing = db.restaurants[index];
  const { name, description, location, image, phone, open_hours } = req.body;

  db.restaurants[index] = {
    ...existing,
    name: name !== undefined ? String(name).trim() : existing.name,
    description: description !== undefined ? String(description).trim() : existing.description,
    location: location !== undefined ? String(location).trim() : existing.location,
    image: image !== undefined ? String(image).trim() : existing.image,
    phone: phone !== undefined ? String(phone).trim() : existing.phone,
    open_hours: open_hours !== undefined ? String(open_hours).trim() : existing.open_hours,
  };

  if (name && name !== existing.name) {
    db.foods.forEach((f) => {
      if (f.restaurant_id === id) {
        f.restaurant_name = name;
      }
    });
  }

  saveDb();
  res.json(db.restaurants[index]);
});

apiRouter.delete('/restaurants/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const index = db.restaurants.findIndex((r) => r.id === id);
  if (index === -1) {
    return res.status(404).json({ error: 'ไม่พบร้านอาหารที่ต้องการลบ' });
  }
  db.restaurants.splice(index, 1);
  db.foods = db.foods.filter((f) => f.restaurant_id !== id);
  saveDb();
  res.json({ success: true, message: 'ลบร้านอาหารและเมนูที่เกี่ยวข้องเรียบร้อยแล้ว' });
});

// REST API: Foods
apiRouter.get('/foods', (req: Request, res: Response) => {
  const search = req.query.search ? String(req.query.search).toLowerCase() : null;
  const restaurant_id = req.query.restaurant_id ? parseInt(String(req.query.restaurant_id), 10) : null;
  const min_kcal = req.query.min_kcal ? parseInt(String(req.query.min_kcal), 10) : null;
  const max_kcal = req.query.max_kcal ? parseInt(String(req.query.max_kcal), 10) : null;
  const sort_by = req.query.sort_by ? String(req.query.sort_by) : null;

  let results = [...db.foods];

  results = results.map((f) => {
    const rest = db.restaurants.find((r) => r.id === f.restaurant_id);
    return {
      ...f,
      restaurant_name: rest ? rest.name : f.restaurant_name || 'ร้านค้าในมหาวิทยาลัย',
    };
  });

  if (search) {
    results = results.filter(
      (f) =>
        f.name.toLowerCase().includes(search) ||
        (f.restaurant_name && f.restaurant_name.toLowerCase().includes(search)) ||
        f.description.toLowerCase().includes(search)
    );
  }

  if (restaurant_id) {
    results = results.filter((f) => f.restaurant_id === restaurant_id);
  }

  if (min_kcal !== null && !isNaN(min_kcal)) {
    results = results.filter((f) => f.kcal >= min_kcal);
  }

  if (max_kcal !== null && !isNaN(max_kcal)) {
    results = results.filter((f) => f.kcal <= max_kcal);
  }

  if (sort_by === 'kcal_asc') {
    results.sort((a, b) => a.kcal - b.kcal);
  } else if (sort_by === 'kcal_desc') {
    results.sort((a, b) => b.kcal - a.kcal);
  } else if (sort_by === 'price_asc') {
    results.sort((a, b) => a.price - b.price);
  } else if (sort_by === 'price_desc') {
    results.sort((a, b) => b.price - a.price);
  }

  res.json(results);
});

apiRouter.get('/foods/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const food = db.foods.find((f) => f.id === id);
  if (!food) {
    return res.status(404).json({ error: 'ไม่พบรายการอาหารที่ระบุ' });
  }
  const rest = db.restaurants.find((r) => r.id === food.restaurant_id);
  res.json({
    ...food,
    restaurant_name: rest ? rest.name : food.restaurant_name || 'ร้านค้าในมหาวิทยาลัย',
  });
});

apiRouter.get('/foods/restaurant/:restaurant_id', (req: Request, res: Response) => {
  const restaurant_id = parseInt(req.params.restaurant_id, 10);
  const rest = db.restaurants.find((r) => r.id === restaurant_id);
  const foods = db.foods
    .filter((f) => f.restaurant_id === restaurant_id)
    .map((f) => ({
      ...f,
      restaurant_name: rest ? rest.name : f.restaurant_name,
    }));
  res.json(foods);
});

apiRouter.post('/foods', (req: Request, res: Response) => {
  const { name, restaurant_id, price, kcal, protein, carbohydrate, fat, image, description, category, is_popular } =
    req.body;
  if (!name || !restaurant_id) {
    return res.status(400).json({ error: 'กรุณาระบุชื่ออาหารและเลือกร้านอาหาร' });
  }
  const restId = parseInt(restaurant_id, 10);
  const rest = db.restaurants.find((r) => r.id === restId);
  if (!rest) {
    return res.status(400).json({ error: 'ร้านอาหารที่เลือกไม่มีอยู่ในระบบ' });
  }

  const maxId = db.foods.reduce((max, f) => Math.max(max, f.id), 0);
  const newFood: Food = {
    id: maxId + 1,
    name: String(name).trim(),
    restaurant_id: restId,
    restaurant_name: rest.name,
    price: Number(price) || 0,
    kcal: Number(kcal) || 0,
    protein: Number(protein) || 0,
    carbohydrate: Number(carbohydrate) || 0,
    fat: Number(fat) || 0,
    image: String(image || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80').trim(),
    description: String(description || '').trim(),
    category: category ? String(category).trim() : 'อาหารจานเดียว',
    is_popular: Boolean(is_popular),
  };
  db.foods.push(newFood);
  saveDb();
  res.status(201).json(newFood);
});

apiRouter.put('/foods/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const index = db.foods.findIndex((f) => f.id === id);
  if (index === -1) {
    return res.status(404).json({ error: 'ไม่พบรายการอาหารที่ต้องการแก้ไข' });
  }
  const existing = db.foods[index];
  const { name, restaurant_id, price, kcal, protein, carbohydrate, fat, image, description, category, is_popular } =
    req.body;

  let targetRestId = existing.restaurant_id;
  if (restaurant_id !== undefined) {
    targetRestId = parseInt(restaurant_id, 10);
  }
  const rest = db.restaurants.find((r) => r.id === targetRestId);

  db.foods[index] = {
    ...existing,
    name: name !== undefined ? String(name).trim() : existing.name,
    restaurant_id: targetRestId,
    restaurant_name: rest ? rest.name : existing.restaurant_name,
    price: price !== undefined ? Number(price) : existing.price,
    kcal: kcal !== undefined ? Number(kcal) : existing.kcal,
    protein: protein !== undefined ? Number(protein) : existing.protein,
    carbohydrate: carbohydrate !== undefined ? Number(carbohydrate) : existing.carbohydrate,
    fat: fat !== undefined ? Number(fat) : existing.fat,
    image: image !== undefined ? String(image).trim() : existing.image,
    description: description !== undefined ? String(description).trim() : existing.description,
    category: category !== undefined ? String(category).trim() : existing.category,
    is_popular: is_popular !== undefined ? Boolean(is_popular) : existing.is_popular,
  };
  saveDb();
  res.json(db.foods[index]);
});

apiRouter.delete('/foods/:id', (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  const index = db.foods.findIndex((f) => f.id === id);
  if (index === -1) {
    return res.status(404).json({ error: 'ไม่พบรายการอาหารที่ต้องการลบ' });
  }
  db.foods.splice(index, 1);
  saveDb();
  res.json({ success: true, message: 'ลบรายการอาหารเรียบร้อยแล้ว' });
});

// Admin stats endpoint
apiRouter.get('/stats', (_req: Request, res: Response) => {
  const total_restaurants = db.restaurants.length;
  const total_foods = db.foods.length;
  const total_kcal = db.foods.reduce((sum, f) => sum + f.kcal, 0);
  const avg_kcal = total_foods > 0 ? Math.round((total_kcal / total_foods) * 10) / 10 : 0;

  const sortedByKcal = [...db.foods].sort((a, b) => b.kcal - a.kcal);
  const max_kcal_food = sortedByKcal.length > 0 ? sortedByKcal[0] : null;

  const foodsWithKcal = db.foods.filter((f) => f.kcal > 0).sort((a, b) => a.kcal - b.kcal);
  const min_kcal_food = foodsWithKcal.length > 0 ? foodsWithKcal[0] : (sortedByKcal.length > 0 ? sortedByKcal[sortedByKcal.length - 1] : null);

  res.json({
    total_restaurants,
    total_foods,
    avg_kcal,
    max_kcal_food,
    min_kcal_food,
  });
});

// Reset data endpoint
apiRouter.post('/reset', (_req: Request, res: Response) => {
  db = initDb();
  saveDb();
  res.json({ message: 'รีเซ็ตข้อมูลเริ่มต้นสำเร็จ', db });
});

export function createServerApp() {
  const app = express();
  app.use(express.json());

  // CORS support
  app.use((_req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    if (_req.method === 'OPTIONS') {
      return res.sendStatus(200);
    }
    next();
  });

  // Mount under both '/api' and '/' to ensure 100% compatibility across
  // standalone Express, local dev proxy, and Vercel serverless functions
  app.use('/api', apiRouter);
  app.use('/', apiRouter);

  return app;
}

const serverApp = createServerApp();
export default serverApp;
