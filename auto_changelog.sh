#! /bin/bash
echo "post-commit started"
gitdir="$(git rev-parse --git-dir)"
hook="$gitdir/hooks/post-commit"

# disable post-commit hook temporarily
[ -x $hook ] && chmod -x $hook

cz changelog
git add CHANGELOG.md
git stage CHANGELOG.md
git commit --amend --no-edit --no-verify
# enable it again
chmod +x $hook
