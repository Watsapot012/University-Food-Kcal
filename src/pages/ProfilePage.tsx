import React, { useState, useEffect } from 'react';
import { User, UserProfile } from '../types';
import { api } from '../services/api';
import { User as UserIcon, Activity, Flame, Heart, Award, ArrowRight, LogOut, CheckCircle2, Save } from 'lucide-react';

interface ProfilePageProps {
  user: User | null;
  onLogout: () => void;
  onNavigateToDashboard: () => void;
  onProfileUpdated?: (profile: UserProfile) => void;
}

export const ProfilePage: React.FC<ProfilePageProps> = ({
  user,
  onLogout,
  onNavigateToDashboard,
  onProfileUpdated,
}) => {
  const [weight, setWeight] = useState<number>(65);
  const [height, setHeight] = useState<number>(175);
  const [age, setAge] = useState<number>(21);
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [activity, setActivity] = useState<number>(1.55);

  const [bmr, setBmr] = useState<number>(1650);
  const [tdee, setTdee] = useState<number>(2558);
  const [targetCalories, setTargetCalories] = useState<number>(2000);

  const [saving, setSaving] = useState<boolean>(false);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);

  // Load existing profile from API
  useEffect(() => {
    if (!user) return;
    api.getProfile(user.id)
      .then((data) => {
        if (data) {
          if (data.weight) setWeight(data.weight);
          if (data.height) setHeight(data.height);
          if (data.age) setAge(data.age);
          if (data.gender) setGender(data.gender);
          if (data.activity) setActivity(data.activity);
          if (data.bmr) setBmr(data.bmr);
          if (data.tdee) setTdee(data.tdee);
          if (data.calories) setTargetCalories(data.calories);
        }
      })
      .catch((err) => console.error('Error fetching profile:', err));
  }, [user]);

  // Recalculate Mifflin-St Jeor formula
  const calculateCalories = () => {
    let calculatedBmr = 0;
    if (gender === 'male') {
      calculatedBmr = 10 * weight + 6.25 * height - 5 * age + 5;
    } else {
      calculatedBmr = 10 * weight + 6.25 * height - 5 * age - 161;
    }
    calculatedBmr = Math.round(calculatedBmr);
    const calculatedTdee = Math.round(calculatedBmr * activity);

    setBmr(calculatedBmr);
    setTdee(calculatedTdee);
    setTargetCalories(calculatedTdee);

    return { calculatedBmr, calculatedTdee };
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);

    const { calculatedBmr, calculatedTdee } = calculateCalories();

    const profileData: UserProfile = {
      weight,
      height,
      age,
      gender,
      activity,
      bmr: calculatedBmr,
      tdee: calculatedTdee,
      calories: targetCalories || calculatedTdee,
      updatedAt: new Date().toISOString(),
    };

    try {
      if (user) {
        await api.saveProfile({
          userId: user.id,
          ...profileData,
        });
      }
      if (onProfileUpdated) {
        onProfileUpdated(profileData);
      }
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error('Error saving profile:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      {/* Top Welcome Card with Avatar */}
      <div className="liquid-card p-6 sm:p-8 mb-8 border border-white/60 shadow-lg">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-5">
            <img
              src={user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80'}
              alt={user?.name || 'User Avatar'}
              className="w-20 h-20 rounded-full object-cover border-2 border-black/10 shadow-md"
            />
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-xs font-semibold text-slate-700 mb-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>ผู้ใช้งานในระบบมหาวิทยาลัย</span>
              </div>
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
                {user?.name || 'นักศึกษาผู้ใช้งาน'}
              </h1>
              <p className="text-sm text-slate-500">{user?.email || 'student@university.ac.th'}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onNavigateToDashboard}
              className="px-5 py-2.5 rounded-full bg-black text-white text-xs font-medium flex items-center gap-2 hover:bg-slate-800 transition-transform active:scale-95 cursor-pointer shadow-sm"
            >
              <span>ดูภาพรวมรายวัน</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onLogout}
              className="px-4 py-2.5 rounded-full border border-slate-300 bg-white hover:bg-slate-50 text-xs font-medium text-slate-600 flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <LogOut className="w-3.5 h-3.5 text-slate-500" />
              <span>ออกจากระบบ</span>
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Profile Inputs & BMR Form */}
        <div className="lg:col-span-7">
          <div className="liquid-card p-6 sm:p-8 border border-white/60 shadow-lg">
            <div className="flex items-center gap-2 mb-6">
              <Activity className="w-5 h-5 text-black" />
              <h2 className="text-lg font-bold text-slate-900">ข้อมูลร่างกาย & แคลอรี่ที่เหมาะสม</h2>
            </div>

            <form onSubmit={handleSave} className="space-y-6">
              {/* Gender */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-2">เพศกำเนิด</label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setGender('male')}
                    className={`py-2.5 px-4 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
                      gender === 'male'
                        ? 'border-black bg-black text-white shadow-xs'
                        : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    ชาย (Male)
                  </button>
                  <button
                    type="button"
                    onClick={() => setGender('female')}
                    className={`py-2.5 px-4 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
                      gender === 'female'
                        ? 'border-black bg-black text-white shadow-xs'
                        : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    หญิง (Female)
                  </button>
                </div>
              </div>

              {/* Weight, Height, Age */}
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">น้ำหนัก (กก.)</label>
                  <input
                    type="number"
                    min="30"
                    max="200"
                    value={weight}
                    onChange={(e) => setWeight(Number(e.target.value))}
                    className="input-underline text-base font-semibold text-slate-900"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">ส่วนสูง (ซม.)</label>
                  <input
                    type="number"
                    min="100"
                    max="230"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    className="input-underline text-base font-semibold text-slate-900"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">อายุ (ปี)</label>
                  <input
                    type="number"
                    min="12"
                    max="100"
                    value={age}
                    onChange={(e) => setAge(Number(e.target.value))}
                    className="input-underline text-base font-semibold text-slate-900"
                  />
                </div>
              </div>

              {/* Activity Level */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-2">ระดับกิจกรรมทางกายภาพ</label>
                <select
                  value={activity}
                  onChange={(e) => setActivity(Number(e.target.value))}
                  className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-medium text-slate-800 focus:outline-none focus:border-black"
                >
                  <option value={1.2}>นั่งทำงาน/เรียนเป็นส่วนใหญ่ ไม่ออกกำลังกาย (x1.2)</option>
                  <option value={1.375}>ออกกำลังกายเบาๆ 1-3 วัน/สัปดาห์ (x1.375)</option>
                  <option value={1.55}>ออกกำลังกายปานกลาง 3-5 วัน/สัปดาห์ (x1.55)</option>
                  <option value={1.725}>ออกกำลังกายหนัก 6-7 วัน/สัปดาห์ (x1.725)</option>
                  <option value={1.9}>ออกกำลังกายหนักมาก / นักกีฬามหาวิทยาลัย (x1.9)</option>
                </select>
              </div>

              {/* Custom Target calories */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  เป้าหมายแคลอรี่ประจำวัน (kcal/วัน)
                </label>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    min="1000"
                    max="5000"
                    step="50"
                    value={targetCalories}
                    onChange={(e) => setTargetCalories(Number(e.target.value))}
                    className="input-underline text-base font-bold text-slate-900 flex-1"
                  />
                  <button
                    type="button"
                    onClick={calculateCalories}
                    className="px-3 py-1.5 rounded-lg border border-slate-200 text-xs text-slate-600 hover:bg-slate-50 cursor-pointer"
                  >
                    ตั้งตาม TDEE ({tdee})
                  </button>
                </div>
              </div>

              {/* Submit / Save button */}
              <div className="pt-2">
                <button
                  type="submit"
                  disabled={saving}
                  className="w-full py-3 px-6 rounded-full bg-black text-white text-xs font-medium flex items-center justify-center gap-2 hover:bg-slate-800 transition-all cursor-pointer shadow-md disabled:opacity-50"
                >
                  {saving ? (
                    <span className="material-symbols-outlined animate-spin text-base">progress_activity</span>
                  ) : (
                    <>
                      <Save className="w-4 h-4" />
                      <span>บันทึกและคำนวณแคลอรี่</span>
                    </>
                  )}
                </button>
              </div>

              {savedSuccess && (
                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>บันทึกข้อมูลร่างกายและเป้าหมายแคลอรี่เรียบร้อยแล้ว</span>
                </div>
              )}
            </form>
          </div>
        </div>

        {/* Results Card */}
        <div className="lg:col-span-5 space-y-6">
          <div className="liquid-card p-6 sm:p-8 border border-white/60 shadow-lg text-slate-900">
            <div className="flex items-center gap-2 mb-4">
              <Flame className="w-5 h-5 text-orange-500" />
              <h3 className="text-base font-bold">ผลการคำนวณโภชนาการ</h3>
            </div>

            <div className="space-y-4">
              {/* BMR */}
              <div className="glass-inner p-4 rounded-xl">
                <div className="text-xs text-slate-500 mb-1">BMR (Basal Metabolic Rate)</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-slate-900">{bmr}</span>
                  <span className="text-xs font-medium text-slate-500">kcal / วัน</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  พลังงานขั้นต่ำที่ร่างกายต้องการสำหรับการทำงานของอวัยวะภายในขณะพัก
                </p>
              </div>

              {/* TDEE */}
              <div className="glass-inner p-4 rounded-xl">
                <div className="text-xs text-slate-500 mb-1">TDEE (Total Daily Energy Expenditure)</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-orange-600">{tdee}</span>
                  <span className="text-xs font-medium text-slate-500">kcal / วัน</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  พลังงานทั้งหมดที่เผาผลาญในแต่ละวัน รวมกิจกรรมทางกายภาพ
                </p>
              </div>

              {/* Calorie Goal */}
              <div className="p-4 rounded-xl bg-black text-white shadow-md">
                <div className="text-xs text-slate-300 mb-1 flex items-center justify-between">
                  <span>เป้าหมายแคลอรี่ของคุณ</span>
                  <Award className="w-4 h-4 text-amber-400" />
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-amber-300">{targetCalories}</span>
                  <span className="text-xs font-medium text-slate-300">kcal / วัน</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-2 border-t border-slate-800 pt-2">
                  ใช้เป็นเป้าหมายในระบบคำนวณและการบันทึกโภชนาการรายวัน
                </p>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-200 flex justify-between items-center text-xs text-slate-500">
              <span>สูตร Mifflin-St Jeor</span>
              <button
                type="button"
                onClick={onNavigateToDashboard}
                className="font-medium text-black hover:underline flex items-center gap-1 cursor-pointer"
              >
                <span>บันทึกอาหารวันนี้</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
