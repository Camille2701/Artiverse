<template>
    <div class="mx-auto w-full max-w-md space-y-4 px-4 py-6 sm:space-y-5 sm:px-6 sm:py-8 lg:max-w-lg lg:space-y-6 lg:px-0">
        <h1 class="text-2xl font-semibold text-slate-900 sm:text-3xl">Me connecter</h1>
        <UserLogin />
        <p class="text-sm text-slate-600 sm:text-base">
            Pas encore de compte ?
            <NuxtLink to="/users/new" class="text-link-accent">S'inscrire</NuxtLink>
        </p>
    </div>
</template>