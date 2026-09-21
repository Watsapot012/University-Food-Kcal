import React from 'react';
import { Flame, Store, ArrowRight } from 'lucide-react';
import { Food } from '../types';

interface FoodCardProps {
  food: Food;
  onSelectFood: (food: Food) => void;
}

export const FoodCard: React.FC<FoodCardProps> = ({
  food,
  onSelectFood,
}) => {
  return (
    <div
      id={`food-card-${food.id}`}
      onClick={() => onSelectFood(food)}
      className="group bg-white rounded-xl border border-slate-200 hover:border-black/20 hover:shadow-lg transition-all duration-200 overflow-hidden flex flex-col cursor-pointer"
    >
      {/* Food Image Container */}
      <div className="relative w-full h-48 bg-slate-100 overflow-hidden">
        <img
          src={food.image}
          alt={food.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />

        {/* Kcal Badge */}
        <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-xs border border-orange-200 text-orange-600 font-bold px-3 py-1 rounded-full text-xs shadow-sm flex items-center gap-1">
          <Flame className="w-3.5 h-3.5 fill-orange-500 text-orange-500" />
          <span>{food.kcal} Kcal</span>
        </div>

        {/* Category Pill */}
        {food.category && (
          <div className="absolute top-3 left-3 bg-slate-900/75 backdrop-blur-xs text-white text-[11px] font-medium px-2.5 py-0.5 rounded-md">
            {food.category}
          </div>
        )}

        {/* Popular Tag */}
        {food.is_popular && (
          <div className="absolute bottom-2 left-2 bg-amber-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-xs">
            ⭐ เมนูยอดนิยม
          </div>
        )}
      </div>

      {/* Card Body */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          {/* Restaurant name */}
          <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1.5">
            <Store className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span className="truncate">{food.restaurant_name || 'ร้านค้าในมหาวิทยาลัย'}</span>
          </div>

          {/* Food Title */}
          <h3 className="font-semibold text-slate-900 text-base line-clamp-1 group-hover:text-black transition-colors">
            {food.name}
          </h3>

          {/* Description */}
          <p className="text-xs text-slate-500 line-clamp-2 mt-1 min-h-[32px]">
            {food.description || 'เมนูอร่อยปรุงสดใหม่ในมหาวิทยาลัย'}
          </p>

          {/* Nutrition Mini Breakdown */}
          <div className="mt-3 grid grid-cols-3 gap-1 bg-slate-50 rounded-lg p-2 text-center text-xs">
            <div className="border-r border-slate-200 pr-1">
              <span className="block text-[10px] text-slate-400 font-medium">โปรตีน</span>
              <span className="font-semibold text-blue-600">{food.protein}g</span>
            </div>
            <div className="border-r border-slate-200 px-1">
              <span className="block text-[10px] text-slate-400 font-medium">คาร์บ</span>
              <span className="font-semibold text-amber-600">{food.carbohydrate}g</span>
            </div>
            <div className="pl-1">
              <span className="block text-[10px] text-slate-400 font-medium">ไขมัน</span>
              <span className="font-semibold text-rose-500">{food.fat}g</span>
            </div>
          </div>
        </div>

        {/* Footer: Price & View Detail Button */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 block">ราคา</span>
            <span className="text-lg font-bold text-slate-900">฿{food.price}</span>
          </div>

          <button
            id={`view-btn-${food.id}`}
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onSelectFood(food);
            }}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-black active:scale-95 text-white shadow-xs hover:shadow-md transition-all cursor-pointer"
          >
            <span>ดูรายละเอียด</span>
            <ArrowRight className="w-3.5 h-3.5 text-slate-300 group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
};
