import React, { useState, useMemo } from 'react';
import { Search, Filter, ArrowUpDown, Flame, Plus, X, Utensils, RotateCcw } from 'lucide-react';
import { Food, Restaurant } from '../types';
import { FoodCard } from '../components/FoodCard';

interface FoodListPageProps {
  foods: Food[];
  restaurants: Restaurant[];
  onSelectFood: (food: Food) => void;
  initialSearch?: string;
  onOpenAddFoodModal: () => void;
}

export const FoodListPage: React.FC<FoodListPageProps> = ({
  foods,
  restaurants,
  onSelectFood,
  initialSearch = '',
  onOpenAddFoodModal,
}) => {
  const [search, setSearch] = useState(initialSearch);
  const [selectedRestaurantId, setSelectedRestaurantId] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [kcalRange, setKcalRange] = useState<string>('all');
  const [priceRange, setPriceRange] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('default');

  // Extract unique categories
  const categories = useMemo(() => {
    const cats = new Set<string>();
    foods.forEach((f) => {
      if (f.category) cats.add(f.category);
    });
    return Array.from(cats);
  }, [foods]);

  // Filtering & Sorting Logic
  const filteredFoods = useMemo(() => {
    return foods
      .filter((food) => {
        // Search filter (name, restaurant, description)
        if (search.trim()) {
          const q = search.toLowerCase();
          const matchName = food.name.toLowerCase().includes(q);
          const matchRest = food.restaurant_name?.toLowerCase().includes(q) || false;
          const matchDesc = food.description?.toLowerCase().includes(q) || false;
          if (!matchName && !matchRest && !matchDesc) return false;
        }

        // Restaurant filter
        if (selectedRestaurantId !== 'all') {
          if (food.restaurant_id !== Number(selectedRestaurantId)) return false;
        }

        // Category filter
        if (selectedCategory !== 'all') {
          if (food.category !== selectedCategory) return false;
        }

        // Kcal Range filter
        if (kcalRange !== 'all') {
          if (kcalRange === 'under-300' && food.kcal >= 300) return false;
          if (kcalRange === '300-500' && (food.kcal < 300 || food.kcal > 500)) return false;
          if (kcalRange === '500-700' && (food.kcal <= 500 || food.kcal > 700)) return false;
          if (kcalRange === 'over-700' && food.kcal <= 700) return false;
        }

        // Price Range filter
        if (priceRange !== 'all') {
          if (priceRange === 'under-40' && food.price >= 40) return false;
          if (priceRange === '40-60' && (food.price < 40 || food.price > 60)) return false;
          if (priceRange === 'over-60' && food.price <= 60) return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === 'kcal-asc') return a.kcal - b.kcal;
        if (sortBy === 'kcal-desc') return b.kcal - a.kcal;
        if (sortBy === 'price-asc') return a.price - b.price;
        if (sortBy === 'price-desc') return b.price - a.price;
        if (sortBy === 'protein-desc') return b.protein - a.protein;
        return a.id - b.id;
      });
  }, [foods, search, selectedRestaurantId, selectedCategory, kcalRange, priceRange, sortBy]);

  const handleResetFilters = () => {
    setSearch('');
    setSelectedRestaurantId('all');
    setSelectedCategory('all');
    setKcalRange('all');
    setPriceRange('all');
    setSortBy('default');
  };

  const hasActiveFilters =
    search !== '' ||
    selectedRestaurantId !== 'all' ||
    selectedCategory !== 'all' ||
    kcalRange !== 'all' ||
    priceRange !== 'all' ||
    sortBy !== 'default';

  return (
    <div className="space-y-8 pb-16">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Utensils className="w-6 h-6 text-slate-900" />
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              รายการอาหาร & ข้อมูลโภชนาการ
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            ค้นหาอาหาร กรองตามร้าน ช่วง Kcal ราคา และเรียงตามลำดับสารอาหาร
          </p>
        </div>

        <button
          onClick={onOpenAddFoodModal}
          className="inline-flex items-center gap-2 bg-slate-900 hover:bg-black text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition-all shadow-xs active:scale-95 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>เพิ่มเมนูอาหารใหม่</span>
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
        {/* Main Search Input */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="ค้นหาชื่ออาหาร, วัตถุดิบ, หรือชื่อร้าน..."
            className="w-full pl-11 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-black"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-1"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Filter Controls Row */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 pt-2">
          {/* Restaurant Filter */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              เลือกร้านอาหาร
            </label>
            <select
              value={selectedRestaurantId}
              onChange={(e) => setSelectedRestaurantId(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">ทุกร้านค้า</option>
              {restaurants.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                </option>
              ))}
            </select>
          </div>

          {/* Kcal Range Filter */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              ช่วงแคลอรี่ (Kcal)
            </label>
            <select
              value={kcalRange}
              onChange={(e) => setKcalRange(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">ทุกระดับแคลอรี่</option>
              <option value="under-300">น้อยกว่า 300 Kcal (เบาๆ)</option>
              <option value="300-500">300 - 500 Kcal (ปานกลาง)</option>
              <option value="500-700">500 - 700 Kcal (อิ่มจุใจ)</option>
              <option value="over-700">มากกว่า 700 Kcal (พลังงานสูง)</option>
            </select>
          </div>

          {/* Price Range Filter */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              ระดับราคา
            </label>
            <select
              value={priceRange}
              onChange={(e) => setPriceRange(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">ทุกราคา</option>
              <option value="under-40">ประหยัด (&lt; 40 บาท)</option>
              <option value="40-60">ปกติ (40 - 60 บาท)</option>
              <option value="over-60">พิเศษ (&gt; 60 บาท)</option>
            </select>
          </div>

          {/* Category Filter */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              หมวดหมู่อาหาร
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">ทุกหมวดหมู่</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              จัดเรียงข้อมูล
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            >
              <option value="default">ค่าเริ่มต้น</option>
              <option value="kcal-asc">⚡ Kcal: ต่ำไปสูง</option>
              <option value="kcal-desc">🔥 Kcal: สูงไปต่ำ</option>
              <option value="price-asc">💵 ราคา: ต่ำไปสูง</option>
              <option value="price-desc">💰 ราคา: สูงไปต่ำ</option>
              <option value="protein-desc">💪 โปรตีนสูงสุด</option>
            </select>
          </div>
        </div>

        {/* Filter Summary & Reset Button */}
        {hasActiveFilters && (
          <div className="flex items-center justify-between pt-2 text-xs text-slate-500 border-t border-slate-100">
            <span>
              พบทั้งหมด <strong>{filteredFoods.length}</strong> รายการ
            </span>
            <button
              onClick={handleResetFilters}
              className="inline-flex items-center gap-1 text-orange-600 hover:text-orange-700 font-medium"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>ล้างตัวกรองทั้งหมด</span>
            </button>
          </div>
        )}
      </div>

      {/* Food Cards Grid */}
      {filteredFoods.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center border border-dashed border-slate-300">
          <Utensils className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-slate-800">
            ไม่พบเมนูอาหารที่ตรงตามเงื่อนไข
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            ลองปรับเปลี่ยนคำค้นหา หรือกดล้างตัวกรองเพื่อดูเมนูทั้งหมด
          </p>
          <button
            onClick={handleResetFilters}
            className="mt-4 px-5 py-2.5 bg-slate-900 hover:bg-black text-white font-semibold rounded-xl text-xs transition-all shadow-xs active:scale-95 cursor-pointer"
          >
            ล้างตัวกรอง
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredFoods.map((food) => (
            <FoodCard
              key={food.id}
              food={food}
              onSelectFood={onSelectFood}
            />
          ))}
        </div>
      )}
    </div>
  );
};
