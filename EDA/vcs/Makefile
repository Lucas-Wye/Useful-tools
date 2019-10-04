.PHONY: format com lca sim simt clean

FILE_NAME = $(FILE).v
TESTBENCH = tb_$(FILE).v

OUTPUT = $(FILE).out
SIM_LOG = $(FILE)_sim.log
ALL_DEFINE = +define+DUMP_VPD
VCS_LOG = $(FILE)_vcs_compile.log
VPD_NAME = +vpdfile+$(OUTPUT).vpd

# Path of Python
Python = $(HOME)/lib/conda/bin/python
# Path of vTbgenerator
vTbgenerator = ./tools/vTbgenerator.py
# Path of iStyle
iSTYLE = $(HOME)/lib/script/iStyle

# -R 编译完成后立即执行 ./simv
# -o simv_file 更改可执行文件名
# -timescale=1ns/1ns 设置仿真精度
# -Mupdate 源文件有修改时只重新编译有改动的.v文件节约编译时间
# -debug_pp 打开生成 VPD 文件的功能,关掉UCLI的功能,节约编译时间
# -sverilog 打开对Systemverilog的支持编译Systemverilog文件时使用
VCS = vcs -full64 -sverilog +v2k -timescale=1ns/1ns \
	-debug_pp +notimingcheck -Mupdate               \
	-o $(OUTPUT) $(VPD_NAME) $(ALL_DEFINE)          \
	-l $(VCS_LOG) -j4 $(FILE_NAME) $(TESTBENCH)

SIM = ./$(OUTPUT) $(VPD_NAME) -l $(SIM_LOG)

all: format com sim
run: com sim

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

tb: guard-FILE 
	$(Python) $(vTbgenerator) $(FILE_NAME) > $(TESTBENCH)

format:
	$(iSTYLE) *.v > /dev/null
	rm *.orig

com: guard-FILE
	$(VCS)

lca: guard-FILE
	$(VCS) -lca -simprofile

sim: guard-FILE
	$(SIM)

simt: guard-FILE
	$(SIM) -simprofile time

wave: guard-FILE
	dve -vpd $(OUTPUT).vpd &

clean:
	rm -rf ucli.key *.log *.vpd *.out* csrc DVEfiles profileReport* simprofile_dir*
