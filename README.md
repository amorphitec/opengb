# Open Gigabot Controller.

**This project is discontinued.**

OpenGB was partly sponsored by [re:3D](https://re3d.org) as part of the [Open Gigabot](https://www.kickstarter.com/projects/re3d/open-gigabot-an-open-source-gigabot-3d-printer-exp) project.

Ultimately [Octoprint](https://octoprint.org/) emerged as a better-resourced and more mature alternative and so work on OpenGB was discontinued in 2017.

You can learn more about OpenGB by watching [@amorphic](https://github.com/amorphic/)'s PyCon AU talk _[Controlling a 3D printer with Python](https://www.youtube.com/watch?v=qgvnPB_77z8)_.

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

## Packaging

Debian packages are created using [dh-virtualenv](https://dh-virtualenv.readthedocs.org):

```
dpkg-buildpackage -us -uc
```

*Note: packages are currently stored in `/packages` until a proper repo is set up.*
