"""Example DAG demonstrating the usage of the BashOperator."""

from __future__ import annotations
import datetime
import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

with DAG(
        dag_id="1.bash_operator_with_params_example",  # UI상 DAG 화면에 보이는 값. 보통 python파일명과 일치시키는 편
        schedule="0 0 * * *",
        start_date=pendulum.datetime(2025, 7, 1, tz="UTC"),  # "Asia/Seoul"
        catchup=False,  # 현재 날짜와 start_date 간의 차이가 있을 때 이 사이에 누락된 구간에 대해 실행할지 말지에 대한 옵션, 날짜별로 차례로 도는게 아닌 한번에 도는점 주의
        dagrun_timeout=datetime.timedelta(
            minutes=60
        ),  # 1시간 돌게되면 dag실패나도록 설정
        tags=["example", "params"],
        # params: DAG 실행 시 사용할 파라미터를 정의
        # UI의 "Trigger DAG w/ config"에서 JSON 형식으로 값을 변경할 수 있음
        params={
            "greeting": "Hello Airflow",
            "target_message": "This is task4 speaking!",
        },
    ) as dag:
        last_empty_task = EmptyOperator(  # task도 객체명과 task_id를 똑같이 하는게 관례
            task_id="this_is_last",
        )
        # task1에서 params 사용 예시
        # bash_command 내에서 '{{ params.greeting }}' 형태로 파라미터 값을 참조

        task1 = BashOperator(
            task_id="task1_with_param",
            bash_command='echo "Message from params: {{ params.greeting }}"',
        )

        # 리스트를 사용하여 반복문에서 생성된 태스크들을 수집
        loop_tasks = []
        for i in range(2, 4):
            task = BashOperator(
                task_id=f"task{i}",
                bash_command='echo "Loop task {{ task.task_id }} | Instance: {{ task_instance_key_str }}" && sleep 1',
            )
            loop_tasks.append(task)

        # task4에서 다른 파라미터를 사용하는 예시
        task4 = BashOperator(
            task_id="task4_with_param",
            bash_command='echo "{{ params.target_message }}" && echo good',
        )
        # 의존성 설정
        # task1이 완료된 후, loop_tasks에 포함된 task2, task3가 병렬로 실행
        # loop_tasks의 모든 태스크가 완료된 후, task4와 last_empty_task가 따로 실행

        task1 >> loop_tasks >> task4
        loop_tasks >> task4
        loop_tasks >> last_empty_task
