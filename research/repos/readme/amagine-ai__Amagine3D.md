Amagine3D 

 From hardware requirements to editable 3D designs 

 Amagine3D is the open-source 3D capability layer Amagine is developing for hardware creation. 
 Give it a product description and reference images, add the key dimensions, and Amagine3D can design an enclosure and assembly structures around the internal components while producing source code that remains editable. STEP, STL, and 3MF files can be exported as needed.

 Capabilities ·
 Example ·
 Quick Start ·
 简体中文 

## From Requirements to Editable Hardware Structures

Amagine3D currently focuses on printable intelligent-hardware enclosures and related structures, creating complete designs from natural-language requirements, reference images, dimensions, and existing geometry.

The design process starts with internal components, arranging mounts and interfaces before creating the enclosure, controls, and thermal-management structures. When a design needs multiple parts, covers, hinges, or latches are developed together with assembly clearances and printing tolerances. For rigid mechanisms such as hinged or sliding covers, the system can also check collisions and operating clearances along a defined motion path.

Every generation records one semantic scene containing its parts, features, interfaces, materials, and BRep masters. Manufactured geometry retains editable Python and build123d source and exports genuine STEP. Product envelopes start from a few key sections joined by lofts; extrusions, revolutions, sweeps, and BRep features shape the rest of the design. Ruled or segmented surfaces are useful when they preserve the intended form. The same geometry produces STL, display GLB, and a profile-bound 3MF package when required, including permanent color regions inside a physical part.

Behind the scenes, the 3D-native Agent turns the request into an immutable intent and one mutable semantic scene. BRep and color exporters compile that scene into one evidence contract. The Agent sees measured dimensions and checks for feature ownership, wall thickness, print orientation, plate fit, connectivity, interference, and exported-file readback, then renders and reads the latest result before accepting it. A cavity formed by subtracting an inner loft is checked for actual wall thickness; section insets alone do not guarantee constant normal thickness.

For appearance-led requests without a supplied visual reference, the workflow
asks the Agent to use the selected search backend—preferably local `a3d search`
with Tavily—to find a few relevant sources when network access is enabled. Search
snippets remain untrusted leads; the Agent must actually retrieve and view any
image used for visual judgment. Engineering dimensions still come from component
drawings or explicit assumptions.

Visual review uses the generated five-view preview (isometric, front, side, top,
bottom) and requires image perception in the configured model/provider. A rendered
PNG or successful text response does not establish that capability. Run
`npm run doctor -- --vision` to check both image attachments and native `view_image`
with two small, randomized image requests. This opt-in check uses the configured
model/API account and leaves diagnostic logs in isolated local sessions. A failed
perception check means visual review remains incomplete; check the model's image
support and gateway forwarding before accepting CAD on visual grounds. The regular
doctor command does not make these API requests.

## Example: BUSY Bar Desktop Device Enclosure

The GIF above shows a desktop device enclosure that Amagine3D generated from public information about [BUSY Bar](https://busy.app/). BUSY Bar is a productivity multi-tool for displaying custom statuses. It includes a built-in Pomodoro timer and apps, supports extensive customization, is open-source, and is friendly to developers and hardware enthusiasts. Amagine3D created a multipart enclosure for it, with a display area on the front, physical controls on top, and internal space arranged around the components and interfaces.

The Agent first used the reference images to position the display area and controls, then divided the enclosure into parts around the internal components. The dimensions that determine appearance and assembly remain editable parameters, so they can be adjusted after generation.

This generation produced complete build123d source code, STEP and STL files, and a check report. The workbench can continue to preview, measure, and modify the model. Parameter changes are written back to the source and rebuild the geometry, and the complete result is saved with the project.

Design reference: [BUSY Bar official website](https://busy.app/).

## 3D-native Agent

Amagine3D defines a 3D-native Agent as an Agent architecture centered on 3D design state. This state records the geometry of every part in the current version and the spatial relationships between them. It determines the Agent's next action, and execution results are written back into it.

```text
User requirements and physical constraints
 │
 ▼
 Accepted 3D design state
 │ create candidate version
 ▼
 ┌── autonomous inner loop ──┐
 │ read model → plan changes │
 │ ↑ ↓ │
 │ analyze results ← run checks│
 └─────────────┬──────────────┘
 │ checks pass
 ▼
 Commit as a new version
 │
 ▼
 Save state and artifacts
```

In this architecture, a design task has two levels. The autonomous inner loop produces candidate designs, while the commit stage decides whether a candidate can become the new accepted version. Keeping them separate lets the Agent try repeatedly without damaging a design that has already passed its checks.

Each iteration of the autonomous inner loop starts from the current design state. The Agent reads the spatial relationships between parts, then decides which structures need to change. The modified model runs in a real geometry environment, where the system measures the generated result directly and checks assembly interference, motion paths, and e