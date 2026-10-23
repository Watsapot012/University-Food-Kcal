import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/HomePage';
import { RestaurantsPage } from './pages/RestaurantsPage';
import { FoodListPage } from './pages/FoodListPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { LoginPage } from './pages/LoginPage';
import { ProfilePage } from './pages/ProfilePage';
import { MealCustomizerPage } from './pages/MealCustomizerPage';
import { DailyDashboardPage } from './pages/DailyDashboardPage';
import { FoodDetailModal } from './components/FoodDetailModal';
import { api } from './services/api';
import { Restaurant, Food, AdminStats, User, UserProfile, MealLogItem } from './types';
import { INITIAL_RESTAURANTS, INITIAL_FOODS } from './data/initialData';
import { Flame, AlertCircle, RefreshCw, X } from 'lucide-react';

const USER_STORAGE_KEY = 'uni_food_user';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('home');
  const [restaurants, setRestaurants] = useState<Restaurant[]>(INITIAL_RESTAURANTS);
  const [foods, setFoods] = useState<Food[]>(INITIAL_FOODS);
  const [stats, setStats] = useState<AdminStats>({
    total_restaurants: INITIAL_RESTAURANTS.length,
    total_foods: INITIAL_FOODS.length,
    avg_kcal: 440,
    max_kcal_food: INITIAL_FOODS[3] || null,
    min_kcal_food: INITIAL_FOODS[16] || null,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // User & Auth State
  const [user, setUser] = useState<User | null>(() => {
    try {
      const savedUser = localStorage.getItem(USER_STORAGE_KEY);
      if (savedUser) return JSON.parse(savedUser);
    } catch {
      // ignore
    }
    // Default logged in demo student user for instant seamless experience
    return {
      id: 'demo-student',
      name: 'นักศึกษา NPRU',
      email: '674259012@webmail.npru.ac.th',
      role: 'student',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
    };
  });

  const [userProfile, setUserProfile] = useState<UserProfile | null>({
    weight: 65,
    height: 175,
    age: 21,
    gender: 'male',
    activity: 1.55,
    bmr: 1650,
    tdee: 2558,
    calories: 2000,
  });

  // Daily Meal Logs State
  const [dailyMeals, setDailyMeals] = useState<MealLogItem[]>([
    {
      id: 'meal-1',
      name: 'ข้าวกะเพราไก่ไข่ดาว',
      calories: 640,
      timestamp: '08:30',
      type: 'breakfast',
      protein: 31,
      carbs: 66,
      fat: 27,
    },
    {
      id: 'meal-2',
      name: 'ก๋วยเตี๋ยวต้มยำหมูน้ำใส',
      calories: 380,
      timestamp: '12:45',
      type: 'lunch',
      protein: 20,
      carbs: 52,
      fat: 10,
    },
  ]);

  const [showLoginModal, setShowLoginModal] = useState<boolean>(false);
  const [customizerFoodId, setCustomizerFoodId] = useState<number | undefined>(undefined);

  // Active detail modal
  const [selectedFood, setSelectedFood] = useState<Food | null>(null);
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [foodSearchQuery, setFoodSearchQuery] = useState<string>('');

  // Quick Toast
  const [toast, setToast] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 2500);
  };

  // Persist user
  useEffect(() => {
    try {
      if (user) {
        localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
      } else {
        localStorage.removeItem(USER_STORAGE_KEY);
      }
    } catch {
      // ignore
    }
  }, [user]);

  // Check backend session & load user logs
  useEffect(() => {
    api.getCurrentUser()
      .then((res) => {
        if (res.user) {
          setUser(res.user);
          if (res.user.id) {
            api.getProfile(res.user.id).then((p) => {
              if (p) setUserProfile(p);
            }).catch(() => {});
            api.getDailyLogs(res.user.id).then((logs) => {
              if (logs && logs.length > 0) setDailyMeals(logs);
            }).catch(() => {});
          }
        }
      })
      .catch(() => {
        // use local demo state
      });
  }, []);

  // Load data from backend API
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [restsData, foodsData, statsData] = await Promise.all([
        api.getRestaurants().catch(() => INITIAL_RESTAURANTS),
        api.getFoods().catch(() => INITIAL_FOODS),
        api.getStats().catch(() => ({
          total_restaurants: INITIAL_RESTAURANTS.length,
          total_foods: INITIAL_FOODS.length,
          avg_kcal: 440,
          max_kcal_food: INITIAL_FOODS[3] || null,
          min_kcal_food: INITIAL_FOODS[16] || null,
        })),
      ]);
      setRestaurants(restsData);
      setFoods(foodsData);
      setStats(statsData);
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError('ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้ กำลังแสดงข้อมูลแคชตัวอย่าง');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Navigation helper
  const handleNavigate = (tab: string, query?: string) => {
    setActiveTab(tab);
    if (query !== undefined) {
      setFoodSearchQuery(query);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Select restaurant helper
  const handleSelectRestaurant = (r: Restaurant | null) => {
    setSelectedRestaurant(r);
    setActiveTab('restaurants');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Daily Meal logging handlers
  const handleAddToDailyLog = (item: {
    name: string;
    calories: number;
    type: string;
    protein?: number;
    carbs?: number;
    fat?: number;
  }) => {
    const timeNow = new Date().toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
    const newLogItem: MealLogItem = {
      id: `meal-${Date.now()}`,
      name: item.name,
      calories: item.calories,
      timestamp: timeNow,
      type: item.type as any,
      protein: item.protein,
      carbs: item.carbs,
      fat: item.fat,
    };

    setDailyMeals((prev) => [newLogItem, ...prev]);

    // Save to backend if user exists
    if (user) {
      api.addDailyLog({
        userId: user.id,
        meal: newLogItem,
      }).catch(() => {});
    }

    showToast(`บันทึก "${item.name}" (${item.calories} kcal) ลงไดอารี่แล้ว`);
  };

  const handleDeleteDailyMeal = (mealId: string) => {
    setDailyMeals((prev) => prev.filter((m) => m.id !== mealId));
    if (user) {
      api.deleteDailyLog(mealId, user.id).catch(() => {});
    }
    showToast('ลบรายการอาหารจากไดอารี่แล้ว');
  };

  // Auth Handlers
  const handleLoginSuccess = (loggedInUser: User) => {
    setUser(loggedInUser);
    setShowLoginModal(false);
    showToast(`ยินดีต้อนรับคุณ ${loggedInUser.name}`);

    // Load profile and logs
    api.getProfile(loggedInUser.id)
      .then((p) => {
        if (p) setUserProfile(p);
      })
      .catch(() => {});

    api.getDailyLogs(loggedInUser.id)
      .then((logs) => {
        if (logs && logs.length > 0) setDailyMeals(logs);
      })
      .catch(() => {});
  };

  const handleLogout = () => {
    api.logout().catch(() => {});
    setUser(null);
    localStorage.removeItem(USER_STORAGE_KEY);
    showToast('ออกจากระบบเรียบร้อยแล้ว');
  };

  // Open customizer for specific food
  const handleOpenCustomizer = (food: Food) => {
    setCustomizerFoodId(food.id);
    setActiveTab('customizer');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Admin operations
  const handleAddRestaurant = async (data: Partial<Restaurant>) => {
    await api.createRestaurant(data);
    await loadData();
  };

  const handleUpdateRestaurant = async (id: number, data: Partial<Restaurant>) => {
    await api.updateRestaurant(id, data);
    await loadData();
  };

  const handleDeleteRestaurant = async (id: number) => {
    await api.deleteRestaurant(id);
    await loadData();
  };

  const handleAddFood = async (data: Partial<Food>) => {
    await api.createFood(data);
    await loadData();
  };

  const handleUpdateFood = async (id: number, data: Partial<Food>) => {
    await api.updateFood(id, data);
    await loadData();
  };

  const handleDeleteFood = async (id: number) => {
    await api.deleteFood(id);
    await loadData();
  };

  const handleResetDatabase = async () => {
    await api.resetDatabase();
    await loadData();
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-black selection:text-white">
      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 bg-black text-white text-xs font-semibold px-4 py-3 rounded-full shadow-2xl flex items-center gap-2 border border-slate-700 animate-bounce">
          <Flame className="w-4 h-4 text-amber-400" />
          <span>{toast}</span>
        </div>
      )}

      {/* Top Floating Pill Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          if (tab !== 'restaurants') setSelectedRestaurant(null);
          handleNavigate(tab);
        }}
        user={user}
        onOpenLogin={() => setShowLoginModal(true)}
        onLogout={handleLogout}
      />

      {/* Error Banner if any */}
      {error && (
        <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 text-xs text-amber-800 flex items-center justify-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>{error}</span>
          <button
            onClick={() => loadData()}
            className="underline font-semibold ml-2 flex items-center gap-1 cursor-pointer"
          >
            <RefreshCw className="w-3 h-3" /> ลองใหม่อีกครั้ง
          </button>
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8">
        {activeTab === 'home' && (
          <HomePage
            restaurants={restaurants}
            foods={foods}
            onSelectFood={(food) => setSelectedFood(food)}
            onNavigate={handleNavigate}
            onSelectRestaurant={handleSelectRestaurant}
          />
        )}

        {activeTab === 'restaurants' && (
          <RestaurantsPage
            restaurants={restaurants}
            foods={foods}
            onSelectFood={(food) => setSelectedFood(food)}
            selectedRestaurant={selectedRestaurant}
            onSelectRestaurant={setSelectedRestaurant}
            onOpenAddRestaurantModal={() => setActiveTab('admin')}
          />
        )}

        {activeTab === 'foods' && (
          <FoodListPage
            foods={foods}
            restaurants={restaurants}
            onSelectFood={(food) => setSelectedFood(food)}
            initialSearch={foodSearchQuery}
            onOpenAddFoodModal={() => setActiveTab('admin')}
          />
        )}

        {activeTab === 'customizer' && (
          <MealCustomizerPage
            foods={foods}
            initialFoodId={customizerFoodId}
            onAddToDailyLog={handleAddToDailyLog}
            onNavigateToDashboard={() => handleNavigate('dashboard')}
          />
        )}

        {activeTab === 'dashboard' && (
          <DailyDashboardPage
            user={user}
            profile={userProfile}
            meals={dailyMeals}
            onAddMeal={handleAddToDailyLog}
            onDeleteMeal={handleDeleteDailyMeal}
            onNavigateToCustomizer={() => handleNavigate('customizer')}
            onNavigateToProfile={() => handleNavigate('profile')}
            onNavigateToFoods={() => handleNavigate('foods')}
          />
        )}

        {activeTab === 'profile' && (
          <ProfilePage
            user={user}
            onLogout={handleLogout}
            onNavigateToDashboard={() => handleNavigate('dashboard')}
            onProfileUpdated={(p) => setUserProfile(p)}
          />
        )}

        {activeTab === 'admin' && (
          <AdminDashboardPage
            restaurants={restaurants}
            foods={foods}
            stats={stats}
            onRefreshData={loadData}
            onAddRestaurant={handleAddRestaurant}
            onUpdateRestaurant={handleUpdateRestaurant}
            onDeleteRestaurant={handleDeleteRestaurant}
            onAddFood={handleAddFood}
            onUpdateFood={handleUpdateFood}
            onDeleteFood={handleDeleteFood}
            onResetDatabase={handleResetDatabase}
          />
        )}
      </main>

      {/* Food Detail Modal */}
      {selectedFood && (
        <FoodDetailModal
          food={selectedFood}
          restaurant={restaurants.find((r) => r.id === selectedFood.restaurant_id) || null}
          onClose={() => setSelectedFood(null)}
          onCustomize={(food) => handleOpenCustomizer(food)}
          onAddToDailyLog={handleAddToDailyLog}
        />
      )}

      {/* Login & Register Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto animate-fade-in">
          <div className="relative w-full max-w-md my-8">
            <button
              onClick={() => setShowLoginModal(false)}
              className="absolute -top-3 -right-3 z-10 w-8 h-8 rounded-full bg-black text-white flex items-center justify-center hover:bg-slate-800 transition-colors shadow-lg cursor-pointer"
              aria-label="Close"
            >
              <X className="w-4 h-4" />
            </button>
            <LoginPage
              onLoginSuccess={handleLoginSuccess}
              onCancel={() => setShowLoginModal(false)}
            />
          </div>
        </div>
      )}

      {/* Original Style Minimal Footer */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-slate-200 mt-auto py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-bold text-xs">
                K
              </div>
              <span className="font-bold text-slate-900">
                Campus Nutrition Analyzer
              </span>
              <span>— University Food Kcal</span>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => handleNavigate('home')}
                className="hover:text-black transition-colors cursor-pointer"
              >
                หน้าแรก
              </button>
              <button
                onClick={() => handleNavigate('restaurants')}
                className="hover:text-black transition-colors cursor-pointer"
              >
                ร้านอาหาร
              </button>
              <button
                onClick={() => handleNavigate('foods')}
                className="hover:text-black transition-colors cursor-pointer"
              >
                เมนูอาหาร
              </button>
              <button
                onClick={() => handleNavigate('customizer')}
                className="hover:text-black transition-colors cursor-pointer"
              >
                ปรับแต่งอาหาร
              </button>
              <button
                onClick={() => handleNavigate('dashboard')}
                className="hover:text-black transition-colors cursor-pointer"
              >
                บันทึกรายวัน
              </button>
              <button
                onClick={() => handleNavigate('admin')}
                className="hover:text-black transition-colors font-semibold text-slate-900 cursor-pointer"
              >
                จัดการข้อมูล (Admin)
              </button>
            </div>

            <div className="text-slate-400 text-center sm:text-right">
              ฐานข้อมูลโภชนาการอ้างอิงกรมอนามัย กระทรวงสาธารณสุข
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
