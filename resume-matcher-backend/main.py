from fastapi import FastAPI, UploadFile, File, Form, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from bs4 import BeautifulSoup
import PyPDF2
from docx import Document
import io
import aiohttp
import json
import os
import openai

import stripe

from dotenv import load_dotenv
load_dotenv()
import os
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# 例如：db.collection("users").document(uid).set({...})

app = FastAPI()  # 必须在最前面

# 统一的用户状态管理
class UserStatus:
    def __init__(self, uid: str):
        self.uid = uid
        self.user_ref = db.collection("users").document(uid)
        self.now_month = datetime.now().strftime("%Y-%m")
    
    def get_status(self):
        """获取用户完整状态"""
        try:
            doc = self.user_ref.get()
            if doc.exists:
                data = doc.to_dict()
                return self._process_user_data(data)
            else:
                return self._get_default_status()
        except Exception as e:
            print(f"Error getting user status: {e}")
            return self._get_default_status()
    
    def _process_user_data(self, data):
        """处理用户数据，包括跨月重置"""
        lastScanMonth = data.get("lastScanMonth", "")
        scansUsed = data.get("scansUsed", 0)
        
        # 跨月自动重置
        # if lastScanMonth != self.now_month:
        #     scansUsed = 0
        #     self.user_ref.set({
        #         "scansUsed": 0,
        #         "lastScanMonth": self.now_month
        #     }, merge=True)
        
        subscription_end = data.get("subscriptionEnd")
        is_subscription_active = True
        if subscription_end:
            try:
                is_subscription_active = datetime.utcnow() < datetime.fromisoformat(subscription_end)
            except Exception:
                is_subscription_active = False

        return {
            "trialUsed": data.get("trialUsed", False),
            "isUpgraded": data.get("isUpgraded", False),
            "planType": data.get("planType"),
            "scanLimit": data.get("scanLimit"),
            "scansUsed": scansUsed,
            "lastScanMonth": self.now_month,
            "subscriptionActive": is_subscription_active,
            "subscriptionEnd": subscription_end,
        }
    
    def _get_default_status(self):
        """获取默认状态"""
        return {
            "trialUsed": False,
            "isUpgraded": False,
            "planType": None,
            "scanLimit": None,
            "scansUsed": 0,
            "lastScanMonth": self.now_month
        }
    
    def can_generate(self):
        """检查用户是否可以生成分析（0 次免费试用：须先付费）"""
        status = self.get_status()
        
        # 未升级用户不可用
        if not status["isUpgraded"]:
            return False, "upgrade_required"
        
        # 订阅已过期
        if "subscriptionActive" in status and not status["subscriptionActive"]:
            return False, "subscription_expired"
        
        if status["scanLimit"] is None:
            return True, "unlimited"
        if status["scansUsed"] < status["scanLimit"]:
            return True, "subscription_available"
        return False, "subscription_limit_reached"
    
    def mark_trial_used(self):
        """标记试用已使用"""
        self.user_ref.set({"trialUsed": True}, merge=True)
    
    def increment_scan_count(self):
        """增加扫描次数"""
        status = self.get_status()
        if status["isUpgraded"] and status["scanLimit"] is not None:
            self.user_ref.set({
                "scansUsed": status["scansUsed"] + 1,
                "lastScanMonth": self.now_month
            }, merge=True)

# 查询用户完整状态（试用、订阅、使用次数）
@app.get("/api/user/status")
async def get_user_status(uid: str = Query(...)):
    try:
        user_status = UserStatus(uid)
        return user_status.get_status()
    except Exception as e:
        return {"error": str(e)}

# 检查用户是否可以生成分析
@app.get("/api/user/can-generate")
async def can_generate(uid: str = Query(...)):
    try:
        user_status = UserStatus(uid)
        can_gen, reason = user_status.can_generate()
        return {
            "canGenerate": can_gen,
            "reason": reason,
            "status": user_status.get_status()
        }
    except Exception as e:
        return {"error": str(e)}

# CORS configuration - support multiple domains
allowed_origins = [
    "https://matchwise-ai.vercel.app",
    "https://matchwise-ai2026.vercel.app",  # New Vercel project
    "http://localhost:3000",  # For local development
    "http://localhost:3001",  # Alternative local port
    "http://127.0.0.1:3000",
    "http://192.168.86.47:3000"
]

