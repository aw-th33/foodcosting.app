# Workbook QA Checklist

## Workbook Info

- Workbook name: Recipe and Menu Costing Workbook
- Date: 2026-04-25
- Reviewer: workbook-qa
- Version reviewed: dry-run-v1

## Release Recommendation

- Recommendation: `ship with fixes`
- Summary reason: The workbook concept is strong, but the dry-run spec still needs a few clarity and edge-case safeguards before it should be treated as release-ready.

## Formula Integrity

- [x] Core formulas are fully defined
- [x] Formula ranges are clear and stable
- [x] Protected cells are identified
- [x] Derived values update correctly when source inputs change
- [x] No obvious circular-reference risk

## Logic Quality

- [x] Unit assumptions are consistent
- [x] Yield / waste logic is explained where needed
- [x] Pricing or margin outputs match the stated method
- [ ] Edge cases are considered
- [ ] Blank or partial inputs do not create misleading outputs

## Usability

- [x] First-use path is clear
- [x] Inputs are easy to identify
- [x] Outputs are easy to find
- [x] Tab names are understandable
- [ ] The workbook does not feel more complicated than necessary

## Trust And Accuracy

- [x] The workbook promise matches the workbook behavior
- [x] No misleading “automation” claims are implied
- [x] Limitations are visible where needed
- [x] App upsell does not hide missing workbook functionality

## Findings

| Severity | Area | Finding | Recommended fix |
|---|---|---|---|
| High | Recipe Costing | The spec does not yet define how blank ingredient rows behave, which risks noisy or misleading line totals. | Define explicit blank-state formulas and display rules for incomplete rows. |
| High | Unit Conversion | The spec mentions conversion factors but does not define how unsupported or invalid conversions should be surfaced. | Add a visible conversion-warning pattern and a fallback state when conversion input is missing or impossible. |
| Medium | Menu Pricing | The workbook supports target food cost % and mentions gross margin, but the user path between them is not fully clarified. | Pick one default pricing method and make the alternative clearly optional. |
| Medium | Complexity | Seven tabs may feel heavy for smaller operators on first use. | Consider a lite version later or stronger visual grouping in `Start Here`. |
| Low | Dashboard | The dashboard output is useful but still broad. | Define one or two primary default views for faster review. |

## Final Notes

- What is strongest: Strong product fit, solid tab architecture, and a clear upgrade path into the app.
- What still worries QA: Confusion around conversion logic and pricing methodology could reduce trust if not handled very explicitly.
- What should be tested again after revision: blank states, sub-recipe updates, invalid units, and first-time user flow.

