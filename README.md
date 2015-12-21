# Open Gigabot Controller.

_Not yet ready for production use._

## Docs

Visit http://opengb.readthedocs.org for all documentation

## Frontends

Note the `opengb-web` frontend was added like this:
```
git remote add -f -t master --no-tags opengb-web git@github.com:re-3D/opengb-web.git
```
It may be updated in future like this:
```
git read-tree --prefix=opengb/frontend/opengb -u opengb-web/master:dist
```