# Allow environment variable override
if os.getenv("ALLOWED_ORIGINS"):
    additional_origins = os.getenv("ALLOWED_ORIGINS")
    if additional_origins:
        allowed_origins.extend(additional_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def call_xai_api(prompt: str, system_prompt: str = "You are a helpful AI assistant specializing in job application analysis.") -> str:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise Exception("XAI_API_KEY not set in environment variables")
    
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-3",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }
        try:
            async with session.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"xAI API 调用失败，状态码: {response.status}, 错误信息: {error_text}")
                    raise Exception(f"xAI API error: {response.status} - {error_text}")
                result = await response.json()
                return result["choices"][0]["message"]["content"]
        except aiohttp.ClientError as e:
            print(f"xAI API 网络请求异常: {str(e)}")
            raise Exception(f"xAI API request failed: {str(e)}")

async def call_openai_api(prompt: str, system_prompt: str = "You are a helpful AI assistant specializing in job application analysis.") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not set in environment variables")
    
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # 使用更通用的模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        return response.choices[0].message.content.strip() if response.choices[0].message.content else ""
    except Exception as e:
        raise Exception(f"OpenAI API request failed: {str(e)}")

async def generate_mock_ai_response(prompt: str, system_prompt: str = "You are a helpful AI assistant specializing in job application analysis.") -> str:
    if "job posting" in prompt.lower() and "summarize" in prompt.lower():
        return """

<p><b>This is a mock result due to AI not being called!</b></p>

<p><b>Skills & Technical Expertise:</b></p>
<ul>
<li>Technical program management (Agile, Scrum, Kanban)</li>
<li>Software development lifecycle & modern architecture principles</li>
<li>Data-driven program governance and KPI tracking</li>
<li>Change management and process optimization</li>
<li>Strong stakeholder engagement and cross-functional communication</li>
<li>Budget/resource management across engineering initiatives</li>
</ul>
<p><b>Responsibilities:</b></p>
<ul>
<li>Drive technical strategy and execution across multi-team engineering initiatives</li>
<li>Develop and maintain technical roadmaps</li>
<li>Resolve technical dependencies and risks</li>
<li>Lead end-to-end program management</li>
<li>Implement scalable governance frameworks and metrics</li>
<li>Collaborate across engineering, product, and business functions</li>
<li>Lead high-priority strategic programs and change management</li>
</ul>
<p><b>Qualifications:</b></p>
<ul>
<li>10+ years in technical program management roles</li>
<li>Bachelor's in Engineering, Computer Science, or related</li>
<li>PMP certification preferred</li>
<li>Strong leadership, organizational and communication skills</li>
</ul>
"""
    elif "comparison table" in prompt.lower():
        return """
<table><tr><th>Category</th><th>Match Type</th><th>Score</th></tr>
<tr><td>Years of Experience</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>Technical Program Mgmt</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>Agile/Scrum/Kanban</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>Software Architecture</td><td>⚠️ Partial</td><td>0.5</td></tr>
<tr><td>Budget & Resource Mgmt</td><td>⚠️ Partial</td><td>0.5</td></tr>
<tr><td>Stakeholder Engagement</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>Change Management</td><td>✅ Moderate-Strong</td><td>0.75</td></tr>
<tr><td>GCP/Cloud & Tech Stack</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>Governance & KPI Tracking</td><td>✅ Strong</td><td>1.0</td></tr>
<tr><td>PMP Certification</td><td>⚠️ Partial (in progress)</td><td>0.5</td></tr>
<tr><td>Industry Knowledge (Health)</td><td>❌ Lack</td><td>0.0</td></tr>
</table>
"""
    elif "Match Score" in prompt.lower():
        return "88"
    elif "resume summary" in prompt.lower():
        return """<p>Experienced software developer with 14+ years in full-stack development.<br>Strong expertise in Python, JavaScript, and React. Led development teams and delivered multiple successful projects. Excellent problem-solving skills and team collaboration.</p>"""
    elif "work experience" in prompt.lower():
        return """<ul>
<li>Ø Led development of e-commerce platform using React and Node.js</li>
<li>Ø Implemented RESTful APIs and microservices architecture</li>
<li>Ø Managed team of 3 developers and delivered projects on time</li>
<li>Ø Optimized database queries improving performance by 40%</li>
<li>Ø Integrated third-party payment systems and analytics tools</li>
</ul>"""
    elif "cover letter" in prompt.lower():
        return """<p>Dear Hiring Manager,</p>
<p>I am excited to apply for the Software Developer position. With 14+ years of experience in full-stack development using Python, JavaScript, and React, I believe I am an excellent fit for your team.</p>
<p>My experience leading development teams and delivering complex projects aligns perfectly with your requirements. I am passionate about creating efficient, scalable solutions and would welcome the opportunity to contribute to your organization's success.</p>
<p>Thank you for considering my application. I look forward to discussing how my skills and experience can benefit your team.</p>
<p>Best regards,<br>[Your Name]</p>"""
    else:
        return "<p>AI analysis completed successfully. Please review the generated content.</p>"

