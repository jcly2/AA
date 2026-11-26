# Architectural Driver
## Primary Functionality (UC 별 1 페이지 이내)
## Use Case Diagram
<작성 방법>
Actor
System의 개발 범위 외부의 대상이다
시스템과 상호작용하는 모든 대상이 Actor로서 식별되어야 한다
System Context Model에서 식별된 External entity와 일관성이 있다
Use case
시스템이 제공할 기능을 나타낸다
사용자 관점의 개별적인 기능 단위를 표현해야 한다
모든 주요 기능 요구사항이 Use case로 식별되어야 한다
Use case diagram에서는 최대 20개의 Use case를 그림으로 표현
Use case text 명세는 중요성이 가장 높은 5개를 선별해서 작성 (UC1~UC5)
다양한 시나리오를 하나의 Use case로 한다
사용자 관점의 궁극적인 결과를 바탕으로 명명한다
Association between actor and use case
Use case를 위하여 필요한 interaction의 대상 Actor와 모든 Association이 정의되어야 한다
Actor와 Use case 간의 연관 관계는 시스템을 통해서 구현되고 제공될 기능을 의미한다. 즉 각 Association이 System과 Actor간의 실제적인 입/출력을 의미한다
Actor와 Use case간의 연관 관계는 제어 흐름을 의미한다 즉 Association의 방향이 interaction의 최초 방향과 일치해야 한다
Generalization
Actor 간의 generalization: 여러 Actor 들 간의 공통적인 UC와의 관계를 간략하게 표현할 때 사용
Use case간의 generalization: 여러 Use case간의 공통적인 동작을 표현할 때 사용. Generalized UC와 Specialized UC의 명세가 복잡하므로 권장되지 않음
Use case간의 <<include>> 관계 사용
Included UC는 Including UC의 공통 기능
Included UC는 Including UC의 부분으로서 수행됨
Included UC는 Including UC에 독립적임
Including UC의 이름은 Included UC의 기능을 포함해야 함
Use case간의 <<extend>> 관계 사용
기본 기능과 추가 기능을 구분하는 목적으로 사용. 추가 기능은 대안 시나리오와 달리 모든 사용자가 아니라, 일부 사용자에게만 추가적으로 제공되는 기능을 의미함. 예) 일부 도서관에서만 연체도서 반납 시 연체료를 부과, 일부 스마트폰에서만 무선충전 기능을 제공함, 일부 사용자에게만 할인을 제공함
기본 기능은 Base UC으로 추가 기능은 Extending UC로 표현
Base UC는 Extending UC에 독립적임
<예시>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## UC-01 [UC Name]
Use Case Scenario
<시나리오 작성 방법>
Use case에 대한 기본 시나리오가 타당한가? 즉 일반적이고 정상적인 상황을 기본 시나리오로서 식별하였는가?
아키텍처 측면에서 고려할 이슈를 포함하는 비기본 시나리오가 식별되었는가?
대안(Alternative) 시나리오
정상적인 상황이지만, 기본 시나리오와 다른 상황
사용자의 다른 선택, 다른 비즈니스 상황, 데이터에 의한 다른 상황
예외(Exceptional) 시나리오
시스템 또는 External Entity의 오동작으로 인해서 발생할 수 있는 상황
입출력 조건 위반 오류, 입출력 시간 초과, 시스템 동작 오류
Scenario Title이 시나리오의 유형과 시나리오가 의미하는 상황을 명확히 표현하는가?
선행 조건
기본 시나리오 동작이 시작되기 위하여 필요한 모든 조건이 식별되어야 함.
선행 조건은
1st step의 입력이 시스템에 들어와도 해당 UC를 시작시키지 않는 타당한(사용자도 수긍할 수 있는) 조건 AND
UC가 수행되는 도중이 아니라, 1st step 시점에서 충족 여부가 판정될 수 있는 조건
선행 조건의 이름이 해당 선행 조건의 내용을 명확히 표현해야 함.
선행 조건의 설명이 해당 선행 조건을 설계/구현할 수 있을 정도로 구체적이고 명확해야 함.
조건/상황의 충족 여부에 대한 판단과 미충족시의 동작은 시스템에 대한 요구사항임, 즉 시스템으로 구현될 수 있는 것만 선행/후행 조건이 되어야 함
후행 조건
기본 시나리오 동작이 종료되었을 때 충족해야할 모든 조건이 식별되어야 함.
후행 조건의 이름이 해당 후행 조건의 내용을 명확히 표현해야 함.
후행 조건의 설명이 해당 후행 조건을 설계/구현할 수 있을 정도로 구체적이고 명확해야 함.
<Flow of Events 작성 방법>
일반
각 Step은 System 또는 오직 하나의 Actor의 동작이 명시되었는가?
System/Actor를 주어로 하는 능동태 문장으로서 하나의 동작만을 표현하였는가?
Actor와 System의 동작이 번갈아 서술되었는가?
System의 기능만을 서술하였는가?
UC Diagram과의 일관성
Use case diagram에서 해당 Use case와 Association된 모든 Actor가 언급되었는가?
첫 Step은 Triggering actor의 입력 동작인가?
시나리오 구체성
주요 시스템 동작(입력, 변환/계산, 출력 등)을 기술하는가?
다른 Use case와 공유되는 데이터/정보를 동일한 이름을 사용하고 공유 데이터/정보임을 표시 필요 예) [공유 데이터 명]

