# 🎨 Visual Design Guide

## Color Palette

### Primary Colors
```
Purple (Primary):   #7C3AED  ████████
Dark Purple:        #6D28D9  ████████
Light Purple:       #8B5CF6  ████████
Secondary Purple:   #9333EA  ████████
Accent Yellow:      #FACC15  ████████
```

### Status Colors
```
Success (Green):    #10B981  ████████
Warning (Orange):   #F59E0B  ████████
Error (Red):        #EF4444  ████████
Info (Blue):        #3B82F6  ████████
```

### Dark Theme
```
Background:         #0F172A  ████████
Secondary BG:       #1E293B  ████████
Tertiary BG:        #334155  ████████
Text:               #E2E8F0  ████████
Secondary Text:     #CBD5E1  ████████
```

### Light Theme
```
Background:         #FFFFFF  ████████
Secondary BG:       #F8FAFC  ████████
Tertiary BG:        #F1F5F9  ████████
Text:               #1E293B  ████████
Secondary Text:     #64748B  ████████
```

## Typography

### Font Family
- Primary: **Inter**
- Fallback: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

### Font Sizes
```
H1: 2.5rem (40px)   - Page titles
H2: 2rem (32px)     - Section headers
H3: 1.75rem (28px)  - Card titles
H4: 1.5rem (24px)   - Subsection titles
H5: 1.25rem (20px)  - Small headers
H6: 1rem (16px)     - Inline headers
Body: 1rem (16px)   - Regular text
Small: 0.875rem     - Labels, captions
Tiny: 0.75rem       - Badges, timestamps
```

### Font Weights
```
Light:    300
Regular:  400
Medium:   500
SemiBold: 600
Bold:     700
```

## Spacing System

```
XS:  0.25rem (4px)
SM:  0.5rem (8px)
MD:  1rem (16px)
LG:  1.5rem (24px)
XL:  2rem (32px)
2XL: 3rem (48px)
```

## Border Radius

```
Small:    0.375rem (6px)   - Small buttons, badges
Medium:   0.5rem (8px)     - Inputs, dropdowns
Large:    0.75rem (12px)   - Standard cards
XL:       1rem (16px)      - Large cards
2XL:      1.5rem (24px)    - Modals, hero sections
Full:     9999px           - Pills, avatars
```

## Shadows

### Shadow Levels
```
SM:  0 1px 2px 0 rgba(0, 0, 0, 0.05)
MD:  0 4px 6px -1px rgba(0, 0, 0, 0.1)
LG:  0 10px 15px -3px rgba(0, 0, 0, 0.1)
XL:  0 20px 25px -5px rgba(0, 0, 0, 0.1)
```

### Glow Effects
```
Primary: 0 0 0 3px rgba(124, 58, 237, 0.1)
Success: 0 0 0 3px rgba(16, 185, 129, 0.1)
Error:   0 0 0 3px rgba(239, 68, 68, 0.1)
```