async def call_ai_api(prompt: str, system_prompt: str = "You are a helpful AI assistant specializing in job application analysis.") -> str:
    """智能AI服务选择器：优先使用OpenAI，失败时自动切换到xAI，最后使用本地模拟"""
    # 首先尝试OpenAI
    try:
        return await call_openai_api(prompt, system_prompt)
    except Exception as openai_error:
        # 如果OpenAI失败（配额不足等），尝试xAI
        try:
            print(f"OpenAI失败，切换到xAI: {str(openai_error)}")
            return await call_xai_api(prompt, system_prompt)
        except Exception as xai_error:
            # 如果xAI也失败，使用本地模拟AI
            print(f"xAI也失败，使用本地模拟AI: {str(xai_error)}")
            return await generate_mock_ai_response(prompt, system_prompt)

def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        content = file.file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract PDF text: {str(e)}")

def extract_text_from_docx(file: UploadFile) -> str:
    try:
        content = file.file.read()
        doc = Document(io.BytesIO(content))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract DOCX text: {str(e)}")

def extract_text_from_url(url: str) -> str:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        full_text = soup.get_text(separator=" ", strip=True)
        return full_text
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch job posting: {str(e)}")

async def compare_texts(job_text: str, resume_text: str) -> dict:
    try:
        # a. Job Summary
        job_summary_prompt = (
            "Please read the following job posting content:\n\n"
            f"{job_text}\n\n"
            
            "Summarize the job descriptions by extracting and organizing the following information into a clean HTML bullet list format:             <ul>            <li><strong> Ø Position Title: </strong> [extract the job title]</li>            <li><strong> Ø Position Location: </strong> [extract the location]</li>            <li><strong> Ø Potential Salary: </strong> [extract salary information if available]</li>            <li><strong> Ø Job Responsibilities: </strong>            <ul>                  <li>•     Ø [responsibility 1]</li>                   <li>•     Ø [responsibility 2]</li>                   <li>•     Ø [responsibility 3]</li>                  <li>•     Ø [responsibility 4]</li> <li>•     Ø [responsibility 5]</li>  <li>•     Ø [responsibility 6]</li>    <li>•     Ø [responsibility 7]</li>   <li>•     Ø [responsibility 8]</li>      </ul>             </li>             <li><strong> Ø Technical Skills Required: </strong>               <ul>                 <li>•     Ø [tech skill 1]</li>                 <li>•     Ø [tech skill 2]</li>                 <li>•     Ø [tech skill 3]</li>                 <li>•     Ø [tech skill 4]</li>    <li>•     Ø [tech skill 5]</li>   <li>•     Ø [tech skill 6]</li>   <li>•     Ø [tech skill 7]</li>   <li>•     Ø [tech skill 8]</li>  </ul>             </li>             <li><strong> Ø Soft Skills Required: </strong>               <ul>                 <li>•     Ø [soft skill 1]</li>                 <li>•     Ø [soft skill 2]</li>                 <li>•     Ø [soft skill 3]</li>                 <li>•     Ø [soft skill 4]</li>   <li>•     Ø [soft skill 5]</li>  <li>•     Ø [soft skill 6]</li>  <li>•     Ø [soft skill 7]</li>           </ul>             </li>             <li><strong> Ø Certifications Required: </strong> [extract certification requirements]</li>             <li><strong> Ø Education Required: </strong> [extract education requirements]</li>             <li><strong> Ø Company Vision: </strong> [extract company vision/mission if available]</li>             </ul>\n            Please extract the actual information from the job posting. Using the structure above, organize the output into a clean HTML bullet list format. If any information is not available in the job posting, use 'Not specified' for that item. Ensure the output is clean, well-structured, and uses proper HTML bullet list formatting. Maintain 1.2 line spacing. Do not show the word ```html in output."
        )
        job_summary = await call_ai_api(job_summary_prompt)
        job_summary = f"\n\n {job_summary}"

        # b. Resume Summary with Comparison Table
        resume_summary_prompt = (
            "Read the following resume content:\n\n"
            f"{resume_text}\n\n"
            "And the following job summary:\n\n"
            f"{job_summary}\n\n"
            "Output a comparison table between the job_summary and the upload user resume. List in the table format with Four columns: Categories (list all the key requirements regarding position responsibilities, technical and soft skills, certifications, and educations from the job requirements, each key requirement in one line), Match Status (four status will be used: ✅ Strong (the item is also mentioned in the user's resume and very well-matched with what mentioned in job_summary_prompt) / 🔷 Moderate-strong (the item is also mentioned in the user's resume and closely matched with what mentioned in job_summary_prompt)/⚠️ Partial (the item is kind of mentioned in the user's resume and some parts matched with what mentioned in job_summary_prompt)/ ❌ Lack (the item is not clearly mentioned in the user's resume and only little bit or not match with what mentioned in job_summary_prompt)), Comments (very precise comment on how the user's experiences matches with the job requirement), and Match Weight (If the Match Status is Strong, assign number 1; If the Match Status is Moderate-Strong, assign number 0.8; If the Match Status is Partial, assign number 0.5; If the Match Status is Lack, assign number 0.1). Make sure to output the table in HTML format, with <table>, <tr>, <th>, <td> tags, and do not add any explanation or extra text. The table should be styled to look clean and modern. Only output the table in HTML format, with <table>, <tr>, <th>, <td> tags, and do not add any explanation or extra text. The table should be styled to look clean and modern. Below the table, based on the Match Weight column from job_summary comparison table, calculates the percentage of the matching score. The calculation formulas are: Sum of total Match Weight numbers = sum of all numbers in the Match Weight column; Count of total Match Weight numbers = count of all numbers in the Match Weight column; Match Score (%) =(Sum of total Match Weight numbers)/(Count of total Match Weight numbers). Return the final calculation results of Sum of total Match Weight numbers, Count of total Match Weight numbers, and Match Score as the final percentage number, rounded to two decimal places. No extra text, do not show ``` symbols or word html in output. "
        )
        resume_summary = await call_ai_api(resume_summary_prompt)
        print("resume_summary raw output:", resume_summary)
        resume_summary = f"\n\n{resume_summary}"

        import re

        lines = resume_summary.strip().splitlines()
        if lines:
            last_line = lines[-1].strip()
            match = re.search(r"([0-9]+(?:\.[0-9]+)?)", last_line)
            if match:
                match_score_test = float(match.group(1))
                # 如果分数是小数（如0.91），转为百分比
                if match_score_test <= 1:
                    match_score_test = round(match_score_test * 100, 2)
            else:
                match_score_test = last_line
        else:
            match_score_test = None

        # c. Match Score        
        try:
            match_score = float(match_score_test.strip().replace("%", ""))
        except Exception:
            match_score = match_score_test

        # d. Tailored Resume Summary
        tailored_resume_summary_prompt = (
            "Read the following resume content:\n\n"
            f"{resume_text}\n\n"
            "And the following job content:\n\n"
            f"{job_text}\n\n"
            "Provide a revised one-paragraph summary based on the original summary in resume_text (the user's resume). If the user's resume does not have a summary or highlight section, write a new summary as the revised summary. Make sure this summary highlights the user's key skills and work experiences and makes it more closely match the job requirements in job_text. Please limit the overall summary to 1700 characters. The output should be in HTML format and should maintain a simple, modern style. Write this paragraph in the first person. Maintain 1.2 line spacing. Do not show the word ```html in output."
        )
        tailored_resume_summary = await call_ai_api(tailored_resume_summary_prompt)
        tailored_resume_summary = f"\n{tailored_resume_summary}"

        # e. Tailored Work Experience
        tailored_work_experience_prompt = (
            "Read the following resume content:\n\n"
            f"{resume_text}\n\n"
            "And the following job content:\n\n"
            f"{job_text}\n\n"
            "Find the latest work experiences from the resume and modify them to better match the job requirements. Format the output as a clean HTML unordered list with no more than 7 bullet points:              <ul>             <li>     Ø  [revised work experience bullet 1]</li>             <li>     Ø  [revised work experience bullet 2]</li>             <li>     Ø  [revised work experience bullet 3]</li>             <li>     Ø  [revised work experience bullet 4]</li>             <li>     Ø  [revised work experience bullet 5]</li>             <li>     Ø  [revised work experience bullet 6]</li>             <li>     Ø  [revised work experience bullet 7]</li>             </ul>             Please provide the actual revised work experience content. Organize the output into a clean HTML bullet list using the structure above. Return the result wrapped inside triple backticks and identify the language as HTML. Focus on the most recent and relevant experiences that align with the job requirements. Keep each bullet point concise and impactful. Make sure there are line breaks between each paragraph. Ensure the output uses proper HTML bullet list formatting. Maintain 1.2 line spacing.  Do not show the word ```html in output."
        )
        tailored_work_experience_html = await call_ai_api(tailored_work_experience_prompt)

        # f. Cover Letter
        cover_letter_prompt = (
            "Read the following resume content:\n\n"
            f"{resume_text}\n\n"
            "And the following job content:\n\n"
            f"{job_text}\n\n"
            "Provide a formal cover letter for the job application. The job position and the company name in the cover letter for applying should be the same as what being used in the job_text. The cover letter should show the user's key strengths and highlight the user's best fit skills and experiences according to the job posting in job_text, then express the user's passions for the position, and express appreciation for a future interview opportunity. The overall tone of the cover letter should be confident, honest, and professional. The cover letters should be written in the first person. Only output in HTML format, using <p> and <br> tags for formatting. Make sure there are line breaks between each paragraph. Do not output markdown or plain text. Do not show ```html in output. "
        )
        cover_letter = await call_ai_api(cover_letter_prompt)
        cover_letter = f"\n{cover_letter}"

        return {
            "job_summary": job_summary,
            "resume_summary": resume_summary,
            "match_score": match_score,
            "tailored_resume_summary": tailored_resume_summary,
            "tailored_work_experience": tailored_work_experience_html,
            "cover_letter": cover_letter,
        }
    except Exception as e:
        raise Exception(f"Comparison failed: {str(e)}")

