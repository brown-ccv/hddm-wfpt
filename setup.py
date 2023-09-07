import platform

from setuptools import setup
from setuptools import Extension

import numpy as np

try:
    from Cython.Build import cythonize

    if platform.system() == "Darwin":
        ext1 = Extension(
            "wfpt",
            ["hddm_wfpt/wfpt.pyx"],
            language="c++",
            extra_compile_args=["-stdlib=libc++"],
            extra_link_args=["-stdlib=libc++", "-mmacosx-version-min=10.9"],
        )
    else:
        ext1 = Extension("wfpt", ["hddm_wfpt/wfpt.pyx"], language="c++")

    ext_modules = cythonize(
        [
            ext1,
            Extension(
                "cdfdif_wrapper",
                ["hddm_wfpt/cdfdif_wrapper.pyx", "hddm_wfpt/cdfdif.c"],
            ),
        ],
        compiler_directives={"language_level": "3", "linetrace": True},
    )

except ImportError:

    ext_modules = [
        Extension("wfpt", ["src/wfpt.cpp"], language="c++"),
        Extension("cdfdif_wrapper", ["src/cdfdif_wrapper.c", "src/cdfdif.c"]),
    ]

setup(
    name="hddm-wfpt",
    version="0.1.0.rc0",
    author="Thomas V. Wiecki, Imri Sofer, Michael J. Frank, Mads Lund Pedersen, Alexander Fengler, Lakshmi Govindarajan, Krishn Bera",
    author_email="alexander_fengler@brown.com",
    url="http://github.com/lncc/hddm-wfpt",
    packages=["hddm_wfpt"],  # 'hddm.cnn', 'hddm.cnn_models', 'hddm.keras_models',
    description="Collects a bunch of cython implementations of basic DDM likelihoods",
    install_requires=["NumPy >=1.23.4", "SciPy >= 1.9.1", "cython >= 0.29.32"],
    include_dirs=[np.get_include()],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    ext_modules=ext_modules,
)
