import { Restaurant, Food, AdminStats } from '../types';

const API_BASE = '/api';

export const api = {
  // Restaurants
  async getRestaurants(): Promise<Restaurant[]> {
    const res = await fetch(`${API_BASE}/restaurants`);
    if (!res.ok) throw new Error('ไม่สามารถโหลดข้อมูลร้านอาหารได้');
    return res.json();
  },

  async getRestaurant(id: number): Promise<Restaurant> {
    const res = await fetch(`${API_BASE}/restaurants/${id}`);
    if (!res.ok) throw new Error('ไม่พบข้อมูลร้านอาหาร');
    return res.json();
  },

  async createRestaurant(data: Partial<Restaurant>): Promise<Restaurant> {
    const res = await fetch(`${API_BASE}/restaurants`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถเพิ่มร้านอาหารได้');
    }
    return res.json();
  },

  async updateRestaurant(id: number, data: Partial<Restaurant>): Promise<Restaurant> {
    const res = await fetch(`${API_BASE}/restaurants/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถแก้ไขร้านอาหารได้');
    }
    return res.json();
  },

  async deleteRestaurant(id: number): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/restaurants/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถลบร้านอาหารได้');
    }
    return res.json();
  },

  // Foods
  async getFoods(params?: {
    search?: string;
    restaurant_id?: number;
    min_kcal?: number;
    max_kcal?: number;
    sort_by?: string;
  }): Promise<Food[]> {
    const query = new URLSearchParams();
    if (params?.search) query.append('search', params.search);
    if (params?.restaurant_id) query.append('restaurant_id', String(params.restaurant_id));
    if (params?.min_kcal !== undefined) query.append('min_kcal', String(params.min_kcal));
    if (params?.max_kcal !== undefined) query.append('max_kcal', String(params.max_kcal));
    if (params?.sort_by) query.append('sort_by', params.sort_by);

    const queryString = query.toString();
    const url = queryString ? `${API_BASE}/foods?${queryString}` : `${API_BASE}/foods`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('ไม่สามารถโหลดข้อมูลเมนูอาหารได้');
    return res.json();
  },

  async getFood(id: number): Promise<Food> {
    const res = await fetch(`${API_BASE}/foods/${id}`);
    if (!res.ok) throw new Error('ไม่พบข้อมูลเมนูอาหาร');
    return res.json();
  },

  async getFoodsByRestaurant(restaurantId: number): Promise<Food[]> {
    const res = await fetch(`${API_BASE}/foods/restaurant/${restaurantId}`);
    if (!res.ok) throw new Error('ไม่สามารถโหลดเมนูของร้านได้');
    return res.json();
  },

  async createFood(data: Partial<Food>): Promise<Food> {
    const res = await fetch(`${API_BASE}/foods`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถเพิ่มเมนูอาหารได้');
    }
    return res.json();
  },

  async updateFood(id: number, data: Partial<Food>): Promise<Food> {
    const res = await fetch(`${API_BASE}/foods/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถแก้ไขเมนูอาหารได้');
    }
    return res.json();
  },

  async deleteFood(id: number): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/foods/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'ไม่สามารถลบเมนูอาหารได้');
    }
    return res.json();
  },

  // Stats
  async getStats(): Promise<AdminStats> {
    const res = await fetch(`${API_BASE}/stats`);
    if (!res.ok) throw new Error('ไม่สามารถโหลดสถิติได้');
    return res.json();
  },

  // Reset database to initial
  async resetDatabase(): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE}/reset`, { method: 'POST' });
    if (!res.ok) throw new Error('ไม่สามารถรีเซ็ตข้อมูลได้');
    return res.json();
  },

  // Auth
  async login(credentials: { email: string; password: string }): Promise<{ token: string; user: any }> {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'เข้าสู่ระบบไม่สำเร็จ');
    }
    return res.json();
  },

  async register(data: { name: string; email: string; password: string }): Promise<{ token: string; user: any }> {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'สมัครสมาชิกไม่สำเร็จ');
    }
    return res.json();
  },

  async getCurrentUser(token?: string): Promise<any> {
    const headers: Record<string, string> = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`${API_BASE}/auth/me`, { headers });
    if (!res.ok) throw new Error('ไม่สามารถดึงข้อมูลผู้ใช้ได้');
    return res.json();
  },

  // User Profile
  async getProfile(userId?: number | string): Promise<any> {
    const url = userId ? `${API_BASE}/profile?userId=${userId}` : `${API_BASE}/profile`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('ไม่สามารถโหลดโปรไฟล์ได้');
    return res.json();
  },

  async saveProfile(profileData: any): Promise<any> {
    const res = await fetch(`${API_BASE}/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileData),
    });
    if (!res.ok) throw new Error('ไม่สามารถบันทึกโปรไฟล์ได้');
    return res.json();
  },

  // Logs
  async getDailyLogs(userId?: number | string): Promise<any> {
    const url = userId ? `${API_BASE}/logs?userId=${userId}` : `${API_BASE}/logs`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('ไม่สามารถโหลดรายการอาหารได้');
    return res.json();
  },

  async addMealLog(logData: any): Promise<any> {
    const res = await fetch(`${API_BASE}/logs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData),
    });
    if (!res.ok) throw new Error('ไม่สามารถเพิ่มรายการอาหารได้');
    return res.json();
  },

  async addDailyLog(logData: any): Promise<any> {
    return this.addMealLog(logData);
  },

  async deleteMealLog(logId: string, userId?: number | string): Promise<any> {
    const url = userId ? `${API_BASE}/logs/${logId}?userId=${userId}` : `${API_BASE}/logs/${logId}`;
    const res = await fetch(url, { method: 'DELETE' });
    if (!res.ok) throw new Error('ไม่สามารถลบรายการอาหารได้');
    return res.json();
  },

  async deleteDailyLog(logId: string, userId?: number | string): Promise<any> {
    return this.deleteMealLog(logId, userId);
  },

  async logout(): Promise<void> {
    localStorage.removeItem('token');
  },
};