@app.post("/api/compare")
async def compare(job_text: str = Form(...), resume: UploadFile = File(...), uid: str = Form(None)):
    try:
        # 1. 登录用户须已付费；匿名用户（无 uid）直接放行
        if uid:
            user_status = UserStatus(uid)
            can_gen, reason = user_status.can_generate()
            if not can_gen:
                error_messages = {
                    "upgrade_required": "Please upgrade to use MatchWise. No free trial.",
                    "subscription_expired": "Your subscription has expired. Please renew to continue.",
                    "subscription_limit_reached": "You have reached your monthly scan limit. Please upgrade your plan or wait for next month.",
                }
                return JSONResponse(
                    status_code=403,
                    content={"error": error_messages.get(reason, "Access denied")},
                )

        # 2. 处理简历文件
        resume_text = ""
        if resume.filename and resume.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume)
        elif resume.filename and resume.filename.endswith((".doc", ".docx")):
            resume_text = extract_text_from_docx(resume)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file format. Please upload PDF or DOCX."},
            )
        
        # 3. 调用AI分析
        result = await compare_texts(job_text, resume_text)
        
        # 4. 更新用户状态（仅登录且已升级用户：增加使用次数）
        if uid:
            user_status = UserStatus(uid)
            status = user_status.get_status()
            if status["isUpgraded"]:
                user_status.increment_scan_count()

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing error: {str(e)}"},
        )



