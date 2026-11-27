# 소프트웨어 아키텍처 명세 보고서 양식 분석

> 원본: `2026_AA_인증과제-보고서-양식-v4_2.docx`
> 문서 성격: 인증과제용 **소프트웨어 아키텍처(AA) 명세서 작성 양식(템플릿)**. 각 절마다 `<작성 방법>`(평가 기준 성격의 체크 항목)과 빈 표/예시 그림 자리가 들어 있음.
> 예시 도메인: 엘리베이터 관리·제어 시스템(Elevator), 주차장 번호 인식(Design Approach 예시)

---

## 1. 문서 전체 구조 한눈에 보기

| 장 | 제목 | 분량 제한 | 핵심 내용 | 성격 |
|---|---|---|---|---|
| 표지 | `<시스템 명>` 소프트웨어 아키텍처 명세 | - | 작성자, Revision History(Version/Date/Summary) | 형식 |
| 1 | Project Overview | 2페이지 이내 | 프로젝트 배경, 이해관계자, 비즈니스 목표 | 요구 분석 |
| 2 | System Overview | 2페이지 이내 | 시스템 컨텍스트, 외부 엔티티, 시스템 기능, 가정 | 요구 분석 |
| 3 | Architectural Driver | UC·QA별 1페이지 이내 | 주요 기능(Use Case), 품질 속성 시나리오 | 아키텍처 동인 |
| 4 | Architectural Design Decision | Goal 0.5p, Approach별 2p, Decision 1p 이내 | QA별 설계 목표, 설계 대안 비교, 결정 | 설계 의사결정 |
| 5 | Architectural Design Description | 제시된 다이어그램·표 양식만 작성 | Structure / Behavior / Deployment 뷰 | 설계 기술 |
| 6 | Epilogue | 1페이지 이내 | 소감, 추가 연구 주제, 특별히 사용한 용어 | 마무리 |

### 전체 흐름(추적성)

```
Stakeholder → Business Goal(BG) → System Feature(SF) → Use Case(UC) / QA Scenario(QA)
   → Design Decision(QA별) → Structure / Behavior / Deployment View
```

- 각 단계의 ID(BG-xx, SF-xx, UC-xx, QA-xx)를 서로 연결해 **요구 → 설계까지 추적 가능**하게 하는 것이 양식의 핵심 구조.
- 요구 분석(1~2장)에서 정한 External Entity는 Use Case의 Actor, Deployment의 외부 노드와도 **일관**되어야 함.

---

## 2. 장별 상세 분석

### 2.1 Project Overview (2페이지 이내)

#### 1.1 Project Background
- 프로젝트 배경 지식, 개발 제품의 일반적 필요성·역할 설명
- 시장 환경, 기존/경쟁 제품 분석·비교는 **간략히**
- 프로젝트 **범위** 제시: 비즈니스가 발생하는 장소/공간, 사용자 범위, 핵심 기능, 가치/기대효과

#### 1.2 Stakeholder List
**작성 기준**

| 평가 관점 | 내용 |
|---|---|
| 구체성 | 조직·단체 같은 광범위 개념이 아니라 **구체적 관련자**로 식별. BG를 고려해 세분화(예: 일반 사용자 vs 관리자) |
| 완전성 | 시스템 **전체 생애주기**(기획, 개발, 시험/인증, 획득/도입, 판매, 배포/설치, 사용, 운영/관리, 유지보수, 폐기) 관련자 포함 |
| 서술 구체성 | **배경**(소속 조직·목적), **역할**(업무), **애로사항**(비즈니스 관점의 어려움, 시스템 관점 아님) |
| BG와의 관련성 | BG를 갖게 된 *배경*만 서술. 원하는 것·목표는 BG에서 서술 |

**표 양식**: `Stakeholder | Description(배경·역할·애로사항)`
예시 행: 엘리베이터 이용자, 건물 관리자, 승강기 안전공단, 승강기 유지관리 업체

#### 1.3 Business Goal List
**작성 기준**

