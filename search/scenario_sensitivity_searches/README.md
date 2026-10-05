# Scenario sensitivity searches

This directory is not part of the primary search.

The primary search has two concept blocks:

1. Social or companion robots.
2. Naturalistic, in-the-wild, or long-term settings.

There is no generic evaluation block in the primary search.

Scenario terms are a sensitivity analysis. Run them separately, log them separately, and do not merge their hit counts into the primary database totals unless the decision log says that a particular sensitivity search was promoted.

## Terms the primary search should not casually expand

The brief gives these constraints. They are not a Boolean query.

- Do not search the bare stem `home*`. It retrieves noise such as homework, homeostasis, and homepage.
- Low-ambiguity platform terms that the brief keeps are Paro, robotic seal, Pleo, and AIBO.
- Do not add NAO or Pepper to the search. The protocol chose not to add those higher-noise platform names.

## What to put in this folder

After the protocol file is available, save each sensitivity query as its own file here. Mark any file that has not been checked by a person with:

```text
# TODO: HUMAN VERIFICATION REQUIRED
```

No sensitivity query is stored yet, because the source Boolean was not available to extend.

# TODO: HUMAN VERIFICATION REQUIRED
