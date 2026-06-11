<script setup lang="ts">
defineProps<{
  eyebrow: string
  title: string
  description: string
  bullets: string[]
}>()
</script>

<template>
  <section class="auth-shell">
    <div class="auth-bg" aria-hidden="true">
      <span class="auth-orb auth-orb-one" />
      <span class="auth-orb auth-orb-two" />
      <span class="auth-grid" />
    </div>

    <div class="auth-copy">
      <span class="auth-pill gold">
        <span class="auth-pill-dot" aria-hidden="true" />
        {{ eyebrow }}
      </span>

      <h1 class="auth-title">
        {{ title }}
      </h1>

      <p class="auth-description">
        {{ description }}
      </p>

      <ul class="auth-bullets" role="list">
        <li v-for="bullet in bullets" :key="bullet" class="auth-bullet">
          <span class="auth-bullet-icon" aria-hidden="true">-</span>
          <span>{{ bullet }}</span>
        </li>
      </ul>
    </div>

    <div class="auth-card-wrap">
      <div class="auth-card">
        <slot />
      </div>
    </div>
  </section>
</template>

<style scoped>
.auth-shell {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 520px);
  gap: 40px;
  align-items: center;
  min-height: calc(100vh - var(--nav-height));
  padding: 56px 40px 72px;
  background:
    radial-gradient(circle at top left, rgba(127, 119, 221, 0.15), transparent 32%),
    radial-gradient(circle at bottom right, rgba(239, 159, 39, 0.1), transparent 30%),
    var(--c-void);
}

.auth-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.auth-orb {
  position: absolute;
  border-radius: 9999px;
  filter: blur(4px);
}

.auth-orb-one {
  top: 8%;
  left: 54%;
  width: 240px;
  height: 240px;
  background: rgba(83, 74, 183, 0.18);
}

.auth-orb-two {
  bottom: 4%;
  right: 8%;
  width: 360px;
  height: 360px;
  background: rgba(239, 159, 39, 0.08);
}

.auth-grid {
  position: absolute;
  inset: 0;
  opacity: 0.18;
  background-image: linear-gradient(rgba(60, 52, 137, 0.45) 1px, transparent 1px), linear-gradient(90deg, rgba(60, 52, 137, 0.45) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: radial-gradient(circle at center, black 40%, transparent 82%);
}

.auth-copy,
.auth-card-wrap {
  position: relative;
  z-index: 1;
}

.auth-copy {
  max-width: 720px;
}

.auth-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 22px;
  padding: 6px 14px;
  border: 0.5px solid var(--c-gold);
  border-radius: var(--radius-full);
  font-size: 0.95rem;
  color: var(--c-text);
}

.auth-pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background: var(--c-teal);
  box-shadow: 0 0 0 6px rgba(93, 202, 165, 0.12);
}

.auth-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(3rem, 6vw, 5.8rem);
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--c-text);
  text-wrap: balance;
}

.auth-description {
  max-width: 60ch;
  margin-top: 22px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--c-purple-muted);
}

.auth-bullets {
  display: grid;
  gap: 12px;
  margin-top: 30px;
}

.auth-bullet {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  border: 0.5px solid var(--c-border);
  border-radius: var(--radius-lg);
  background: rgba(38, 33, 92, 0.72);
  color: var(--c-purple-pale);
  box-shadow: 0 16px 40px rgba(5, 3, 20, 0.18);
}

.auth-bullet-icon {
  color: var(--c-gold-light);
  font-size: 1.2rem;
  line-height: 1;
}

.auth-card-wrap {
  display: flex;
  justify-content: center;
}

.auth-card {
  width: min(100%, 470px);
  padding: 28px;
  border: 0.5px solid rgba(83, 74, 183, 0.55);
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(38, 33, 92, 0.92), rgba(26, 16, 64, 0.94));
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(16px);
}

@media (max-width: 960px) {
  .auth-shell {
    grid-template-columns: 1fr;
    gap: 28px;
    padding: 36px 20px 44px;
  }

  .auth-card {
    width: 100%;
  }
}
</style>