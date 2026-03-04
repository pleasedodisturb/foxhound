# TPM Task for Wolt: Ring Ultra Case Study

**Source:** https://docs.google.com/document/d/1Nr2i_8sriyv_HfcHEMNtqgfwlTqmVNqUOPWxza1bq2o/
**Context:** This was the interview presentation/task Vitalii prepared for the Wolt TPM role.

## Overview

A detailed case study of the Ring Ultra program -- a complex, cross-functional R&D initiative at Ring/Amazon.

**Note to reader (from the document):** "My presentation plan is to go through this story as-is and then cover any gaps by Q/A, also I've replaced many of the program artifacts with program memes, which we generated during the program itself. I also created diagrams for this presentation, those are rough, but accurate. I also added STAR indents for cases, which I can cover during my narrative."

## Program Details

**Program:** Ring Ultra
**Lifecycle:** Sep 2018 - Jan 2020 (ca. 16 months)
**Role:** Vitalii Garan, TPM for Long-Term Research turned Sensor Research turned Ultra Team

**STAR Summary:** Ring was looking for an innovative solution in the IoT camera space and tasked me and my team to find one, so we tested multiple technologies, narrowed it down to radar and created a full-scale prototype solution. It became a premium floodlight camera and doorbell later.

## Context

Ring Ultra was a complex R&D endeavor, evolving from Ring's desire for innovation in IoT home surveillance, which was saturated by nearly equal competing products from Nest, Arlo, Eufy and others, all utilizing a combination of PIR (passive infra-red sensors) and CV (computer vision) algorithms.

Data privacy laws like GDPR and CCPA were maturing, putting additional pressure on surveillance and cloud data retaining devices.

## Key Objectives (volatile and evolving)

- **Hardware Product:** Develop a high-tier next-gen camera (extremely broad)
- **Product Use Case:** Find a once-and-for-all solution for weak sides of existing CV and sensors - recurring motion (flags, leaves), human-only identification, weather and environment (fog, dust and anything with low visibility, like lens flare) - relatively measured by precision:recall ratio at the time
- **Privacy:** Find a way to identify home security threats without using PII data at all (personally identifiable information)
- **Technology:** Deliver a POC (proof of concept) for the technology for the upcoming high-tier devices

## Program Scale

**Number of teams involved:** ~10 critical teams spanning across all locations
- Hardware
- Firmware
- Data collection, annotation and data validation - in-house in Kyiv
- Data collection as trials effort in Santa Monica and across USA

**Key stakeholders:**
- Jamie, CEO
- Jason, CPO
- Spiro, head of hardware
- Serhii, head of research
- Kira, COO for Ring Research

## Team & Organization Diagram

Multi-site operation across:
- **Santa Monica** (HQ) - Launch Teams, App Design, Legal, Ops, Hardware Design, Product Management
- **Kyiv** - Ring Research (all algorithms), Data Annotation and Validation, Ring App Development, Wireless/Wired Devices Firmware, DevOps
- **Buenos Aires** - Ring Admin Panel, Ring Backend Services (all Databases)
- **Taipei** - Hardware Production, Hardware Design, Manufacturing Validation
- **Vendors** - Texas Instruments, Socionext, Vayyar, misc.

## Major Dependencies

Team started as a 7-person do-it-all team (1 SDM, 3 PhD professors, 1 C++ engineer and 1 QA/SDET) and a zoo of various sensors, radars, lidars, sonars, PIR-clusters and camera lenses, which we connected and applied to existing cameras and set in the corridors of the Ring Research office in Kyiv.

When settled on radar as go-to technology, got greenlight on budgets (unlimited with strings attached) and priority (high), but still had to compete with P0 behemoth launches (device releases) and P0 features (features bound to device releases).

## Problem Statement

Retrospectively, Ring Ultra had notable obstacles and tailwinds.

### Tailwinds (things which really helped)

- Greenlight by top stakeholders, CPO as main program sponsor and guardian
- Interest in the idea and motivation across the whole company and most teams
- Virtually unlimited budget, challenged by lead times, hire times and unreasonable expectations and deadlines, and ultimately cost of radar testing equipment easily going to millions of $ per test bench
- Top hires in most of the domains (except Radio Frequency), competency across the board in all program areas, especially in ML algorithms and CV
- Working data collection processes in both Kyiv and Santa Monica offices
  - STAR: needed at least 100 hours of unique footage for 100 cameras (10000 hours total) collected and annotated to build a second generation PoC for sensor fusion feature

### Headwinds (things which really harmed or pushed back)

- No domain expertise in radars at the start of the program
- Stakeholder-driven development - dramatic change of scope at pivot points
  - STAR: Ring was very aggressive with release cycles and at some point hardware release schedule included 8 different cameras and doorbells in 1 calendar year. This put all other programs and non-revenue-generating research initiatives at risk. Created a working live demo for Jamie (CEO) when visiting Kyiv, but Jamie's input was detached from actual development status and set unrealistic vision
- Bleeding edge technology - early stage prototypes with unreliable software, defects in manufacturing and non-uniform data output
- Ring didn't have a hardware innovation process or charter, so the program stood in line with algorithm research programs (abstract knowledge problems) and hardware development programs, while being neither of two in reality
- Political competition: Ring was slowly assimilated by Amazon structures and various corporate parties started competing for influence and resources

## Program Structure and Execution

Challenges in governance and methodology lied in overlapping lifecycles and paradigms. Ultra had to incorporate hardware, ML/data, and software methodologies.

Used Kanban board and RACI matrix for internal team, with common Agile rituals for time boxing. Firmware teams had code freeze dates which had to be respected at all times.

For radar-only features, asked each team (software, hardware, firmware) to dedicate a single person as single-threaded owner to not interfere with internal lifecycles and processes.

Visited other teams' standups and ad-hoc meetings where interests were at stake.

### Program Lifecycle Diagram

Venn diagram showing overlap between:
- **Data & ML** lifecycle: Problem Definition -> Data Investigation -> Data Preparation -> Deployment -> Monitoring & Improvement (circular)
- **Hardware** lifecycle: Specification -> High-level design -> Detailed design -> Production -> Integration testing -> Acceptance (waterfall)
- **Ring Ultra** sitting at the intersection of both

## Email Evidence

Included actual email exchanges between Jason (CPO) and Vitalii:
- Jason: "You wanted to do this now do it"
- Vitalii: "Sounds properly ambitious."
- Jason: "2 radars... doesn't matter cost"

## Why This Document Matters

This TPM task demonstrates:
1. **Complex multi-site program management** across 5+ global locations
2. **Hardware + software + ML lifecycle management** -- rare TPM skill
3. **CEO/CPO-level stakeholder management** at Ring/Amazon
4. **Research-to-product pipeline management** -- from vague innovation mandate to shipped products
5. **Resource orchestration** with $millions budget and 400+ team members
6. **Working with ambiguity** -- objectives were "volatile and evolving" by design
7. **Genuine humor and culture building** -- the memes show team culture creation
8. **Honesty about challenges** -- tailwinds AND headwinds, not just a success narrative