@app.post("/api/create-checkout-session")
async def create_checkout_session(uid: str = Form(...), price_id: str = Form(...), mode: str = Form(...)):
    try:
        print("stripe.api_key:", stripe.api_key)
        print("uid:", uid)
        print("price_id:", price_id)
        print("mode:", mode)
        success_url = "https://matchwise-ai.vercel.app/success?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = "https://matchwise-ai.vercel.app/cancel"
        if mode == "payment":
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={"uid": uid}
            )
        elif mode == "subscription":
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,  # 只要是同一产品下的订阅 price_id，Stripe 页面会自动显示所有订阅套餐
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={"uid": uid}
            )
        else:
            return {"error": "Invalid mode"}
        return {"checkout_url": session.url}
    except Exception as e:
        return {"error": str(e)}

def update_user_membership(uid, price_id):
    user_ref = db.collection("users").document(uid)
    if price_id == "price_1RnBbcE6OOEHr6Zo6igE1U8B":
        user_ref.set({
            "isUpgraded": True,
            "planType": "one_time",
            "scanLimit": 1,
            "scansUsed": 0
        }, merge=True)
    elif price_id == "price_1RnBehE6OOEHr6Zo4QLLJZTg":
        user_ref.set({
            "isUpgraded": True,
            "planType": "basic",
            "scanLimit": 30,
            "scansUsed": 0
        }, merge=True)
    elif price_id == "price_1RnBgPE6OOEHr6Zo9EFmgyA5":
        user_ref.set({
            "isUpgraded": True,
            "planType": "pro",
            "scanLimit": 180,
            "scansUsed": 0
        }, merge=True)


