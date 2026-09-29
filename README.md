# wren-reset

Static pages for the Wren Hale / Company AI Architect offers, on GitHub Pages.

Edit `main`. The `build-and-publish` workflow force-mirrors `main` to `gh-pages`, which is the Pages source, on every push. Do not commit to `gh-pages` directly; the next mirror overwrites it.

| Path | Role |
|---|---|
| `index.html` | $27 30-Day Reset sales page. Buy buttons use the placeholder `STRIPE_PAYMENT_LINK_27` (2 places). |
| `ads/index.html` | $397 "3 AI UGC Video Ads" page. Deposit buttons use the placeholder `STRIPE_LINK_397` (2 places). |
| `dl-*/index.html` | Buyer download page (noindex). Set as the Stripe after-payment redirect for the $27 link. |
| `dl-*/30-day-reset-v1.zip` | The file that page serves. |

To turn on payments, replace each placeholder with the real Stripe Payment Link URL and push to `main`.

Buying the product is permission to download the zip. It is not permission to republish it.
