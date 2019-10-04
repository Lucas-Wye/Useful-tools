@echo off

SET VLOG=vlog
SET VLIB=vlib
SET VOPT=vopt
SET VSIM=vsim

SET VWORK=work
SET FILE_LIST=src.flist
SET VLOG_TB_TOP=tb_pad
SET VOPT_TB_TOP=%VLOG_TB_TOP%_opt

SET COMPILTE_FLAGS=-pedanticerrors -suppress 2577 -suppress 2583

: create a library
%VLIB% %VWORK%

: compile source code
%VLOG% -work %VWORK% %COMPILTE_FLAGS% -f %FILE_LIST%

: design optimization
%VOPT% -debugdb -fsmdebug -pedanticerrors +acc %VLOG_TB_TOP% -o %VOPT_TB_TOP%

: run simulation with GUI
%VSIM% -gui -debugdb -lib %VWORK% %VOPT_TB_TOP% -do "vsim_gui.tcl"

: run simulation without GUI
: %VSIM% -c -debugdb -lib %VWORK% %VOPT_TB_TOP% -do "vsim_cli.tcl"

pause