| 평가 관점 | 내용 |
|---|---|
| 타당성 | 이해관계자별 비즈니스 수준 목표. 역할/애로사항과 부합해야 함 |
| 명확성 | 달성 여부를 판단할 **지표와 목표치** 제시 |
| 달성 가능성 | 이후 System Feature를 통해 실현 가능해야 하며, 목표치도 시스템으로 달성 가능해야 함 |
| 중요도 | BG 간 충돌 시 우선순위로 쓸 수 있도록 타당하게 부여 |

**이해관계자별 BG 예시(양식 제공)**

| 이해관계자 | 예시 목표 |
|---|---|
| 최종 사용자 | 업무 편의성/효율성 개선, 만족도 개선 |
| 비즈니스 관리자/운영자 | 고객 만족도 개선, 시장 점유율 확대, 매출 증대, 관리·운영 비용 절감 |
| 시스템 개발/판매 조직 | 개발 편의성·비용 절감(개발), 시장 점유율·매출(판매) |
| 시스템 관리자/운영자 | 비즈니스 연속성 제고, 고객 만족도 제고 |
| 시스템 유지보수 조직 | 유지보수 편의성·비용 절감, 고객 만족도 개선 |

**표 양식**: `Stakeholder | ID(BG-01…) | Statement | I(Importance: 상/중/하)`

---

### 2.2 System Overview (2페이지 이내)

#### 2.1 System Context Model

**2.1.1 System Context Diagram**
- 개발 대상 시스템과 **External Entity**(사용자, 외부 시스템, 외부 장치)를 명확히 구분
- External Entity는 개발 범위 **외부** 대상이며, 시스템과 직접 상호작용하는 모든 대상을 식별. 이후 Use Case의 **Actor와 일치**해야 함
- 명칭은 구체적이고 역할을 의미해야 하며, **Multiplicity**를 명시(BG 측면에서 타당해야 함)
- **External Interface**
  - 식별 기준: Entity와 시스템 간 **communication channel별**로 정의
  - 방향: 데이터 흐름이 아니라 **최초 제어 방향**(Client/Server 기준). Use Case의 association과 일치
  - 명명: **External Entity 입장**에서, 인터페이스의 목적/특성이 드러나게 (시스템 관점의 기능명 아님)
- 예시 그림 제공(원본에는 다이어그램 자리)

**2.1.2 External Entity List**
- Context Diagram의 모든 Entity를 나열
- 유형: 사용자 / 외부 시스템 / 외부 장치
- 설명: 시스템 관점에서의 **역할**, multiplicity와 BG 부합 근거
  - 사용자: 단말기 환경 및 숙련도
  - 외부 장치/시스템: 가용성, 성능, 신뢰성 등 품질 수준
- 표 양식: `Name | Kind | Description`

#### 2.2 System Feature List
| 평가 관점 | 내용 |
|---|---|
| 타당성 | Feature와 BG의 관련이 타당. **각 BG마다 feature가 누락 없이** 제시. 이해관계자가 이해·평가할 수준(구체 기능/품질 아님) |
| Title | 시스템 기능이 아니라 **이해관계자의 BG 수준(비즈니스 수준)** 으로 기술 |
| Description | 시스템이 어떤 역할을 해서 BG를 달성시키는지, **이해관계자가 이해할 수준**으로 서술 |
| Importance | 관련 BG의 이해관계자가 동의할 수 있는 타당한 중요도 |

표 양식: `ID(SF-01…) | Title | Description | I(상/중/하) | Related Business Goal ID`

#### 2.3 Assumptions about the System
- 안내 자료에 없지만 설계에 필요한 **가정**을 상세 기술
- 안내 자료의 조건/기능을 **수정·확장**했다면 그 내용도 기술

---

### 2.3 Architectural Driver

#### 3.1 Primary Functionality (UC별 1페이지 이내)

**3.1.1 Use Case Diagram**

