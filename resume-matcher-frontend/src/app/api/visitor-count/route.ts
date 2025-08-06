import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

const VISITOR_COUNT_FILE = path.join(process.cwd(), 'visitor-count.json');

interface VisitorData {
  count: number;
  lastUpdated: string;
}

// 内存存储作为Vercel环境的临时解决方案
let memoryVisitorData: VisitorData | null = null;

async function getVisitorCount(): Promise<VisitorData> {
  // 首先尝试从内存获取
  if (memoryVisitorData) {
    console.log('✅ Using memory visitor count:', memoryVisitorData);
    return memoryVisitorData;
  }

  try {
    console.log('📁 Attempting to read visitor count file:', VISITOR_COUNT_FILE);
    const data = await fs.readFile(VISITOR_COUNT_FILE, 'utf-8');
    const parsedData = JSON.parse(data);
    console.log('✅ Successfully read visitor count from file:', parsedData);
    
    // 将文件数据加载到内存
    memoryVisitorData = parsedData;
    return parsedData;
  } catch (error) {
    console.log('⚠️ Failed to read visitor count file, creating new one:', error);
    // 如果文件不存在，返回初始值（设置为116以保持现有计数）
    const initialData = {
      count: 116,
      lastUpdated: new Date().toISOString()
    };
    
    // 尝试创建文件
    try {
      await fs.writeFile(VISITOR_COUNT_FILE, JSON.stringify(initialData, null, 2));
      console.log('✅ Created new visitor count file');
    } catch (writeError) {
      console.error('❌ Failed to create visitor count file:', writeError);
      console.log('⚠️ Using memory-only storage for Vercel environment');
    }
    
    // 将初始数据加载到内存
    memoryVisitorData = initialData;
    return initialData;
  }
}

async function updateVisitorCount(): Promise<VisitorData> {
  console.log('🔄 Updating visitor count...');
  const currentData = await getVisitorCount();
  const newData: VisitorData = {
    count: currentData.count + 1,
    lastUpdated: new Date().toISOString()
  };
  
  console.log('📊 Current count:', currentData.count, '-> New count:', newData.count);
  
  // 更新内存数据
  memoryVisitorData = newData;
  
  // 尝试写入文件（在Vercel中可能会失败，但不影响功能）
  try {
    await fs.writeFile(VISITOR_COUNT_FILE, JSON.stringify(newData, null, 2));
    console.log('✅ Successfully updated visitor count file');
  } catch (error) {
    console.error('❌ Failed to write visitor count file:', error);
    console.log('⚠️ Using memory-only storage - count will reset on deployment');
  }
  
  return newData;
}

export async function GET() {
  console.log('📡 GET /api/visitor-count called');
  try {
    const visitorData = await getVisitorCount();
    console.log('✅ GET response:', visitorData);
    return NextResponse.json(visitorData);
  } catch (error) {
    console.error('❌ GET error:', error);
    return NextResponse.json(
      { error: 'Failed to get visitor count', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function POST() {
  console.log('📡 POST /api/visitor-count called');
  try {
    const visitorData = await updateVisitorCount();
    console.log('✅ POST response:', visitorData);
    return NextResponse.json(visitorData);
  } catch (error) {
    console.error('❌ POST error:', error);
    return NextResponse.json(
      { error: 'Failed to update visitor count', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
} 