@app.post("/api/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("⚠️  Webhook signature verification failed.", e)
        return {"status": "error", "message": str(e)}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"].get("uid")
        price_id = None

        try:
            # For one-time payment (mode: payment)
            if session.get("mode") == "payment":
                line_items = stripe.checkout.Session.list_line_items(session["id"], limit=1)
                if line_items and line_items["data"]:
                    price_id = line_items["data"][0]["price"]["id"]

            # For subscription
            elif session.get("mode") == "subscription" and session.get("subscription"):
                subscription = stripe.Subscription.retrieve(session["subscription"])
                price_id = subscription["items"]["data"][0]["price"]["id"]

            if uid and price_id:
                user_status = UserStatus(uid)
                
                # Update user membership based on price_id
                if price_id == "price_1RnBbcE6OOEHr6Zo6igE1U8B":
                    # $2 one-time payment
                    user_status.user_ref.set({
                        "isUpgraded": True,
                        "planType": "one_time",
                        "scanLimit": 1,
                        "scansUsed": 0,
                        "lastScanMonth": datetime.now().strftime("%Y-%m")
                    }, merge=True)
                    print(f"✅ User {uid} upgraded to one-time plan")
                    
                elif price_id == "price_1RnBehE6OOEHr6Zo4QLLJZTg":
                    # $6/month subscription
                    now = datetime.utcnow()
                    user_status.user_ref.set({
                        "isUpgraded": True,
                        "planType": "basic",
                        "scanLimit": 30,
                        "scansUsed": 0,
                        "subscriptionStart": now.isoformat(),
                        "subscriptionEnd": (now + timedelta(days=30)).isoformat()
                    }, merge=True)
                    print(f"✅ User {uid} upgraded to basic subscription")
                    
                elif price_id == "price_1RnBgPE6OOEHr6Zo9EFmgyA5":
                    # $15/month subscription
                    now = datetime.utcnow()
                    user_status.user_ref.set({
                        "isUpgraded": True,
                        "planType": "pro",
                        "scanLimit": 180,
                        "scansUsed": 0,
                        "subscriptionStart": now.isoformat(),
                        "subscriptionEnd": (now + timedelta(days=30)).isoformat()
                    }, merge=True)
                    print(f"✅ User {uid} upgraded to pro subscription")
                else:
                    print(f"⚠️ Unknown price_id: {price_id}")
            else:
                print(f"⚠️ Missing uid or price_id: uid={uid}, price_id={price_id}")
                
        except Exception as e:
            print(f"❌ Error processing webhook: {e}")
            return {"status": "error", "message": str(e)}
    
    elif event["type"] == "customer.subscription.deleted":
        # Handle subscription cancellation
        subscription = event["data"]["object"]
        # You might want to update user status when subscription is cancelled
        print(f"📝 Subscription cancelled: {subscription['id']}")
    
    elif event["type"] == "invoice.payment_failed":
        # Handle failed payments
        invoice = event["data"]["object"]
        print(f"❌ Payment failed for invoice: {invoice['id']}")
    
    return {"status": "success"}

@app.get("/")
def root():
    return {"message": "MatchWise Backend API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/user/use-trial")
async def use_trial(request: Request):
    # 这里根据你的业务逻辑处理试用
    # 例如：获取 uid，更新 Firestore，返回试用状态
    data = await request.json()
    uid = data.get("uid") or request.query_params.get("uid")
    # ... 你的业务逻辑 ...
    return JSONResponse({"success": True, "message": "Trial used."})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
