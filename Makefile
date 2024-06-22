default: all


sinhtest:
	@python -B scripts/sinhTest.py --amount 100 --minstrlen 100 --maxstrlen 1000 --minquery 100 --maxquery 500


buildproblem:
	@python -B scripts/buildProblemConfig.py


uploadproblem:
	@python -B scripts/uploadProblem.py --sessionid yrylmrxo5gwwng49pagqb8kr9exj2dai --url http://localhost


clean:
	-@del /F /S /Q *.zip ||:
	-@rmdir /S /Q *__pycache__ ||:
	-@rmdir /S /Q build ||:
	@echo OK!


install:
	@python -m pip install --upgrade pip
	@python -m pip install -r requirements.txt

	
all: clean sinhTest buildProblem uploadProblem