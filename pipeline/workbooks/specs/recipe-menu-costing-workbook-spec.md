# Workbook Specification Template

## Overview

- Workbook name: Recipe and Menu Costing Workbook
- Date: 2026-04-25
- Architect: workbook-architect
- Version: dry-run-v1

## Purpose

- Primary outcome for the user: Calculate accurate per-portion recipe cost and translate that into a menu price using target food cost or gross margin logic.
- Business problem solved: Operators often do not know the true cost of a recipe or whether their selling price protects margin.
- In-scope: Ingredient master list, unit costs, recipe costing, sub-recipes, portion cost, target menu price, summary outputs
- Out-of-scope: Inventory counts, supplier sync, multi-location collaboration, historical price tracking

## Target User

- Primary user: Owner-operator, chef, kitchen manager
- Business types: Restaurant, cafe, bakery, caterer, food truck
- Skill level: Beginner to intermediate spreadsheet user
- Frequency of use: Weekly or monthly, plus whenever ingredient prices change

## Workbook Format

- Format: `multi-tab workbook`
- Platform priority: `Google Sheets first`
- Complexity: `high`

## User Flow

1. First open experience: User lands on a `Start Here` tab with a short explanation and a three-step setup flow.
2. First required inputs: Add business settings, currency, and key units; then enter ingredients in the master list.
3. First useful output: Build one recipe and immediately see batch cost, portion cost, and suggested selling price.
4. Ongoing usage pattern: Update ingredient costs, duplicate recipe rows, reuse sub-recipes, and review summary metrics.
5. Natural upgrade trigger: When the user wants automatic updates across many recipes, audit history, collaboration, or real inventory linkage.

## Tab Structure

### Tab 1

- Tab name: Start Here
- Purpose: Onboard the user and explain the workflow
- User inputs: None required beyond reading instructions
- Protected / formula cells: Fully protected
- Notes: Includes a short quick-start checklist and color legend

### Tab 2

- Tab name: Settings
- Purpose: Define currency, measurement assumptions, default target food cost %, and markup logic
- User inputs: Currency, default target food cost %, default margin target, preferred units
- Protected / formula cells: Mostly inputs with a few helper formulas
- Notes: Keeps reusable values out of recipe tabs

### Tab 3

- Tab name: Ingredient Master
- Purpose: Store purchase unit, purchase price, recipe unit, conversion factor, supplier note, and active cost per recipe unit
- User inputs: Ingredient name, category, purchase unit, purchase price, recipe unit, conversion
- Protected / formula cells: Cost-per-recipe-unit formulas protected
- Notes: This is the core data layer powering the workbook

### Tab 4

- Tab name: Sub-Recipes
- Purpose: Cost reusable prep items such as sauces, doughs, batters, or spice mixes
- User inputs: Sub-recipe name, ingredient lines, batch yield, usable portion
- Protected / formula cells: Line cost and batch cost formulas protected
- Notes: Sub-recipes can be referenced in the main recipe tab as ingredients

### Tab 5

- Tab name: Recipe Costing
- Purpose: Build dish-level recipes using ingredients and optional sub-recipes
- User inputs: Recipe name, ingredient or sub-recipe selection, quantity used, serving count
- Protected / formula cells: Line item cost, batch cost, portion cost formulas protected
- Notes: Main working tab for dish costing

### Tab 6

- Tab name: Menu Pricing
- Purpose: Translate recipe cost into suggested selling price using target food cost % or gross margin assumptions
- User inputs: Recipe selection, desired food cost %, optional manual selling price
- Protected / formula cells: Suggested menu price, expected margin %, contribution amount
- Notes: Allows operators to compare current vs recommended pricing

### Tab 7

- Tab name: Summary Dashboard
- Purpose: Show key metrics and highlight recipes with weak margins
- User inputs: Optional filters
- Protected / formula cells: Fully formula-driven
- Notes: Designed for fast review and decision-making

## Core Data Model

- Key entities: ingredient, sub-recipe, recipe, menu price scenario
- Shared variables: currency, default food cost %, preferred measurement units
- Reusable master lists: ingredient names, categories, units, recipe names
- Naming conventions: singular item names, standardized units, stable recipe names

## Formula / Logic Notes

- Key calculations: cost per recipe unit, line cost, batch cost, portion cost, target price, gross margin %
- Unit conversion logic: Convert purchase-unit price into recipe-unit price before recipe math
- Yield or waste assumptions: Optional yield factor for ingredients where edible portion differs from purchased amount
- Margin / pricing logic: Suggested menu price = portion cost / target food cost %
- Error handling expectations: Blank recipe rows should not show misleading prices; invalid conversions should surface clear warnings

## Validation Rules

- Dropdowns: ingredient names, categories, purchase units, recipe units, sub-recipe names
- Required fields: ingredient name, purchase price, purchase unit, recipe quantity, serving count
- Invalid input handling: highlight missing or impossible conversion values
- Protected areas: all formula columns, dashboard cells, helper reference ranges

## Summary / Outputs

- Primary outputs shown to the user: portion cost, total batch cost, target menu price, expected food cost %
- Secondary outputs: highest-cost ingredients, recipes below target margin, optional recipe ranking
- Dashboard or summary behavior: filterable overview of recipes and pricing performance

## UX Notes

- What should feel easy: entering ingredients, building one first recipe, seeing a recommended price quickly
- Where users are likely to get confused: unit conversion, sub-recipes, target food cost vs gross margin logic
- Guidance needed from copy: strong Start Here tab, unit examples, plain-language explanation of pricing formulas

## Constraints And Risks

- Known limitations: no live inventory data, no supplier sync, no version history
- Spreadsheet pain points: manual maintenance grows with recipe count
- Future app-only features to hint at: saved ingredient database, collaboration, audit history, multi-location rollups

## Handoff Notes

### For Copywriter

- Copy needs: onboarding flow, unit conversion help text, pricing explanation, dashboard labels
- Terms that must be explained: food cost %, gross margin, purchase unit, recipe unit, yield

### For QA

- Risky logic areas: conversions, sub-recipe inheritance, serving count, blank states
- Edge cases to test: zero servings, missing purchase price, mismatched units, sub-recipe update flow

### For Funnel Strategist

- Strongest upgrade moments: multi-recipe updates, audit history, team usage, growing ingredient libraries
- Best user promise: know what each dish costs and what to charge without rebuilding formulas every week

