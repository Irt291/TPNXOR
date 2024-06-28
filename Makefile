default: all


sinhtest:
	@python -B scripts/sinhTest.py --amount 100 --minstrlen 100 --maxstrlen 1000 --minquery 100 --maxquery 500


buildproblem:
	@python -B scripts/buildProblemConfig.py


uploadproblem:
	@python -B scripts/uploadProblem.py --sessionid 73i65zzb75h47ek6cgn9la0pkkf6yu3d --url http://localhost


clean:
	-@del /F /S /Q *.zip ||:
	-@rmdir /S /Q *__pycache__ ||:
	-@rmdir /S /Q build ||:
	@echo OK!


install:
	@python -m pip install --upgrade pip
	@python -m pip install -r requirements.txt



update: buildProblem uploadProblem
all: clean sinhTest update









# cloudflared tunnel create TPNXORDEV
# cloudflared tunnel route dns TPNXORDEV static.irt291.eu.org

runDevTunnel:
	# python -m http.server 8090 --directory ./src/Assets/html
	@cloudflared tunnel --url http://127.0.0.1:8090 run TPNXORDEV
	