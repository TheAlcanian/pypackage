<h1 align="center">PyPackage</h1>
[![black-workflow](https://img.shields.io/github/workflow/status/TheAlcanian/pypackage/Black?label=black%20formatting&style=flat-square)](https://github.com/TheAlcanian/pypackage/actions?query=workflow%3ABlack) [![pylint-workflow](https://img.shields.io/github/workflow/status/TheAlcanian/pypackage/Pylint?label=pylint&style=flat-square)](https://github.com/TheAlcanian/pypackage/actions?query=workflow%3APylint) [![issues-open](https://img.shields.io/github/issues-raw/TheAlcanian/pypackage?label=issues%20open&style=flat-square)](https://github.com/TheAlcanian/pypackage/issues) [![prs-open](https://img.shields.io/github/issues-pr-raw/TheAlcanian/pypackage?label=pull%20requests%20open&style=flat-square)](https://github.com/TheAlcanian/pypackage/pulls) [![license](https://img.shields.io/github/license/TheAlcanian/pypackage?style=flat-square)](https://unlicense.org/) 
<h2>What is PyPackage?</h2>

PyPackage is a package manager which works a little bit differently - it can be run by normal users and manages software which comes in archives (think the `.tar.gz` download of Firefox, Discord, etc).

<h2>How is PyPackage made?</h2>

PyPackage is written in Python, tested with Python version 3.7.8.
It requires the PyPI package <code>urlgrabber</code>, which can be obtained with the command <code>pip3.7 install urlgrabber</code>.

PyPackage attempts to comply with PyLint and use Black's code style. We use <a href="https://github.com/TheAlcanian/pypackage/actions">GitHub Actions</a> to check for these. PyPackage is also frequently scanned by CodeQL for vulnerabilities; also done with GitHub Actions.

<h2>Why was PyPackage made?</h2>

PyPackage was written originally for use by myself, but a friend of mine said it should be easier to access, saving it from the `hax` directory on my profile.

I made PyPackage because I was annoyed that I had to open a browser, go to the program's website, download the files, extract, delete the old files, move the extracted files to the location of the old files, all manually - it got really annoying and repetitive, so I made PyPackage.

<h2>Why doesn't PyPackage do <code>$THING</code>?</h2>

PyPackage is in very early stages of development, and a lot of features are planned, but missing (like zipfile extraction, removal of software and easy addition to the repos of software).

<h2>How can I help with PyPackage?</h2>

In any way you want! Report bugs, create pull requests, even just starring it helps!

Remember that all contributions must fall under the terms of The Unlicense (which means no taking code from projects w/o licenses, projects with MIT licenses or other "less free" licenses).

I am not accepting any donations at this time, though.