| 요소 | 작성 기준 |
|---|---|
| Actor | 개발 범위 외부 대상, 상호작용하는 모든 대상 식별, Context Model의 External Entity와 **일관** |
| Use Case | 사용자 관점의 개별 기능 단위. 주요 기능 요구사항이 모두 UC로 식별. 다이어그램에는 **최대 20개**, 텍스트 명세는 중요도 상위 **5개(UC-01~05)** 만 작성. 여러 시나리오를 하나의 UC로 묶고, 사용자 관점의 궁극적 결과로 명명 |
| Association | Actor-UC 간 실제 입출력(구현·제공될 기능)을 의미, **제어 흐름 방향 = 최초 interaction 방향** |
| Generalization | Actor 간: 공통 UC 관계를 간략히 표현할 때 사용. UC 간: 명세가 복잡해지므로 **권장되지 않음** |
| `<<include>>` | Included UC는 Including UC의 **공통 기능**이자 **일부로 수행**되며 Including UC에 독립적. Including UC 이름은 Included UC 기능을 포함 |
| `<<extend>>` | 기본 기능(Base UC)과 추가 기능(Extending UC)을 구분. 추가 기능은 **일부 사용자에게만** 제공(예: 일부 도서관의 연체료, 일부 스마트폰의 무선충전). Base UC는 Extending UC에 독립적 |

**3.1.2~3.1.6 UC-01 ~ UC-05 [UC Name]: Use Case 명세**

*시나리오 작성 기준*

| 구분 | 기준 |
|---|---|
| 기본 시나리오 | 일반적·정상적 상황 |
| 대안(Alternative) 시나리오 | 정상이지만 기본과 다른 상황(사용자의 다른 선택, 다른 비즈니스 상황, 데이터에 의한 차이) |
| 예외(Exceptional) 시나리오 | 시스템/외부 엔티티 오동작(입출력 조건 위반, 시간 초과, 시스템 동작 오류) |
| 시나리오 Title | 유형과 상황이 명확히 드러나야 함 |
| 선행 조건 | 1st step 시점에 판정 가능, 입력이 들어와도 UC를 시작시키지 않는 타당한 조건, 이름·설명이 구체적, **시스템이 구현할 수 있는 것만** 포함, 미충족 시 동작도 요구사항 |
| 후행 조건 | 기본 시나리오 종료 시 충족해야 할 모든 조건, 이름·설명이 구체적 |

*Flow of Events 작성 기준*
- 각 Step은 **System 또는 오직 하나의 Actor**의 동작 하나만 기술(능동태), Actor와 System이 **번갈아** 서술
- System 기능만 서술, 첫 Step은 **Triggering actor의 입력**
- UC Diagram에서 해당 UC와 연결된 **모든 Actor가 언급**되어야 함
- 주요 시스템 동작(입력, 변환/계산, 출력) 기술, 다른 UC와 공유되는 데이터는 같은 이름 사용 + `[공유 데이터 명]` 표기

*표 양식*

| 항목 | 내용 |
|---|---|
| UC name | |
| Pre-conditions | 조건1(이름): 설명, 미충족 시 시스템 동작 |
| Flow of events | Main success flow (1, 2, 3…) / A1·A2: Alternative flow / E1: Exceptional flow |
| Post-conditions | 조건1(이름): 설명, 미충족 시 시스템 동작 |

#### 3.2 Quality Attribute Scenario (QA별 1페이지 이내)

**3.2.1 QA Scenario List**
- QA가 시스템 경쟁력·사업적 우위 관점에서 의미 있게 선정되었는가
- System Feature 실현에 필요한 **모든 QA** 식별, **중요한 순서대로 QA-01부터** 배치
- QA Type이 올바르고 Title이 구체적일 것
- **Importance(I)**: stakeholder(특히 사용자) 관점에서 합의, **Difficulty(D)**: 개발자 관점에서 합의
- 관련 기능 요구사항이 Use Case로 연결될 것
- 표 양식: `ID | Title | Type | Priority(I, D) | Related Use Case | System Feature ID`
- 총 **5개** QA 명세 작성 (QA-01~QA-05)

**3.2.2~3.2.6 QA-0x Title Scenario: 6요소 명세**