| UC name |  |
| --- | --- |
| Pre-conditions | 조건1(이름): 조건설명, 미충족시 시스템 동작 설명<br>조건2(이름): … |
| Flow of events | Main success flow | 1.<br>2.<br>3. |
|  | Alternative or exceptional flow | A1: alternative 시나리오 명<br>1.<br>2. |
|  |  | A2: alternative 시나리오 명<br>1.<br>2. |
|  |  | E1: exceptional 시나리오 명<br>1.<br>2. |
| Post-conditions | 조건1(이름): 조건설명, 미충족시 시스템 동작 설명<br>조건2(이름): … |

## UC-02 [UC Name]
## UC-03 [UC Name]
## UC-04 [UC Name]
## UC-05 [UC Name]
## Quality Attribute Scenario (QA 별 1 페이지 이내)
## QA Scenario List
<작성 방법>
QA가 시스템의 경쟁력과 사업적 우위를 점하기 위해 유의미하게 선정되었는가?
System feature를 실현하기 위하여 필요한 모든 QA를 식별한다.
시스템에 중대한 순서대로 QA-01부터 배치했는가?
QA Type이 올바른가? 즉 해당 QA에 올바른 QA Type을 기술하였는가?
Title이 QA를 구체적으로 표현하고 있는가?
Importance가 stakeholder(특히 사용자) 관점에서 타당하고 합의되었는가?
Difficulty가 개발자 관점에서 타당하고 합의되었는가?
QA와 관련된 기능 요구사항이 Use case로서 올바르게 제시되었는가?

| ID | Title | Type | Priority | Related<br>Use Case | System<br>Feature<br>ID |
| --- | --- | --- | --- | --- | --- |
|  |  |  | I | D |  |  |
| QA-01 |  |  |  |  | UC-01 | SF-01 |
| QA-02 |  |  |  |  | UC-02 | SF-02 |
|  |  |  |  |  |  |  |

## QA-01 Title Scenario
<작성 방법>
Description: 해당 QA Scenario에 대한 간략한 설명을 명확하게 기술 필요
Source
Stimulus를 발생시키는 시스템 내부/외부의 존재임
성능, 보안 등의 경우 입력 부하를 암시하는 Stimulus의 규모도 서술 필요
Stimulus
Source가 발생/요구하며, Artifact의 Response를 유발하는 이벤트 서술
구체적이어야 함. 즉 아키텍처 평가를 수행할 때 실제 어떤 입력이 사용되는 명확하게 판단할 수 있어야 함.
성능 예) 센서데이터  초당 1,000개 센서 데이터; External Interface의 항목과 일관성 필요
변경 용이성 예) 기능의 추가  새로운 암호화 알고리즘의 추가
Artifact
Runt-time QA: 시스템 동작과 관련된 QA(성능, 보안 등)의 경우, Stimulus를 수신하여 Response를 생성하는 주체가 되어야 함
Development-time QA: 개발자가 관련하는 QA(예, 유지보수성 등)의 경우 Artifact는 Response(수정, 테스트 등)의 대상이 되어야 함.
Environment
Response가 발생/수행되는 시스템 내부/외부 상황(Resource) 서술; 특히 Measure에 영향을 미칠 수 있는 Artifact의 Resource 및 관련 외부 환경(외부 장치/시스템, 네트워크 등) 상황 서술
Stimulus에 대한 Response를 관찰하며 Measure의 수치가 기대될 수 있는 구체적인 환경이 기술되어야 함. 예) Stimulus 수신 당시 시스템의 부하
Response
Stimulus에 따라서 필요한 동작/작업을 서술함
구체적이어야 함. 즉 해당 QA에 대한 평가를 수행할 때 관찰/판단의 대상이 되는 동작/결과를 구체적으로 기술 필요
Response Measure
QA의 충족 여부의 판단 기준을 서술함
Response와 일관성 필요; Measure의 유형 및 수치가 Response와 일관성 필요
구체적이어야 함; Response를 관찰/분석함으로써 Measure의 충족 여부/수준을 결정할 수 있어야 함
Stimulus, Environment, Response, Measure 등이 System Feature를 달성하기에 타당하고 충분해야 함.

| QA Type |  |
| --- | --- |
| Description |  |
| Source of Stimulus |  |
| Stimulus |  |
| Artifact |  |
| Environment |  |
| Response |  |
| Response Measure | 측정 기준: stimulus 입력에서 response 완료까지의 소요 시간<br>목표치: 평균 2초<br>목표치 설정 근거: 관련 SF 및 BG 측면에서 목표치 설정 근거를 서술 |

## QA-02 Title Scenario
## QA-03 Title Scenario
## QA-04 Title Scenario
## QA-05 Title Scenario
* 총 5개 QA 명세
