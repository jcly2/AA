# System Overview (2페이지 이내)
## System Context Model
## System Context Diagram
<작성 방법>
개발 대상 시스템 자체와 외부의 대상(External Entity)을 명확하게 구분되어야 함.
External entity는 System의 개발 범위 외부의 대상이어야 함.
시스템과 직접적으로 상호 작용하는 모든 대상(사용자, 외부 시스템, 외부 장치 등)이 External entity로서 식별되어야 함.
추후 Use Case Model의 actor와 일치함.
Stakeholder 중에서 System과 직접적으로 interaction하는 사용자는 external entity에 해당될 수 있음.
External entity의 명칭이 구체적이며 해당 Entity의 역할을 의미함.
External entity의 Multiplicity가 명확히 명시되어야 한다 Multiplicity가 Business goal 측면에서 타당해야 함.
External interface
식별 기준: External entity와 시스템 간의 communication channel 별로 interface를 정의함.
방향
Client/Server 기준으로 방향 정의, 즉 데이터 흐름의 방향이 아니라 최초 제어의 방향임
Use case diagram의 association과 개념이 일치함
External Interface 명명
External entity 입장에서 명명; 시스템 관점에서의 기능/역할이 아니라
Interface의 목적/특성 등이 반영된 이름을 정의함.
<예시>
[그림 또는 다이어그램: 원본 문서의 해당 위치를 참조]
## External Entity List
<작성 방법>
System Context Diagram의 각 External entity가 모두 나열되어야 함.
유형: 사용자, 외부 시스템, 외부 장치
설명
각 External entity의 시스템 관점에서의 역할을 기술함.
각 External entity에 대한 multiplicity 설정 및 Business goal에 부합되는 지에 대한 근거 제시 필요
사용자 유형: 단말기 환경 및 숙련도
외부 장치/시스템 유형: 가용성, 성능, 신뢰성 등 해당 EE의 품질 수준

| Name | Kind | Description |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

## System Feature List
<작성 방법>
타당성
Feature 별로 관련된 business goal이 타당해야 함. 즉 해당 Feature는 Business goal 달성에 기여할 수 있어야 함.
Business goal을 달성하기 위하여 필요한 시스템이 제공할 feature가 누락되지 않고 나열한다. 즉 각 Business goal 별로 feature가 제시되어야 함.
Stakeholder 관점에서 이해/평가할 수 있는 수준으로 제시되어야 함. 즉, 구체적인 기능/품질을 의미하지 않음
Title
시스템의 기능/역할이 아니라 이해관계자의 Business Goal 수준으로 기술
시스템 수준이 아니라 비즈니스 수준에서 기술
Description
시스템이 어떤 역할을 함으로써 목표로 하는 Business goal을 달성시킬 수 있는 지를 서술함.
즉, 시스템이 제공할 핵심 역할을 통해서 어떻게 Business goal이 충족될 수 있는 지를 서술함.
개발자가 아니라 이해관계자가 이해할 수 있는 수준으로 서술함.
Importance
Feature의 Importance가 타당해야 함. 즉 관련 Business goal의 Stakeholder들이 동의해야 함.

| ID | Title | Description | I | Related<br>Business Goal ID |
| --- | --- | --- | --- | --- |
| SF-01 |  |  |  | BG-01 |
| SF-02 |  |  |  | BG-01 |
|  |  |  |  | BG-02 |

* I(Importance): 상 중 하로 구분
## Assumptions about the System
<작성 방법>
프로젝트 안내 자료에 명시되지 않았으나 시스템의 설계에서 필요한 여러 가정을 상세히 기술한다.
특히 기존 안내 자료에서 표현된 조건이나 기능 중 본 과제를 위해 수정하였거나 확장한 부분이 있다면 그에 대해 기술한다.
