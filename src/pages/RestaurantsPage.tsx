import React, { useState } from 'react';
import { Store, MapPin, Clock, Phone, Search, Utensils, ArrowLeft, Plus } from 'lucide-react';
import { Restaurant, Food } from '../types';
import { FoodCard } from '../components/FoodCard';

interface RestaurantsPageProps {
  restaurants: Restaurant[];
  foods: Food[];
  onSelectFood: (food: Food) => void;
  selectedRestaurant: Restaurant | null;
  onSelectRestaurant: (restaurant: Restaurant | null) => void;
  onOpenAddRestaurantModal: () => void;
}

export const RestaurantsPage: React.FC<RestaurantsPageProps> = ({
  restaurants,
  foods,
  onSelectFood,
  selectedRestaurant,
  onSelectRestaurant,
  onOpenAddRestaurantModal,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('ทั้งหมด');

  const locations = ['ทั้งหมด', 'โรงอาหารกลาง', 'อาคารเรียนรวม', 'หอพักนักศึกษา'];

  // Filter restaurants
  const filteredRestaurants = restaurants.filter((r) => {
    const matchesSearch =
      r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLocation =
      selectedLocation === 'ทั้งหมด' || r.location.includes(selectedLocation);
    return matchesSearch && matchesLocation;
  });

  // If a restaurant is selected, show its detail view + all foods in it
  if (selectedRestaurant) {
    const restaurantFoods = foods.filter((f) => f.restaurant_id === selectedRestaurant.id);

    return (
      <div className="space-y-8 pb-16">
        {/* Back Button */}
        <div>
          <button
            onClick={() => onSelectRestaurant(null)}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-slate-300 bg-white text-xs font-semibold text-slate-800 hover:bg-slate-100 hover:text-black transition-all shadow-xs cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>กลับไปหน้ารวมร้านอาหาร</span>
          </button>
        </div>

        {/* Restaurant Header Banner */}
        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="relative h-56 sm:h-72 w-full bg-slate-100">
            <img
              src={selectedRestaurant.image}
              alt={selectedRestaurant.name}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent flex items-end p-6 text-white">
              <div>
                <span className="bg-orange-500 text-white text-xs font-semibold px-2.5 py-1 rounded-md mb-2 inline-block">
                  ร้านอาหารในมหาวิทยาลัย
                </span>
                <h1 className="text-2xl sm:text-4xl font-extrabold text-white">
                  {selectedRestaurant.name}
                </h1>
                <p className="text-sm text-slate-200 mt-1 flex items-center gap-1.5">
                  <MapPin className="w-4 h-4 text-orange-400" />
                  {selectedRestaurant.location}
                </p>
              </div>
            </div>
          </div>

          <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-3">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                เกี่ยวกับร้านนี้
              </h3>
              <p className="text-sm text-slate-700 leading-relaxed">
                {selectedRestaurant.description}
              </p>
            </div>

            <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-2.5 text-xs text-slate-600">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-orange-500 shrink-0" />
                <span>เวลาทำการ: <strong>{selectedRestaurant.open_hours || '08:00 - 18:00 น.'}</strong></span>
              </div>
              {selectedRestaurant.phone && (
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4 text-orange-500 shrink-0" />
                  <span>เบอร์ติดต่อ: {selectedRestaurant.phone}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Utensils className="w-4 h-4 text-orange-500 shrink-0" />
                <span>จำนวนเมนูที่บันทึกไว้: <strong>{restaurantFoods.length} เมนู</strong></span>
              </div>
            </div>
          </div>
        </div>

        {/* Menu Items of this Restaurant */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                รายการอาหารของ {selectedRestaurant.name}
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                เลือกเมนูเพื่อดูข้อมูลโภชนาการ ปรับแต่ง หรือบันทึกลงไดอารี่
              </p>
            </div>
            <span className="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
              {restaurantFoods.length} เมนู
            </span>
          </div>

          {restaurantFoods.length === 0 ? (
            <div className="bg-white rounded-2xl p-12 text-center border border-dashed border-slate-300">
              <Utensils className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-sm font-medium text-slate-700">ยังไม่มีเมนูอาหารสำหรับร้านนี้</p>
              <p className="text-xs text-slate-500 mt-1">
                สามารถเพิ่มเมนูอาหารของร้านนี้ได้ที่หน้า Admin Dashboard
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {restaurantFoods.map((food) => (
                <FoodCard
                  key={food.id}
                  food={food}
                  onSelectFood={onSelectFood}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-16">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Store className="w-6 h-6 text-slate-900" />
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              ร้านอาหารในมหาวิทยาลัย
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            รวบรวมร้านค้า โรงอาหารกลาง และซุ้มเครื่องดื่มภายในรั้วมหาวิทยาลัย
          </p>
        </div>

        <button
          onClick={onOpenAddRestaurantModal}
          className="inline-flex items-center gap-2 bg-slate-900 hover:bg-black text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition-all shadow-xs active:scale-95 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>เพิ่มร้านอาหารใหม่</span>
        </button>
      </div>

      {/* Search & Location Filter */}
      <div className="liquid-card p-4 rounded-2xl border border-white/60 shadow-md space-y-3">
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="ค้นหาชื่อร้าน หรือตำแหน่งสถานที่ตั้ง (เช่น โรงอาหารกลาง, หอพัก)..."
            className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm focus:bg-white focus:outline-none focus:border-black"
          />
        </div>

        {/* Location category tags */}
        <div className="flex flex-wrap gap-2 pt-1">
          <span className="text-xs text-slate-400 self-center">โซนโรงอาหาร:</span>
          {locations.map((loc) => (
            <button
              key={loc}
              type="button"
              onClick={() => setSelectedLocation(loc)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-all cursor-pointer ${
                selectedLocation === loc
                  ? 'bg-black text-white shadow-xs'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              {loc}
            </button>
          ))}
        </div>
      </div>

      {/* Restaurants Grid */}
      {filteredRestaurants.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center border border-dashed border-slate-300">
          <Store className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-slate-800">ไม่พบร้านอาหารที่ตรงกับการค้นหา</h3>
          <p className="text-xs text-slate-500 mt-1">ลองเปลี่ยนคำค้นหา หรือเพิ่มร้านอาหารใหม่</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredRestaurants.map((restaurant) => {
            const menuCount = foods.filter((f) => f.restaurant_id === restaurant.id).length;

            return (
              <div
                key={restaurant.id}
                onClick={() => onSelectRestaurant(restaurant)}
                className="group bg-white rounded-2xl border border-slate-200 hover:border-orange-300 hover:shadow-lg transition-all overflow-hidden cursor-pointer flex flex-col"
              >
                <div className="h-48 w-full relative overflow-hidden bg-slate-100">
                  <img
                    src={restaurant.image}
                    alt={restaurant.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-xs px-2.5 py-1 rounded-full text-xs font-bold text-orange-600 shadow-xs">
                    {menuCount} เมนู
                  </div>
                </div>

                <div className="p-5 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-orange-600 transition-colors">
                      {restaurant.name}
                    </h3>
                    <div className="flex items-center gap-1 text-xs text-orange-600 font-medium mt-1">
                      <MapPin className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{restaurant.location}</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-2 line-clamp-2">
                      {restaurant.description}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-slate-400" />
                      {restaurant.open_hours || '08:00 - 18:00 น.'}
                    </span>
                    <span className="text-xs font-semibold text-slate-900 group-hover:text-black flex items-center gap-1">
                      เปิดดูเมนู →
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
