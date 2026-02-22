# Collaborative Work Guide

**Purpose**: Explain how you and your team should use the various documents for effective collaboration  
**Audience**: Arun & Surendar  
**Created**: February 22, 2026

---

## 📋 The Three Collaboration Documents

### 1. **ROUGH_NOTES.md** 
*For: Raw work, quick thoughts, draft ideas*

**Use When**:
- You have a quick idea or thought
- You're sketching out code or architecture
- You have incomplete thoughts or questions
- You want to dump raw notes without structure
- You're brainstorming within your own section

**Format**: Completely informal, no structure required

**Example Entry**:
```
Been thinking about how to handle state in strategies.
Backtests need stateless, but live trading needs state tracking.
Maybe two different initialization modes?
Or create StateManager wrapper?

Surendar - what's your take on this?
```

**When to Clean Up**: Develop promising ideas into IDEAS_AND_DISCUSSIONS.md

---

### 2. **IDEAS_AND_DISCUSSIONS.md**
*For: Structured idea development & team discussions*

**Use When**:
- You have a formed idea ready for discussion
- You want to propose a feature
- You want to discuss options
- You're responding to someone's idea
- You want stakeholder feedback

**Format**: Semi-structured with clear sections

**Stages of Ideas**:
1. 🤔 **Under Consideration**: Early concept
2. 🔄 **In Review**: Ready for discussion
3. ✅ **Ready for Development**: Clear path forward

**Example Entry**:
```
**Idea: Dynamic Position Sizing (Arun - Feb 25)**

Thinking we should implement Kelly Criterion for position sizing instead of fixed %.

Key idea:
- Use win rate and average win/loss ratio
- Calculate optimal position size mathematically
- Reduces risk in losing periods, scales up in winning periods

Benefits:
- More scientific approach than fixed %
- Adapts to strategy performance
- Reduces risk of ruin

Implementation:
- Add to RiskManager class
- Use win rate from historical trades
- Validate with backtests

Questions for Surendar:
- How would we calculate initial position size before we have history?
- Should we cap the Kelly fraction (e.g., Kelly/2)?
```

---

### 3. **MEETING_NOTES.md**
*For: Decisions, action items, and coordination*

**Use When**:
- You've made a decision (record it!)
- You have action items
- You want to track project status
- You need to coordinate next steps
- There are blockers or issues

**Format**: Structured but evolves over time

**Key Sections**:
- Meeting summaries with decisions
- Active discussion points needing decisions
- Decision log
- Action item tracking

**Example Entry**:
```
### Action Items

- [ ] **Arun**: Create architecture diagram with state management approach
- [ ] **Surendar**: Implement Kelly Criterion calculator and unit tests
- [ ] **Both**: Review existing backtest results and identify discrepancies
```

---

## 📖 How to Use Them Together

### Workflow Example

```
Initial thought → Rough Notes → Discussion → Decision → Implementation
     ↓                 ↓            ↓           ↓          ↓
"I'm wondering    Add to my        Formal      Record     Write code
 about X"         workspace        proposal    decision
                  section          in IDEAS    in MEETINGS
```

### Real Example: Position Sizing

**Step 1: Initial Thought (ROUGH_NOTES)**
```
In Arun's workspace:
> Been reading about Kelly Criterion optimization.
> Could apply to position sizing.
> How would this work in backtesting?
```

**Step 2: Develop Idea (Still ROUGH_NOTES)**
```
Kelly Criterion Math:
f = (bp - q) / b
where:
- f = fraction of bankroll to risk
- b = odds received
- p = probability of winning
- q = probability of losing

For trading:
- Use win rate as p
- Use avg_win / avg_loss as odds
- Calculate optimal bet size

Surendar - implementation complexity?
```

**Step 3: Propose Formally (IDEAS_AND_DISCUSSIONS)**
```
**Idea: Kelly Criterion Position Sizing (Arun - Feb 25)**

Current approach: Fixed 2% of capital per trade
Proposed: Dynamic sizing based on Kelly Criterion...
[Full proposal with benefits, concerns, questions]
```

**Step 4: Discuss & Refine**
```
> Response from Surendar:
> Good idea! But need to handle:
> 1. Initial trades (no history yet)
> 2. Over-aggressive Kelly (can lose 25% in one trade)
> 3. Need to recalculate after each trade cycle
```