| 요소 | 작성 기준 |
|---|---|
| Description | 시나리오 간략 설명 |
| Source of Stimulus | Stimulus를 발생시키는 내·외부 존재. 성능·보안은 **입력 부하 규모**도 서술 |
| Stimulus | Artifact의 Response를 유발하는 이벤트. 평가 시 실제 입력이 무엇인지 판단 가능할 정도로 **구체적**. External Interface와 일관 (성능 예: 초당 1,000개 센서 데이터 / 변경용이성 예: 새로운 암호화 알고리즘 추가) |
| Artifact | **Runtime QA**(성능, 보안 등): Stimulus를 받아 Response를 만드는 주체 / **Development-time QA**(유지보수성 등): Response(수정, 테스트)의 **대상** |
| Environment | Response가 발생하는 내·외부 상황. Measure에 영향을 주는 자원·외부 환경(장치, 네트워크, 시스템 부하 등) |
| Response | Stimulus에 따른 동작/작업. 평가 시 관찰·판단 대상이 되는 동작·결과를 구체적으로 |
| Response Measure | 충족 여부 판단 기준. Response와 **유형·수치 일관**, 관찰·분석으로 판정 가능. 측정 기준 / 목표치 / **목표치 설정 근거**(관련 SF·BG 측면) 포함 |

- 표 양식 예: `QA Type`, `Description`, `Source of Stimulus`, `Stimulus`, `Artifact`, `Environment`, `Response`, `Response Measure(측정 기준: stimulus 입력~response 완료 소요시간, 목표치: 평균 2초, 근거 서술)`
- Stimulus/Environment/Response/Measure 전체가 **System Feature 달성에 타당하고 충분**해야 함

---

### 2.4 Architectural Design Decision (QA별 반복: 4.1~4.5)

QA-01~05 각각에 대해 **Design Goal → Design Approach List → Decision** 3단계로 작성.

#### Design Goal (0.5페이지 이내)
- QA를 다시 서술하지 말고, 달성을 막는 **세부·구체적 설계 이슈**로 구체화
- QA 유형별 고려 예시

| QA | Goal 설정 시 던질 질문 |
|---|---|
| 성능 | Bottleneck은? 대규모 입력인가, 빈번한 입력인가, 처리 복잡도인가? |
| 가용성 | 어떤 상황에서, 얼마나 자주 fault가 발생? Fault 탐지가 어렵거나 느린 원인은? |
| 변경용이성 | 어떤 상황·빈도로 변경 요청 발생? 수용이 어렵거나 느린 원인은? |
| 정확성 | 저해 요인은 데이터 문제(부족, 노이즈, 오차)인가, 계산 로직의 부정확성인가? |
| 사용성 | 사용자를 불편하게 하는 입력은? 왜 반복 입력·실수가 많은가? |

#### Design Approach List (Approach별 2페이지 이내)
- 목표 QA를 달성할 수 있는 **대안들을 제시하고 비교**
  - 적절한 예: crash 탐지를 위한 *ping/echo vs heartbeat* 비교
  - 부적절한 예: *ping/echo(crash 탐지) vs exception handling(incorrect response 탐지)* 비교 (해결하려는 문제가 서로 다름)
- 외부 연동 시스템/장치, 사용자 인터페이스 방식은 **요구사항**이므로 Design Decision 대상이 아님
- **학습한 패턴·전술(tactic) 적용** 중심. 플랫폼/프레임워크 비교·선택이나, component/interface 식별과 거리가 먼 알고리즘 선택은 다루지 않음
- 각 Approach 작성 기준
  - **Title**: 핵심 기법, 다른 DA와 차별성 명확
  - **설명**: 적절한 View(Structure/Behavior/Deployment)로 표현, 패턴·Tactics 적용을 **명시**
  - **설계 구체성**: 일반론이 아니라 **이 시스템에 적용한 아키텍처 모습** 제시

