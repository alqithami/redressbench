# Anonymous Submission Checklist

Before attaching this repository to a double-anonymous submission, verify:

## Repository identity

- [ ] Repository owner/organization is anonymous.
- [ ] README contains no author names, emails, personal websites, labs, or institutions.
- [ ] Commit history does not reveal author identities; use a clean anonymous repository if necessary.
- [ ] Git remotes do not point to identifying repositories in shared instructions.

## Files

- [ ] No API keys, `.env` files, tokens, or private paths.
- [ ] No OS user names in logs or generated files.
- [ ] No private condition mapping shared with annotators unless intended.
- [ ] No annotator names in public files; use IDs such as `A1`, `A2`.
- [ ] No IRB correspondence containing institution or staff names in reviewer-facing files.
- [ ] No PDF or LaTeX metadata with author names.

## Paper consistency

- [ ] Paper and README use the same benchmark version numbers.
- [ ] Paper results match files under `analysis/` or `results/`.
- [ ] The paper states that automatic scores are diagnostic if human annotation is incomplete.
- [ ] Human annotation status is accurately described.

## After acceptance

- [ ] Restore author identities if appropriate.
- [ ] Add final license.
- [ ] Add citation metadata.
- [ ] Archive a stable release with DOI if required.
