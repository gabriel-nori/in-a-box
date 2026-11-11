THE RULE

Remove a worktree only after looking at what is in it; work that is not committed or pushed is never deleted without the owner's yes for that worktree.

What must be true at the end:
- Every removed worktree was clean, or its changes were committed or explicitly dropped by the owner.
- Branches merged into the default branch are removed together with their worktree.

How it is handled:
- List worktrees with their status and unpushed commits before touching any of them.
- Ask once per worktree that holds uncommitted or unpushed work; clean merged ones can go in one pass.

WHY

A worktree is where unfinished work lives. Deleting by pattern loses it silently and there is no undo.

HOW TO APPLY

Applies to developers and to release-in-a-box when a release branch is done. Deletion is an irreversible action, so it follows the gate rule of CONVENTIONS section 6.

RELATED

Idea taken from the ub-mode skill (MIT; reached through a short link, https://lnkd.in/dfJ7xq5d; the text is not copied). Roles: developer, release-manager.
