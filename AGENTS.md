# DSAG Agent Guidelines

## Subagent Workflow Safety (MANDATORY)

When using `delegate_task` to spawn subagents for parallel work:

1. **NEVER commit review artifacts**
   - Subagents may output `review-*.json` or similar temporary files
   - Before ANY `git commit`, run `git status` and `git diff --cached --stat`
   - If review files appear staged: `git rm review-*.json` immediately
   - Add `review-*.json` to `.gitignore` in every project using subagents

2. **ALWAYS verify after applying fixes**
   - After any CSS/HTML/JS change: start Hugo server, take screenshots
   - Verify both light mode AND dark mode
   - Verify responsive breakpoints (mobile 375px, tablet 768px, desktop 1200px+)
   - Test interactive elements (collapsible sections, nav, search)
   - Confirm `hugo --quiet` exits 0 before committing

3. **NEVER delete CSS rules without confirming selectors are unused**
   - Search the entire codebase (JS, HTML templates) for the selector before removal
   - If a rule is removed, test the feature it styled immediately
   - Prefer commenting out over deletion during active debugging

4. **Commit hygiene**
   - One logical change per commit
   - Verify `git diff --stat` matches intent before push
   - Never push directly to `main` without review if CI is configured
   - Use conventional commits: `type(scope): description`

5. **Model switching awareness**
   - When switching models (e.g., deepseek-v4-flash -> kimi-k2.6), verify the new model is active
   - Subagents should use the same model family to avoid compatibility issues
   - Always confirm subagent output quality before trusting results

## Project Context

- Hugo static site, 60 chapters, 12 parts
- Template compliance:
    1. **Definition**: Concise technical summary.
    2. **Background & Philosophy**: Theoretical grounding and design rationale.
    3. **Use Cases**: Practical applications.
    4. **Memory Mechanics**: Low-level details (cache, stack/heap, GC).
    5. **Operations & Complexity**: Table with Big-O bounds.
    6. **Idiomatic Go Implementation**: Generic-aware, clean Go code.
    7. **Decision Matrix**: Comparison of when to use vs. avoid.
    8. **Edge Cases & Pitfalls**: Common bugs and boundary conditions.
    9. **Anti-Patterns**: What NOT to do.
    10. **Quick Reference**: Summary table per chapter.
    11. **See Also**: Links to related chapters.
- Go code must be idiomatic (not Rust/C++/Python disguised).
- Python scripts exist for structural compliance scanning.
- Style guide and formatting rules are enforced strictly.

