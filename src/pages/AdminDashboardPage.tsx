import React, { useState } from 'react';
import {
  ShieldCheck,
  Store,
  Utensils,
  Flame,
  Plus,
  Edit2,
  Trash2,
  TrendingUp,
  Award,
  RefreshCw,
  Search,
  Check,
  AlertTriangle,
  X,
} from 'lucide-react';
import { Restaurant, Food, AdminStats } from '../types';

interface AdminDashboardPageProps {
  restaurants: Restaurant[];
  foods: Food[];
  stats: AdminStats;
  onRefreshData: () => Promise<void>;
  onAddRestaurant: (data: Partial<Restaurant>) => Promise<void>;
  onUpdateRestaurant: (id: number, data: Partial<Restaurant>) => Promise<void>;
  onDeleteRestaurant: (id: number) => Promise<void>;
  onAddFood: (data: Partial<Food>) => Promise<void>;
  onUpdateFood: (id: number, data: Partial<Food>) => Promise<void>;
  onDeleteFood: (id: number) => Promise<void>;
  onResetDatabase: () => Promise<void>;
}

export const AdminDashboardPage: React.FC<AdminDashboardPageProps> = ({
  restaurants,
  foods,
  stats,
  onRefreshData,
  onAddRestaurant,
  onUpdateRestaurant,
  onDeleteRestaurant,
  onAddFood,
  onUpdateFood,
  onDeleteFood,
  onResetDatabase,
}) => {
  const [activeTab, setActiveTab] = useState<'restaurants' | 'foods'>('restaurants');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Modal States
  const [restaurantModalOpen, setRestaurantModalOpen] = useState(false);
  const [editingRestaurant, setEditingRestaurant] = useState<Restaurant | null>(null);
  const [restaurantForm, setRestaurantForm] = useState({
    name: '',
    description: '',
    location: '',
    image: '',
    phone: '',
    open_hours: '08:00 - 18:00 น.',
  });

  const [foodModalOpen, setFoodModalOpen] = useState(false);
  const [editingFood, setEditingFood] = useState<Food | null>(null);
  const [foodForm, setFoodForm] = useState({
    name: '',
    restaurant_id: restaurants[0]?.id || 1,
    price: 45,
    kcal: 450,
    protein: 20,
    carbohydrate: 50,
    fat: 15,
    image: '',
    description: '',
    category: 'อาหารจานเดียว',
    is_popular: false,
  });

  const [deleteConfirm, setDeleteConfirm] = useState<{
    type: 'restaurant' | 'food';
    id: number;
    name: string;
  } | null>(null);

  const [resetConfirmOpen, setResetConfirmOpen] = useState(false);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  // Open Add Restaurant
  const handleOpenAddRestaurant = () => {
    setEditingRestaurant(null);
    setRestaurantForm({
      name: '',
      description: '',
      location: '',
      image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80',
      phone: '',
      open_hours: '08:00 - 18:00 น.',
    });
    setRestaurantModalOpen(true);
  };

  // Open Edit Restaurant
  const handleOpenEditRestaurant = (r: Restaurant) => {
    setEditingRestaurant(r);
    setRestaurantForm({
      name: r.name,
      description: r.description,
      location: r.location,
      image: r.image,
      phone: r.phone || '',
      open_hours: r.open_hours || '08:00 - 18:00 น.',
    });
    setRestaurantModalOpen(true);
  };

  // Submit Restaurant Form
  const handleSubmitRestaurant = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!restaurantForm.name || !restaurantForm.location) {
      showToast('กรุณาระบุชื่อร้านและตำแหน่งสถานที่ตั้ง', 'error');
      return;
    }
    setLoading(true);
    try {
      if (editingRestaurant) {
        await onUpdateRestaurant(editingRestaurant.id, restaurantForm);
        showToast('แก้ไขข้อมูลร้านอาหารสำเร็จ');
      } else {
        await onAddRestaurant(restaurantForm);
        showToast('เพิ่มร้านอาหารใหม่สำเร็จ');
      }
      setRestaurantModalOpen(false);
    } catch (err: any) {
      showToast(err.message || 'เกิดข้อผิดพลาด', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Open Add Food
  const handleOpenAddFood = () => {
    setEditingFood(null);
    setFoodForm({
      name: '',
      restaurant_id: restaurants[0]?.id || 1,
      price: 45,
      kcal: 450,
      protein: 20,
      carbohydrate: 50,
      fat: 15,
      image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',
      description: '',
      category: 'อาหารจานเดียว',
      is_popular: false,
    });
    setFoodModalOpen(true);
  };

  // Open Edit Food
  const handleOpenEditFood = (f: Food) => {
    setEditingFood(f);
    setFoodForm({
      name: f.name,
      restaurant_id: f.restaurant_id,
      price: f.price,
      kcal: f.kcal,
      protein: f.protein,
      carbohydrate: f.carbohydrate,
      fat: f.fat,
      image: f.image,
      description: f.description,
      category: f.category || 'อาหารจานเดียว',
      is_popular: Boolean(f.is_popular),
    });
    setFoodModalOpen(true);
  };

  // Submit Food Form
  const handleSubmitFood = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!foodForm.name) {
      showToast('กรุณาระบุชื่อเมนูอาหาร', 'error');
      return;
    }
    setLoading(true);
    try {
      if (editingFood) {
        await onUpdateFood(editingFood.id, foodForm);
        showToast('แก้ไขเมนูอาหารสำเร็จ');
      } else {
        await onAddFood(foodForm);
        showToast('เพิ่มเมนูอาหารใหม่สำเร็จ');
      }
      setFoodModalOpen(false);
    } catch (err: any) {
      showToast(err.message || 'เกิดข้อผิดพลาด', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Confirm Delete
  const handleExecuteDelete = async () => {
    if (!deleteConfirm) return;
    setLoading(true);
    try {
      if (deleteConfirm.type === 'restaurant') {
        await onDeleteRestaurant(deleteConfirm.id);
        showToast('ลบร้านอาหารเรียบร้อยแล้ว');
      } else {
        await onDeleteFood(deleteConfirm.id);
        showToast('ลบเมนูอาหารเรียบร้อยแล้ว');
      }
      setDeleteConfirm(null);
    } catch (err: any) {
      showToast(err.message || 'เกิดข้อผิดพลาดในการลบ', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Confirm Reset
  const handleExecuteReset = async () => {
    setLoading(true);
    try {
      await onResetDatabase();
      showToast('รีเซ็ตข้อมูลตัวอย่างทั้งหมดเรียบร้อยแล้ว');
      setResetConfirmOpen(false);
    } catch (err: any) {
      showToast(err.message || 'ไม่สามารถรีเซ็ตได้', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Filtered lists for table
  const filteredRestaurants = restaurants.filter(
    (r) =>
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      r.location.toLowerCase().includes(search.toLowerCase())
  );

  const filteredFoods = foods.filter(
    (f) =>
      f.name.toLowerCase().includes(search.toLowerCase()) ||
      (f.restaurant_name && f.restaurant_name.toLowerCase().includes(search.toLowerCase())) ||
      (f.category && f.category.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-8 pb-16">
      {/* Toast Notification */}
      {message && (
        <div
          className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-xl shadow-lg text-sm font-medium flex items-center gap-2 animate-fade-in ${
            message.type === 'success'
              ? 'bg-emerald-600 text-white'
              : 'bg-rose-600 text-white'
          }`}
        >
          {message.type === 'success' ? <Check className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
          <span>{message.text}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-orange-500" />
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Admin Dashboard (จัดการข้อมูล)
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            จัดการข้อมูลร้านอาหารและเมนูอาหาร (เพิ่ม, แก้ไข, ลบ) และดูภาพรวมสถิติแคลอรี่
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onRefreshData()}
            className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 transition-colors shadow-xs"
            title="รีเฟรชข้อมูล"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <button
            onClick={() => setResetConfirmOpen(true)}
            className="px-3.5 py-2.5 rounded-xl border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-medium transition-colors"
          >
            รีเซ็ตข้อมูลตัวอย่าง
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Total Restaurants */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">ร้านอาหาร</span>
            <Store className="w-4 h-4 text-orange-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{stats.total_restaurants}</div>
          <span className="text-[11px] text-slate-500">ร้านค้าในระบบ</span>
        </div>

        {/* Total Foods */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">เมนูอาหาร</span>
            <Utensils className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{stats.total_foods}</div>
          <span className="text-[11px] text-slate-500">รายการเมนูทั้งหมด</span>
        </div>

        {/* Avg Kcal */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">Kcal เฉลี่ย</span>
            <TrendingUp className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{stats.avg_kcal}</div>
          <span className="text-[11px] text-slate-500">Kcal / เมนู</span>
        </div>

        {/* Max Kcal Food */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs col-span-1">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase text-rose-600">Kcal สูงสุด 🔥</span>
            <Flame className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-sm font-bold text-slate-900 truncate">
            {stats.max_kcal_food ? stats.max_kcal_food.name : '-'}
          </div>
          <span className="text-xs font-semibold text-rose-600">
            {stats.max_kcal_food ? `${stats.max_kcal_food.kcal} Kcal` : '-'}
          </span>
        </div>

        {/* Min Kcal Food */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs col-span-2 lg:col-span-1">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase text-emerald-600">Kcal ต่ำสุด ⚡</span>
            <Award className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-sm font-bold text-slate-900 truncate">
            {stats.min_kcal_food ? stats.min_kcal_food.name : '-'}
          </div>
          <span className="text-xs font-semibold text-emerald-600">
            {stats.min_kcal_food ? `${stats.min_kcal_food.kcal} Kcal` : '-'}
          </span>
        </div>
      </div>

      {/* Main Tab Controls & Actions */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          {/* Tab Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setActiveTab('restaurants');
                setSearch('');
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-colors cursor-pointer ${
                activeTab === 'restaurants'
                  ? 'bg-orange-500 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <Store className="w-4 h-4" />
              <span>จัดการร้านอาหาร ({restaurants.length})</span>
            </button>

            <button
              onClick={() => {
                setActiveTab('foods');
                setSearch('');
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-colors cursor-pointer ${
                activeTab === 'foods'
                  ? 'bg-orange-500 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <Utensils className="w-4 h-4" />
              <span>จัดการเมนูอาหาร ({foods.length})</span>
            </button>
          </div>

          {/* Add Button */}
          <div>
            {activeTab === 'restaurants' ? (
              <button
                onClick={handleOpenAddRestaurant}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-xl text-xs font-medium transition-colors shadow-xs"
              >
                <Plus className="w-4 h-4" />
                <span>เพิ่มร้านอาหารใหม่</span>
              </button>
            ) : (
              <button
                onClick={handleOpenAddFood}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-xl text-xs font-medium transition-colors shadow-xs"
              >
                <Plus className="w-4 h-4" />
                <span>เพิ่มเมนูอาหารใหม่</span>
              </button>
            )}
          </div>
        </div>

        {/* Search Input for Admin Table */}
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={
              activeTab === 'restaurants'
                ? 'ค้นหาร้านอาหารตามชื่อ หรือสถานที่ตั้ง...'
                : 'ค้นหาเมนูอาหารตามชื่อ ร้าน หรือหมวดหมู่...'
            }
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-orange-500"
          />
        </div>

        {/* Data Table: Restaurants */}
        {activeTab === 'restaurants' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">ID</th>
                  <th className="px-4 py-3">รูปภาพ</th>
                  <th className="px-4 py-3">ชื่อร้าน</th>
                  <th className="px-4 py-3">ตำแหน่ง / ที่ตั้ง</th>
                  <th className="px-4 py-3">เวลาทำการ</th>
                  <th className="px-4 py-3">จำนวนเมนู</th>
                  <th className="px-4 py-3 text-right">การจัดการ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredRestaurants.map((r) => {
                  const menuCount = foods.filter((f) => f.restaurant_id === r.id).length;
                  return (
                    <tr key={r.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3 font-mono font-bold text-slate-400">{r.id}</td>
                      <td className="px-4 py-3">
                        <img
                          src={r.image}
                          alt={r.name}
                          className="w-12 h-12 rounded-lg object-cover bg-slate-100"
                        />
                      </td>
                      <td className="px-4 py-3 font-semibold text-slate-900">{r.name}</td>
                      <td className="px-4 py-3 text-slate-600">{r.location}</td>
                      <td className="px-4 py-3 text-slate-500">{r.open_hours || '-'}</td>
                      <td className="px-4 py-3">
                        <span className="bg-orange-50 text-orange-700 font-semibold px-2 py-0.5 rounded-full text-[11px]">
                          {menuCount} เมนู
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right space-x-1">
                        <button
                          onClick={() => handleOpenEditRestaurant(r)}
                          className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="แก้ไข"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() =>
                            setDeleteConfirm({
                              type: 'restaurant',
                              id: r.id,
                              name: r.name,
                            })
                          }
                          className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                          title="ลบ"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Data Table: Foods */}
        {activeTab === 'foods' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">ID</th>
                  <th className="px-4 py-3">รูปภาพ</th>
                  <th className="px-4 py-3">ชื่ออาหาร</th>
                  <th className="px-4 py-3">ร้านค้า</th>
                  <th className="px-4 py-3">ราคา</th>
                  <th className="px-4 py-3">Kcal</th>
                  <th className="px-4 py-3">โปรตีน/คาร์บ/ไขมัน</th>
                  <th className="px-4 py-3 text-right">การจัดการ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredFoods.map((f) => (
                  <tr key={f.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-slate-400">{f.id}</td>
                    <td className="px-4 py-3">
                      <img
                        src={f.image}
                        alt={f.name}
                        className="w-12 h-12 rounded-lg object-cover bg-slate-100"
                      />
                    </td>
                    <td className="px-4 py-3 font-semibold text-slate-900">
                      <div>{f.name}</div>
                      {f.is_popular && (
                        <span className="text-[10px] text-amber-600 font-bold">
                          ⭐ เมนูยอดนิยม
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-slate-600">{f.restaurant_name}</td>
                    <td className="px-4 py-3 font-semibold text-slate-900">฿{f.price}</td>
                    <td className="px-4 py-3">
                      <span className="bg-orange-50 text-orange-700 font-bold px-2 py-0.5 rounded-full text-[11px]">
                        {f.kcal} Kcal
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-500">
                      P: {f.protein}g / C: {f.carbohydrate}g / F: {f.fat}g
                    </td>
                    <td className="px-4 py-3 text-right space-x-1">
                      <button
                        onClick={() => handleOpenEditFood(f)}
                        className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="แก้ไข"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() =>
                          setDeleteConfirm({
                            type: 'food',
                            id: f.id,
                            name: f.name,
                          })
                        }
                        className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                        title="ลบ"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal: Add / Edit Restaurant */}
      {restaurantModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <h3 className="font-bold text-lg text-slate-900">
                {editingRestaurant ? 'แก้ไขร้านอาหาร' : 'เพิ่มร้านอาหารใหม่'}
              </h3>
              <button
                onClick={() => setRestaurantModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitRestaurant} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  ชื่อร้านอาหาร *
                </label>
                <input
                  type="text"
                  required
                  value={restaurantForm.name}
                  onChange={(e) => setRestaurantForm({ ...restaurantForm, name: e.target.value })}
                  placeholder="เช่น ร้านป้าณี ตามสั่งตามใจ"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  ตำแหน่ง / สถานที่ตั้ง *
                </label>
                <input
                  type="text"
                  required
                  value={restaurantForm.location}
                  onChange={(e) => setRestaurantForm({ ...restaurantForm, location: e.target.value })}
                  placeholder="เช่น โรงอาหารกลาง 1 ล็อค 04"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    เวลาเปิด-ปิด
                  </label>
                  <input
                    type="text"
                    value={restaurantForm.open_hours}
                    onChange={(e) => setRestaurantForm({ ...restaurantForm, open_hours: e.target.value })}
                    placeholder="08:00 - 18:00 น."
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    เบอร์โทรศัพท์
                  </label>
                  <input
                    type="text"
                    value={restaurantForm.phone}
                    onChange={(e) => setRestaurantForm({ ...restaurantForm, phone: e.target.value })}
                    placeholder="081-xxx-xxxx"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  URL รูปภาพร้านอาหาร
                </label>
                <input
                  type="url"
                  value={restaurantForm.image}
                  onChange={(e) => setRestaurantForm({ ...restaurantForm, image: e.target.value })}
                  placeholder="https://images.unsplash.com/..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  รายละเอียดร้าน
                </label>
                <textarea
                  rows={3}
                  value={restaurantForm.description}
                  onChange={(e) => setRestaurantForm({ ...restaurantForm, description: e.target.value })}
                  placeholder="คำอธิบายร้านอาหาร เมนูเด่น..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setRestaurantModalOpen(false)}
                  className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-medium text-slate-600 hover:bg-slate-50"
                >
                  ยกเลิก
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-semibold shadow-xs"
                >
                  {loading ? 'กำลังบันทึก...' : 'บันทึกข้อมูล'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add / Edit Food */}
      {foodModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-200 my-8">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <h3 className="font-bold text-lg text-slate-900">
                {editingFood ? 'แก้ไขเมนูอาหาร' : 'เพิ่มเมนูอาหารใหม่'}
              </h3>
              <button
                onClick={() => setFoodModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitFood} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    ชื่อเมนูอาหาร *
                  </label>
                  <input
                    type="text"
                    required
                    value={foodForm.name}
                    onChange={(e) => setFoodForm({ ...foodForm, name: e.target.value })}
                    placeholder="เช่น ข้าวกะเพราไก่ไข่ดาว"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    ร้านอาหาร *
                  </label>
                  <select
                    value={foodForm.restaurant_id}
                    onChange={(e) =>
                      setFoodForm({ ...foodForm, restaurant_id: Number(e.target.value) })
                    }
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  >
                    {restaurants.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    ราคา (บาท) *
                  </label>
                  <input
                    type="number"
                    required
                    min={0}
                    value={foodForm.price}
                    onChange={(e) =>
                      setFoodForm({ ...foodForm, price: Number(e.target.value) })
                    }
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    แคลอรี่ (Kcal) *
                  </label>
                  <input
                    type="number"
                    required
                    min={0}
                    value={foodForm.kcal}
                    onChange={(e) =>
                      setFoodForm({ ...foodForm, kcal: Number(e.target.value) })
                    }
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500 font-bold text-orange-600"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    หมวดหมู่
                  </label>
                  <input
                    type="text"
                    value={foodForm.category}
                    onChange={(e) =>
                      setFoodForm({ ...foodForm, category: e.target.value })
                    }
                    placeholder="อาหารจานเดียว"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                  />
                </div>

                <div className="flex items-center pt-5">
                  <label className="flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={foodForm.is_popular}
                      onChange={(e) =>
                        setFoodForm({ ...foodForm, is_popular: e.target.checked })
                      }
                      className="w-4 h-4 rounded-sm text-orange-600 focus:ring-orange-500"
                    />
                    <span>เมนูยอดนิยม</span>
                  </label>
                </div>
              </div>

              {/* Nutrition Macros Inputs */}
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                <span className="block text-xs font-semibold text-slate-700 mb-2">
                  ข้อมูลสารอาหารหลักต่อจาน (กรัม)
                </span>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-[11px] text-blue-600 font-semibold mb-1">
                      โปรตีน (Protein) g
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min={0}
                      value={foodForm.protein}
                      onChange={(e) =>
                        setFoodForm({ ...foodForm, protein: Number(e.target.value) })
                      }
                      className="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] text-amber-600 font-semibold mb-1">
                      คาร์บ (Carb) g
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min={0}
                      value={foodForm.carbohydrate}
                      onChange={(e) =>
                        setFoodForm({ ...foodForm, carbohydrate: Number(e.target.value) })
                      }
                      className="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-amber-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] text-rose-600 font-semibold mb-1">
                      ไขมัน (Fat) g
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min={0}
                      value={foodForm.fat}
                      onChange={(e) =>
                        setFoodForm({ ...foodForm, fat: Number(e.target.value) })
                      }
                      className="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-rose-500"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  URL รูปภาพอาหาร
                </label>
                <input
                  type="url"
                  value={foodForm.image}
                  onChange={(e) => setFoodForm({ ...foodForm, image: e.target.value })}
                  placeholder="https://images.unsplash.com/..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  รายละเอียดเมนูอาหาร
                </label>
                <textarea
                  rows={2}
                  value={foodForm.description}
                  onChange={(e) =>
                    setFoodForm({ ...foodForm, description: e.target.value })
                  }
                  placeholder="วัตถุดิบ รสชาติ หรือส่วนประกอบพิเศษ..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:bg-white focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setFoodModalOpen(false)}
                  className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-medium text-slate-600 hover:bg-slate-50"
                >
                  ยกเลิก
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-semibold shadow-xs"
                >
                  {loading ? 'กำลังบันทึก...' : 'บันทึกข้อมูล'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-slate-200 text-center">
            <div className="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-3">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              ยืนยันการลบข้อมูล
            </h3>
            <p className="text-xs text-slate-500 mt-2">
              คุณแน่ใจหรือไม่ว่าต้องการลบ {deleteConfirm.type === 'restaurant' ? 'ร้านอาหาร' : 'เมนูอาหาร'}:{' '}
              <strong>"{deleteConfirm.name}"</strong>?
              {deleteConfirm.type === 'restaurant' && (
                <span className="block text-rose-500 font-semibold mt-1">
                  * เมนูอาหารทั้งหมดของร้านนี้จะถูกลบไปด้วย
                </span>
              )}
            </p>

            <div className="flex justify-center gap-3 mt-6">
              <button
                type="button"
                onClick={() => setDeleteConfirm(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-medium text-slate-600 hover:bg-slate-50"
              >
                ยกเลิก
              </button>
              <button
                type="button"
                onClick={handleExecuteDelete}
                disabled={loading}
                className="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold shadow-xs"
              >
                {loading ? 'กำลังลบ...' : 'ยืนยันลบข้อมูล'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reset Confirmation Modal */}
      {resetConfirmOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-slate-200 text-center">
            <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-3">
              <RefreshCw className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              ยืนยันรีเซ็ตข้อมูลตัวอย่าง
            </h3>
            <p className="text-xs text-slate-500 mt-2 leading-relaxed">
              การกระทำนี้จะล้างข้อมูลปัจจุบันทั้งหมด และโหลดร้านค้าตัวอย่าง 5 ร้าน พร้อมเมนูอาหารมาตรฐาน 17 เมนูกลับคืนมา
            </p>

            <div className="flex justify-center gap-3 mt-6">
              <button
                type="button"
                onClick={() => setResetConfirmOpen(false)}
                className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-medium text-slate-600 hover:bg-slate-50"
              >
                ยกเลิก
              </button>
              <button
                type="button"
                onClick={handleExecuteReset}
                disabled={loading}
                className="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold shadow-xs"
              >
                {loading ? 'กำลังรีเซ็ต...' : 'ยืนยันรีเซ็ต'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
