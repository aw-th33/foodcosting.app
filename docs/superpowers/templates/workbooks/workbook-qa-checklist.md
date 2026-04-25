# Workbook QA Checklist

## Workbook Info

- Workbook name:
- Date:
- Reviewer:
- Version reviewed:

## Release Recommendation

- Recommendation: `ship | ship with fixes | hold`
- Summary reason:

## Formula Integrity

- [ ] Core formulas are fully defined
- [ ] Formula ranges are clear and stable
- [ ] Protected cells are identified
- [ ] Derived values update correctly when source inputs change
- [ ] No obvious circular-reference risk

## Logic Quality

- [ ] Unit assumptions are consistent
- [ ] Yield / waste logic is explained where needed
- [ ] Pricing or margin outputs match the stated method
- [ ] Edge cases are considered
- [ ] Blank or partial inputs do not create misleading outputs

## Usability

- [ ] First-use path is clear
- [ ] Inputs are easy to identify
- [ ] Outputs are easy to find
- [ ] Tab names are understandable
- [ ] The workbook does not feel more complicated than necessary

## Trust And Accuracy

- [ ] The workbook promise matches the workbook behavior
- [ ] No misleading “automation” claims are implied
- [ ] Limitations are visible where needed
- [ ] App upsell does not hide missing workbook functionality

## Findings

| Severity | Area | Finding | Recommended fix |
|---|---|---|---|
| High |  |  |  |
| Medium |  |  |  |
| Low |  |  |  |

## Final Notes

- What is strongest:
- What still worries QA:
- What should be tested again after revision:

