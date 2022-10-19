import os

try:
    from Cython.Build import cythonize

except ImportError:

    def build(setup_kwargs):
        pass

else:

    def build(setup_kwargs):

        from setuptools import Extension
        from distutils.command.build_ext import build_ext

        import numpy as np

        ext_modules = cythonize(
            [
                Extension(
                    "wfpt",
                    ["hddm_wfpt/wfpt.pyx"],
                    language="c++",
                    extra_compile_args=["-stdlib=libc++"],
                    extra_link_args=["-stdlib=libc++", "-mmacosx-version-min=10.9"],
                ),
                Extension(
                    "cdfdif_wrapper",
                    ["hddm_wfpt/cdfdif_wrapper.pyx", "hddm_wfpt/cdfdif.c"],
                ),
                Extension(
                    "data_simulators",
                    ["hddm_wfpt/cddm_data_simulation.pyx"],
                    language="c++",
                ),
            ],
            compiler_directives={"language_level": "3", "linetrace": True},
        )

        os.environ["CFLAGS"] = "-O3"

        setup_kwargs.update(
            {
                "ext_modules": ext_modules,
                "cmdclass": {"build_ext": build_ext},
                "include_dirs": [np.get_include()],
            }
        )
