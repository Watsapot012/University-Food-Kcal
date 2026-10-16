/**
 * Test Suite สำหรับระบบ University Food Kcal
 * รันด้วยคำสั่ง: npm test หรือ npx tsx tests/run_tests.ts
 */

import http from 'http';
import { createServerApp } from '../src/serverApp.js';

interface TestResult {
  name: string;
  category: string;
  passed: boolean;
  message?: string;
  durationMs: number;
}

const results: TestResult[] = [];

function assert(condition: boolean, message: string) {
  if (!condition) {
    throw new Error(message);
  }
}

async function runTestCase(name: string, category: string, fn: () => Promise<void> | void) {
  const start = Date.now();
  try {
    await fn();
    const duration = Date.now() - start;
    results.push({ name, category, passed: true, durationMs: duration });
    console.log(`  \x1b[32m✔ [ผ่าน]\x1b[0m ${name} (${duration}ms)`);
  } catch (err: any) {
    const duration = Date.now() - start;
    results.push({ name, category, passed: false, message: err.message, durationMs: duration });
    console.log(`  \x1b[31m✖ [ไม่ผ่าน]\x1b[0m ${name}: ${err.message}`);
  }
}

// Helper ส่ง request ไปยัง Express server
function requestHelper(server: http.Server, path: string, method = 'GET', body?: any): Promise<{ status: number; headers: http.IncomingHttpHeaders; body: any }> {
  return new Promise((resolve, reject) => {
    const addr = server.address();
    if (!addr || typeof addr === 'string') {
      return reject(new Error('Server address not available'));
    }

    const payload = body ? JSON.stringify(body) : null;
    const req = http.request(
      {
        hostname: '127.0.0.1',
        port: addr.port,
        path,
        method,
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          ...(payload ? { 'Content-Length': Buffer.byteLength(payload) } : {}),
        },
      },
      (res) => {
        let rawData = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          rawData += chunk;
        });
        res.on('end', () => {
          let parsed = rawData;
          try {
            parsed = JSON.parse(rawData);
          } catch {
            // keep raw string
          }
          resolve({ status: res.statusCode || 0, headers: res.headers, body: parsed });
        });
      }
    );

    req.on('error', reject);
    if (payload) {
      req.write(payload);
    }
    req.end();
  });
}

// ตรวจสอบภาษาไทยว่าไม่มี Mojibake (เช่น à¸ หรือ เธ)
function isThaiClean(text: string): boolean {
  if (!text) return true;
  // Mojibake patterns
  const mojibakePatterns = [
    /à¸/, /à¹/, /Ã/, /Â/, /เธ‚/, /เน‰/, /เธ/
  ];
  return !mojibakePatterns.some(pattern => pattern.test(text));
}

// ฟังก์ชันคำนวณ BMR
function calculateBMR(weight: number, height: number, age: number, gender: 'male' | 'female'): number {
  if (gender === 'male') {
    return Math.round(10 * weight + 6.25 * height - 5 * age + 5);
  }
  return Math.round(10 * weight + 6.25 * height - 5 * age - 161);
}

// ฟังก์ชันคำนวณ TDEE
function calculateTDEE(bmr: number, activityMultiplier: number): number {
  return Math.round(bmr * activityMultiplier);
}

