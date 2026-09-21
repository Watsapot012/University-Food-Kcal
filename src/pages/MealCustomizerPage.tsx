import React, { useState, useMemo } from 'react';
import { Food, ModifierOption } from '../types';
import { Sliders, Plus, Minus, Check, Flame, Sparkles, ArrowRight } from 'lucide-react';

interface MealCustomizerPageProps {
  foods: Food[];
  initialFoodId?: number;
  onAddToDailyLog: (logItem: { name: string; calories: number; type: string; protein: number; carbs: number; fat: number }) => void;
  onNavigateToDashboard: () => void;
}

const MODIFIER_OPTIONS: ModifierOption[] = [
  // Add-ons
  { id: 'fried_egg', name: 'ไข่ดาว (Fried Egg)', category: 'add-on', kcal: 90, carbs: 1, pro: 6, fat: 7 },
  { id: 'extra_meat', name: 'เพิ่มเนื้อสัตว์ (Extra Meat)', category: 'add-on', kcal: 120, carbs: 0, pro: 18, fat: 5 },
  { id: 'cheese', name: 'ชีสแผ่น (Cheese Slice)', category: 'add-on', kcal: 105, carbs: 1, pro: 7, fat: 9 },
  { id: 'sausage', name: 'กุนเชียงทอด (Chinese Sausage)', category: 'add-on', kcal: 140, carbs: 8, pro: 5, fat: 11 },
  // Adjustments
  { id: 'half_rice', name: 'ข้าวครึ่งเดียว (Half Rice)', category: 'adjustment', kcal: -100, carbs: -25, pro: -2, fat: 0 },
  { id: 'less_oil', name: 'ลดน้ำมัน / ผัดน้ำ (Less Oil)', category: 'adjustment', kcal: -50, carbs: 0, pro: 0, fat: -6 },
  { id: 'extra_sauce', name: 'เพิ่มน้ำซอส (Extra Sauce)', category: 'adjustment', kcal: 20, carbs: 4, pro: 0, fat: 0 },
  { id: 'no_skin', name: 'ไม่ใส่หนัง (No Skin)', category: 'adjustment', kcal: -40, carbs: 0, pro: 0, fat: -4.5 },
];

