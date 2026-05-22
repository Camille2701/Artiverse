# Artiverse Design System Implementation Guide

This guide explains the new graphical chart implementation for the Artiverse platform.

## Overview

The design system has been completely overhauled to match the modern, dark-mode aesthetic defined in the graphical chart. The implementation focuses on:

- **Dark mode by default** - Cinematic experience that makes media covers pop
- **Category-specific colors** - Visual distinction between movies, series, games, and books
- **Modern typography** - Space Grotesk for headings, Inter for body text
- **Gamification elements** - Badges with different styles (flat, gradient, glassmorphism, holographic)
- **Social discovery** - Human-centric recommendations and profiles

## Color Palette

### Background Colors
- **Primary**: `#12121A` - Deep dark background with subtle blue/purple tint
- **Secondary**: `#1E1E28` - Anthracite gray for cards and UI elements
- **Tertiary**: `#2A2A38` - Lighter gray for inputs and secondary elements

### Category Colors
- **Movies**: `#FF4757` - Coral red (cinema seats, red curtain)
- **Series**: `#9B51E0` - Neon purple (modern, binge-watching)
- **Games**: `#00D2D3` - Electric cyan (tech, futuristic, LEDs)
- **Books**: `#ECCC68` - Mustard gold (classic elegance, aged paper)

### Text Colors
- **Primary**: `#FFFFFF` - Main text
- **Secondary**: `#A0A0B0` - Descriptive text
- **Tertiary**: `#707080` - Metadata and hints

## Typography

### Headings
- **Font**: Space Grotesk or Outfit
- **Usage**: Titles, numbers, badges
- **Classes**: `font-display` or `font-heading`

### Body Text
- **Font**: Inter
- **Usage**: Reviews, descriptions, general content
- **Class**: `font-body`

## Components

### 1. Badge System (`Badge.vue`)

Four distinct badge styles for different achievement levels:

```vue
<Badge
  :badge="{
    id: '1',
    name: 'Cinéphile Expert',
    description: 'A regardé 100 films',
    icon: '🎬',
    level: 'Expert',
    style: 'holographic', // 'flat' | 'gradient' | 'glass' | 'holographic'
    mediaType: 'movie' // optional, for color customization
  }"
  size="md" // 'sm' | 'md' | 'lg'
/>
```

**Badge Levels:**
- **Flat** - Beginner level, solid colors
- **Gradient** - Intermediate, subtle gradients
- **Glass** - Advanced, glassmorphism effect
- **Holographic** - Expert, iridescent 3D effect

### 2. Media Cards (`MediaShow.vue`, `MediaCard.vue`)

Modern media cards with hover effects and category-specific styling:

```vue
<MediaShow
  :media="{
    id: '1',
    title: 'Inception',
    type: 'Movie',
    image: 'https://example.com/poster.jpg',
    rating: 8.5,
    releaseDate: '2010-07-16',
    description: 'A thief who steals corporate secrets...'
  }"
/>
```

**Features:**
- Responsive design with hover animations
- Category-specific color accents
- Quick actions on hover (favorites, add to list)
- Rating badges with glassmorphism
- Gradient placeholders for missing images

### 3. User Profile (`UserProfile.vue`)

Comprehensive profile with gamification elements:

```vue
<UserProfile
  :user="{
    id: '1',
    username: 'Cinéphile Passionné',
    bio: 'Amateur de cinéma indépendant',
    level: 12,
    experiencePoints: 3450
  }"
  :stats="{
    movies: 45,
    series: 23,
    games: 31,
    books: 18
  }"
  :badges="[...]"
  :favorite-media="[...]"
  :recent-activity="[...]"
/>
```

**Features:**
- Dynamic banner with favorite media collage
- Gamification stats (XP, level, badges)
- Radar chart for media consumption distribution
- Recent activity feed
- Badge collection display

### 4. Social Discovery Feed (`SocialDiscoveryFeed.vue`)

Human-centric recommendation system:

```vue
<SocialDiscoveryFeed
  :recommendations="[{
    id: '1',
    user: { username: 'Alice', avatar: '...' },
    media: { title: 'Inception', type: 'Movie', rating: 9.0 },
    reason: 'Parce que vous aimez les films de Nolan',
    review: 'Un chef-d\'œuvre de science-fiction...',
    likes: 42,
    comments: 8
  }]"
/>
```

**Features:**
- User avatars prominently displayed
- Social context for recommendations
- Like and comment interactions
- Category-specific badges

## CSS Classes

### Cards
```css
.card          /* Base card style */
.card-hover    /* Card with hover lift effect */
```

### Buttons
```css
.btn-primary       /* Primary action button */
.btn-movie         /* Movie-specific button */
.btn-series        /* Series-specific button */
.btn-game          /* Game-specific button */
.btn-book          /* Book-specific button */
```

### Input Fields
```css
.input-field    /* Styled input with dark mode */
```

