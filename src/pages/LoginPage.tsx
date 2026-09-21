import React, { useState } from 'react';
import { User } from '../types';
import { api } from '../services/api';
import { Lock, Mail, User as UserIcon, LogIn, ArrowRight, ShieldCheck, Sparkles, CheckCircle2 } from 'lucide-react';

interface LoginPageProps {
  onLoginSuccess: (user: User, token?: string) => void;
  onNavigateToHome?: () => void;
  onCancel?: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess, onNavigateToHome, onCancel }) => {
  const [isRegister, setIsRegister] = useState<boolean>(false);
  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('student@npru.ac.th');
  const [password, setPassword] = useState<string>('password123');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      if (isRegister) {
        if (!name.trim()) {
          throw new Error('กรุณากรอกชื่อ-นามสกุล');
        }
        const res = await api.register({ name, email, password });
        setSuccessMsg('สมัครสมาชิกสำเร็จ! กำลังเข้าสู่ระบบ...');
        setTimeout(() => {
          onLoginSuccess(res.user, res.token);
        }, 600);
      } else {
        const res = await api.login({ email, password });
        setSuccessMsg('เข้าสู่ระบบสำเร็จ!');
        setTimeout(() => {
          onLoginSuccess(res.user, res.token);
        }, 500);
      }
    } catch (err: any) {
      setError(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemoLogin = async () => {
    setEmail('student@npru.ac.th');
    setPassword('password123');
    setLoading(true);
    setError(null);
    try {
      const res = await api.login({ email: 'student@npru.ac.th', password: 'password123' });
      setSuccessMsg('เข้าสู่ระบบด้วยบัญชีนักศึกษาตัวอย่างสำเร็จ!');
      setTimeout(() => {
        onLoginSuccess(res.user, res.token);
      }, 500);
    } catch {
      // Fallback local login
      const demoUser: User = {
        id: 1,
        name: 'นักศึกษาสุขภาพดี',
        email: 'student@npru.ac.th',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
      };
      onLoginSuccess(demoUser, 'demo-token');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    // Simulated Google OAuth login
    setLoading(true);
    setTimeout(() => {
      const googleUser: User = {
        id: 99,
        name: 'Google Student Account',
        email: 'student.google@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=400&q=80',
      };
      setSuccessMsg('เข้าสู่ระบบด้วย Google สำเร็จ');
      setTimeout(() => {
        onLoginSuccess(googleUser, 'google-oauth-token');
        setLoading(false);
      }, 500);
    }, 600);
  };

  return (
    <div className="relative min-h-[82vh] flex items-center justify-center py-10 px-4">
      {/* Ambient background blob from original UI */}
      <div className="ambient-blob w-72 h-72 top-10 left-1/4 bg-orange-100 opacity-60"></div>
      <div className="ambient-blob w-80 h-80 bottom-10 right-1/4 bg-amber-100 opacity-50"></div>

      {/* Liquid Card Modal/Form */}
      <div className="liquid-card w-full max-w-md p-8 sm:p-10 relative z-10 border border-white/80 shadow-2xl">
        {/* Header Icon */}
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="w-14 h-14 rounded-full bg-black text-white flex items-center justify-center shadow-lg mb-4">
            <span className="material-symbols-outlined text-2xl">restaurant</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            {isRegister ? 'สมัครสมาชิก' : 'เข้าสู่ระบบ'}
          </h1>
          <p className="text-xs text-slate-500 mt-1.5 max-w-xs">
            {isRegister
              ? 'สร้างบัญชีเพื่อบันทึกและติดตามแคลอรี่อาหารมหาวิทยาลัย'
              : 'Campus Nutrition Analyzer — ระบบวิเคราะห์โภชนาการ'}
          </p>
        </div>

        {/* Tab switch buttons */}
        <div className="flex rounded-full bg-slate-100 p-1 mb-6">
          <button
            type="button"
            id="tab-login-btn"
            onClick={() => {
              setIsRegister(false);
              setError(null);
              setSuccessMsg(null);
            }}
            className={`flex-1 py-2 text-xs font-semibold rounded-full transition-all cursor-pointer ${
              !isRegister ? 'bg-black text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            เข้าสู่ระบบ
          </button>
          <button
            type="button"
            id="tab-register-btn"
            onClick={() => {
              setIsRegister(true);
              setError(null);
              setSuccessMsg(null);
            }}
            className={`flex-1 py-2 text-xs font-semibold rounded-full transition-all cursor-pointer ${
              isRegister ? 'bg-black text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            สมัครสมาชิก
          </button>
        </div>

        {/* Error / Success message */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs flex items-center gap-2">
            <span className="material-symbols-outlined text-base shrink-0">error</span>
            <span>{error}</span>
          </div>
        )}

        {successMsg && (
          <div className="mb-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {isRegister && (
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1 flex items-center gap-1.5">
                <UserIcon className="w-3.5 h-3.5 text-slate-400" />
                ชื่อ - นามสกุล
              </label>
              <input
                type="text"
                required
                id="input-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="เช่น สมชาย สุขภาพดี"
                className="input-underline text-sm font-medium text-slate-900 placeholder:text-slate-400"
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1 flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-slate-400" />
              อีเมล (Email)
            </label>
            <input
              type="email"
              required
              id="input-email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@university.ac.th"
              className="input-underline text-sm font-medium text-slate-900 placeholder:text-slate-400"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-slate-400" />
              รหัสผ่าน (Password)
            </label>
            <input
              type="password"
              required
              id="input-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="input-underline text-sm font-medium text-slate-900 placeholder:text-slate-400"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            id="btn-auth-submit"
            className="w-full py-3 px-6 mt-2 rounded-full bg-black text-white font-medium text-sm flex items-center justify-center gap-2 hover:bg-slate-800 active:scale-95 transition-all shadow-md cursor-pointer disabled:opacity-50"
          >
            {loading ? (
              <span className="material-symbols-outlined animate-spin text-base">progress_activity</span>
            ) : (
              <>
                <span>{isRegister ? 'สมัครสมาชิก' : 'เข้าสู่ระบบ'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Divider */}
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-200"></div>
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-white/80 px-3 text-slate-400">หรือ</span>
          </div>
        </div>

        {/* Google login emulation */}
        <button
          type="button"
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full py-2.5 px-4 rounded-full border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium flex items-center justify-center gap-2.5 transition-all cursor-pointer shadow-xs"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#EA4335"
              d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"
            />
            <path
              fill="#4285F4"
              d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5.1 3.7-8.8z"
            />
            <path
              fill="#FBBC05"
              d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12.3 0 15s.7 5.3 1.9 7.7l3.7-2.9c0-1.7 0-3.3 0-5z"
            />
            <path
              fill="#34A853"
              d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.4-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"
            />
          </svg>
          <span>เข้าสู่ระบบด้วย Google</span>
        </button>

        {/* Demo Account Quick Access */}
        <button
          type="button"
          onClick={handleQuickDemoLogin}
          disabled={loading}
          className="w-full mt-3 py-2 px-4 rounded-full bg-orange-50 hover:bg-orange-100 text-orange-700 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer border border-orange-200"
        >
          <Sparkles className="w-3.5 h-3.5 text-orange-500" />
          <span>เข้าสู่ระบบด่วนด้วยบัญชีทดสอบ (1-Click Demo)</span>
        </button>

        {/* Guest Return link */}
        {onNavigateToHome && (
          <div className="text-center mt-6">
            <button
              type="button"
              onClick={onNavigateToHome}
              className="text-xs text-slate-400 hover:text-slate-600 underline cursor-pointer"
            >
              กลับสู่หน้าหลักโดยไม่เข้าสู่ระบบ
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