export const MealCustomizerPage: React.FC<MealCustomizerPageProps> = ({
  foods,
  initialFoodId,
  onAddToDailyLog,
  onNavigateToDashboard,
}) => {
  const [selectedFoodId, setSelectedFoodId] = useState<number>(initialFoodId || (foods[0]?.id ?? 1));
  const [selectedModifiers, setSelectedModifiers] = useState<Record<string, boolean>>({});
  const [mealType, setMealType] = useState<string>('lunch');
  const [logSuccess, setLogSuccess] = useState<boolean>(false);

  const baseFood = useMemo(() => {
    return foods.find((f) => f.id === selectedFoodId) || foods[0] || {
      id: 1,
      name: 'ข้าวกะเพราไก่',
      restaurant_id: 1,
      price: 50,
      kcal: 550,
      carbohydrate: 65,
      protein: 25,
      fat: 20,
      image: 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=800&q=80',
      description: 'เมนูยอดนิยมประจำมหาวิทยาลัย',
    };
  }, [foods, selectedFoodId]);

  const toggleModifier = (id: string) => {
    setSelectedModifiers((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // Calculate customized totals
  const customizedTotals = useMemo(() => {
    let totalKcal = baseFood.kcal;
    let totalCarbs = baseFood.carbohydrate;
    let totalPro = baseFood.protein;
    let totalFat = baseFood.fat;

    MODIFIER_OPTIONS.forEach((mod) => {
      if (selectedModifiers[mod.id]) {
        totalKcal += mod.kcal;
        totalCarbs += mod.carbs;
        totalPro += mod.pro;
        totalFat += mod.fat;
      }
    });

    return {
      kcal: Math.max(0, totalKcal),
      carbs: Math.max(0, totalCarbs),
      pro: Math.max(0, totalPro),
      fat: Math.max(0, totalFat),
    };
  }, [baseFood, selectedModifiers]);

  const activeModifiersList = useMemo(() => {
    return MODIFIER_OPTIONS.filter((mod) => selectedModifiers[mod.id]);
  }, [selectedModifiers]);

  const handleSaveToLog = () => {
    const modifierText = activeModifiersList.length > 0
      ? ` (${activeModifiersList.map((m) => m.name.split(' (')[0]).join(', ')})`
      : '';
    const customMealName = `${baseFood.name}${modifierText}`;

    onAddToDailyLog({
      name: customMealName,
      calories: customizedTotals.kcal,
      type: mealType,
      protein: customizedTotals.pro,
      carbs: customizedTotals.carbs,
      fat: customizedTotals.fat,
    });

    setLogSuccess(true);
    setTimeout(() => setLogSuccess(false), 2500);
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-xs font-semibold text-slate-700 mb-2">
            <Sliders className="w-3.5 h-3.5" />
            <span>Interactive Meal Customizer</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            ปรับแต่งเมนู & โภชนาการแบบเรียลไทม์
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            ปรับเปลี่ยนส่วนผสม เช่น เพิ่มไข่ดาว ลดข้าว ลดน้ำมัน เพื่อดูการเปลี่ยนแปลงของ Kcal และสารอาหารทันที
          </p>
        </div>

        {/* Dish Selector Dropdown */}
        <div className="w-full sm:w-72">
          <label className="block text-xs font-semibold text-slate-700 mb-1">เลือกเมนูหลัก</label>
          <select
            value={selectedFoodId}
            onChange={(e) => {
              setSelectedFoodId(Number(e.target.value));
              setSelectedModifiers({});
            }}
            className="w-full bg-white border border-slate-300 rounded-xl px-4 py-2.5 text-xs font-medium text-slate-800 shadow-xs focus:outline-none focus:border-black cursor-pointer"
          >
            {foods.map((food) => (
              <option key={food.id} value={food.id}>
                {food.name} ({food.kcal} kcal)
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Base Meal & Modifiers */}
        <div className="lg:col-span-7 space-y-6">
          {/* Base Meal Card */}
          <div className="liquid-card p-6 border border-white/60 shadow-lg">
            <div className="flex items-center gap-4">
              <img
                src={baseFood.image}
                alt={baseFood.name}
                className="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-cover shadow-md shrink-0 border border-slate-100"
              />
              <div className="flex-1 min-w-0">
                <span className="text-xs font-semibold text-orange-600 bg-orange-50 px-2.5 py-0.5 rounded-md inline-block mb-1">
                  เมนูหลัก (Base Dish)
                </span>
                <h2 className="text-lg sm:text-xl font-bold text-slate-900 truncate">{baseFood.name}</h2>
                <p className="text-xs text-slate-500 line-clamp-1 mt-0.5">{baseFood.description}</p>
                <div className="text-sm font-semibold text-slate-800 mt-1.5">
                  ราคาปกติ {baseFood.price} บาท
                </div>
              </div>
            </div>

            {/* Baseline Nutrition Bar */}
            <div className="mt-5 pt-4 border-t border-slate-100 grid grid-cols-4 gap-2 text-center">
              <div className="bg-slate-50 rounded-xl p-2">
                <div className="text-[11px] text-slate-500 font-medium">พลังงาน</div>
                <div className="text-sm font-extrabold text-slate-900">{baseFood.kcal}</div>
                <div className="text-[10px] text-slate-400">kcal</div>
              </div>
              <div className="bg-slate-50 rounded-xl p-2">
                <div className="text-[11px] text-slate-500 font-medium">คาร์บ</div>
                <div className="text-sm font-extrabold text-slate-900">{baseFood.carbohydrate}g</div>
                <div className="text-[10px] text-slate-400">carbs</div>
              </div>
              <div className="bg-slate-50 rounded-xl p-2">
                <div className="text-[11px] text-slate-500 font-medium">โปรตีน</div>
                <div className="text-sm font-extrabold text-slate-900">{baseFood.protein}g</div>
                <div className="text-[10px] text-slate-400">protein</div>
              </div>
              <div className="bg-slate-50 rounded-xl p-2">
                <div className="text-[11px] text-slate-500 font-medium">ไขมัน</div>
                <div className="text-sm font-extrabold text-slate-900">{baseFood.fat}g</div>
                <div className="text-[10px] text-slate-400">fat</div>
              </div>
            </div>
          </div>

          {/* Modifiers Selection: Add-ons & Adjustments */}
          <div className="liquid-card p-6 border border-white/60 shadow-lg">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Plus className="w-4 h-4 text-emerald-600" />
              <span>ตัวเลือกเสริม & การปรับแต่ง (Modifiers)</span>
            </h3>

            {/* Add-ons */}
            <div className="mb-6">
              <h4 className="text-xs font-semibold text-slate-500 mb-3">ท็อปปิ้งและเครื่องเคียง (Add-ons)</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {MODIFIER_OPTIONS.filter((m) => m.category === 'add-on').map((mod) => {
                  const isChecked = Boolean(selectedModifiers[mod.id]);
                  return (
                    <div
                      key={mod.id}
                      onClick={() => toggleModifier(mod.id)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        isChecked
                          ? 'border-black bg-slate-900 text-white shadow-sm'
                          : 'border-slate-200 bg-white hover:border-slate-300 text-slate-800'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {}}
                          className="modifier-checkbox"
                        />
                        <div>
                          <div className="text-xs font-bold leading-tight">{mod.name}</div>
                          <div className={`text-[10px] mt-0.5 ${isChecked ? 'text-slate-300' : 'text-slate-500'}`}>
                            +{mod.pro}g โปรตีน / +{mod.fat}g ไขมัน
                          </div>
                        </div>
                      </div>
                      <div className={`text-xs font-bold shrink-0 ${isChecked ? 'text-amber-300' : 'text-orange-600'}`}>
                        +{mod.kcal} kcal
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Adjustments */}
            <div>
              <h4 className="text-xs font-semibold text-slate-500 mb-3">การปรับสูตร (Adjustments)</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {MODIFIER_OPTIONS.filter((m) => m.category === 'adjustment').map((mod) => {
                  const isChecked = Boolean(selectedModifiers[mod.id]);
                  return (
                    <div
                      key={mod.id}
                      onClick={() => toggleModifier(mod.id)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        isChecked
                          ? 'border-black bg-slate-900 text-white shadow-sm'
                          : 'border-slate-200 bg-white hover:border-slate-300 text-slate-800'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {}}
                          className="modifier-checkbox"
                        />
                        <div>
                          <div className="text-xs font-bold leading-tight">{mod.name}</div>
                          <div className={`text-[10px] mt-0.5 ${isChecked ? 'text-slate-300' : 'text-slate-500'}`}>
                            {mod.carbs !== 0 ? `${mod.carbs > 0 ? '+' : ''}${mod.carbs}g คาร์บ` : ''}{' '}
                            {mod.fat !== 0 ? `${mod.fat > 0 ? '+' : ''}${mod.fat}g ไขมัน` : ''}
                          </div>
                        </div>
                      </div>
                      <div
                        className={`text-xs font-bold shrink-0 ${
                          isChecked
                            ? mod.kcal < 0
                              ? 'text-emerald-300'
                              : 'text-amber-300'
                            : mod.kcal < 0
                            ? 'text-emerald-600'
                            : 'text-orange-600'
                        }`}
                      >
                        {mod.kcal > 0 ? `+${mod.kcal}` : mod.kcal} kcal
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Real-time Total Impact */}
        <div className="lg:col-span-5 space-y-6">
          <div className="liquid-card p-6 sm:p-8 border border-white/60 shadow-xl sticky top-24">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Real-time Total Impact
              </span>
              <button
                type="button"
                onClick={() => setSelectedModifiers({})}
                className="text-[11px] text-slate-400 hover:text-slate-700 underline cursor-pointer"
              >
                ล้างการปรับแต่ง
              </button>
            </div>

            {/* Total Kcal Big Display */}
            <div className="text-center py-6 bg-radial from-slate-50 to-white rounded-2xl border border-slate-100 mb-6">
              <div className="text-xs text-slate-500 font-medium mb-1">แคลอรี่รวมหลังปรับแต่ง</div>
              <div className="flex items-baseline justify-center gap-2">
                <span className="text-5xl sm:text-6xl font-black text-slate-900 tracking-tight transition-all">
                  {customizedTotals.kcal}
                </span>
                <span className="text-sm font-bold text-slate-500">kcal</span>
              </div>
              <div className="text-xs font-semibold mt-2">
                {customizedTotals.kcal > baseFood.kcal && (
                  <span className="text-orange-600">
                    +{customizedTotals.kcal - baseFood.kcal} kcal จากสูตรปกติ
                  </span>
                )}
                {customizedTotals.kcal < baseFood.kcal && (
                  <span className="text-emerald-600">
                    ลดลง {baseFood.kcal - customizedTotals.kcal} kcal จากสูตรปกติ
                  </span>
                )}
                {customizedTotals.kcal === baseFood.kcal && (
                  <span className="text-slate-400">เท่ากับสูตรมาตรฐาน</span>
                )}
              </div>
            </div>

            {/* Macro Breakdown Bars */}
            <div className="space-y-4 mb-6">
              {/* Carbs */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1 text-slate-700">
                  <span>คาร์โบไฮเดรต (Carbs)</span>
                  <span>{customizedTotals.carbs} g</span>
                </div>
                <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-blue-500 transition-all duration-300"
                    style={{ width: `${Math.min(100, (customizedTotals.carbs / 100) * 100)}%` }}
                  ></div>
                </div>
              </div>

              {/* Protein */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1 text-slate-700">
                  <span>โปรตีน (Protein)</span>
                  <span>{customizedTotals.pro} g</span>
                </div>
                <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 transition-all duration-300"
                    style={{ width: `${Math.min(100, (customizedTotals.pro / 80) * 100)}%` }}
                  ></div>
                </div>
              </div>

              {/* Fat */}
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1 text-slate-700">
                  <span>ไขมัน (Fat)</span>
                  <span>{customizedTotals.fat} g</span>
                </div>
                <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-amber-500 transition-all duration-300"
                    style={{ width: `${Math.min(100, (customizedTotals.fat / 60) * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Meal Type Selection for logging */}
            <div className="mb-5">
              <label className="block text-xs font-semibold text-slate-700 mb-2">มื้ออาหารที่จะบันทึก</label>
              <div className="grid grid-cols-4 gap-1.5">
                {[
                  { id: 'breakfast', label: 'เช้า' },
                  { id: 'lunch', label: 'กลางวัน' },
                  { id: 'dinner', label: 'เย็น' },
                  { id: 'snack', label: 'ของว่าง' },
                ].map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setMealType(item.id)}
                    className={`py-2 text-xs font-semibold rounded-xl border transition-all cursor-pointer ${
                      mealType === item.id
                        ? 'border-black bg-black text-white shadow-xs'
                        : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-400'
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                type="button"
                onClick={handleSaveToLog}
                className="w-full py-3.5 px-6 rounded-full bg-slate-900 hover:bg-black active:scale-95 text-white text-sm font-semibold flex items-center justify-center gap-2 shadow-md transition-all cursor-pointer"
              >
                <Sparkles className="w-4 h-4 text-amber-300" />
                <span>บันทึกเมนูนี้ลงไดอารี่ประจำวัน</span>
              </button>
            </div>

            {logSuccess && (
              <div className="mt-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center justify-between">
                <span>บันทึกเมนูที่ปรับแต่งสำเร็จแล้ว!</span>
                <button
                  type="button"
                  onClick={onNavigateToDashboard}
                  className="font-bold underline flex items-center gap-1 cursor-pointer"
                >
                  <span>ดูบันทึก</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
