# Caution

This GitHub repository contains code to build and package the **StatRep**
LaTeX package. If you are looking for the package itself, please download the statrep.zip file from one of these locations.

  * SAS (http://support.sas.com/StatRepPackage)
  * CTAN (http://www.ctan.org/pkg/statrep)


# Overview

The **StatRep** system is an open-source package that works with SAS, LaTeX, 
and a suite of SAS macros to enable you to create dynamic documents with reproducible results. It combines the LaTeX markup language with your SAS code so that your SAS code and results are automatically displayed in your final PDF document.

With **StatRep**, your analysis is fully documented and reproducible from a single source--your LaTeX document. The system automatically produces a SAS program so that both the SAS output and the SAS code that produced the output are displayed.

The package provides two environments and two tags that work together to display your SAS code and results and to generate the SAS program that produces those results. The two environments (``Datastep`` and ``Sascode``) display SAS code. The two tags (``Listing`` and ``Graphic``) display SAS output.

Full documentation is included in the distribution, available at the links provided above.

  * Documentation on the LaTeX implementation (`statrep.pdf`)
  * *The StatRep User's Guide* (`statrepmanual.pdf`) includes installation instructions.
  * A simple example of using the package (`quickstart.tex`)

The generated SAS program includes calls to macros that use the SAS
Output Delivery System (ODS) document to capture the output as external files.
These SAS macros are included in this package (statrep_macros.sas).

# License

Copyright (c) 2014 SAS Institute Inc.

Permission is granted to copy, distribute, and/or modify this software
under the terms of the LaTeX Project Public License (LPPL), version 1.3.

This software is provided by SAS Institute Inc. as a service to its users.
It is provided 'as is', without warranty of any kind, either expressed or
implied, including, but not limited to, the implied warranties of
merchantibility and fitness for a particular purpose.
See http://www.latex-project.org/lppl.txt for the details of that license.

This work has the LPPL maintenance status 'maintained'. The Current Maintainer of this work is Tim Arnold (tim dot arnold at sas dot com).

# Requirements

  * ``pdfLaTeX`` typesetting engine 1.30 or later
  * LaTeX packages: verbatim, graphicx, xkeyval, calc, ifthen
  * SAS 9.2 or later