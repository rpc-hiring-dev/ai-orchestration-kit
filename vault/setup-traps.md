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
- **Email quotas count incoming mail too.** On Resend's free plan (100 a day), inbound email shares the daily limit with outgoing. One flapping alarm sent about 350 alert emails and every app email failed for a day. When an email "didn't go out", check the app's email log for the provider's error first. Route bulk incoming mail elsewhere (e.g. Cloudflare Email Routing to a Worker).
- **Cloudflare build settings only stick after pressing Save,** and only a push to the production branch builds. Turn preview-branch builds off unless they're wanted.
- **Anthropic API keys must be workspace-scoped.** An organisation-level key gets a 400 asking for `anthropic-workspace-id`.

## Cloud sessions (Claude projects)
- No raw database connections (Postgres ports are blocked) and no Docker. Run migrations through the provider's HTTPS API (Supabase Management API) or CI; test against a local Postgres.
- Preview hosts such as `*.vercel.app` may be blocked from the container, so only the owner can open preview links.
- Long branch names truncate to the same preview alias (`claude/project-thread-*`), so an alias can show another branch. Send the production address or the deployment's own link.
- A hosting import page may always build `main`. Trigger builds by pushing the tracked branch.
- Allowed-domain changes reach running sessions within about a minute; secrets don't (see above).
- The auto-mode safety check refuses writes to secrets and sign-in settings unless the owner OK'd that exact change in the thread. Ask first, by decision card, and quote the change.
- Edge Function console logs (Supabase) come from the Management API's analytics endpoint (`/v1/projects/<ref>/analytics/endpoints/logs`, ClickHouse SQL `FROM logs WHERE source = 'function_logs'`, a window of 24 hours at most).

## Installable apps (PWA)
- **Stale copies.** A phone or PC can keep an old version through a hard refresh. Ship a `/version.json` that is never cached, check it on load, and reload to the new version at the next tap (never mid-typing); show the version in Settings. The owner's fix for an already-stuck copy: send any waiting work first, then site settings > Delete data, reload, sign in.

## Data
- **Source sheets can mislabel things** (a "profit" column that is really revenue). Check a source's numbers against something the owner trusts before building on it.
- **Exports differ by screen.** Confirm the exact export path and download a real header row before writing an importer.
