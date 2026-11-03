# Setup traps

Things that cost real time on earlier builds. The PM reads this before asking the owner to set anything up, and words each setup request so the trap can't happen. Add a line whenever a new one bites. Keep it under 60 lines.

## Keys and settings
- **Names drift.** Owners type `SUPABASE_BE_URL` for `SUPABASE_DB_URL`, or add the key but not the URL. Give the exact name to copy, and run `tools/preflight.py` after they say "done".
- **Cloud settings only reach new sessions.** After the owner adds a variable to the cloud environment, continue in a fresh thread; the current one will never see it.
- **A setting left on test data.** A data-source switch (e.g. `DATA_SOURCE=fixture`) set during the build stays that way in production, and the live app quietly shows sample rows. Mark such settings `live` in `env.manifest` and run `preflight.py --live` before go-live.
- **A whole JSON key in one variable.** Service-account keys go in as the entire JSON file. Code should accept it pasted with or without line breaks and log the provider's refusal reason, not just "failed".
- **Telegram bot typos.** A misspelled bot name is a different bot. Check the token with `getMe` and compare the @name.

## Accounts and providers
- **Supabase sign-in email is capped** at about 2 emails an hour on the built-in sender. Set up custom SMTP (e.g. Resend with a verified domain) before inviting anyone.
- **Auth redirect lists** must include every address people sign in from: preview link, production link and any custom domain. Update `site_url` when the domain changes.
- **Google Workspace blocks service-account keys** by default on newer organisations (`iam.managed.disableServiceAccountKeyCreation`). Ask the owner to override the policy for that one project, or create the project under a personal Google account.
- **Google sheets read by a service account** must be shared with its email as Viewer.
- **Internal Google OAuth apps** must be created in the same Workspace as the inbox they read.
- **Free tiers run out mid-month** (e.g. hosting build credits). Check remaining credits before planning a redeploy on a free tier.

## Cloud sessions (Claude projects)
- No raw database connections (Postgres ports are blocked) and no Docker. Run migrations through the provider's HTTPS API (Supabase Management API) or CI; test against a local Postgres.
- Preview hosts such as `*.vercel.app` may be blocked from the container, so only the owner can open preview links.
- Long branch names truncate to the same preview alias (`claude/project-thread-*`), so an alias can show another branch. Send the production address or the deployment's own link.
- A hosting import page may always build `main`. Trigger builds by pushing the tracked branch.

## Data
- **Source sheets can mislabel things** (a "profit" column that is really revenue). Check a source's numbers against something the owner trusts before building on it.
- **Exports differ by screen.** Confirm the exact export path and download a real header row before writing an importer.
