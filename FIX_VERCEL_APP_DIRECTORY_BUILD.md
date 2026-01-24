# Fix: "Couldn't find any `pages` or `app` directory" — Vercel Build Error

## Root cause

Vercel is building from the **repository root** instead of the Next.js app folder.

- The Next.js app (with `src/app/`) lives in **`resume-matcher-frontend/`**.
- The repo root has no `app` or `pages` directory, so `next build` fails.

## Fix: Set Root Directory in Vercel

1. Open your Vercel project:
   - https://vercel.com/emma-wangs-projects/matchwise-ai_2026/settings  
   - Or: **Dashboard → matchwise-ai** (or your project) → **Settings**.

2. Go to **Build and Deployment** → **Root Directory**.

3. Set **Root Directory** to:
   ```
   resume-matcher-frontend
   ```
   (No leading/trailing slash.)

4. Click **Save**.

5. **Redeploy**:
   - **Deployments** → select the latest deployment → **Redeploy**,
   - Or push a new commit to trigger a deploy.

## Verify

After redeploy, the build should:

- Run from `resume-matcher-frontend/`
- Find `src/app/` and run `next build` successfully.

## About the F12 / console errors

- **React #418 (hydration)**  
  Often from a broken or error page (e.g. failed deploy). Fixing the build usually resolves it.

- **api.knock.app 429**  
  Vercel / Knock notification rate limiting. Unrelated to your app.

- **Pusher / Sentry 429**  
  Same: third‑party services, not your MatchWise code.

Focus on fixing the **Root Directory** and **build** first; then re-check the app.
