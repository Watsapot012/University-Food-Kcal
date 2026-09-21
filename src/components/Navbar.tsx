import React, { useState } from 'react';
import { Utensils, Flame, Store, BookOpen, ShieldCheck, Menu, X, User as UserIcon, Sliders, CalendarCheck, LogIn, LogOut } from 'lucide-react';
import { User } from '../types';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  user: User | null;
  onOpenLogin: () => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  user,
  onOpenLogin,
  onLogout,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'หน้าแรก', icon: Utensils },
    { id: 'restaurants', label: 'ร้านอาหาร', icon: Store },
    { id: 'foods', label: 'เมนูอาหาร', icon: BookOpen },
    { id: 'customizer', label: 'ปรับแต่งอาหาร', icon: Sliders },
    { id: 'dashboard', label: 'บันทึกรายวัน', icon: CalendarCheck },
    { id: 'admin', label: 'จัดการข้อมูล (Admin)', icon: ShieldCheck },
  ];

  const handleNavClick = (id: string) => {
    setActiveTab(id);
    setMobileMenuOpen(false);
    setUserDropdownOpen(false);
  };

  return (
    <header className="sticky top-3 z-50 px-4 sm:px-6 max-w-7xl mx-auto w-full">
      <nav className="rounded-full bg-white/90 backdrop-blur-xl border border-black/10 shadow-[0_15px_35px_rgba(0,0,0,0.06)] px-4 sm:px-6 py-2.5 flex items-center justify-between transition-all">
        {/* Logo & Brand */}
        <div
          className="flex items-center gap-3 cursor-pointer group shrink-0"
          onClick={() => handleNavClick('home')}
        >
          <div className="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center shadow-md group-hover:scale-105 transition-transform">
            <Utensils className="w-4 h-4 text-white" />
          </div>
          <div className="hidden sm:block">
            <span className="font-extrabold tracking-tight text-sm sm:text-base text-slate-900 block leading-tight">
              Campus Nutrition Analyzer
            </span>
            <span className="text-[10px] text-slate-500 font-semibold tracking-wide">
              University Food Kcal
            </span>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <div className="hidden lg:flex items-center space-x-1 text-xs font-semibold text-slate-600">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                id={`nav-link-${item.id}`}
                onClick={() => handleNavClick(item.id)}
                className={`px-3.5 py-2 rounded-full transition-all cursor-pointer flex items-center gap-1.5 ${
                  isActive
                    ? 'bg-slate-900 text-white shadow-sm font-semibold'
                    : 'text-slate-700 hover:text-slate-950 hover:bg-slate-100 font-medium'
                }`}
              >
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* User Auth Section */}
        <div className="flex items-center gap-2">
          {user ? (
            <div className="relative">
              <button
                type="button"
                id="user-profile-menu-btn"
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="flex items-center gap-2 pl-2 pr-3 py-1 rounded-full border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
              >
                <img
                  src={user.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'}
                  alt={user.name}
                  className="w-6 h-6 rounded-full object-cover border border-slate-300"
                />
                <span className="text-xs font-semibold text-slate-800 max-w-[100px] truncate hidden sm:inline">
                  {user.name}
                </span>
              </button>

              {userDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 rounded-2xl bg-white shadow-xl border border-slate-100 p-2 z-50 animate-in fade-in slide-in-from-top-2">
                  <div className="px-3 py-2 border-b border-slate-100 mb-1">
                    <div className="text-xs font-bold text-slate-900 truncate">{user.name}</div>
                    <div className="text-[10px] text-slate-400 truncate">{user.email}</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleNavClick('profile')}
                    className="w-full text-left px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 rounded-lg flex items-center gap-2 cursor-pointer"
                  >
                    <UserIcon className="w-3.5 h-3.5 text-slate-500" />
                    <span>โปรไฟล์ & BMR/TDEE</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => handleNavClick('dashboard')}
                    className="w-full text-left px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 rounded-lg flex items-center gap-2 cursor-pointer"
                  >
                    <CalendarCheck className="w-3.5 h-3.5 text-slate-500" />
                    <span>ภาพรวมรายวัน</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      onLogout();
                      setUserDropdownOpen(false);
                    }}
                    className="w-full text-left px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 rounded-lg flex items-center gap-2 cursor-pointer mt-1 pt-1 border-t border-slate-100"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    <span>ออกจากระบบ</span>
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button
              type="button"
              id="nav-login-btn"
              onClick={onOpenLogin}
              className="px-4 py-1.5 rounded-full bg-black text-white text-xs font-semibold flex items-center gap-1.5 hover:bg-slate-800 active:scale-95 transition-all shadow-xs cursor-pointer"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span>เข้าสู่ระบบ</span>
            </button>
          )}

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-1.5 rounded-full text-slate-700 hover:bg-slate-100 focus:outline-none cursor-pointer"
            aria-label="Toggle Menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </nav>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden mt-2 rounded-2xl bg-white/95 backdrop-blur-xl border border-slate-200 p-3 shadow-xl space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-4 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive ? 'bg-black text-white' : 'text-slate-700 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </div>
              </button>
            );
          })}

          {user && (
            <button
              onClick={() => handleNavClick('profile')}
              className="w-full flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 border-t border-slate-100 pt-2"
            >
              <UserIcon className="w-4 h-4 text-slate-500" />
              <span>โปรไฟล์ผู้ใช้งาน & BMR/TDEE</span>
            </button>
          )}
        </div>
      )}
    </header>
  );
};