## Component Styles

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #7C3AED, #9333EA)
color: white
padding: 1rem 2rem
border-radius: 0.75rem
font-weight: 500
hover: transform translateY(-2px) + shadow
```

#### Secondary Button
```css
background: var(--bg-tertiary)
color: var(--text-primary)
padding: 1rem 2rem
border-radius: 0.75rem
hover: darken background
```

#### Icon Button
```css
width: 36px
height: 36px
border-radius: 0.5rem
background: var(--bg-tertiary)
hover: background primary color
```

### Cards

#### Glass Effect Card
```css
background: rgba(255, 255, 255, 0.03)
backdrop-filter: blur(10px)
border: 1px solid rgba(255, 255, 255, 0.1)
border-radius: 1rem
padding: 1.5rem
box-shadow: medium
```

#### Hover Lift Effect
```css
transition: transform 250ms, box-shadow 250ms
hover: transform translateY(-4px)
hover: box-shadow xl
```

### Forms

#### Input Fields
```css
background: var(--bg-tertiary)
border: 1px solid var(--border-color)
border-radius: 0.5rem
padding: 1rem
font-size: 0.875rem
focus: border-color primary + glow
```

#### Floating Labels
```css
label position: absolute
label top: 50%
input focus: label moves to top
input focus: label scales to 0.75rem
label color: primary on focus
```

### Navigation

#### Navbar
```css
height: 64px
background: var(--bg-secondary) with backdrop blur
border-bottom: 1px solid border-color
sticky position at top
z-index: 1000
```

#### Sidebar
```css
width: 260px
background: var(--bg-secondary)
border-right: 1px solid border-color
fixed position
height: 100vh
overflow-y: auto
```

#### Nav Item
```css
padding: 1rem
border-radius: 0.75rem
color: var(--text-secondary)
hover: background tertiary + color primary
active: gradient background + left border indicator
```

### Tables

#### Modern Table
```css
thead background: var(--bg-tertiary)
th: uppercase, letter-spacing, small font
td: padding 1rem 1.5rem
tr hover: background var(--bg-tertiary)
border-bottom: 1px solid border-color
```

### Modals

#### Modal Overlay
```css
background: rgba(0, 0, 0, 0.7)
backdrop-filter: blur(5px)
position: fixed, full screen
z-index: 2000
```

#### Modal Content
```css
max-width: 500px (large: 800px)
border-radius: 1.5rem
padding: 2rem
glass effect
transform: scale(0.9) to scale(1) on show
```

## Animation Timing

### Transitions
```
Fast:   150ms ease-in-out
Normal: 250ms ease-in-out
Slow:   350ms ease-in-out
```

### Keyframe Animations
```
fadeIn:        opacity 0→1, translateY 20px→0
slideInRight:  opacity 0→1, translateX 100%→0
float:         infinite loop, translate + scale
```

## Icon Usage

### Font Awesome Classes
```
Solid:   <i class="fas fa-icon-name"></i>
Regular: <i class="far fa-icon-name"></i>
Brand:   <i class="fab fa-icon-name"></i>
```

### Common Icons
```
📚 Books:        fa-book, fa-book-open
👤 User:         fa-user, fa-user-circle
⚙️ Settings:     fa-cog, fa-sliders-h
🔍 Search:       fa-search
📊 Dashboard:    fa-chart-bar, fa-home
📋 List:         fa-list, fa-th
➕ Add:          fa-plus, fa-plus-circle
✏️ Edit:         fa-edit, fa-pen
🗑️ Delete:       fa-trash, fa-trash-alt
✓ Check:        fa-check, fa-check-circle
✕ Close:        fa-times, fa-times-circle
⚠️ Warning:      fa-exclamation-triangle
ℹ️ Info:         fa-info-circle
📅 Calendar:     fa-calendar, fa-calendar-alt
🔔 Notification: fa-bell
🔒 Security:     fa-lock, fa-shield-alt
```

## Status Indicators

### Badge Styles
```
Available:  background green 10%, color green, border green 20%
Unavailable: background red 10%, color red, border red 20%
Warning:    background yellow 10%, color yellow, border yellow 20%
Due Soon:   background orange 10%, color orange
Overdue:    background red 10%, color red
```

### Status Colors
```
Active:     #10B981 (Green)
Inactive:   #94A3B8 (Gray)
Pending:    #3B82F6 (Blue)
Overdue:    #EF4444 (Red)
Warning:    #F59E0B (Orange)
```

## Grid Layouts

### Books Grid
```
columns: repeat(auto-fill, minmax(280px, 1fr))
gap: 1.5rem
```

### Dashboard Stats
```
columns: repeat(auto-fit, minmax(250px, 1fr))
gap: 1.5rem
```

### Admin Cards
```
columns: repeat(2, 1fr)
gap: 1.5rem
```

## Responsive Breakpoints

```
Mobile:    < 480px
Tablet:    480px - 768px
Desktop:   768px - 1024px
Large:     1024px - 1440px
XLarge:    > 1440px
```

### Mobile Adjustments
```
- Hide sidebar (toggle with hamburger)
- Stack grid columns to 1 column
- Reduce font sizes slightly
- Hide secondary navigation
- Full-width modals
- Simplify tables (show fewer columns)
```

## Accessibility

### ARIA Labels
```html
<button aria-label="Close menu">
<nav aria-label="Main navigation">
<input aria-describedby="error-message">
```

### Focus States
```css
outline: 2px solid var(--primary)
outline-offset: 2px
```

### Color Contrast
```
Text on dark bg: minimum 4.5:1 ratio
Text on light bg: minimum 4.5:1 ratio
Interactive elements: 3:1 ratio
```

## Loading States

### Button Loading
```html
<button class="loading">
    <i class="fas fa-spinner fa-spin"></i>
    Loading...
</button>
```

### Skeleton Loaders
```css
background: linear-gradient(90deg, bg-tertiary, bg-secondary, bg-tertiary)
animation: shimmer 2s infinite
```

## Empty States

### Style
```
Icon: 4rem size, text-secondary color
Title: 1.25rem, semibold
Description: text-secondary
Action Button: primary style
Padding: 3rem all sides
Text align: center
```

## Print Styles

```css
@media print {
    - Hide: navbar, sidebar, buttons
    - Remove: margins, padding
    - Black text on white background
    - Show full URLs for links
}
```

---

## Quick Reference

### Common Class Combinations

```html
<!-- Card with hover effect -->
<div class="glass-effect hover-lift">

<!-- Primary action button -->
<button class="btn btn-primary btn-gradient">

<!-- Success status badge -->
<span class="status-badge active">

<!-- Floating label input -->
<div class="form-group floating-label">

<!-- Page with fade animation -->
<div class="page-fade-in">

<!-- Icon with specific color -->
<i class="fas fa-book text-primary">
```

This design system ensures consistency across all pages! 🎨✨