**Step 5: Make Decision (MEETING_NOTES)**
```
### Decision: Kelly Criterion Implementation

Status: ✅ Approved
Approach: Kelly/2 (half Kelly for safety)
Initial Position: 1% until we have 20+ trades
Recalculation: Weekly
Owner: Surendar
Timeline: 1 week
```

**Step 6: Track Progress (MEETING_NOTES)**
```
### Action Items
- [x] Design Kelly calculator
- [ ] Implement calculator in RiskManager
- [ ] Write unit tests
- [ ] Validate with backtests
- [ ] Document in config
```

---

## 💡 Best Practices

### For Arun (Strategy & Architecture)

1. **Share Design Thoughts Freely**: Add rough ideas to ROUGH_NOTES
2. **Formal Proposals**: Use IDEAS_AND_DISCUSSIONS for big architectural changes
3. **Record Decisions**: Always document in MEETING_NOTES after deciding
4. **Ask Questions**: Tag Surendar with specific questions - get implementation feedback
5. **Keep It Organized**: Move refined ideas from ROUGH → IDEAS → MEETINGS

### For Surendar (Implementation & Testing)

1. **Share Implementation Concerns**: Use ROUGH_NOTES to raise blockers
2. **Technical Feasibility**: Comment in IDEAS_AND_DISCUSSIONS on implementation complexity
3. **Estimate Effort**: Provide effort estimates for approved ideas
4. **Track Progress**: Update action items in MEETING_NOTES
5. **Ask for Clarification**: Use IDEAS_AND_DISCUSSIONS to clarify requirements before coding

### For Both

1. **Update Timestamps**: Always include dates on new content
2. **Reference Each Other**: Use @mentions or quotes
3. **Keep It Moving**: Don't let ideas stall - either move forward or Archive
4. **Consolidate**: Periodically clean up old discussions
5. **Be Concise**: Rough notes don't need perfection

---

## 🚀 Common Workflows

### Weekly Development Cycle

**Monday**: Review ROUGH_NOTES and IDEAS from the week
**Tuesday**: Discuss any new ideas that need decision
**Wednesday**: Finalize decisions, update MEETING_NOTES
**Thursday**: Start implementation of approved ideas
**Friday**: Progress update, raise blockers

### Adding New Feature

1. **Day 1**: Add rough sketch to ROUGH_NOTES
2. **Day 2**: Develop in ROUGH_NOTES or move to IDEAS_AND_DISCUSSIONS
3. **Day 3**: Get feedback and refine
4. **Day 4**: Make formal decision, record in MEETING_NOTES
5. **Days 5+**: Implement with clear action items

### Resolving Blockers

1. **Identify**: Note in ROUGH_NOTES
2. **Escalate**: Move to IDEAS_AND_DISCUSSIONS as discussion point
3. **Discuss**: Back and forth with alternatives
4. **Decide**: Record decision path in MEETING_NOTES
5. **Implement**: Move forward with clear direction

---

## 📝 Templates You Can Copy

### Sharing An Idea (IDEAS_AND_DISCUSSIONS)
```
**Idea: [Short Title] ([Your Name] - [Date])**

[Brief description of idea]

Key benefits:
- Benefit 1
- Benefit 2

Implementation:
- How would this work?
- Where would code go?

Concerns/Questions:
- Potential issue 1
- Question for [Other Person]?
```

### Quick Note (ROUGH_NOTES)
```
**[Topic Name]**
```
[Your raw thoughts and sketches here]
[Code sketches welcome]
[Questions welcome]
[Incomplete is OK]

Thoughts @[Other Person]?
```

### Recording A Decision (MEETING_NOTES)
```
### Decision: [What was decided]