async function main() {
  console.log('\n======================================================');
  console.log('🧪 เริ่มต้นการรันชุดทดสอบ (Run Tests) - University Food Kcal');
  console.log('======================================================\n');

  const app = createServerApp();
  const server = http.createServer(app);

  await new Promise<void>((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve());
  });

  try {
    console.log('\x1b[36m--- หมวดที่ 1: ตรวจสอบ API Endpoints พื้นฐาน ---\x1b[0m');

    await runTestCase('GET /api/health คืนค่า status 200 และระบบ online', 'API', async () => {
      const res = await requestHelper(server, '/api/health');
      assert(res.status === 200, `คาดหวัง 200 แต่ได้ ${res.status}`);
      assert(res.body.status === 'online', 'สถานะระบบต้องเป็น online');
      assert(typeof res.body.service === 'string', 'ต้องมีชื่อ service');
    });

    await runTestCase('GET /api/restaurants คืนค่ารายการร้านอาหารในมหาวิทยาลัย', 'API', async () => {
      const res = await requestHelper(server, '/api/restaurants');
      assert(res.status === 200, `คาดหวัง 200 แต่ได้ ${res.status}`);
      assert(Array.isArray(res.body), 'ข้อมูลร้านค้าต้องเป็น Array');
      assert(res.body.length > 0, 'ต้องมีข้อมูลร้านค้าอย่างน้อย 1 ร้าน');
      const first = res.body[0];
      assert(first.name && first.location, 'ร้านค้าต้องมีชื่อและสถานที่ตั้ง');
    });

    await runTestCase('GET /api/foods คืนค่ารายการอาหารและค่าสารอาหารครบถ้วน', 'API', async () => {
      const res = await requestHelper(server, '/api/foods');
      assert(res.status === 200, `คาดหวัง 200 แต่ได้ ${res.status}`);
      assert(Array.isArray(res.body), 'ข้อมูลอาหารต้องเป็น Array');
      assert(res.body.length > 0, 'ต้องมีข้อมูลเมนูอาหารในระบบ');
      const sample = res.body[0];
      assert(typeof sample.kcal === 'number', 'แคลอรี่ต้องเป็นตัวเลข');
      assert(typeof sample.protein === 'number', 'โปรตีนต้องเป็นตัวเลข');
      assert(typeof sample.fat === 'number', 'ไขมันต้องเป็นตัวเลข');
      assert(typeof sample.carbohydrate === 'number', 'คาร์โบไฮเดรตต้องเป็นตัวเลข');
    });

    await runTestCase('GET /api/stats คืนค่าสถิติรวมของระบบ', 'API', async () => {
      const res = await requestHelper(server, '/api/stats');
      assert(res.status === 200, `คาดหวัง 200 แต่ได้ ${res.status}`);
      assert(typeof res.body.total_restaurants === 'number', 'ต้องมีจำนวนร้านทั้งหมด');
      assert(typeof res.body.total_foods === 'number', 'ต้องมีจำนวนเมนูทั้งหมด');
      assert(typeof res.body.avg_kcal === 'number', 'ต้องมีค่าเฉลี่ยแคลอรี่');
    });

    console.log('\n\x1b[36m--- หมวดที่ 2: ตรวจสอบการรองรับภาษาไทย (Thai UTF-8 Encoding) ---\x1b[0m');

    await runTestCase('ตรวจสอบ Header Content-Type รองรับ UTF-8 ภาษาไทย', 'Encoding', async () => {
      const res = await requestHelper(server, '/api/restaurants');
      const contentType = res.headers['content-type'] || '';
      assert(contentType.includes('utf-8') || contentType.includes('UTF-8'), `Content-Type ควรมี UTF-8: ${contentType}`);
    });

    await runTestCase('ชื่อร้านอาหารและเมนูอาหารต้องเป็นภาษาไทยที่ถูกต้องและไม่มีตัวอักษรเพี้ยน (Mojibake)', 'Encoding', async () => {
      const res = await requestHelper(server, '/api/foods');
      const thaiFood = res.body.find((f: any) => /[\u0E00-\u0E7F]/.test(f.name));
      assert(!!thaiFood, 'ต้องพบรายการอาหารที่มีตัวอักษรภาษาไทย');
      for (const food of res.body.slice(0, 10)) {
        assert(isThaiClean(food.name), `ชื่ออาหาร "${food.name}" มีอักขระผิดเพี้ยน`);
        if (food.description) {
          assert(isThaiClean(food.description), `คำอธิบาย "${food.description}" มีอักขระผิดเพี้ยน`);
        }
      }
    });

    console.log('\n\x1b[36m--- หมวดที่ 3: ตรวจสอบตรรกะคำนวณโภชนาการ (Nutrition Logic) ---\x1b[0m');

    await runTestCase('ตรวจสอบสูตรแคลอรี่ (Protein*4 + Carbs*4 + Fat*9) สัมพันธ์กับค่า Kcal', 'Nutrition', async () => {
      const res = await requestHelper(server, '/api/foods');
      for (const food of res.body) {
        const calculatedKcal = food.protein * 4 + food.carbohydrate * 4 + food.fat * 9;
        // ค่าพลังงานที่คำนวณจาก macronutrients ไม่ควรห่างจาก kcal เกิน 35%
        const diff = Math.abs(calculatedKcal - food.kcal);
        assert(diff <= Math.max(food.kcal * 0.35, 60), `เมนู ${food.name} แคลอรี่ผิดปกติ: ระบุ ${food.kcal} คำนวณได้ ${calculatedKcal}`);
      }
    });

    await runTestCase('สูตรคำนวณ BMR & TDEE (Mifflin-St Jeor Formula)', 'Nutrition', () => {
      // ตัวอย่าง ผู้ชาย น้ำหนัก 70kg ส่วนสูง 175cm อายุ 22 ปี
      // BMR = 10*70 + 6.25*175 - 5*22 + 5 = 700 + 1093.75 - 110 + 5 = 1688.75 -> 1689
      const maleBmr = calculateBMR(70, 175, 22, 'male');
      assert(maleBmr === 1689, `คำนวณ BMR ชายผิด: คาดหวัง 1689 แต่ได้ ${maleBmr}`);

      // ตัวอย่าง ผู้หญิง น้ำหนัก 55kg ส่วนสูง 160cm อายุ 20 ปี
      // BMR = 10*55 + 6.25*160 - 5*20 - 161 = 550 + 1000 - 100 - 161 = 1289
      const femaleBmr = calculateBMR(55, 160, 20, 'female');
      assert(femaleBmr === 1289, `คำนวณ BMR หญิงผิด: คาดหวัง 1289 แต่ได้ ${femaleBmr}`);

      // TDEE ออกกำลังกายปานกลาง (activity = 1.55)
      const tdee = calculateTDEE(maleBmr, 1.55);
      assert(tdee === 2618, `คำนวณ TDEE ผิด: คาดหวัง 2618 แต่ได้ ${tdee}`);
    });

    console.log('\n\x1b[36m--- หมวดที่ 4: ตรวจสอบระบบค้นหาและกรองข้อมูล (Search & Filter) ---\x1b[0m');

    await runTestCase('ค้นหาอาหารด้วยคำว่า "กะเพรา"', 'Search', async () => {
      const res = await requestHelper(server, '/api/foods?search=' + encodeURIComponent('กะเพรา'));
      assert(res.status === 200, `สถานะต้องเป็น 200`);
      assert(Array.isArray(res.body), 'ผลการค้นหาต้องเป็น Array');
      if (res.body.length > 0) {
        const match = res.body.every((f: any) => f.name.includes('กะเพรา') || (f.description && f.description.includes('กะเพรา')));
        assert(match, 'ผลลัพธ์ทุกรายการต้องเกี่ยวข้องกับกะเพรา');
      }
    });

    await runTestCase('กรองอาหารตามช่วงแคลอรี่ (min_kcal=100 & max_kcal=400)', 'Search', async () => {
      const res = await requestHelper(server, '/api/foods?min_kcal=100&max_kcal=400');
      assert(res.status === 200, `สถานะต้องเป็น 200`);
      assert(Array.isArray(res.body), 'ผลการกรองต้องเป็น Array');
      for (const food of res.body) {
        assert(food.kcal >= 100 && food.kcal <= 400, `เมนู ${food.name} มี ${food.kcal} kcal ซึ่งอยู่นอกช่วง 100-400`);
      }
    });

  } finally {
    server.close();
  }

  // สรุปผล
  const total = results.length;
  const passed = results.filter((r) => r.passed).length;
  const failed = total - passed;

  console.log('\n======================================================');
  console.log('📊 สรุปผลการทดสอบ (Test Results Summary):');
  console.log(`   ทั้งหมด:   ${total} การทดสอบ`);
  console.log(`   \x1b[32mผ่าน:      ${passed} การทดสอบ\x1b[0m`);
  if (failed > 0) {
    console.log(`   \x1b[31mไม่ผ่าน:   ${failed} การทดสอบ\x1b[0m`);
  } else {
    console.log(`   \x1b[32mสถานะ:     ผ่านการทดสอบทั้งหมด 100% (All Passed! 🎉)\x1b[0m`);
  }
  console.log('======================================================\n');

  if (failed > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error('Fatal error running tests:', err);
  process.exit(1);
});