| 적용 설계 | 구체화해야 할 결정 |
|---|---|
| Layer 패턴 | Layer 수, 각 역할, Layer interface |
| Health check(ping/echo, heartbeat) | liveness, state consistency(invariant) 판단 수준 |
| Cache | 보관 데이터, Update 방법 |
| Passive redundancy | 동기화 대상 데이터, 주기, 비용 |

- 예시 DA: `#1 주차장에서 번호 인식 수행` / `#2 1차적으로 주차장에서 처리, 불가 시 중앙서버에서 처리`

#### Decision (1페이지 이내)
| 평가 관점 | 내용 |
|---|---|
| 분석의 완전성 | 목표 QA 및 관련 AD 관점의 장단점 모두 제시 |
| 분석의 타당성 | 장단점이 올바르고 목표 QA 측면에서 분석됨 |
| 분석의 구체성 | 단순 사실이 아니라 기준(QA 등)에 **어떤 이유로 어느 정도 영향**을 주는지 서술. 예: "오버헤드 존재 → 성능에 얼마나?", "복잡하다 → 유지보수성/비용에 얼마나?" |
| 차이점 중심 | DA 간 **공통점이 아니라 상대 대비 차이**를 서술 |
| 선택의 타당성 | 분석 결과에 부합하는 DA 선택 |
| 선택안의 단점 대책 | 위험성 분석(발생 가능성, 피해 규모). 수용 불가 시 **발생 가능성 낮추기 / 피해 규모 줄이기** 방안을 설계에 반영 |

**표 양식(예시)**: 행 = QA(+구축·운영 비용), 열 = `Analysis(Pros/Cons)`, `Approach #1 (Selected)`, `Approach #2`. 셀에는 `(+)`, `(++)`, `(-)`, `(--)` 로 영향 정도를 표기하고 사유를 함께 적음.

---

### 2.5 Architectural Design Description (제시된 다이어그램·표 양식만 작성)

#### 5.1 Structure View
- Deployment Model에서 **SW 컴포넌트가 배치되는 노드별**로 작성 (예: Elevator 관리 서버, Elevator 제어 서버)
- 각 노드마다 **System Structure Model**(Simplified / Strict 버전) + **Component List**

**Component·Interface 작성 기준**

| 구분 | 기준 |
|---|---|
| Component | AD(기능·QA) 달성에 필요한 주요 컴포넌트 식별, **높은 응집도**(기능·변경·재사용 단위), 구현 방법·플랫폼·범위를 구체적으로 표현, QA 달성에 맞는 **Multiplicity**, 많으면 Package로 grouping |
| Interface | Component 기능 명세, **ISP 충족**(Client별 인터페이스), **Provider 독립**(구현 방법·플랫폼 암시 금지), **Client 독립**(특정 Client 관점 기능 명세 금지) |
| 설계 기법 | QA에 맞는 아키텍처 패턴(유지보수성: Layer, Front controller, Gateway, Wrapper 등 / 성능: Master-slave 등)과 Tactic 적용 |
| Strict version | 각 Component의 **Port** 식별, 각 Port의 communication mechanism을 **stereotype**으로 명시 |

**Component List 표 양식**: `Layer | Component | Component Responsibility | Provided Interfaces | Provided Interfaces 설명`

예시(Elevator 관리 서버)

| Layer | Component | Provided Interface |
|---|---|---|
| presentation | Elevator관리UI | N/A |
| business logic | Elevator관리 | IElevator관리 |
| business logic | ElevatorScheduler | IElevator선택 |
| system access | Elevator제어GW | IElevator제어 |
| data access | Elevator상태관리 | IElevator상태갱신, IElevator상태조회 |

#### 5.2 Behavior View
- Architectural Driver로 식별된 **각 UC에 대한 realization(Sequence Diagram)** 정의 (예: UC-01 Elevator관리, UC-04 Elevator이동)
- 체크 항목
  - UC 기능 구현에 필요한 **component instance를 lifeline**으로 정의
  - 각 instance의 **deployment target이 Deployment View의 node와 일치**
  - 각 message = receiver component의 **interface operation**
  - 기본 시나리오 + 주요 대안 시나리오를 message로 표현, `alt / opt / loop`로 구체화
  - 각 message의 **인자(parameter)** 제시 + interface 연산 인자와 일치
  - UC 간 `<<include>>`는 **Interaction Use**로 표현

