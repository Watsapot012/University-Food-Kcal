import React, { useState } from 'react';
import { Search, Flame, Store, ArrowRight, Sparkles, CheckCircle2, TrendingUp, Activity } from 'lucide-react';
import { Food, Restaurant } from '../types';
import { FoodCard } from '../components/FoodCard';

interface HomePageProps {
  restaurants: Restaurant[];
  foods: Food[];
  onSelectFood: (food: Food) => void;
  onNavigate: (tab: string, query?: string) => void;
  onSelectRestaurant: (restaurant: Restaurant) => void;
}

export const HomePage: React.FC<HomePageProps> = ({
  restaurants,
  foods,
  onSelectFood,
  onNavigate,
  onSelectRestaurant,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onNavigate('foods', searchTerm.trim());
    }
  };

  // Popular or featured foods
  const popularFoods = foods.filter((f) => f.is_popular).slice(0, 6);
  const displayFoods = popularFoods.length > 0 ? popularFoods : foods.slice(0, 6);

  // Quick categories
  const categories = [
    { label: 'อาหารจานเดียว', query: 'อาหารจานเดียว' },
    { label: 'ก๋วยเตี๋ยว', query: 'ก๋วยเตี๋ยว' },
    { label: 'อาหารเพื่อสุขภาพ', query: 'เพื่อสุขภาพ' },
    { label: 'เครื่องดื่ม', query: 'เครื่องดื่ม' },
  ];

  return (
    <div className="space-y-12 pb-16">
      {/* Original UI Hero Section */}
      <section className="relative rounded-3xl liquid-card border border-white/70 shadow-xl p-8 sm:p-14 overflow-hidden text-center">
        {/* Ambient floating blobs */}
        <div className="ambient-blob w-72 h-72 -top-10 -left-10 bg-orange-100 opacity-60"></div>
        <div className="ambient-blob w-80 h-80 -bottom-10 -right-10 bg-amber-100 opacity-50"></div>

        <div className="relative max-w-3xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 bg-black text-white px-4 py-1.5 rounded-full text-xs font-semibold shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>Campus Nutrition Analyzer — University Food Kcal</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-slate-900 leading-[1.15]">
            วิเคราะห์โภชนาการอาหาร <br className="hidden sm:inline" />
            <span className="text-slate-900">
              ในมหาวิทยาลัย
            </span>
          </h1>

          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            ค้นหาข้อมูลโภชนาการจากร้านอาหารในมหาวิทยาลัยของคุณได้อย่างง่ายดาย วางแผนมื้ออาหารเพื่อสุขภาพที่ดีกว่า
            คำนวณ Kcal คาร์โบไฮเดรต โปรตีน และไขมัน ท่ามกลางชีวิตในรั้วมหาวิทยาลัย
          </p>

          {/* Action CTA Buttons */}
          <div className="flex flex-wrap justify-center items-center gap-3.5 pt-2">
            <button
              onClick={() => onNavigate('restaurants')}
              className="px-6 py-3.5 rounded-full bg-slate-900 hover:bg-black text-white text-xs sm:text-sm font-semibold flex items-center gap-2 active:scale-95 transition-all shadow-md cursor-pointer"
            >
              <span>เริ่มดูโภชนาการอาหาร</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate('customizer')}
              className="px-6 py-3.5 rounded-full border border-slate-300 bg-white hover:bg-slate-100 text-slate-800 text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all cursor-pointer shadow-xs active:scale-95"
            >
              <span>ปรับแต่งเมนู (Customizer)</span>
            </button>
            <button
              onClick={() => onNavigate('dashboard')}
              className="px-6 py-3.5 rounded-full border border-slate-300 bg-white hover:bg-slate-100 text-slate-800 text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all cursor-pointer shadow-xs active:scale-95"
            >
              <span>บันทึกแคลอรี่วันนี้</span>
            </button>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearchSubmit} className="max-w-xl mx-auto relative flex items-center pt-3">
            <div className="relative w-full">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                id="home-search-input"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="ค้นหาชื่ออาหาร เช่น ข้าวกะเพราไก่, สลัด, หรือชื่อร้าน..."
                className="w-full pl-11 pr-24 py-3 bg-white text-slate-900 rounded-full shadow-sm border border-slate-300 focus:outline-none focus:border-black focus:ring-1 focus:ring-black text-xs sm:text-sm placeholder-slate-400"
              />
              <button
                type="submit"
                className="absolute right-1.5 top-1/2 -translate-y-1/2 bg-slate-900 hover:bg-black active:scale-95 text-white font-semibold px-5 py-2 rounded-full text-xs transition-all shadow-xs cursor-pointer"
              >
                ค้นหา
              </button>
            </div>
          </form>

          {/* Quick Category Chips */}
          <div className="flex flex-wrap justify-center items-center gap-2 pt-1">
            <span className="text-xs text-slate-500 font-medium">หมวดหมู่ยอดฮิต:</span>
            {categories.map((cat) => (
              <button
                key={cat.label}
                onClick={() => onNavigate('foods', cat.query)}
                className="text-xs bg-white border border-slate-300 hover:border-slate-900 hover:bg-slate-900 hover:text-white text-slate-700 font-medium px-3.5 py-1.5 rounded-full shadow-xs transition-all cursor-pointer"
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Feature badges */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-10 pt-6 border-t border-slate-200/60 text-slate-600 text-xs">
          <div className="flex items-center gap-2.5 justify-center sm:justify-start">
            <CheckCircle2 className="w-4 h-4 text-black shrink-0" />
            <span>ข้อมูลแคลอรี่ตรงตามสัดส่วนอาหารจริง</span>
          </div>
          <div className="flex items-center gap-2.5 justify-center sm:justify-start">
            <TrendingUp className="w-4 h-4 text-black shrink-0" />
            <span>คำนวณสารอาหารหลัก โปรตีน/คาร์บ/ไขมัน</span>
          </div>
          <div className="flex items-center gap-2.5 justify-center sm:justify-start">
            <Activity className="w-4 h-4 text-black shrink-0" />
            <span>คำนวณ BMR & TDEE และเป้าหมายรายวัน</span>
          </div>
        </div>
      </section>

      {/* Popular Foods Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Flame className="w-5 h-5 text-orange-500" />
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
                เมนูยอดนิยม & แคลอรี่
              </h2>
            </div>
            <p className="text-sm text-slate-500 mt-1">
              เมนูอาหารที่นักศึกษานิยมรับประทานพร้อมค่าพลังงาน Kcal
            </p>
          </div>

          <button
            onClick={() => onNavigate('foods')}
            className="flex items-center gap-1.5 text-orange-600 hover:text-orange-700 font-semibold text-sm transition-colors"
          >
            <span>ดูทั้งหมด ({foods.length})</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Foods Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayFoods.map((food) => (
            <FoodCard
              key={food.id}
              food={food}
              onSelectFood={onSelectFood}
            />
          ))}
        </div>
      </section>

      {/* Campus Restaurants Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Store className="w-5 h-5 text-orange-500" />
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
                ร้านอาหารในมหาวิทยาลัย
              </h2>
            </div>
            <p className="text-sm text-slate-500 mt-1">
              ร้านค้าและโรงอาหารที่พร้อมให้บริการนักศึกษา
            </p>
          </div>

          <button
            onClick={() => onNavigate('restaurants')}
            className="flex items-center gap-1.5 text-orange-600 hover:text-orange-700 font-semibold text-sm transition-colors"
          >
            <span>ดูร้านทั้งหมด ({restaurants.length})</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Restaurant Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => {
            const restaurantFoodsCount = foods.filter((f) => f.restaurant_id === restaurant.id).length;
            return (
              <div
                key={restaurant.id}
                onClick={() => onSelectRestaurant(restaurant)}
                className="group bg-white rounded-2xl border border-slate-200 hover:border-orange-300 hover:shadow-lg transition-all overflow-hidden cursor-pointer flex flex-col"
              >
                <div className="h-44 w-full relative overflow-hidden bg-slate-100">
                  <img
                    src={restaurant.image}
                    alt={restaurant.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-xs px-2.5 py-1 rounded-full text-xs font-semibold text-slate-800 shadow-xs">
                    {restaurantFoodsCount} เมนู
                  </div>
                </div>

                <div className="p-5 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-orange-600 transition-colors">
                      {restaurant.name}
                    </h3>
                    <p className="text-xs text-orange-600 font-medium mt-1">
                      📍 {restaurant.location}
                    </p>
                    <p className="text-xs text-slate-500 mt-2 line-clamp-2">
                      {restaurant.description}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span>{restaurant.open_hours || '08:00 - 18:00 น.'}</span>
                    <span className="font-semibold text-orange-600 flex items-center gap-1">
                      ดูเมนูของร้าน <ArrowRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};
