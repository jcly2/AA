# Architectural Design Decision
## Design Decision for QA-01 Title
## Design Goal (0.5 페이지 이내)
<작성 방법>
목표로 하는 QA를 달성하기 위하여 해결이 필요한 세부/구체적인 설계 이슈를 서술한다. 즉, QA를 다시 서술하지 않고, 해당 QA를 구체화해야 한다.
각 QA를 달성하는데 장애 요소를 바탕으로 Goal을 설정한다. 예를 들어
성능: 무엇이 Bottle-neck인지? 대규모 입력인지? 빈번한 입력인지? 입력에 대한 처리의 복잡도인지?
가용성: 어떤 상황에서 fault가 발생하는지? 얼마나 자주 발생하는지? Fault 탐지가 어렵거나, 빠르지 않을 수 있는 원인은 무엇인지?
변경용이성: 어떤 상황에서 변경 요청이 발생하는지? 얼마나 자주 변경 요청이 발생하는지? 변경 요청을 수용하기 어렵거나, 빠르지 않을 수 있는 원인은 무엇인지?
정확성: 정확성을 저해하는 요인은 무엇인지? 데이터 문제(데이터 부족, 데이터 부정확성(노이즈, 오차 등) 등)인지, 계산 로직 자체의 부정확성인지?
사용성: 사용자를 불편하게 하는 입력은 무엇인지? 왜 반복적인 입력을 하거나, 입력 시 실수를 많이 하는지?
서술된 Design goal은 Design Approach을 통해서 접근/달성되어야 한다.
## Design Approach List (각 Approach 별 2 페이지 이내)
<작성 방법>
Design decision의 타당성
목표로 하는 QA를 달성할 수 있는 approaches들을 제시하고 비교해야 함
즉, 제시된 문제(Design goal) 해결을 위한 approaches 제시/비교가 필요함. 예를 들어, Design goal이 Application process의 liveness 분석일 때
적절한 예: crash 탐지를 위한 방법들(ping/echo, heartbeat 등) 제시/비교
부적절한 예: ping/echo(crash 탐지), exception handling(incorrect response 탐지) 비교
외부 연동될 시스템/장치 및 사용자와의 인터페이스 방식 등은 요구사항이므로 Design decision에 해당되지 않음
학습한 설계 기법 위주로 설계 제시 필요
기존 플랫폼, 프레임워크에 대한 비교 및 선택이 아니라, 학습한 패턴, 전술 등의 적용에 초점을 둠
아키텍처 설계 즉 component 식별, 인터페이스 식별 등과 거리가 있는 알고리즘의 선택은 다루지 않음
## Design Approach #1 Description: 주차장에서 번호 인식 수행
<작성 방법>
## Design goal 달성하기 위한 주요/타당한 Design approach들이 식별되었는가?
각 Design approach의 설명이 목표로 하는 design goal과 일관성이 있어야 한다.
Title
## Design goal을 달성하기 위한 핵심 기법이 무엇인지?
다른 DA와의 차별성이 명확하게 나타나도록 한다
설명
이 Design Approach를 적절한 View(Structure, Behavior, Deployment)을 통해서 명확하게 표현한다.
적용한 설계 방법 즉 패턴, Tactics 등의 적용을 명시적으로 언급한다.
설계 구체성
적용 설계 approach에 대한 일반적인 설명이 아니라 해당 approach를 이 시스템에 적용할 때의 아키텍처 모습을 구체적으로 제시해야 한다.
## Design goal을 달성하기 위한 실질적이고 세부적인 design이 제시되어야 한다.
Layer patter 적용의 경우: Layer의 수 및 각 layer의 역할, Layer interface 설계 등에 대한 decision이 제시될 필요가 있음
Ping/echo vs Heartbeat에 대한 단순 비교 보다는
Health check 수준: liveness, state consistency(invariant) 등에 대한 decision
Cache 적용의 경우: Cache에 보관할 데이터는? Cache Update 방법은?
Passive redundancy 적용의 경우: 동기화될 데이터는? 동기화 주기는? 동기화에 소요되는 비용은?
## Design Approach #2 Description: 1차적으로 주차장에서 처리, 불가이면 중앙서버에서 처리
## Decision (1페이지 이내)
<작성 방법>
각 Design approach에 대한 장/단점 분석이 타당하고 구체적이어야 함
분석의 완전성
목표 QA를 포함한 관련 AD 관점에서 장단점 제시 필요
분석의 타당성
서술된 장/단점이 올바른 가?
목표로 하는 QA측면에서 분석하였는가?
분석의 구체성
장/단점 서술 시 단순한 사실이 아니라 해당 기준(QA 등 AD)에 미치는 영향 분석 필요; DA가 해당 기준의 달성/실패에 어떤 이유로 어느 정도로 영향을 미치는 지 서술
오버헤드 존재한다  성능에 영향을 미치는지? 얼마나 영향을 미치는지?
복잡하다  유지보수성/비용 등에 영향을 미치는지? 얼마나 영향을 미치는지?
DA 간의 공통점이 아니라 차이점, 즉 상대 DA와 비교할 때의 장/단점을 서술
설계 선택의 타당성
장/단점 분석 결과를 바탕으로 올바른 DA를 선택하였는가?
선택된 DA의 단점에 대한 대책 설계
관련 위험성 분석(문제 발생 가능성과 발생 시 피해 규모 등)
수용할 수 없는 위험성이라면 위험성 관리 방안 제시 및 설계 반영
발생 가능성 낮추기
발생 시 피해 규모 줄이기

| Quality Attribute | Analysis | Approach #1 주차장에서 번호 인식 수행<br>(Selected) | Approach #2 1차적으로 주차장에서 처리, 불가이면 중앙서버에서 처리 |
| --- | --- | --- | --- |
| ID | Title |  |  |  |
| QA-01 | 입차 성능 | Pros | (+) 이미지 전송 오버헤드를 제거 | (+) |
|  |  | Cons | (-) 번호인식 장치 오작동 시 입차 처리 불가 | (-) |
| QA-02 | 출차 성능 | Pros | (+) |  |
|  |  | Cons | (-) 번호인식 장치 오작동 시 출차 처리 불가 |  |
| QA-03 | 번호판추가 유지보수성 | Pros | 없음 | (++) |
|  |  | Cons | (--) |  |
| QA-04 | 번호인식 정확도 | Pros | 해당없음 |  |
|  |  | Cons | (-) 임베디드 기기 특성상 번호 인식 정확도가 낮을 수 있음 | (--) |
| 구축 및 운영 비용 | Pros |  |  |
|  | Cons |  |  |

## Design Decision for QA-02 Title
## Design Decision for QA-03 Title
## Design Decision for QA-04 Title
## Design Decision for QA-05 Title