#### 5.3 Deployment View

**5.3.1 Deployment Model**
- Context/UC Diagram ↔ Infrastructure Diagram **일관성**: External entity/Actor의 존재·multiplicity, External interface/Association의 존재·방향·Protocol·multiplicity가 Communication Path로 이어짐
- **Node 설계**: 이름에 역할(기능/QA) 표현, 각 instance의 역할 명시(Primary, Spare(Hot/Warm/Cold), DB Server Master-slave 등)
- **Comm. Path 설계**: 필요성(메시지 전송과 일관), 방향(Client→Server), Multiplicity(동시 유지 상대 노드 수), 상대가 N개면 **결정 동작 설계**(Load balancer, Broker, Client-side load balancing)
- **«execution environment»**: 노드의 QA를 고려한 SW 플랫폼 결정, **Protocol과 일관**(예: http → Server side에 Web server)

**5.3.2 Deployment Specification**
- 노드별 `Name | Description | Deployed BL Components`
- Description: 노드가 기능/QA 측면에서 하는 **역할**, 복수 multiplicity면 **각 instance 역할** 명시
- Deployed BL Components: 해당 노드에 배치되는 business logic 컴포넌트. **Structure View의 business logic layer 컴포넌트와 일치**해야 함

| Name | Deployed BL Components(예시) |
|---|---|
| 관리자 PC | 없음 |
| Elevator 관리 서버 | Elevator관리, ElevatorScheduler |
| Elevator 제어 서버 | Elevator이동, Elevator상태관리 |
| Elevator DB 서버 | 없음 |

---

### 2.6 Epilogue (1페이지 이내)
- 소감, 더 연구해 볼 만한 주제, 특별하게 사용된 용어 등

---

## 3. 일관성(Consistency) 체크포인트 총정리

양식 전반에 흩어진 "일관성" 요구를 한곳에 모으면 다음과 같습니다.

| 출발 | 도착 | 일관성 내용 |
|---|---|---|
| Stakeholder | Business Goal | BG는 이해관계자의 역할·애로사항과 부합 |
| Business Goal | System Feature | **모든 BG에 feature 존재**, Feature 중요도는 BG 이해관계자가 동의 |
| External Entity (Context) | Actor (UC Diagram) | 동일한 대상, 명칭·multiplicity 일치 |
| External Interface | Association(UC), Comm. Path(Deployment) | 존재·방향(최초 제어)·Protocol·multiplicity 일치 |
| System Feature | UC / QA | QA 목록에서 관련 UC, SF ID 연결 |
| Stimulus | External Interface | 입력 종류·규모 일관 |
| Response ↔ Response Measure | - | 유형·수치 일관 |
| QA | Design Goal → Approach → Decision | 목표 QA의 장애 요인 → 해결 대안 → 장단점 분석 |
| UC | Sequence Diagram | 모든 주요 UC에 realization, lifeline·message가 interface와 일치 |
| Component(Structure) | Node(Deployment) | BL Component 배치가 노드와 일치 |
| Sequence의 lifeline | Deployment Node | 배치 대상 노드 일치 |

---

## 4. 분량·개수 제약 요약

| 항목 | 제한 |
|---|---|
| 1장 Project Overview | 2페이지 이내 |
| 2장 System Overview | 2페이지 이내 |
| Use Case 다이어그램 | UC 최대 20개 |
| Use Case 명세 | 상위 5개(UC-01~05), UC별 1페이지 이내 |
| QA Scenario | 총 5개(QA-01~05), QA별 1페이지 이내 |
| Design Goal | 0.5페이지 이내 |
| Design Approach | Approach별 2페이지 이내 |
| Decision | 1페이지 이내 |
| 5장 Architectural Design Description | 제시된 다이어그램·표 양식만 작성 |
| Epilogue | 1페이지 이내 |

