# CRIBBED FROM
# https://github.com/collective/collective.recipe.omelette/blob/master/collective/recipe/omelette/__init__.py

import os
import sys
import shutil
import pkg_resources
import argparse

import logging
log = logging.getLogger("scrambler")


WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

if WIN32:
    import ntfsutils.junction

    islink = ntfsutils.junction.isjunction

    def symlink(source, link_name):
        if not os.path.isdir(source):
            return
        ntfsutils.junction.create(source, link_name)

    def unlink(path):
        if not ntfsutils.junction.isjunction(path):
            return False
        ntfsutils.junction.unlink(path)
        return True

    def rmtree(location, nonlinks=True):
        # Explicitly unlink all junction'd links
        names = os.listdir(location)
        for dir in names:
            path = os.path.join(location, dir)
            if unlink(path):
                continue
            if os.path.isdir(path):
                rmtree(path)
        # Then get rid of everything else
        if nonlinks:
            shutil.rmtree(location)

else:
    symlink = os.symlink
    islink = os.path.islink
    rmtree = shutil.rmtree
    unlink = None


def create_namespaces(dist, namespaces, location, ns_base=()):
    iterator = namespaces.items

    if hasattr(namespaces, "iteritems"):
        # python 2
        iterator = namespaces.iteritems

    for k, v in iterator():
        ns_parts = ns_base + (k,)
        link_dir = os.path.join(location, *ns_parts)

        if not os.path.exists(link_dir):
            os.makedirs(link_dir)

        if len(v) > 0:
            create_namespaces(dist, v, location, ns_parts)
        egg_ns_dir = os.path.join(dist.location, *ns_parts)

        if not os.path.isdir(egg_ns_dir):
            log.info(
                "(While processing egg %s) Package '%s' is zipped. "
                "Skipping." % (
                    dist.project_name, os.path.sep.join(ns_parts)))
            continue
        dirs = os.listdir(egg_ns_dir)
        for name in dirs:
            if name.startswith('.'):
                continue
            name_parts = ns_parts + (name,)
            src = os.path.join(dist.location, *name_parts)
            dst = os.path.join(location, *name_parts)
            if os.path.exists(dst):
                continue
            symlink(src, dst)


def main(args=None):
    location = os.path.abspath('scrambled')

    parser = argparse.ArgumentParser(
        prog="scrambler",
        description='scrambler symlinks to python packages into a folder')

    parser.add_argument(
        "--target",
        help="target folder")

    # when called through 'python setup.py test' we have to ignore the
    # first passed argument
    if sys.argv[1:] == ['test']:
        args = args or []
    else:
        args = args or sys.argv[1:] or []

    parsed = parser.parse_args(args)

    if parsed.target:
        location = os.path.abspath(parsed.target)

    if not os.path.exists(location):
        os.makedirs(location)

    for dist in pkg_resources.working_set.by_key.values():
        project_name = dist.project_name
        namespaces = {}
        for line in dist._get_metadata('namespace_packages.txt'):
            ns = namespaces
            for part in line.split('.'):
                ns = ns.setdefault(part, {})

        top_level = sorted(list(dist._get_metadata('top_level.txt')))
        create_namespaces(dist, namespaces, location)

        for package_name in top_level:
            if package_name in namespaces:
                # These are processed in create_namespaces
                continue
            else:
                if not os.path.isdir(dist.location):
                    info_message = (
                        "(While processing egg %s) Package '%s' is "
                        "zipped. Skipping.")
                    log.info(
                        info_message % (
                            project_name, package_name))
                    continue
                package_location = os.path.join(dist.location, package_name)
                link_location = os.path.join(location, package_name)
                # check for single python module
                if not os.path.exists(package_location):
                    package_location = os.path.join(
                        dist.location, package_name + ".py")
                    link_location = os.path.join(
                        location, package_name + ".py")
                # check for native libs
                # XXX - this should use native_libs from above
                if not os.path.exists(package_location):
                    package_location = os.path.join(
                        dist.location, package_name + ".so")
                    link_location = os.path.join(
                        location, package_name + ".so")
                if not os.path.exists(package_location):
                    package_location = os.path.join(
                        dist.location, package_name + ".dll")
                    link_location = os.path.join(
                        location, package_name + ".dll")
                if not os.path.exists(package_location):
                    log.warn(
                        "Warning: (While processing egg %s) Package '%s' "
                        "not found. Skipping." % (
                            project_name, package_name))
                    continue

                if not os.path.exists(link_location):
                    if WIN32 and not os.path.isdir(package_location):
                        log.warn(
                            "Warning: (While processing egg %s) Can't link "
                            "files on Windows (%s -> %s). Skipping." % (
                                project_name, package_location, link_location))
                        continue
                    try:
                        symlink(package_location, link_location)
                    except OSError as e:
                        # TODO: deal with dangling symlinks
                        warning = (
                            "While processing egg %s) symlink fails "
                            "(%s, %s). Skipping.\nOriginal Exception:\n%s")
                        log.warn(
                            warning % (
                                project_name, package_location,
                                link_location, str(e)))


if __name__ == "__main__":
    main(sys.argv[1:])
