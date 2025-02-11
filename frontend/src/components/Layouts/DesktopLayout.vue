<template>
  <div class="flex h-screen w-screen">
    <!-- <div class="h-full border-r bg-surface-menu-bar">
      <AppSidebar />
    </div> -->
    <div class="flex-1 flex flex-col h-full overflow-auto bg-[surface-white]">
      <div class="flex items-center justify-between px-4 py-2 border-b border-surface-border bg-[#343A40]">
        <div class="flex items-center gap-2">
          <CRMLogo class="size-8 shrink-0 rounded" />
          <h1 class="text-2xl font-semibold text-white">Orbis CRM</h1>
        </div>
        <div class="flex items-center gap-2">
          <div class="hidden w-full md:block md:w-auto" id="navbar-default">
            <ul
              class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:dark:bg-gray-900 dark:border-gray-700">
              <li>
                <a href="#"
                  class="block py-2 px-3 text-white bg-blue-700 rounded-sm md:bg-transparent md:p-0 dark:text-white md:dark:text-blue-500"
                  aria-current="page">Dashboard</a>
              </li>
              <li>
                <router-link to="/leads"
                  class="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Leads</router-link>
              </li>
              <li>
                <router-link to="/deals"
                  class="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Deals</router-link>
              </li>
              <li>
                <router-link to="/contacts"
                  class="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Contacts</router-link>
              </li>
              <li>
                <router-link to="/organizations"
                  class="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Organizations</router-link>
              </li>
              <li>
                <router-link to="/financial-discovery"
                  class="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Financial Discovery</router-link>
              </li>
            </ul>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            class="px-4 py-2 text-gray-900 bg-white rounded-sm hover:bg-blue-500 hover:text-white" @click="logout.submit()">Logout</button>
        </div>
      </div>
      <AppHeader />
      <slot />
    </div>
  </div>
</template>
<script setup>
import CRMLogo from '@/components/Icons/CRMLogo.vue'
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import AppHeader from '@/components/Layouts/AppHeader.vue'
import { sessionStore } from '@/stores/session'
const { logout } = sessionStore()
</script>