---

## 5. 양식의 평가 관점 요약 (작성 시 주의점)

1. **비즈니스 수준 vs 시스템 수준 구분**: Stakeholder 애로사항·BG·System Feature Title은 *비즈니스 관점*, Use Case·QA·설계부터 *시스템 관점*.
2. **구체성과 측정 가능성**: BG는 지표·목표치, QA는 Stimulus·Measure 수치, Design Approach는 "이 시스템에 적용한 구체 구조"를 요구.
3. **설계 대안은 같은 문제에 대한 비교**: 서로 다른 문제를 푸는 기법끼리 비교하면 부적절.
4. **학습한 패턴·전술 중심**: 프레임워크/플랫폼 선택이나 알고리즘 선택은 범위 밖.
5. **인터페이스 방식은 요구사항**: 외부 시스템 연동·UI 방식은 Design Decision이 아님.
6. **단점 대책 필수**: 선택한 DA의 단점은 위험성 분석 후 설계에 반영.
7. **ID 기반 추적성**: BG → SF → UC/QA → Design → View로 이어지는 ID 연결을 유지.

---

## 6. 원본 문서에서 확인된 특이사항

- 원본은 **양식 파일**이므로 `<작성 방법>` 블록은 제출 시 삭제하고 내용을 채워야 하는 안내문임.
- 다이어그램 영역(`<예시>`, `<Simplified version>`, `<Strict version>`)은 이미지 자리로, 텍스트로는 추출되지 않아 위 분석에 포함하지 못함.
- 표 안의 `Elevator`, `주차장 번호 인식` 내용은 **작성 예시**일 뿐 본 과제(전자칠판)의 내용이 아님.
- 목차의 페이지 번호(5, 8, 10 …)는 양식 기준이며 실제 작성 후 갱신 필요. 5.1~5.3 소제목(Elevator 관리 서버 등)은 프로젝트에 맞게 교체해야 함.
- 5장은 "제시된 Diagram 및 표 양식만 작성"이라는 지침이 있어 자유 서술 분량은 최소화.

---

## 7. 전자칠판 프로젝트에 대입해 보기 (참고)

지금까지 팀에서 논의한 내용을 이 양식에 매핑하면 다음과 같이 이어 쓸 수 있습니다. (예시이며 팀 합의에 따라 조정 필요)

| 양식 항목 | 연결 가능한 기존 산출물 |
|---|---|
| External Entity / Actor | 교사(사용자), 학생(열람자), 관리자, 외부 생성형 AI 서비스, 클라우드/USB, 앱 스토어·펌웨어 서버, 입력 소스(HDMI/DP/USB-C) |
| System Feature | 필기·펜(SFR-003), 스티커(SFR-004), 텍스트 인식·저장(SFR-002), 업데이트(SFR-001) |
| Use Case 후보 | 판서하기, 스티커 붙이기, 손글씨 텍스트 변환·저장, 펌웨어/앱 업데이트 |
| QA 후보 | 성능(PFR-001/002), 신뢰성(QUR-001 AI 장애 대응), 시험 용이성(QA_003/TER-001), 유지보수성·수정용이성, 사용성(USR-001~004) |
| Design Decision 소재 | AI 장애 시 기본 기능 유지(Bulkhead, Circuit Breaker, 대기열 재시도), 외부 AI 교체 용이성(Adapter, Wrapper), 테스트 용이성 전술(abstract data sources, record/playback 등) |
| Deployment | 전자칠판(Android 등) 노드, 외부 AI 서비스, 업데이트/배포 서버, 클라우드 저장소 |

> 팀의 Refined QAS 형식(Requirement-ID/Category/Source/Stimulus/Artifacts/Environment/Response/Response Measure)은 이 양식의 QA 6요소 표(Source of Stimulus/Stimulus/Artifact/Environment/Response/Response Measure)와 거의 같은 구조이므로 그대로 옮길 수 있습니다. 단, 이 양식은 **Description, QA Type, 목표치 설정 근거**를 추가로 요구합니다.
