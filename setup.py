from setuptools import setup, find_packages


def scm_version():
    def local_scheme(version):
        if version.tag and not version.distance:
            return version.format_with("")
        else:
            return version.format_choice("+{node}", "+{node}.dirty")
    return {
        "relative_to": __file__,
        "version_scheme": "guess-next-dev",
        "local_scheme": local_scheme
    }


setup(
    name="amaranth_wb2axip",
    use_scm_version=scm_version(),
    author="andresdemski",
    author_email="andresdemski@gmail.com",
    description="Amaranth wrapper for http://github.com/zipcpu/wb2axip cores",
    license="BSD",
    python_requires="~=3.6",
    install_requires=[
        "amaranth",
    ],
    packages=find_packages(exclude=["*.test*"]),
    package_data={
        'amaranth_wb2axip': ['rtl/*']
    }
)
