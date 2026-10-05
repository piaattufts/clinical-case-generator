# Google Scholar

Google Scholar is a supplementary source. It is not one of the structured database exports.

## What is unresolved

The number of Scholar results to screen is not set. `docs/unresolved_protocol_decisions.md` lists that choice. Do not pick a number in this file and then treat it as the protocol.

## How to record a Scholar pass

When a person does run Scholar:

1. Write the date, the query text actually used, the filters, and the number screened in `search/search_log.csv`.
2. Save any export or a copy of the screened hits under `data/raw/scholar/`.
3. Import those rows with `--database google_scholar` so they enter normalization, duplicate detection, and screening.
4. Do not mark a hit eligible because it came from Scholar.

## Query text

Use the same two concept blocks as the primary search: social or companion robots, and naturalistic or long-term settings. Do not add a generic evaluation block. Do not paste the scenario sensitivity block into the primary Scholar search.

The Boolean string itself still has to come from the protocol. It is not invented here.

# TODO: HUMAN VERIFICATION REQUIRED
