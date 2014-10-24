

Creates statrep.dtx and longfigure.dtx in subdirectories of current dir.
Files present:

  * statrep.wrapper
  * longfigure.wrapper
  * longfigure.inc

statrep.wrapper is read and longfigure.inc is inserted to create statrep.dtx
longfigure.wrapper is read and longfigure.inc is inserted to create longfigure.dtx

This is used to keep the longfigure package synced with statrep. If any edits are
made to longfigure package, it should be in longfigure.inc since both the statrep
and longfigure package include that file.

The files that are distributed still come from the *.dtx files; this subdirectory
is used only for creating them.
