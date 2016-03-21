# Open Gigabot Controller.

## Docs

Visit http://opengb.readthedocs.org for all documentation

## Frontends

Note the `opengb-web` frontend was added via `git read-tree` as described in #2 [here](http://stackoverflow.com/a/30386041/1273241):

```
git remote add -f -t master --no-tags opengb-web git@github.com:re-3D/opengb-web.git
git merge -s ours --no-commit opengb-web/master
git read-tree --prefix=opengb/frontend/opengb -u opengb-web/master:dist
git commit
```

It may be updated in future like this:

```
git fetch opengb-web
git merge -s ours --no-commit opengb-web/master
git rm -rf opengb/frontend/opengb
git read-tree --prefix=opengb/frontend/opengb -u opengb-web/master:dist
git commit
```
