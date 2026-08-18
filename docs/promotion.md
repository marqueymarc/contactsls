# Release and promotion automation

The workflows in `.github/workflows/` are intentionally quiet until you configure them. A normal release needs only a version tag; the optional integrations need repository settings in GitHub.

## Release and Homebrew

Push an annotated tag such as `v1.0.2`. The **Release and update Homebrew** workflow validates the macOS command, creates GitHub release notes, and then updates `marqueymarc/homebrew-tap`.

For the immediate tap update, add this repository secret to `marqueymarc/contactsls`:

| Name | Value |
| --- | --- |
| `HOMEBREW_TAP_TOKEN` | A fine-grained GitHub token with **Contents: Read and write** access only to `marqueymarc/homebrew-tap`. |

Without that secret, the separate tap workflow checks the newest release once per day and updates the formula then. The token is never printed by the workflow.

## Announcements

The **Announce release** workflow runs when GitHub publishes a release. It has no outbound effect until you explicitly enable a channel with a repository variable. First use **Run workflow** with `dry_run` enabled; it prints the exact text or payload instead of publishing.

### Mastodon

| Repository setting | Value |
| --- | --- |
| Variable `PROMOTE_MASTODON` | `true` |
| Variable `MASTODON_BASE_URL` | Your instance URL, for example `https://mastodon.social` |
| Secret `MASTODON_ACCESS_TOKEN` | A posting token created in that Mastodon account |

### Bluesky

| Repository setting | Value |
| --- | --- |
| Variable `PROMOTE_BLUESKY` | `true` |
| Variable `BLUESKY_HANDLE` | The account handle, for example `name.bsky.social` |
| Secret `BLUESKY_APP_PASSWORD` | A dedicated Bluesky app password—not the account password |

### Webhook services, including LinkedIn workflows

The webhook channel sends a small JSON payload containing `project`, `tag`, `url`, and `install`. It fits a Zapier, Make, n8n, or self-hosted webhook that can then post to LinkedIn, an email list, Slack, or another service.

| Repository setting | Value |
| --- | --- |
| Variable `PROMOTE_WEBHOOK` | `true` |
| Secret `PROMOTION_WEBHOOK_URL` | The receiving service's secret webhook URL |

Keep the channel variable unset or `false` to disable it. Do not put tokens, app passwords, or webhook URLs in the repository or workflow file.
