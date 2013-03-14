Install:
	need python 2.6 or higher edition, we take the /usr/local/bin/python2.6 as the default python path.
	step1: check out source
	step2: make input dir , output dir, and the log dir
		you should prepare two dirs as input and output path for psven. we use
		Input and Output in the following.
		make sure the psven directory has a dir named log.
	step3: check the PYTHONEXE is all right.
		open run.sh and check the python path(PYTHONEXE) is all right. the default path
		is /usr/local/bin/python2.6, or you should change it to your python interpreter path.

Run:
	in the psven directory, run:
	./run.sh Input Output [<# of concurrent connections>] [<# of threads>] 
	the fourth param ( # of threads ) is recommended as double count of your cpu
	cores.
	the third param is recommended as ( 512 or 1024 ) devided by the fourth
	param.
	also you can leave the last two params blank to use the default value.

