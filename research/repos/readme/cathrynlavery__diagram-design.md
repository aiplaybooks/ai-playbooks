[](docs/screenshots/architecture.png)

[](docs/screenshots/loop.png)

*New in 2.0 — the Loop: flywheels with a shared-memory hub. The dashed lines are the write-backs.*

*New in 2.3: semantic system patterns and optional accessible motion, while static output stays the default.*

*New in 2.5.10: ten more layout grammars — Sankey, fishbone, Wardley map, kanban, user journey, deployment, dependency graph, UML class, story map, and database schema.*

Editorial diagram types for Claude Code, Codex, Factory Droid, Pi, and Agent Skills-compatible hosts. Self-contained HTML + SVG. No shadows. No Mermaid slop. Semantic patterns describe behavior separately from layout, so a queue, policy trace, or trust boundary can use the nearest existing type without expanding the type count. Static HTML remains the default; optional motion is available for ordered explanations. The skill also redraws draw.io, Mermaid, or Excalidraw sources at a chosen format, size, and detail level.

No Figma. No generic rounded boxes. No 30-minute color-picking sessions.

Project site: [diagramdesign.dev](https://diagramdesign.dev?utm_source=diagram-design&utm_medium=readme&utm_campaign=github&utm_content=intro)

---

## Why I built it

I write at [littlemight.com](https://littlemight.com?utm_source=diagram-design&utm_medium=readme&utm_campaign=github&utm_content=intro) (and run [BestSelf.co](https://bestself.co?utm_source=diagram-design&utm_medium=readme&utm_campaign=github&utm_content=intro) on the side). Every time I needed a diagram — an architecture sketch, a flowchart, a pyramid of what matters most — I'd ask Claude and get back a generic rounded-box thing that looked nothing like the rest of the site. I'd either fight with Figma for 30 minutes or just skip the diagram.

So I built a Claude Code skill for it. Editorial-quality visual types, matched to your brand in 60 seconds by reading your website.

> *The highest-quality move is usually deletion.* Every node earns its place. The accent color is reserved for the 1–2 things the reader should look at first. Target density: 4/10.

---

## What it makes

Every visual type ships in three static variants: minimal light, minimal dark, and full-editorial. Open any of them directly in a browser. There is no build step, JavaScript, or external image dependency.

 Architecture Components + connections 
 IT current-state Legacy landscape + modernization 
 Flowchart Decision logic 

 Sequence Messages over time 
 State machine States + transitions 
 ER / data model Entities + fields 

 Timeline Events on an axis 
 Swimlane Cross-functional flow 
 Quadrant Two-axis positioning 

 Radar / spider Multi-axis comparison 
 Loop / flywheel Reinforcing cycle + shared hub 
 Nested Hierarchy by containment 

 Tree Parent → children 
 Org chart Ownership + routing 
 Layer stack Stacked abstractions 

 Venn Set overlap 
 Pyramid / funnel Ranked hierarchy or drop-off 
 Bar chart Categorical comparison 

 Treemap Part-of-whole by area 
 Line chart Trends over time 
 Gantt Tasks + phases on a timeline 

 Scatter plot Distribution + correlation 
 High-Level End-to-end stack on a cluster 
 Process Multi-actor sequential workflow 

 Medallion Multi-tier data storage 
 Data flow Role-scoped pipeline steps 
 DP integration Sources → core → consumers 

 DP security matrix Per-role access permissions 
 Sankey Quantities that split + merge 
 Fishbone Grouped causes → one effect 

 Wardley map Value chain × evolution 
 Kanban Work in progress by state 
 User journey Stages, actions + sentiment 

 Deployment Zones, hosts + artifacts 
 Dependency graph Fan-in, ranks + cycles 
 UML class Classes, operations + typed relations 

 Story map Backbone × release slices 
 Database schema Physical tables + column FKs 
 Polar chart Cyclic magnitude · linear radius 

 Waterfall Running total + signed bridges 
 Architecture delta Before · Changes · After topology 
 Exploded axonometric Parts pulled apart on one axis 

 Axonometric plan Rooms and buildings on one plate 
 Heatmap Value per row × column cell 

Architecture delta compares synchronized topologies through a Before · Changes · After ledger of added, removed, changed, moved, and rewired objects. See its [reference](skills/diagram-design/references/type-architecture-delta.md) and [order-fulfilment example](skills/diagram-design/assets/example-architecture-delta.html). Attribute-only comparisons remain tables; a single snapshot uses Architecture.

Exploded axonometric draws one object in 2:1 dimetric projection with its parts lifted apart at equal gaps: a [phone teardown](skills/diagram-design/assets/example-exploded-phone.html), an [unboxing](skills/diagram-design/assets/example-exploded-unboxing.html), an [app stack](skills/diagram-design/assets/example-exploded.html), an [AI agent stack](skills/diagram-design/assets/example-exploded-ai-stack.html), or a [mechanical keyboard](skills/diagram-design/assets/example-exploded-keyboard.html). Every coordinate comes from one projection function, and the [animated phone](skills/diagram-design/assets/example-exploded-phone-animated.html) opens assembled and explodes once. See its [reference](skills/diagram-design/references/type-exploded.md).

Axonometric plan uses the same projection for one floor or one site: walls cut at desk height so every room reads from a single view, or buildings on a campus tagged by build phase. See the [office floor](skills/diagram-design/assets/example-axonometric-plan.html), the [campus](skills/diagram-design/assets/example-axonometric-plan-campus.html), the [coffee shop](skills/diagram-design/assets/example-axonometric-plan-coffee-shop.html), the [fulfillment floor](skills/diagram-design/assets/example-axonometric-plan-warehouse.html), the [phased campus animation](skills/diagram-design/assets/example-axonometric-plan-campus-animated.html), and the [reference](skills/diagram-design/references/type-axonometric-plan.md).

The v2.5.10 release added ten layout grammars. Compare their light