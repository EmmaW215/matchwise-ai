import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const body = await req.text();
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com';
  const res = await fetch(`${backendUrl}/api/create-checkout-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
} 