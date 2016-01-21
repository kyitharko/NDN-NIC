from distutils.core import setup, Extension

module1 = Extension("xorhash",
                    sources=["xorhash.c"],
                    extra_compile_args=["-std=c99"])

setup(name="xorhash",
      version="0.0",
      description="XorHash for NDN-NIC simulator",
      ext_modules=[module1])
