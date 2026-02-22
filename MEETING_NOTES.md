# Team Meeting Notes & Action Items

**Purpose**: Record discussions, decisions, and action items from team syncs  
**Frequency**: Weekly or as-needed  
**Keep Updated**: After each discussion

---

## Meeting 1 - Feb 22, 2026 (Project Kickoff)

**Attendees**: Arun, Surendar  
**Location**: Initial documentation sync  
**Duration**: Async (via document review)

### Topics Discussed

1. **Project Structure**
   - ✅ Documentation framework created
   - ✅ Base strategy classes defined
   - ✅ Backtester skeleton completed
   - Decision: Keep simple initially, enhance as we go

2. **Strategy Approach**
   - Agreed: Start with Trend Following and Mean Reversion
   - Agreed: Breakout strategy as third option
   - TBD: ML integration timing

3. **Development Priorities**
   - P1: Get basic backtest working with sample data
   - P2: Implement real data source integration
   - P3: Risk management system
   - P4: Live trading connector

### Decisions Made

| Decision | Rationale | Owner |
|----------|-----------|-------|
| Start with simple MA strategies | Proven, easy to validate | Both |
| Use JSON for config | Human-readable, flexible | Both |
| Docker for environment | Consistency across machines | Surendar |
| Python 3.9+ | Modern features, good libraries | Both |
| PostgreSQL + Redis | Industry standard | Surendar |

### Action Items

- [ ] **Arun**: Create detailed architecture diagram with data flows
- [ ] **Arun**: Define signal normalization approach (how to combine signals)
- [ ] **Surendar**: Implement sample data loader (CSV or fake generator)
- [ ] **Surendar**: Test Docker setup locally on Mac
- [ ] **Both**: Review and populate IDEAS_AND_DISCUSSIONS.md with initial ideas
- [ ] **Both**: Set up weekly sync meeting time

### Issues/Blockers

None identified yet - project just starting.

### Notes

```
- Both agreed documentation is comprehensive for MVP
- Should prioritize getting a working example running ASAP
- Plan to iterate rather than over-engineer upfront
- Need to decide on data source (real vs. simulated for testing)
```

---

## Meeting 2 - [DATE TBD]

**Attendees**:  
**Location**:  
**Duration**:

### Topics to Discuss

- [ ] Backtester implementation status
- [ ] Sample data approach (real or generated?)
- [ ] Risk management system design
- [ ] Strategy signal combination method
- [ ] Next phases and priorities

### Decisions

(To be filled)

### Action Items

(To be filled)

### Blockers / Issues

(To be filled)

---

## Active Discussion Points

### 1. Strategy Composition
**Started**: Feb 22  
**Status**: Needs discussion

**Question**: How should we combine signals from multiple strategies?
- Option A: Majority voting (which direction has most votes)
- Option B: Weighted average (weight by confidence)
- Option C: Separate positions for each strategy
- Option D: Hierarchical (primary strategy, secondary confirms)

**Arun's thoughts needed on**: Which approach fits the architecture best?

---

### 2. Backtest Realism vs Speed
**Started**: Feb 22  
**Status**: Needs decision

**Trade-off**: Accurate simulation vs execution speed

**Approaches**:
- Conservative: Max slippage, detailed commission
- Realistic: Market-dependent slippage, broker commissions
- Optimistic: Minimal assumptions
- User-selectable: Let user choose

**Surendar's recommendation**: Start with "Realistic", make easy to adjust later.

---

### 3. Risk Management Integration
**Started**: Feb 22  
**Status**: Needs architecture input

**Questions**:
1. Should risk checks happen pre-signal or post-signal?
2. Single global risk manager or per-strategy managers?
3. Hard stops (reject order) or soft warnings (flag and ask)?

---

## Key Decisions & Guidelines

### Code Quality Standards
- [x] Type hints required
- [x] Docstrings for all public methods
- [x] Tests before merge
- [x] PEP 8 compliance
- [x] Max 100 char line length

### Testing Requirements
- [x] Unit tests for all new functions
- [x] Integration tests for major features
- [x] Backtest validation (compare with expected results)
- [x] Code coverage maintained >80%

### Documentation Policy
- [x] Update docs with code changes
- [x] Examples for complex features
- [x] Architecture changes documented
- [x] Configuration options explained

### Deployment Process (TBD)
- Develop on feature branches
- Pull request review required
- All tests must pass
- Merge to main
- Tag releases

---

## Decision Log

```
Decision          | Date      | Owner | Status   | Notes
------------------|-----------|-------|----------|------------------
Start with 3 basic strategies | Feb 22 | Both | ✅ Decided | Will expand later
Use Docker        | Feb 22 | Surendar | ✅ Decided | Consistent environment
JSON config       | Feb 22 | Both | ✅ Decided | Human-readable
PostgreSQL+Redis  | Feb 22 | Surendar | ✅ Decided | Standard stack
Strategy composition method | Feb 22 | Team | ⏳ Pending | Needs discussion
Backtest realism  | Feb 22 | Team | ⏳ Pending | Needs decision
Live trading MVP criteria | TBD | Team | ⏳ Pending | When do we go live?
```

---

## Upcoming Discussions (Scheduled)

| Topic | Requested by | Date | Notes |
|-------|--------------|------|-------|
| Walk-forward validation details | Arun | TBD | How to implement advanced WFA |
| Parameter optimization approach | Arun | TBD | Grid search, genetic algo, etc. |
| Real-time data integration | Surendar | TBD | Architecture for intraday support |
| Broker API connections | Both | TBD | Which brokers to support first? |

---

## Deferred Items

**Items decided to handle later (post-MVP):**

- Machine learning strategy integration
- Real-time streaming data
- Multiple data source providers
- Advanced risk analytics dashboard
- Multi-asset portfolio support
- Sector rotation strategies
- Momentum strategies
- Pair trading strategies

---

## Communication Protocol

### How We Discuss

1. **Quick Questions**: Slack/inline comments
2. **Ideas**: Add to IDEAS_AND_DISCUSSIONS.md
3. **Rough Work**: Add to ROUGH_NOTES.md
4. **Decisions**: Record in this file
5. **Code Review**: GitHub pull request comments

### Response Expectations

- Simple questions: 24 hours
- Design decisions: 2-3 days
- Code review: 2 days
- Bug fixes: ASAP

### Escalation Path

1. Try async discussion (notes)
2. Ping in team chat
3. Quick 15-min sync call
4. Full team meeting if needed

---

## Template for New Meetings

```markdown
## Meeting N - [DATE]

**Attendees**: 
**Location**: 
**Duration**: 

### Topics Discussed

1. **Topic Name**
   - Point 1
   - Point 2
   - Decision/Action

### Decisions Made

| Decision | Rationale | Owner |
|----------|-----------|-------|
| Decision 1 | Why | Who |

### Action Items

- [ ] **[Owner]**: Description
- [ ] **[Owner]**: Description

### Issues/Blockers

- Issue description

### Notes

```
Free-form notes
```
```

---

## Quick Reference

**This Week's Focus**: Set up development environment and get first backtest running

**This Month's Goals**:
1. MVP with working backtest
2. First strategy validated
3. Team development rhythm established
4. Initial data integration

**Blocking Questions**:
- How should signals combine?
- What data sources for testing?
- When do we involve real data?

---

**Last Updated**: February 22, 2026  
**Meeting Frequency**: Weekly (Thursdays 3pm tentative)  
**Next Meeting**: [TBD - schedule with Surendar]  
**Last Review**: February 22, 2026
