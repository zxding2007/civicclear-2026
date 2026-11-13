# CivicClear system design / UML

## Use-case diagram

```mermaid
flowchart TB
    R((Resident)) --> U1[Browse official agenda items]
    R --> U2[Read stage-aware plain explanation]
    R --> U3[Check ward and original evidence]
    R --> U4[View verified participation information]
    R --> U5[Estimate 2025 vs 2026 municipal tax]
    M((Authorized municipal analyst)) --> U6[Submit official page text and PDF]
    M --> U7[Review citations and generated claims]
```

## Class diagram

```mermaid
classDiagram
    class DecisionCard {
        +str item_id
        +str title
        +list~str~ wards
        +str what_is_proposed
        +str why
        +str who_is_affected
        +list~Stage~ stages
        +list~str~ conditions
        +Participation participation
        +list~Phrase~ procedural_phrases
        +list~str~ uncertainties
    }
    class Stage {
        +str body
        +str date
        +StageType stage_type
        +Outcome outcome
        +str quote
    }
    class Participation {
        +str can_still_comment
        +str deadline_text
        +str how
        +str quote
    }
    class Phrase {
        +str phrase
        +str meaning_here
        +str quote
    }
    DecisionCard "1" *-- "many" Stage
    DecisionCard "1" *-- "1" Participation
    DecisionCard "1" *-- "many" Phrase
```

## Sequence diagram

```mermaid
sequenceDiagram
    actor A as Analyst
    participant UI as Streamlit
    participant R as Redaction
    participant AI as Claude API
    participant V as Source verification
    participant S as Status rules
    A->>UI: Unlock admin mode and paste agenda page/PDF
    UI->>R: Remove sensitive sections
    R-->>UI: Cleaned text
    UI->>AI: Structured extraction (no citations)
    AI-->>UI: Pydantic DecisionCard
    UI->>V: Verify stage quotes against submitted sources
    V-->>UI: Verified stage flags
    UI->>S: Compute overall decision status
    S-->>UI: Decision-status label
    UI->>AI: Separate cited explanation request
    AI-->>UI: Explanations and citation locations
    UI-->>A: Preview marked UNREVIEWED
    Note over A,UI: Human source review required before publication
```

## Design rationale

1. **Two API calls:** Structured JSON output and interleaved citations cannot be requested in the same Claude API response, so the system separates format validation and cited narrative.
2. **Code-determined status:** A quote must match a source before its stage can drive a status label. Council actions take precedence over earlier committee actions.
3. **Offline-safe demo:** The public view has four bundled curated cases; there are no background requests or API charges just for opening the website.
4. **Privacy-aware ingestion:** Drop named-correspondent and speaker sections before external API transmission. In a production system this must be supplemented by manual review and a privacy impact assessment.
5. **Cautious uncertainty:** The absence of a confirmed participation deadline is shown as such, not guessed from a calendar date.
