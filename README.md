# Caution

This GitHub repository contains code to build and package the **StatRep**
LaTeX package. If you are looking for the package itself, please download the file ``statrep.zip`` from one of these locations.

  * SAS (http://support.sas.com/StatRepPackage)
  * CTAN (http://www.ctan.org/pkg/statrep)

You can see a brief online example here: 
http://tiarno.github.io/StatRep/

# Overview

The **StatRep** system is an open-source package that works with SAS, LaTeX, 
and a suite of SAS macros to enable you to create dynamic documents with reproducible results. It combines the LaTeX markup language with your SAS code so that both the code and resulting SAS output are automatically displayed in your final PDF document.

With **StatRep**, your analysis is fully documented and reproducible from a single source--your LaTeX document. The system automatically produces a SAS program so that both the SAS output and the SAS code that produced the output are displayed.

The package provides two environments and two tags that work together to display your SAS code and results and to generate the SAS program that produces those results. The two environments (``Datastep`` and ``Sascode``) display SAS code. The two tags (``Listing`` and ``Graphic``) display SAS output.

Full documentation is included in the distribution, available at the links provided above.

  * *The StatRep User's Guide* (`statrepmanual.pdf`) includes installation instructions and details on how to use the system.
  * A simple example of using the package (`quickstart.tex`)
  * Documentation on the LaTeX implementation (`statrep.pdf`)

The generated SAS program includes calls to macros that use the SAS
Output Delivery System (ODS) document to capture the output as external files.
These SAS macros are included in this package (``statrep_macros.sas``).

Limited support is provided for SAS-generated LaTeX output, using a special tagset: you can generate the tagset with the included SAS program ``statrep_tagset.sas``. 

# License

    Copyright (c) 2014 SAS Institute Inc.

    Permission is granted to copy, distribute, and/or modify this software
    under the terms of the LaTeX Project Public License (LPPL), version 1.3.

    This software is provided by SAS Institute Inc. as a service to its users.
    It is provided 'as is', without warranty of any kind, either expressed or
    implied, including, but not limited to, the implied warranties of
    merchantibility and fitness for a particular purpose.
    See http://www.latex-project.org/lppl.txt for the details of that license.

    This work has the LPPL maintenance status 'maintained'. 
    The Current Maintainer of this work is Tim Arnold 
    (tim dot arnold at sas dot com).

# Requirements

  * ``pdfLaTeX`` typesetting engine 1.30 or later
  * LaTeX packages: ``verbatim``, ``graphicx``, ``xkeyval``, ``calc``, ``ifthen``. These packages are contained in a standard LaTeX distribution, such as **TeXLive** or **MiKTeX**.
  * SAS 9.2 or later


# Note on Packaging

This github repo is meant for packaging the ``StatRep`` and ``longfigure`` packages. To create the packages, 
 1. put the ``benchmark``, ``content``, and ``supplement`` directories along with ``build.py`` into a clean working directory. 
 2. Execute the ``build.py`` script to create a new ``build`` directory.

Inside the ``build`` directory there will be subdirectories called ``ctan``, ``sas`` that contain the files to be distributed at those locations. There are also directories ``test`` and ``work`` that were used to create the new distributions.

Inside the distribution directories are the zip files. For the ``sas`` distribution, the ``*.sty`` files are included so people don't have to do any extra steps. Here is the layout of the zip file for the distribution (``statrep.zip``):

    README
    LICENSE
    statrep.dtx
    statrep.ins
    statrep.sty
    longfigure.sty
    doc/
        images/
        quickstart.tex
        statrepmanual.tex
        statrepmanual.pdf -- with example.tex attached inside
        statrep.pdf
    sas/
        statrep_macros.sas
        statrep_tagset.sas

The CTAN folks don't want the extra ``*.sty`` files since they are normally just created by compiling the ``*.dtx`` file, so we omit them for the CTAN version. The layout for this version (``statrep.zip``) appears as follows:

    README
    LICENSE
    statrep.dtx
    statrep.ins
    doc/
        images/
        quickstart.tex
        statrepmanual.tex
        statrepmanual.pdf -- with example.tex attached inside
        statrep.pdf
    sas/
        statrep_macros.sas
        statrep_tagset.sas

The ``longfigure`` package is simple and exists only in the ``ctan`` directory. The layout of the zip file looks like this (``longfigure.zip``):

    README
    LICENSE
    longfigure.dtx
    longfigure.ins
    longfigure.pdf



