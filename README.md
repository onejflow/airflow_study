### Docker Compose를 이용한 에어플로우 설치 방법
[Running Airflow in Docker — Airflow 3.0.2 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
1. Fetching docker-compose.yaml 
2. container mount를 위한 디렉토리 생성 및  airflow user setting
	 - `mkdir -p ./dags ./logs ./plugins ./config`
	 - `echo -e "AIRFLOW_UID=$(id -u)" > .env`  .env에 사용자 UID로 설정

3. docker compose up -d 로 실행
이 후 https://<호스트 IP>:8080 또는 localhost:8080 으로 이동하여 최초 로그인 후 계정 생성
- 초기 로그인은 따로 설정을 하지 않았다면 id/pw가  airflow/airflow 이다

### 실습용 환경 구성
`로컬 환경에서 만든 dag를 컨테이너까지 배포하는 것`
1. Proxmox로 만든 Ubuntu VM에 Docker Compose를 이용하여 에어플로우 설치
2. 로컬 컴퓨터에 airflow 프로젝트용 uv 생성 - airflow 설치된 버전과 동일한 파이썬버전 설치 
	- 서버에 접속하여 airflow-worker 컨테이너의 파이썬 버전 확인한다. 
	- 실습을 위한 디렉토리에 `uv init 프로젝트명 --python 3.12 --app`  으로 프로젝트를 생성한다. (에어플로우와 동일한 버전의 파이썬)
	- vscode 사용시 Python: Select Interpreter 로 해당 환경 설정
3. Github 레파지토리 생성
	- 로컬과 연동 후 로컬 내용 push
4. 로컬 컴퓨터 프로젝트에 uv를 통해 Airflow 라이브러리 설치 (저사양 아키텍처로 설치되어 여러 제약이 있음)
	- [Quick Start — Airflow 3.0.2 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
	- [Installation from PyPI — Airflow 3.0.2 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
	- `uv pip install "apache-airflow[celery] ...` 으로 설치 하면 된다.
	- 로컬에서 실행 해보고 싶을 시 아래와 같이 할 수 있고 localhost:8080 으로 접속하면 된다.
	```bash
	cd /path/to/your/project
	export AIRFLOW_HOME=$(pwd)
	airflow standalone
	```
5. 로컬에 dags 디렉토리 생성 및 예시 DAG 작성
5. VM 서버에 Git 설치 및 airflow 프로젝트 디렉토리에서 git clone
6. VM 서버에서 github 레포지토리에서 받은 dags 디렉토리를 볼 수 있도록 docker-compose.yaml 파일의 volumes 수정
    - `:` 을 기준으로 왼쪽 로컬, 오른쪽 도커 컨테이너
    - 기존 같은 경우 ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags 로 프로젝트 디렉토리 하위로 존재하는 dags 디렉토리를 마운트
    - 이를 깃헙레포로 받은 dags 디렉토리 경로로 수정을 해줘야한다.
    - ${AIRFLOW_PROJ_DIR:-.}/깃헙레포명/dags:/opt/airflow/dags
	-  ${AIRFLOW_PROJ_DIR:-.}/airflow_study/dags:/opt/airflow/dags

실습이기에 따로 CICD는 구성하지 않는다.