Status: ✅ Approved / 🔄 In Progress / ⏳ Pending
Rationale: [Why this decision]
Owner: [Who will drive implementation]
Timeline: [When should this be done]
Notes: [Any other context]
```

---

## 🔄 Document Maintenance

### Keep These Updated

- **ROUGH_NOTES**: Ongoing, as you think
- **IDEAS_AND_DISCUSSIONS**: Once per week, promote ready ideas
- **MEETING_NOTES**: After discussing anything important

### Periodic Cleanup

- **Monthly**: Review ROUGH_NOTES, archive old items to IDEAS
- **Monthly**: Consolidate IDEAS that became implementation
- **Quarterly**: Clean up MEETING_NOTES, move completed items

### When to Archive

- Idea implemented → Note completion in MEETING_NOTES
- Question answered → Summarize answer, move on
- Decision made → Record it, don't revisit unless context changes

---

## ⚡ Quick Decision Checklist

Before moving an idea from ROUGH → IDEAS → ACTION:

- [ ] Clear problem statement
- [ ] Proposed solution described
- [ ] Benefits articulated
- [ ] Implementation approach sketched
- [ ] Questions identified for discussion
- [ ] Effort estimate provided (when appropriate)
- [ ] Owner/responsible party identified
- [ ] Timeline proposed

---

## 🎯 Success Indicators

You'll know this system is working when:

✅ Ideas don't get lost in context
✅ Decisions are recorded and referenced
✅ Action items have clear owners and deadlines
✅ Blocker resolution is tracked
✅ Both team members understand what's being worked on
✅ Less time in meetings, more async progress
✅ Easy to onboard new team members (they can read history)

---

## 📍 Document Locations

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| ROUGH_NOTES.md | Raw work & ideas | Daily |
| IDEAS_AND_DISCUSSIONS.md | Structured proposals | Weekly |
| MEETING_NOTES.md | Decisions & actions | Weekly |
| This File | Guide & instructions | Every few weeks |

---

## 🤝 Making It Work

### Key Principles

1. **Async First**: Use documents. Don't wait for meetings.
2. **Real-time Updates**: Update docs as you progress
3. **Transparent**: Share everything - no hidden decisions
4. **Collaborative**: Build on each other's ideas
5. **Documented**: If it's decided, it's written down

### Communication Norms

- **Questions**: Tag the person with a question in the relevant document
- **Urgent**: Use Slack for urgent issues, then document later
- **Long Discussions**: Move to IDEAS_AND_DISCUSSIONS
- **Decisions**: Final decision always goes in MEETING_NOTES
- **Complete Thoughts**: Respond to ideas with complete thoughts (not one-liners)

---

## 💬 Example Conversation

**Arun in ROUGH_NOTES:**
```
**Risk Management Architecture**

Wondering if we should have per-strategy risk managers or one global?

Per-strategy pros:
- Each strategy has different risk profile
- Easier to understand

Global pros:
- Single point of enforcement
- Portfolio-wide limits easier

Thoughts @Surendar?
```

**Surendar in ROUGH_NOTES (same section):**
```
Good question. I think we actually need both:
- Per-strategy limits (don't let one strategy blow up)
- Global limits (portfolio safety net)
- Maybe a third layer: per-market limits?

My implementation brain says:
1. Strategy creates risk context
2. RiskManager checks against both strategy limits and global limits
3. Return approved size or 0

But architecture question: One RiskManager instance managing all?
Or factory pattern creating per-strategy managers?

Could sketch something if you want.
```

**Arun responds:**
```
Ah yes! Both makes sense. Like belt+suspenders for safety.

Architecture-wise: One global RiskManager that knows about all strategies
and their limits. Much simpler than managing multiple instances.

> One RiskManager instance managing all?

Yeah, let's go with this. Single source of truth for risk decisions.

This is ready to move to IDEAS_AND_DISCUSSIONS if you want?
```

**Arun then moves to IDEAS_AND_DISCUSSIONS:**
```
**Idea: Layered Risk Management (Arun & Surendar - Feb 25)**

After discussion in ROUGH_NOTES, we've landed on approach:

Implement three-layer risk management:
1. **Per-Strategy Limits**: Each strategy respects its own constraints
2. **Global Portfolio Limits**: Entire portfolio never exceeds limits  
3. **Per-Market Limits**: Exposure per market/symbol limited

Architecture:
- Single RiskManager instance (global)
- Connected to all active strategies
- Consulted before any trade execution
- Hard stop: rejected orders don't execute

Implementation:
- Surendar to design class structure
- Update config files for limits
- Unit test each layer
```

---

## 🎓 Learning More

- See DOCUMENTATION_INDEX.md for full project docs
- Check README.md for project overview
- Review existing IDEAS_AND_DISCUSSIONS.md for examples
- Look at ROUGH_NOTES.md for messy brainstorming examples

---

**Remember**: The goal is to keep ideas flowing and decisions clear. Don't overthink it!

Just start writing and the rhythm will develop.

**Happy collaborating!** 🚀

---

**Created**: February 22, 2026  
**For**: Arun & Surendar  
**Last Updated**: February 22, 2026
