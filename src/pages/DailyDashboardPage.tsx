import React, { useState } from 'react';
import { MealLogItem, User, UserProfile } from '../types';
import { Flame, Plus, Trash2, Calendar, Award, Utensils, Coffee, Moon, Sun, ArrowRight, CheckCircle2 } from 'lucide-react';

interface DailyDashboardPageProps {
  user: User | null;
  profile: UserProfile | null;
  meals: MealLogItem[];
  onAddMeal: (meal: { name: string; calories: number; type: string; protein?: number; carbs?: number; fat?: number }) => void;
  onDeleteMeal: (mealId: string) => void;
  onNavigateToCustomizer: () => void;
  onNavigateToProfile: () => void;
  onNavigateToFoods: () => void;
}

export const DailyDashboardPage: React.FC<DailyDashboardPageProps> = ({
  user,
  profile,
  meals,
  onAddMeal,
  onDeleteMeal,
  onNavigateToCustomizer,
  onNavigateToProfile,
  onNavigateToFoods,
}) => {
  const [showAddForm, setShowAddForm] = useState<boolean>(false);
  const [foodName, setFoodName] = useState<string>('');
  const [calories, setCalories] = useState<string>('');
  const [mealType, setMealType] = useState<'breakfast' | 'lunch' | 'dinner' | 'snack'>('lunch');

  const calorieGoal = profile?.calories || profile?.tdee || 2000;
  const totalCalories = meals.reduce((sum, m) => sum + (m.calories || 0), 0);
  const remaining = calorieGoal - totalCalories;
  const percentConsumed = Math.min(100, Math.round((totalCalories / calorieGoal) * 100));

  const totalProtein = meals.reduce((sum, m) => sum + (m.protein || 0), 0);
  const totalCarbs = meals.reduce((sum, m) => sum + (m.carbs || 0), 0);
  const totalFat = meals.reduce((sum, m) => sum + (m.fat || 0), 0);

  // Targets
  const targetProtein = Math.round((calorieGoal * 0.25) / 4);
  const targetCarbs = Math.round((calorieGoal * 0.50) / 4);
  const targetFat = Math.round((calorieGoal * 0.25) / 9);

  // Current Thai Date
  const thaiDateString = new Date().toLocaleDateString('th-TH', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const handleQuickAdd = (e: React.FormEvent) => {
    e.preventDefault();
    if (!foodName.trim() || !calories) return;

    onAddMeal({
      name: foodName.trim(),
      calories: Number(calories),
      type: mealType,
      protein: Math.round(Number(calories) * 0.04),
      carbs: Math.round(Number(calories) * 0.12),
      fat: Math.round(Number(calories) * 0.03),
    });

    setFoodName('');
    setCalories('');
    setShowAddForm(false);
  };

  const getMealIcon = (type: string) => {
    switch (type) {
      case 'breakfast':
        return <Sun className="w-4 h-4 text-amber-500" />;
      case 'lunch':
        return <Utensils className="w-4 h-4 text-orange-500" />;
      case 'dinner':
        return <Moon className="w-4 h-4 text-indigo-500" />;
      default:
        return <Coffee className="w-4 h-4 text-emerald-500" />;
    }
  };

  const getMealLabel = (type: string) => {
    switch (type) {
      case 'breakfast':
        return 'มื้อเช้า';
      case 'lunch':
        return 'มื้อกลางวัน';
      case 'dinner':
        return 'มื้อเย็น';
      default:
        return 'ของว่าง/เครื่องดื่ม';
    }
  };

  // SVG Circular progress math
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentConsumed / 100) * circumference;

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Header with Date */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-xs font-semibold text-slate-700 mb-2">
            <Calendar className="w-3.5 h-3.5" />
            <span>{thaiDateString}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            ภาพรวมโภชนาการประจำวัน
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {user ? `สวัสดีคุณ ${user.name} — ติดตามแคลอรี่เป้าหมายและการรับประทานอาหารวันนี้` : 'ติดตามแคลอรี่และสารอาหารประจำวัน'}
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={onNavigateToCustomizer}
            className="px-4 py-2.5 rounded-full border border-slate-300 bg-white hover:bg-slate-100 text-xs font-semibold text-slate-800 flex items-center gap-1.5 transition-all cursor-pointer shadow-xs active:scale-95"
          >
            <span>ปรับแต่งเมนูเอง</span>
          </button>
          <button
            onClick={onNavigateToProfile}
            className="px-4 py-2.5 rounded-full bg-slate-900 hover:bg-black text-white text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer shadow-xs active:scale-95"
          >
            <span>ตั้งเป้าหมาย BMR/TDEE</span>
          </button>
        </div>
      </div>

      {/* Top Stats Cards: Circular Progress & Macros */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        {/* Circular Progress Ring Card */}
        <div className="lg:col-span-6 liquid-card p-6 sm:p-8 border border-white/60 shadow-lg flex flex-col items-center justify-center text-center">
          <div className="relative w-44 h-44 flex items-center justify-center my-2">
            <svg className="w-full h-full transform -rotate-90">
              {/* Background track */}
              <circle
                cx="88"
                cy="88"
                r={radius}
                stroke="#e2e8f0"
                strokeWidth="12"
                fill="transparent"
              />
              {/* Progress track */}
              <circle
                cx="88"
                cy="88"
                r={radius}
                stroke={remaining < 0 ? '#ef4444' : '#000000'}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                className="progress-ring__circle"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span className="text-3xl sm:text-4xl font-black text-slate-900 leading-none">
                {totalCalories}
              </span>
              <span className="text-xs font-semibold text-slate-400 mt-1">/ {calorieGoal} kcal</span>
              <span className="text-[11px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full mt-2">
                {percentConsumed}% ของเป้าหมาย
              </span>
            </div>
          </div>

          <div className="w-full grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-slate-100">
            <div>
              <div className="text-[11px] text-slate-400 font-medium">บริโภคแล้ว</div>
              <div className="text-lg font-bold text-slate-900">{totalCalories} kcal</div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">
                {remaining >= 0 ? 'คงเหลือสำหรับวันนี้' : 'เกินเป้าหมาย'}
              </div>
              <div className={`text-lg font-bold ${remaining >= 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                {Math.abs(remaining)} kcal
              </div>
            </div>
          </div>
        </div>

        {/* Macronutrient Distribution */}
        <div className="lg:col-span-6 liquid-card p-6 sm:p-8 border border-white/60 shadow-lg flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900">
                สารอาหารหลัก (Macronutrients)
              </h3>
              <span className="text-xs text-slate-400">เป้าหมายประจำวัน</span>
            </div>

            <div className="space-y-5">
              {/* Protein */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1.5">
                  <span className="text-slate-700">โปรตีน (Protein)</span>
                  <span className="text-slate-900 font-bold">{totalProtein} / {targetProtein} g</span>
                </div>
                <div className="h-2.5 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full transition-all"
                    style={{ width: `${Math.min(100, Math.round((totalProtein / targetProtein) * 100))}%` }}
                  ></div>
                </div>
              </div>

              {/* Carbs */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1.5">
                  <span className="text-slate-700">คาร์โบไฮเดรต (Carbohydrates)</span>
                  <span className="text-slate-900 font-bold">{totalCarbs} / {targetCarbs} g</span>
                </div>
                <div className="h-2.5 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full transition-all"
                    style={{ width: `${Math.min(100, Math.round((totalCarbs / targetCarbs) * 100))}%` }}
                  ></div>
                </div>
              </div>

              {/* Fat */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1.5">
                  <span className="text-slate-700">ไขมัน (Fats)</span>
                  <span className="text-slate-900 font-bold">{totalFat} / {targetFat} g</span>
                </div>
                <div className="h-2.5 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-amber-500 rounded-full transition-all"
                    style={{ width: `${Math.min(100, Math.round((totalFat / targetFat) * 100))}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>คำนวณตามสัดส่วนโภชนาการ 50-25-25</span>
            <button
              type="button"
              onClick={onNavigateToFoods}
              className="text-black font-bold hover:underline flex items-center gap-1 cursor-pointer"
            >
              <span>ค้นหาเมนูในมหาวิทยาลัย</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Meals Log Section */}
      <div className="liquid-card p-6 sm:p-8 border border-white/60 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-2">
            <Utensils className="w-5 h-5 text-black" />
            <h2 className="text-lg font-bold text-slate-900">
              รายการอาหารวันนี้ ({meals.length} รายการ)
            </h2>
          </div>

          <button
            type="button"
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2.5 rounded-full bg-slate-900 hover:bg-black text-white text-xs font-semibold flex items-center gap-2 transition-all cursor-pointer shadow-xs active:scale-95"
          >
            <Plus className="w-4 h-4" />
            <span>{showAddForm ? 'ปิดแบบฟอร์ม' : 'เพิ่มรายการอาหาร'}</span>
          </button>
        </div>

        {/* Quick Add Form Drawer */}
        {showAddForm && (
          <form onSubmit={handleQuickAdd} className="mb-6 p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-xs">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
              บันทึกอาหารด่วน (Quick Log)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
              <div className="sm:col-span-5">
                <label className="block text-xs font-medium text-slate-600 mb-1">ชื่ออาหารหรือเครื่องดื่ม</label>
                <input
                  type="text"
                  required
                  value={foodName}
                  onChange={(e) => setFoodName(e.target.value)}
                  placeholder="เช่น ข้าวกะเพราหมูสับ, กาแฟดำ"
                  className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
                />
              </div>

              <div className="sm:col-span-3">
                <label className="block text-xs font-medium text-slate-600 mb-1">แคลอรี่ (kcal)</label>
                <input
                  type="number"
                  required
                  min="0"
                  max="4000"
                  value={calories}
                  onChange={(e) => setCalories(e.target.value)}
                  placeholder="เช่น 450"
                  className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
                />
              </div>

              <div className="sm:col-span-4">
                <label className="block text-xs font-medium text-slate-600 mb-1">มื้ออาหาร</label>
                <select
                  value={mealType}
                  onChange={(e: any) => setMealType(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black"
                >
                  <option value="breakfast">มื้อเช้า</option>
                  <option value="lunch">มื้อกลางวัน</option>
                  <option value="dinner">มื้อเย็น</option>
                  <option value="snack">ของว่าง / เครื่องดื่ม</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-2.5 mt-4">
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="px-4 py-2 rounded-xl border border-slate-300 bg-white text-xs font-semibold text-slate-700 hover:bg-slate-100 cursor-pointer transition-all"
              >
                ยกเลิก
              </button>
              <button
                type="submit"
                className="px-5 py-2 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-semibold cursor-pointer shadow-xs active:scale-95 transition-all"
              >
                บันทึกอาหาร
              </button>
            </div>
          </form>
        )}

        {/* Meal List */}
        {meals.length === 0 ? (
          <div className="text-center py-12 border-2 border-dashed border-slate-200 rounded-2xl bg-white">
            <Utensils className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <div className="text-sm font-bold text-slate-700">ยังไม่มีรายการอาหารที่บันทึกสำหรับวันนี้</div>
            <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
              คุณสามารถเลือกเพิ่มรายการอาหารจากหน้าค้นหาร้านอาหาร หรือใช้ปุ่มเพิ่มรายการอาหารด้านบน
            </p>
            <div className="mt-4 flex justify-center gap-3">
              <button
                type="button"
                onClick={onNavigateToFoods}
                className="px-5 py-2.5 rounded-full bg-slate-900 hover:bg-black text-white text-xs font-semibold shadow-xs active:scale-95 transition-all cursor-pointer"
              >
                ดูเมนูอาหารในมหาวิทยาลัย
              </button>
            </div>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {meals.map((meal) => (
              <div
                key={meal.id}
                className="py-4 flex items-center justify-between gap-4 hover:bg-slate-50/70 px-3 rounded-xl transition-colors"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center shrink-0">
                    {getMealIcon(meal.type)}
                  </div>
                  <div className="min-w-0">
                    <div className="text-sm font-bold text-slate-900 truncate">{meal.name}</div>
                    <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                      <span className="font-medium text-slate-600">{getMealLabel(meal.type)}</span>
                      <span>•</span>
                      <span>{meal.timestamp}</span>
                      {(meal.protein || meal.carbs || meal.fat) ? (
                        <>
                          <span>•</span>
                          <span>P:{meal.protein || 0}g C:{meal.carbs || 0}g F:{meal.fat || 0}g</span>
                        </>
                      ) : null}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <div className="text-sm font-extrabold text-slate-900 bg-slate-100 px-3 py-1 rounded-full">
                    {meal.calories} <span className="text-[10px] font-medium text-slate-500">kcal</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => onDeleteMeal(meal.id)}
                    className="p-1.5 text-slate-300 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors cursor-pointer"
                    title="ลบรายการนี้"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
