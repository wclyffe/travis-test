# packaging script
import os
import shutil

# High-level utilities to create and read compressed and archived files are also provided. They rely on the zipfile and tarfile modules.
#
# shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])
#
#     Create an archive file (such as zip or tar) and return its name.
#
#     base_name is the name of the file to create, including the path, minus any format-specific extension.
#
#     format is the archive format: one of “zip”, “tar”, “bztar” (if the bz2 module is available) or “gztar”.
#
#     root_dir is a directory that will be the root directory of the archive;
#              for example, we typically chdir into root_dir before creating the archive.
#
#     base_dir is the directory where we start archiving from; i.e. base_dir will be the common prefix of all files and directories in the archive.
#
#     root_dir and base_dir both default to the current directory.
#
#     owner and group are used when creating a tar archive. By default, uses the current owner and group.
#
#     logger must be an object compatible with PEP 282, usually an instance of logging.Logger.

cwd = os.getcwd()

current_dir = os.path.dirname(__file__)
package_dir = os.path.join(cwd, 'foo-package')

print("current working dir: {}".format(cwd))
print("current file dir: {}".format(current_dir))

archive_name = shutil.make_archive(base_name='foo-package',
                                   format="zip",
                                   root_dir=cwd,
                                   base_dir=package_dir)


print("archive_name: {}".format(archive_name))