### Navigation
```css
.nav-link       /* Navigation link with underline effect */
```

### Badges
```css
.badge              /* Base badge style */
.badge-flat         /* Flat style badge */
.badge-gradient     /* Gradient style badge */
.badge-glass        /* Glassmorphism badge */
.badge-holographic  /* Holographic badge */
```

### Special Effects
```css
.glass              /* Glassmorphism background */
.glass-hover        /* Glass effect on hover */
.holographic        /* Holographic gradient */
.stat-card          /* Statistics card */
```

## Category-Specific Classes

### Movies
```css
.media-movie          /* Text color */
.media-movie-bg       /* Background color */
.media-movie-border   /* Border color */
.media-movie-glow     /* Glow effect */
```

### Series
```css
.media-series          /* Text color */
.media-series-bg       /* Background color */
.media-series-border   /* Border color */
.media-series-glow     /* Glow effect */
```

### Games
```css
.media-game          /* Text color */
.media-game-bg       /* Background color */
.media-game-border   /* Border color */
.media-game-glow     /* Glow effect */
```

### Books
```css
.media-book          /* Text color */
.media-book-bg       /* Background color */
.media-book-border   /* Border color */
.media-book-glow     /* Glow effect */
```

## Layout Structure

### Main Layout (`default.vue`)

The main layout includes:
- **Sticky glass header** with navigation and logo
- **Responsive container** for main content
- **Footer** with links and copyright
- **Dark mode enabled by default**

### Page Structure

```vue
<template>
  <div class="max-w-7xl mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-display font-bold text-text-primary">
        Page Title
      </h1>
      <p class="text-text-secondary mt-2 font-body">
        Page description
      </p>
    </div>

    <!-- Page content -->
  </div>
</template>
```

## Responsive Design

The design system is fully responsive with breakpoints:
- **Mobile**: `sm:`
- **Tablet**: `md:`
- **Desktop**: `lg:`
- **Large Desktop**: `xl:`

Example grid system:
```vue
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <!-- Cards -->
</div>
```

## Animation and Transitions

### Built-in Animations
- `animate-pulse-slow` - Slow pulsing effect
- `animate-float` - Floating animation
- `hover:scale-105` - Scale on hover
- `transition-transform` - Smooth transforms

### Duration Examples
```css
duration-200   /* Fast transitions */
duration-300   /* Medium transitions */
duration-500   /* Slow transitions */
```

## Accessibility

- **Semantic HTML** - Proper use of headings, buttons, and links
- **Focus states** - Visible focus rings for keyboard navigation
- **Color contrast** - WCAG AA compliant color ratios
- **Screen reader support** - Proper aria labels where needed

## Performance

- **Google Fonts** - Optimized font loading with display:swap
- **CSS animations** - Hardware-accelerated transforms
- **Lazy loading** - Images load on demand
- **Component-based** - Reusable components reduce bundle size

## Customization

### Adding New Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  'your-color': '#HEX',
  'your-color-hover': '#HEX',
}
```

### Adding New Animations

Edit `tailwind.config.ts`:

```typescript
animation: {
  'your-animation': 'your-animation 3s ease-in-out infinite',
},
keyframes: {
  'your-animation': {
    '0%, 100%': { /* styles */ },
    '50%': { /* styles */ },
  }
}
```

## Best Practices

1. **Use semantic classes** - Leverage the design system classes
2. **Maintain consistency** - Use established patterns for similar elements
3. **Responsive first** - Design for mobile, then enhance for larger screens
4. **Accessibility** - Ensure keyboard navigation and screen reader support
5. **Performance** - Use CSS animations over JavaScript when possible

## Migration Notes

### Old → New Class Mapping

| Old Class | New Class |
|-----------|-----------|
| `bg-gray-50` | `bg-bg-primary` |
| `bg-gray-900` | `glass` |
| `text-gray-900` | `text-text-primary` |
| `text-gray-600` | `text-text-secondary` |
| `border-gray-200` | `border-border-color` |
| `bg-white` | `bg-bg-secondary` |
| `shadow-md` | `shadow-lg` |

### Breaking Changes

1. **Dark mode is now default** - Remove light mode specific styles
2. **New typography** - Update font references to use new system
3. **Color system** - Use new color palette instead of grays
4. **Component props** - Some components have updated prop interfaces

## Support

For questions or issues with the design system:
1. Check this guide first
2. Review component source files for detailed implementation
3. Test in different browsers for compatibility
4. Ensure Google Fonts are loaded properly

## Future Enhancements

Planned improvements to the design system:
- [ ] Additional badge styles and animations
- [ ] Advanced chart components (activity timelines, progress rings)
- [ ] Micro-interactions and delight factors
- [ ] Theme customization options
- [ ] Accessibility improvements
- [ ] Performance optimizations

---

**Note**: This design system implements the graphical chart defined in `charte_graphique.md`. All visual decisions align with the modern, dark-mode aesthetic designed for the Artiverse platform.