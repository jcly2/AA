# Architectural Design Description (제시된 Diagram 및 표 양식만 작성)
## Structure View
<작성 방법>
Deployment model에서 표시된 각 노드 중에서 SW 컴포넌트가 배치되는 노드에 대하여 작성
## Elevator 관리 서버
## System Structure Model
<작성 방법>
Component
시스템의 AD(기능 및 QA)를 달성하기 위하여 필요한 주요 Component가 식별되었는가?
각 컴포넌트는 높은 응집도를 가지는가? 즉 기능적, 변경, 재사용 단위가 될 수 있는가?
Component는 Provided Interface를 구현하는 특정 구현 방법, 플랫폼, 기능의 범위 등을 구체적으로 표현한다.
Component는 시스템의 QA(성능, 가용성 등) 달성에 필요한 적절한 Multiplicity가 정의되었는가?
Component의 수가 많은 경우 Package를 이용하여 Component들을 타당하게 grouping 하였는가?
Interface
Interface는 Component가 구현하는 기능에 대한 명세를 정의하는가?
각 Provided Interface는 ISP를 충족시키고 있는가? 즉 Component의 Client 별로 Interface를 정의되었는가?
Interface는 Provider Component에 독립적인가? Interface는 구현 방법, 플랫폼, 기능의 범의 등을 암시하지 않는 일반적인 용어로 표현한다
Interface는 Client Component에 독립적인가? Interface가 특정 Client Component 관점에서 필요한 기능을 명세하지 않아야 한다.
설계 기법 적용
QA 달성에 필요한 다양한 architecture pattern이 적절하게 적용되었는가?
유지보수성: Layer, Front controller, Gateway, Wrapper, …
성능: Mas.ter-sla.ve, …
Tactic 적용
Availability, Performance 등의 QA에 대하여 적절한 설계 전술(tactic)이 적용되었는가?
Strict version
각 Component의 Port가 명확히 식별되었는가?
각 Port는 communication mechanism이 stereotype으로 명시되었는가?
<Simplified version>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
<Strict version>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## Component List

| Layer | Component | Component<br>Responsibility | Provided<br>Interfaces | Provided Interfaces 설명 |
| --- | --- | --- | --- | --- |
| presentation | Elevator관리UI | … | N/A |  |
| business logic | Elevator관리 | … | IElevator관리 | … |
| business logic | ElevatorScheduler | … | IElevator선택 | … |
| system access | Elevator제어GW | … | IElevator제어 | … |
| data access | Elevator상태관리 | … | IElevator상태갱신 | … |
|  |  |  | IElevator상태조회 | … |

## Elevator 제어 서버
## System Structure Model
<Simplified version>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
<Strict version>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## Behavior View
<작성 방법>
주요 기능 요구사항에 대한 realization이 정의되었는가? 즉 Architectural driver로서 식별된 각 use case에 대하여 realization이 정의되었는가?
## UC-01 Elevator관리
<작성 방법>
해당 Use case의 기능을 realization하기 위하여 필요한 component instance가 lifeline으로서 정의되었는가?
각 component instance의 deployment target이 Deployment view의 node와 일치하는가?
각 message는 receiver component의 interface operation에 해당되는가?
UC 시나리오가 구체적으로 Message로 표현되는가? 즉 UC 기본 시나리오 및 주요 대안 시나리오에 해당되는 동작이 Message로 표현되었는가? 기본 시나리오 및 주요 대안 시나리오의 동작이 alt, opt, loop 등으로 구체화되었는가?
각 Message에 대하여 인자(parameter)가 제시되었는가? 이 인자가 Message에 해당되는 interface 연산의 인자와 일치하는가?
UC간의 <<include>>는 Interaction Use로 표현하였는가?
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## UC-04 Elevator이동
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## Deployment View
## Deployment Model
<작성 방법>
Context/UC Diagram  Infrastructure Diagram 일관성
External entity/Actor의 존재/multiplicity  external entity로 표현
External interface/Association 존재/방향/Protocol/multiplicity  Comm. Path 존재/방향/Protocol/multiplicity
Node 설계
Node 명: Node의 역할(기능/QA) 표현
각 노드 Instance의 역할 명시: 예) Primary, Spare(Hot, Warm, Cold), DB Server Mas.ter-sla.ve 등
Comm. Path의 설계
필요성: 상대 노드와의 communication(즉, message 전송)과의 일관성
방향: Client  Server
Multiplicity
동시에 몇 개의 상대 노드와 comm. Path를 유지할지
상대가 N개인 경우, 메시지 전송 상대에 대한 결정 동작에 대한 설계 필요
Load balancer, Broker
Client-side load balancing
«execution environment» 설계
노드에 요구되는 QA(성능, 가용성, 신뢰성 등)을 고려한 SW 플랫폼 결정
Comm. Path의 Protocol과의 일관성 필요
예) http이면 Server side에는 Web serve가 «execution environment» 가 되어야 함
<예시>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## Deployment Specification
<작성 방법>
Infrastructure model에서 표시된 각 노드 별로 기술한다.
Description
각 노드의 설명이 구체적인가?
각 노드가 시스템의 기능/QA 측면에서 어떤 역할을 하는지 설명이 필요하다.
복수 개 Multiplicity 인 경우 각 Instance의 역할을 명확히 기술한다.
Deployed BL(Business Logic) Components
해당 노드에 배치(배포)되는 Component들 중에서 business logic components를 나열한다.
Structure View의 business logic layer에 포함된 Component와 일치해야 한다

| Name | Description | Deployed BL Components |
| --- | --- | --- |
| 관리자 PC |  | 없음 |
| Elevator 관리 서버 |  | Elevator관리<br>ElevatorScheduler |
| Elevator 제어 서버 |  | Elevator이동<br>Elevator상태관리 |
| Elevator DB 서버 |  | 없음 |

