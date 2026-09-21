import React from 'react';
import { X, Flame, Store, Plus, Minus, Check, MapPin, Clock, Sliders, CalendarCheck } from 'lucide-react';
import { Food, Restaurant } from '../types';

interface FoodDetailModalProps {
  food: Food | null;
  restaurant?: Restaurant | null;
  onClose: () => void;
  onCustomize?: (food: Food) => void;
  onAddToDailyLog?: (meal: { name: string; calories: number; type: string; protein?: number; carbs?: number; fat?: number }) => void;
}

export const FoodDetailModal: React.FC<FoodDetailModalProps> = ({
  food,
  restaurant,
  onClose,
  onCustomize,
  onAddToDailyLog,
}) => {
  const [quantity, setQuantity] = React.useState<number>(1);
  const [justLogged, setJustLogged] = React.useState<boolean>(false);

  if (!food) return null;

  // Calculate calories contribution from macros
  const proteinKcal = food.protein * 4;
  const carbKcal = food.carbohydrate * 4;
  const fatKcal = food.fat * 9;
  const totalMacroKcal = proteinKcal + carbKcal + fatKcal || 1;

  const proteinPct = Math.round((proteinKcal / totalMacroKcal) * 100);
  const carbPct = Math.round((carbKcal / totalMacroKcal) * 100);
  const fatPct = Math.max(0, 100 - proteinPct - carbPct);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto animate-fade-in">
      <div
        className="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-200 my-8"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 w-9 h-9 bg-white/95 hover:bg-white text-slate-800 hover:text-black rounded-full shadow-lg flex items-center justify-center transition-all cursor-pointer border border-slate-200"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Hero Image */}
        <div className="relative h-64 sm:h-72 w-full bg-slate-100">
          <img
            src={food.image}
            alt={food.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="bg-orange-500 text-white text-xs font-semibold px-2.5 py-1 rounded-md flex items-center gap-1">
                <Flame className="w-3.5 h-3.5" />
                {food.kcal} Kcal
              </span>
              {food.category && (
                <span className="bg-white/20 backdrop-blur-xs text-white text-xs px-2.5 py-1 rounded-md">
                  {food.category}
                </span>
              )}
              {food.is_popular && (
                <span className="bg-amber-400 text-slate-900 text-xs font-bold px-2.5 py-1 rounded-md">
                  ⭐ เมนูยอดนิยม
                </span>
              )}
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              {food.name}
            </h2>
            <div className="flex items-center gap-2 text-sm text-slate-200 mt-1">
              <Store className="w-4 h-4 text-orange-400" />
              <span>{food.restaurant_name || restaurant?.name || 'ร้านค้าในมหาวิทยาลัย'}</span>
              <span>•</span>
              <span className="text-orange-400 font-bold text-base">฿{food.price}</span>
            </div>
          </div>
        </div>

        {/* Modal Content */}
        <div className="p-6 space-y-6">
          {/* Restaurant Location and Hours if available */}
          {restaurant && (
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-600 flex flex-wrap gap-4">
              <div className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-orange-500 shrink-0" />
                <span>{restaurant.location}</span>
              </div>
              {restaurant.open_hours && (
                <div className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-slate-400 shrink-0" />
                  <span>เวลาเปิด-ปิด: {restaurant.open_hours}</span>
                </div>
              )}
            </div>
          )}

          {/* Description */}
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
              รายละเอียดอาหาร
            </h4>
            <p className="text-sm text-slate-700 leading-relaxed">
              {food.description || 'ไม่มีรายละเอียดเพิ่มเติมสำหรับเมนูนี้'}
            </p>
          </div>

          {/* Nutrition Detailed Cards */}
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              ข้อมูลโภชนาการต่อ 1 จาน / หน่วยบริโภค
            </h4>

            {/* Macro Cards Grid */}
            <div className="grid grid-cols-4 gap-3">
              <div className="bg-orange-50 border border-orange-100 rounded-xl p-3 text-center">
                <span className="block text-xs text-orange-600 font-medium">พลังงาน</span>
                <span className="text-xl font-bold text-orange-700">{food.kcal}</span>
                <span className="block text-[10px] text-orange-500">Kcal</span>
              </div>

              <div className="bg-blue-50 border border-blue-100 rounded-xl p-3 text-center">
                <span className="block text-xs text-blue-600 font-medium">โปรตีน</span>
                <span className="text-xl font-bold text-blue-700">{food.protein}</span>
                <span className="block text-[10px] text-blue-500">กรัม (g)</span>
              </div>

              <div className="bg-amber-50 border border-amber-100 rounded-xl p-3 text-center">
                <span className="block text-xs text-amber-600 font-medium">คาร์โบไฮเดรต</span>
                <span className="text-xl font-bold text-amber-700">{food.carbohydrate}</span>
                <span className="block text-[10px] text-amber-500">กรัม (g)</span>
              </div>

              <div className="bg-rose-50 border border-rose-100 rounded-xl p-3 text-center">
                <span className="block text-xs text-rose-600 font-medium">ไขมัน</span>
                <span className="text-xl font-bold text-rose-700">{food.fat}</span>
                <span className="block text-[10px] text-rose-500">กรัม (g)</span>
              </div>
            </div>

            {/* Macronutrient Distribution Bar */}
            <div className="mt-4">
              <div className="flex justify-between text-xs text-slate-500 mb-1 font-medium">
                <span>สัดส่วนพลังงานสารอาหารหลัก (Macronutrients)</span>
                <span>โปรตีน {proteinPct}% / คาร์บ {carbPct}% / ไขมัน {fatPct}%</span>
              </div>
              <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden flex">
                <div
                  style={{ width: `${proteinPct}%` }}
                  className="bg-blue-500 h-full"
                  title={`โปรตีน ${proteinPct}%`}
                />
                <div
                  style={{ width: `${carbPct}%` }}
                  className="bg-amber-500 h-full"
                  title={`คาร์โบไฮเดรต ${carbPct}%`}
                />
                <div
                  style={{ width: `${fatPct}%` }}
                  className="bg-rose-500 h-full"
                  title={`ไขมัน ${fatPct}%`}
                />
              </div>
            </div>
          </div>

          {/* Action Row: Quantity + Add Button + Customize */}
          <div className="pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
            {/* Quantity Selector */}
            <div className="flex items-center justify-between sm:justify-start gap-3">
              <div className="flex items-center border border-slate-300 rounded-xl p-1 bg-white shadow-xs">
                <button
                  type="button"
                  onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                  className="w-9 h-9 rounded-lg bg-slate-100 hover:bg-slate-200 active:scale-90 text-slate-800 font-extrabold flex items-center justify-center transition-all cursor-pointer"
                  title="ลดจำนวน"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="w-10 text-center font-bold text-sm text-slate-900">
                  {quantity}
                </span>
                <button
                  type="button"
                  onClick={() => setQuantity((q) => q + 1)}
                  className="w-9 h-9 rounded-lg bg-slate-100 hover:bg-slate-200 active:scale-90 text-slate-800 font-extrabold flex items-center justify-center transition-all cursor-pointer"
                  title="เพิ่มจำนวน"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>

              {/* Total calculation for selected quantity */}
              <div className="text-right sm:text-left">
                <span className="text-[11px] text-slate-500 font-medium block">
                  รวม ({quantity} จาน)
                </span>
                <span className="text-base font-extrabold text-slate-900">
                  {food.kcal * quantity} Kcal
                </span>
              </div>
            </div>

            {/* Buttons Group */}
            <div className="flex items-center gap-2.5">
              {onCustomize && (
                <button
                  type="button"
                  onClick={() => {
                    onCustomize(food);
                    onClose();
                  }}
                  className="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-slate-300 bg-white hover:bg-slate-100 text-slate-800 text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer shadow-xs active:scale-95"
                  title="ปรับแต่งส่วนผสม ท็อปปิ้ง และลด/เพิ่มแคลอรี่"
                >
                  <Sliders className="w-4 h-4 text-slate-600" />
                  <span>ปรับแต่งเมนู</span>
                </button>
              )}

              {onAddToDailyLog && (
                <button
                  id="modal-add-to-daily-log"
                  type="button"
                  onClick={() => {
                    onAddToDailyLog({
                      name: food.name,
                      calories: food.kcal * quantity,
                      type: 'lunch',
                      protein: food.protein * quantity,
                      carbs: food.carbohydrate * quantity,
                      fat: food.fat * quantity,
                    });
                    setJustLogged(true);
                    setTimeout(() => setJustLogged(false), 2000);
                  }}
                  className={`flex-1 sm:flex-initial px-5 py-2.5 rounded-xl font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all cursor-pointer shadow-sm active:scale-95 ${
                    justLogged
                      ? 'bg-emerald-600 text-white'
                      : 'bg-black hover:bg-slate-800 text-white'
                  }`}
                >
                  {justLogged ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>บันทึกแล้ว!</span>
                    </>
                  ) : (
                    <>
                      <CalendarCheck className="w-4 h-4" />
                      <span>บันทึกลงไดอารี่</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
