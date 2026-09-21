export interface Restaurant {
  id: number;
  name: string;
  description: string;
  location: string;
  image: string;
  phone?: string;
  open_hours?: string;
  created_at?: string;
}

export interface Food {
  id: number;
  name: string;
  restaurant_id: number;
  restaurant_name?: string;
  price: number;
  kcal: number;
  protein: number;
  carbohydrate: number;
  fat: number;
  image: string;
  description: string;
  category?: string;
  is_popular?: boolean;
}

export interface CartItem {
  food: Food;
  quantity: number;
}

export interface NutritionSummary {
  totalKcal: number;
  totalProtein: number;
  totalCarbs: number;
  totalFat: number;
  itemCount: number;
}

export interface User {
  id: number | string;
  name: string;
  email: string;
  avatar?: string;
  role?: string;
}

export interface AdminStats {
  total_restaurants: number;
  total_foods: number;
  avg_kcal: number;
  max_kcal_food: Food | null;
  min_kcal_food: Food | null;
}

export interface UserProfile {
  weight: number;
  height: number;
  age: number;
  gender: 'male' | 'female';
  activity: number;
  bmr: number;
  tdee: number;
  calories: number;
  updatedAt?: string;
}

export interface MealLogItem {
  id: string;
  name: string;
  calories: number;
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  timestamp: string;
  protein?: number;
  carbs?: number;
  fat?: number;
}

export interface DailyLog {
  meals: MealLogItem[];
  totalCalories: number;
  totalProtein?: number;
  totalCarbs?: number;
  totalFat?: number;
}

export interface ModifierOption {
  id: string;
  name: string;
  category: 'add-on' | 'adjustment';
  kcal: number;
  carbs: number;
  pro: number;
  fat: number;
}

